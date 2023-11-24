-- Keep a log of any SQL queries you execute as you solve the mystery.

-- All you know is that the theft 
-- took place on July 28, 2021 at 10:15am
-- it took place on Humphrey Street
-- Sometime within 10 minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money
-- When the thief was leaving the bakery, they called someone who talked to them for less than a minute
-- they were planning to take the earliest flight out of Fiftyville tomorrow




SELECT description FROM crime_scene_reports
WHERE year = 2021
AND month = 7
AND day = 28
AND street = "Humphrey Street";
-- +--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
-- |                                                                                                       description                                                                                                        |
-- +--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
-- | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
-- | Littering took place at 16:36. No known witnesses.                                                                                                                                                                       |
-- +--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


SELECT name, transcript FROM interviews
WHERE year = 2021
AND month = 7
AND day = 28;
-- +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
-- |  name   |                                                                                                                                                     transcript                                                                                                                                                      |
-- +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
-- | Jose    | “Ah,” said he, “I forgot that I had not seen you for some weeks. It is a little souvenir from the King of Bohemia in return for my assistance in the case of the Irene Adler papers.”                                                                                                                               |
-- | Eugene  | “I suppose,” said Holmes, “that when Mr. Windibank came back from France he was very annoyed at your having gone to the ball.”                                                                                                                                                                                      |
-- | Barbara | “You had my note?” he lasked with a deep harsh voice and a strongly marked German accent. “I told you that I would call.” He looked from one to the other of us, as if uncertain which to address.                                                                                                                   |
-- | Ruth    | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
-- | Eugene  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
-- | Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
-- | Lily    | Our neighboring courthouse has a very annoying rooster that crows loudly at 6am every day. My sons Robert and Patrick took the rooster to a city far, far away, so it may never bother us again. My sons have successfully arrived in Paris.                                                                        |
-- +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+







-- took place on July 28, 2021 at 10:15am
-- it took place on Humphrey Street
-- Sometime within 10 minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- Who leaves the scene between 10:15-10:25
SELECT people.name, people.license_plate, bakery_security_logs.hour, bakery_security_logs.minute FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE (hour = 10 AND minute >= 15 AND minute <= 25 AND activity = "exit" AND year = 2021 AND month = 7 AND day = 28)
ORDER BY name ASC;
-- +---------+---------------+------+--------+
-- |  name   | license_plate | hour | minute |
-- +---------+---------------+------+--------+
-- | Barry   | 6P58WS2       | 10   | 18     |
-- | Bruce   | 94KL13X       | 10   | 18     |
-- | Diana   | 322W7JE       | 10   | 23     |
-- | Iman    | L93JTIZ       | 10   | 21     |
-- | Kelsey  | 0NTHK55       | 10   | 23     |
-- | Luca    | 4328GD8       | 10   | 19     |
-- | Sofia   | G412CB7       | 10   | 20     |
-- | Vanessa | 5P2BI95       | 10   | 16     |
-- +---------+---------------+------+--------+



-- Withdrawing money on Leggett Street
SELECT name FROM people
JOIN bank_accounts ON people.id = person_id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw";
-- +---------+
-- |  name   |
-- +---------+
-- | Bruce   |
-- | Diana   |
-- | Brooke  |
-- | Kenny   |
-- | Iman    |
-- | Luca    |
-- | Taylor  |
-- | Benista |
-- +---------+

-- Bruce, Diana, Iman, Luca



-- Suspcsion Phone number
SELECT * FROM people
WHERE name = "Bruce" OR name = "Diana" OR name = "Iman" OR name = "Luca";
-- +--------+-------+----------------+-----------------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate |
-- +--------+-------+----------------+-----------------+---------------+
-- | 396669 | Iman  | (829) 555-5269 | 7049073643      | L93JTIZ       |
-- | 467400 | Luca  | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       |
-- | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
-- +--------+-------+----------------+-----------------+---------------+


-- When the thief was leaving the bakery, they called someone who talked to them for less than a minute
SELECT people.name, phone_calls.caller, phone_calls.receiver, phone_calls.duration FROM people
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE (caller = "(829) 555-5269" OR caller = "(389) 555-5198" OR caller = "(770) 555-1861" OR caller = "(367) 555-5533")
AND (year = 2021 AND month = 7 AND day = 28)
AND duration < 60;
-- +-------+----------------+----------------+----------+
-- | name  |     caller     |    receiver    | duration |
-- +-------+----------------+----------------+----------+
-- | Bruce | (367) 555-5533 | (375) 555-8161 | 45       |
-- | Diana | (770) 555-1861 | (725) 555-3243 | 49       |
-- +-------+----------------+----------------+----------+


