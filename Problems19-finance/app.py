import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


################################################# INDEX #################################################
@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    acc_id = session["user_id"]
    if acc_id != None:
        # Update current stocks price to update total value
        # Get the user data in db
        user_db = db.execute("SELECT * FROM portfolio WHERE pofo_id = ?", acc_id)

        # Loop through the list
        def get_current_price(user_db):
            # Create a NEW_LIST for display
            latest_update = []

            # Get the symbol 1 by 1
            for data in user_db:
                # Tempoary dict
                temp_dict = data
                # {'pofo_id': 2, 'time': '2022-09-09', 'symbol': 'UVXY', 'name': 'Stock_Name', 'shares': 1, 'total': 9.5}

                # Pass the symbol to lookup function to lookup the current price
                symbol = data["symbol"]
                current_data = lookup(symbol)
                # Update current_price in temp_dict
                get_current_price = current_data["price"]
                # Display 2 decimal places always that I found, and the float is for usd function
                # current_price = float("{:.2f}".format(get_current_price))
                current_price = get_current_price
                temp_dict["current_price"] = current_price
                # {'symbol': 'UVXY', 'current_price': 9.18}

                # Update total in temp_dict
                shares = data["shares"]
                get_current_total = current_price * shares
                # Display 2 decimal places always that I found, and the float is for usd function
                # current_total = float("{:.2f}".format(get_current_total))
                current_total = get_current_total
                temp_dict["total"] = current_total

                # Update stock,price, stock value in db
                db.execute("UPDATE portfolio SET current_price = ?, total = ? WHERE symbol = ?", current_price, current_total, symbol)

                # Put "user data" from db + "current price" to NEW_LIST
                # "latest_update = []" will show on the index page
                # if shares < 1, don't show on the index page
                if shares > 0:
                    latest_update.append(temp_dict)
            return latest_update
            # [{'pofo_id': 2, 'time': '2022-09-09', 'symbol': 'SQQQ', 'name': 'STOCK_NAME', 'shares': 1, 'total': 44.69, 'current_price': 42.48}, {'pofo_id': 2, 'time': '2022-09-09', 'symbol': 'UVXY', 'name': 'STOCK_NAME', 'shares': 1, 'total': 9.5, 'current_price': 9.17}

        # Use the NEW_LIST as a content and loop through to display
        # The different is added a 'current_price'
        contents = get_current_price(user_db)
        # contents data look like
        # [{'pofo_id': 2, 'time': '2022-09-09', 'symbol': 'SQQQ', 'name': 'STOCK_NAME', 'shares': 1, 'total': 44.69, 'current_price': 42.48}, {'pofo_id': 2, 'time': '2022-09-09', 'symbol': 'UVXY', 'name': 'STOCK_NAME', 'shares': 1, 'total': 9.5, 'current_price': 9.17}

        cash_db = db.execute("SELECT cash FROM users WHERE id = ?", acc_id)
        # It wil get [{'cash': 10000}]
        # Grab the 10000 out
        get_cash = cash_db[0]["cash"]
        # Display 2 decimal places always that I found, and the float is for usd function
        # cash = float("{:.2f}".format(get_cash))
        cash = get_cash

        stock_total_db = db.execute("SELECT SUM(total) FROM portfolio WHERE pofo_id = ?", acc_id)
        # [{'SUM(total)': 54.19}]
        stock_total = stock_total_db[0]["SUM(total)"]

        # If no stock, return 0 value
        # If don't do this, will get error when nothing in list
        if stock_total == None:
            stock_total = 0

        get_total_assets = get_cash + stock_total
        # Display 2 decimal places always that I found, and the float is for usd function
        # total_assets = float("{:.2f}".format(get_total_assets))
        total_assets = get_total_assets

        # Display on the webpage
        return render_template("portfolio.html", jinja_contents=contents, jinja_cash=cash, jinja_total=total_assets)

    else:
        return render_template("login.html")