-- Who did they called
SELECT people.name, phone_calls.caller, phone_calls.duration FROM people
JOIN phone_calls ON phone_calls.receiver = people.phone_number
WHERE (receiver = "(375) 555-8161" OR receiver = "(725) 555-3243")
AND (year = 2021 AND month = 7 AND day = 28)
AND duration < 60;
-- +--------+----------------+----------+
-- |  name  |     caller     | duration |
-- +--------+----------------+----------+
-- | Robin  | (367) 555-5533 | 45       |Bruce
-- | Philip | (770) 555-1861 | 49       |Diana
-- +--------+----------------+----------+




-- they were planning to take the earliest flight out of Fiftyville tomorrow
-- July 29
SELECT * FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
JOIN flights ON flights.id = passengers.flight_id
JOIN airports ON airports.id = flights.origin_airport_id
WHERE (year = 2021 AND month = 7 AND day = 29)
AND flights.origin_airport_id = 8
AND (passengers.passport_number = 3592750733 OR passengers.passport_number = 5773159633);
-- +--------+-------+----------------+-----------------+---------------+-----------+-----------------+------+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate | flight_id | passport_number | seat | id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | id | abbreviation |          full_name          |    city    |
-- +--------+-------+----------------+-----------------+---------------+-----------+-----------------+------+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+
-- | 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       | 18        | 3592750733      | 4C   | 18 | 8                 | 6                      | 2021 | 7     | 29  | 16   | 0      | 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
-- | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       | 36        | 5773159633      | 4A   | 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     | 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
-- +--------+-------+----------------+-----------------+---------------+-----------+-----------------+------+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+




-- Where are the theft going
SELECT * FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE flights.origin_airport_id = 8
AND (year = 2021 AND month = 7 AND day = 29)
AND (passengers.passport_number = 3592750733 OR passengers.passport_number = 5773159633)
ORDER BY flights.hour, flights.minute;
-- +--------+-------+----------------+-----------------+---------------+-----------+-----------------+------+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate | flight_id | passport_number | seat | id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | id | abbreviation |          full_name          |    city    |
-- +--------+-------+----------------+-----------------+---------------+-----------+-----------------+------+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+
-- | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       | 36        | 5773159633      | 4A   | 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     | 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
-- | 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       | 18        | 3592750733      | 4C   | 18 | 8                 | 6                      | 2021 | 7     | 29  | 16   | 0      | 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
-- +--------+-------+----------------+-----------------+---------------+-----------+-----------------+------+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+


SELECT * FROM airports
-- +----+--------------+-----------------------------------------+---------------+
-- | id | abbreviation |                full_name                |     city      |
-- +----+--------------+-----------------------------------------+---------------+
-- | 1  | ORD          | O'Hare International Airport            | Chicago       |
-- | 2  | PEK          | Beijing Capital International Airport   | Beijing       |
-- | 3  | LAX          | Los Angeles International Airport       | Los Angeles   |
-- | 4  | LGA          | LaGuardia Airport                       | New York City |
-- | 5  | DFS          | Dallas/Fort Worth International Airport | Dallas        |
-- | 6  | BOS          | Logan International Airport             | Boston        |
-- | 7  | DXB          | Dubai International Airport             | Dubai         |
-- | 8  | CSF          | Fiftyville Regional Airport             | Fiftyville    |
-- | 9  | HND          | Tokyo International Airport             | Tokyo         |
-- | 10 | CDG          | Charles de Gaulle Airport               | Paris         |
-- | 11 | SFO          | San Francisco International Airport     | San Francisco |
-- | 12 | DEL          | Indira Gandhi International Airport     | Delhi         |
-- +----+--------------+-----------------------------------------+---------------+

-- Diana going to Boston
-- Bruce going to New York City


-- The "earliest" flight
SELECT * FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
JOIN flights ON flights.id  = passengers.flight_id
JOIN airports ON airports.id = flights.origin_airport_id
WHERE flights.origin_airport_id = 8
AND (year = 2021 AND month = 7 AND day = 29)
AND (passengers.passport_number = 3592750733 OR passengers.passport_number = 5773159633)
ORDER BY flights.hour, flights.minute
LIMIT 1;
-- +--------+-------+----------------+-----------------+---------------+-----------+-----------------+------+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate | flight_id | passport_number | seat | id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | id | abbreviation |          full_name          |    city    |
-- +--------+-------+----------------+-----------------+---------------+-----------+-----------------+------+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+
-- | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       | 36        | 5773159633      | 4A   | 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     | 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
-- +--------+-------+----------------+-----------------+---------------+-----------+-----------------+------+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-----------------------------+------------+

-- The THIEF is Bruce
-- He going to New York City
-- He called Robin