################################################# BUY #################################################
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    acc_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        # Ensure password was submitted
        elif not request.form.get("shares"):
            return apology("must provide shares", 403)

        # date_time = datetime.now().date()
        date_time = datetime.now()

        # Query symbol in the lookup function
        symbol = request.form.get("symbol")
        shares_input = request.form.get("shares")
        symbol_lookup = lookup(symbol)
        # {'name': 'ProShares Trust - ProShares Ultra VIX Short-Term Futures ETF 2x Shares', 'price': 9.73, 'symbol': 'UVXY'}

        # Ensure uses input shares is a int
        try:
            int(shares_input)
            shares_int_check = True
        except ValueError:
            shares_int_check = False

        if shares_int_check == False:
            return apology("invalid shares", 400)

        shares = int(shares_input)

        # Check the symbol first, ensure can get data from lookup()
        if symbol_lookup == None:
            return apology("invalid symbol", 400)

        # Check enough cash to afford the stock
        cash_db = db.execute("SELECT cash FROM users WHERE id = ?", acc_id)
        # It wil get [{'cash': 10000}]

        stock_name = symbol_lookup["name"]
        stock_price = symbol_lookup["price"]
        stock_symbol = symbol_lookup["symbol"]

        cash = cash_db[0]["cash"]
        cost = stock_price * shares
        balance = cash - cost
        trade_total = round(stock_price * shares, 2)

        if shares < 1:
            return apology("invalid shares", 400)

        elif cost > cash:
            return apology("can't afford", 400)

        else:
            flash("Bought!")
            # Update cash in users table
            db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, acc_id)

            # Check if the stock is exists in db or NOT
            stock_held = db.execute(
                "SELECT shares FROM portfolio WHERE EXISTS(SELECT symbol FROM portfolio WHERE pofo_id = ? AND symbol = ?)", acc_id, stock_symbol)

            # Check if the stock is NOT exists in db
            # Use SQL INSERT
            if len(stock_held) == 0:
                # INSERT - Update portfolio
                db.execute("INSERT INTO portfolio (pofo_id, time, symbol, name, shares, total) VALUES (?, ?, ?, ?, ?, ?)",
                           acc_id, date_time, stock_symbol, stock_name, shares, trade_total)

                # INSERT history db
                sql_type = "buy"
                db.execute("INSERT INTO history (id, time, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?, ?)",
                           acc_id, date_time, stock_symbol, shares, stock_price, sql_type)

            # If the stock exists, update the esist data
            # Use SQL UPDATE
            else:
                # How many holding
                helding_shares = db.execute("SELECT shares FROM portfolio WHERE symbol = ? AND pofo_id = ?", stock_symbol, acc_id)
                # [{'shares': 15}]

                update_shares = (helding_shares[0]['shares']) + shares
                update_total_1 = update_shares * stock_price
                update_total = round(update_total_1, 2)

                # Update portfolio db
                db.execute("UPDATE portfolio SET shares = ? , total = ? WHERE symbol = ?",
                           update_shares, update_total, stock_symbol)

                # INSERT history db
                sql_type = "buy"
                db.execute("INSERT INTO history (id, time, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?, ?)",
                           acc_id, date_time, stock_symbol, shares, stock_price, sql_type)

                return redirect("/")

            return redirect("/")

    return render_template("buy.html")


################################################# HISTORY #################################################
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Keep and Know who is logging in
    acc_id = session["user_id"]

    if acc_id != None:
        # Update current stocks price to update total value
        # Get the user data in db
        history_list = db.execute("SELECT * FROM history WHERE id = ?", acc_id)

    return render_template("history.html", jinja_history_list=history_list)


################################################# LOGIN #################################################
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


################################################# LOGOUT #################################################
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


################################################# QUOTE #################################################
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        # Query symbol in the lookup function
        symbol = request.form.get("symbol")
        stock_symbol = lookup(symbol)

        if stock_symbol == None:
            return apology("invalid symbol", 400)

        else:
            print(stock_symbol)
            stock_name = stock_symbol["name"]
            stock_price = stock_symbol["price"]
            display_stock_symbol = stock_symbol["symbol"]

            return render_template("stock_quote.html", jinja_stock_name=stock_name, jinja_display_stock_symbol=display_stock_symbol, jinja_stock_price=stock_price)

    return render_template("quote.html")


################################################# REGISTER #################################################
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        user_name = request.form.get("username")
        password = request.form.get("password")
        pw_confirmation = request.form.get("confirmation")

        # Check if the username is available
        user_name_check = db.execute("SELECT * FROM users WHERE username = ?", user_name)

        # Password confirmation
        if password != pw_confirmation:
            return apology("password not match", 400)

        hash_password = generate_password_hash(password)

        if len(user_name_check) >= 1:
            return apology("username has been taken", 400)

        # Add user data into db then log the user in
        else:
            flash("Registered!")

            # Use SQL INSERT to add the data to db
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user_name, hash_password)

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            return redirect("/")

    return render_template("register.html")


################################################# SELL #################################################
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    ########## Basic checking ##########
    """Sell shares of stock"""
    # Keep and Know who is logging in
    acc_id = session["user_id"]

    sell_list_option = db.execute("SELECT * FROM portfolio WHERE (pofo_id = ? AND shares > 0)", acc_id)
    # [{'pofo_id': 2, 'time': '2022-09-13', 'symbol': 'SQQQ', 'name': 'ProShares Trust - ProShares UltraPro Short QQQ -3x Shares', 'shares': 13, 'current_price': 40.31, 'total': 524.03}, {'pofo_id': 2, 'time': '2022-09-13', 'symbol': 'UVXY', 'name': 'ProShares Trust - ProShares Ultra VIX Short-Term Futures ETF 2x Shares', 'shares': 1, 'current_price': 9.27, 'total': 9.27}]

    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", acc_id)
    cash = cash_db[0]["cash"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure password was submitted
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)

        # date_time = datetime.now().date()
        date_time = datetime.now()

        # Query symbol in the lookup function
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        symbol_lookup = lookup(symbol)
        # {'name': 'ProShares Trust - ProShares Ultra VIX Short-Term Futures ETF 2x Shares', 'price': 9.73, 'symbol': 'UVXY'}

        # Check the symbol first, ensure can get data from lookup()
        if symbol_lookup == None:
            return apology("invalid symbol", 400)

        ########## Sell Feature ##########
        # Check enough shares to sell
        # Use id and symbol to filter and get db data
        shares_db = db.execute("SELECT shares FROM portfolio WHERE (pofo_id = ? AND symbol = ?)", acc_id, symbol)
        # [{'shares': 10}]

        # Get the current price
        stock_price = symbol_lookup["price"]
        stock_symbol = symbol_lookup["symbol"]

        shares_holding = shares_db[0]["shares"]
        update_shares = shares_holding - shares
        update_total = update_shares * stock_price
        receive_cash = shares * stock_price
        balance = receive_cash + cash

        if shares < 1:
            return apology("invalid shares", 400)

        elif shares > shares_holding:
            return apology("too many shares", 400)

        else:
            flash("Sold!")

            # Update shares in portfolio db
            db.execute("UPDATE portfolio SET shares = ? WHERE (pofo_id = ? AND symbol = ?)", update_shares, acc_id, symbol)

            # Update cash in users db
            db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, acc_id)

            # Update shares and total in portfolio db
            db.execute("UPDATE portfolio SET shares = ? , total = ? WHERE symbol = ?", update_shares, update_total, stock_symbol)

            # INSERT Sell to history db
            # Tune to nigative for display
            nigative_shares_num = shares * -1
            sql_type = "sell"
            db.execute("INSERT INTO history (id, time, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?, ?)",
                       acc_id, date_time, stock_symbol, nigative_shares_num, stock_price, sql_type)

            return redirect("/")

    return render_template("sell.html", jinja_sell_list=sell_list_option)


################################################# CHANGE PASSWORD #################################################
@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Change Password"""
    ########## Basic Checking ##########
    # Keep and Know who is logging in
    acc_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        new_pw_confirmation = request.form.get("new_pw_confirmation")

        # Ensure username was submitted
        if not request.form.get("old_password"):
            return apology("must provide old password", 403)

        # Ensure password was submitted
        if not request.form.get("new_password"):
            return apology("must provide new password", 403)

        # Ensure password was submitted
        if not request.form.get("new_pw_confirmation"):
            return apology("must confirm password", 403)

        ########## Change Password Feature ##########
        # Query database
        rows = db.execute("SELECT * FROM users WHERE id = ?", acc_id)
        # [{'id': 9, 'username': 'j_01', 'hash': 'pbkdf2:sha256:260000$hrrWfY0MEkZRbZ5a$308f47d9d9268c3c4c9915eb747ec473c77dc9aa57b4a495ef7a66bf402208c7', 'cash': 10000}]

        if not check_password_hash(rows[0]["hash"], old_password):
            return apology("invalid old password", 403)

        if new_password != new_pw_confirmation:
            return apology("new password not match", 403)

        else:
            flash("Password Changed!")

            hash_password = generate_password_hash(new_password)

            db.execute("UPDATE users SET hash = ? WHERE id = ?", hash_password, acc_id)

            return render_template("changepasswordsuccess.html")

    return render_template("changepassword.html")
    # Ensure username exists and password is correct


################################################# ADD CASH #################################################
@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add additiional cash to the account."""
    # Keep and Know who is logging in
    acc_id = session["user_id"]

    if request.method == "POST":

        if not request.form.get("cash_amount"):
            return apology("invalid cash amount", 400)

        # Query symbol in the lookup function
        get_cash_amount = request.form.get("cash_amount")
        cash_amount = float(get_cash_amount)

        if cash_amount <= 0:
            return apology("invalid cash amount", 400)

        else:
            current_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", acc_id)
            # [{'cash': 9577.359999999999}]

            current_cash = current_cash_db[0]['cash']
            update_cash = current_cash + cash_amount
            db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, acc_id)

            return render_template("addcashsuccess.html", jinja_added_cash=cash_amount, jinja_update_cash=update_cash)

    return render_template("addcash.html")