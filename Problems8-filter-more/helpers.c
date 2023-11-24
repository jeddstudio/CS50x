#include "helpers.h"
#include <math.h>

// (int height, int width, RGBTRIPLE image[height][width]) is CS50 made for us
// It is automaticly get picture heigh and width
// .rgbtRed, ..rgbtGreen and .rgbtBlue is a "typedef struct" from bmp.h


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Get the pixel 1 by 1 from left to right
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Get current pixel's colour
            float red = image[i][j].rgbtRed;
            float green = image[i][j].rgbtGreen;
            float blue = image[i][j].rgbtBlue;

            // Algorithm of Grayscale
            float new_pixel = round((red + green + blue) / 3);

            // Update a new colour to current pixel
            image[i][j].rgbtRed = new_pixel;
            image[i][j].rgbtGreen = new_pixel;
            image[i][j].rgbtBlue = new_pixel;
        }
    }
    return;
}


// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Get the pixel 1 by 1 from left to right
    for (int i = 0; i < height; i++)
    {
        // "width / 2", because if you don't do this, it will nothing to change because
        // if 0-5(total 6), only need to loop 3 times, if loop more than 3 times, it will return to original
        for (int j = 0, new_position = width - 1; j < width / 2; j++, new_position--)
        {
            // Save the current pixel to tmp
            RGBTRIPLE tmp = image[i][j];

            // Algorithm of Reflect
            // Swap the last and first pixel
            // e.g 1 become 10
            image[i][j] = image[i][new_position];
            // e.g 10 become 1
            image[i][new_position] = tmp;
        }
    }
    return;
}



// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // for temporay data storage
    RGBTRIPLE tmp[height][width];

    // Get the pixel 1 by 1 from left to right
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // store the current pixel to tmp
            tmp[i][j] = image[i][j];
        }
    }

    // Get the pixel 1 by 1 from left to right
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Nearby pixels's(3x3 matrix) colour channel
            float nearby_red = 0;
            float nearby_green = 0;
            float nearby_blue = 0;

            // A algorithm virable
            // if current pixel at the edge, it might not are 3x3, it maybe 2x2, 2x3
            // counting how many vaild nearby pixel
            float pixel_counter = 0;

            // Get the pixel 1 by 1 from left to right in the matrix
            // "-1" because start form -1 => 0 => 1, from left to right
            for (int x = -1; x < 2; x++)
            {
                // y is column in the matrix, start form -1 => 0 => 1
                for (int y = -1; y < 2; y++)
                {
                    // get the nearby pxiel(e.g the first will be top left then top then top right)
                    int row = i + x;
                    int column = j + y;

                    // Ensure no pixel is taken outside the picture
                    if (row >= 0 && row <= (height - 1) && column >= 0 && column <= (width - 1))
                    {
                        // Algorithm of Blur
                        // result colour form nearby pixel after the algorithm
                        nearby_red = nearby_red + image[row][column].rgbtRed;
                        nearby_green = nearby_green + image[row][column].rgbtGreen;
                        nearby_blue = nearby_blue + image[row][column].rgbtBlue;
                        pixel_counter++;
                    }
                    // store the colour form nearby pixel to tmp
                    tmp[i][j].rgbtRed = round(nearby_red / pixel_counter);
                    tmp[i][j].rgbtGreen = round(nearby_green / pixel_counter);
                    tmp[i][j].rgbtBlue = round(nearby_blue / pixel_counter);
                }
            }
        }
    }
    // Get the pixel 1 by 1 from left to right
    // The loop above actually only processes one pixel(e.g pixel 0, 0 then the next is 0, 1)
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Update the current pixel colour
            image[i][j].rgbtRed = tmp[i][j].rgbtRed;
            image[i][j].rgbtGreen = tmp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = tmp[i][j].rgbtBlue;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // for temporay data storage
    RGBTRIPLE tmp[height][width];

    // Get the pixel 1 by 1 from left to right
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Save the current pixel to tmp
            tmp[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // store Gx and Gy colour
            float Gx_red = 0;
            float Gx_green = 0;
            float Gx_blue = 0;
            float Gy_red = 0;
            float Gy_green = 0;
            float Gy_blue = 0;

            // Gx and Gy matrix
            int pixel_gx = 0;
            int pixel_gy = 0;

            // Gx calculation
            // Get the Gx pixel 1 by 1 from Gx matrix
            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    // Get the value in the matrix with the condition
                    // this come from the Gx formula
                    if ((x == -1 && y == -1) || (x == 1 && y == -1))
                    {
                        pixel_gx = -1;
                    }
                    else if (x == 0 && y == -1)
                    {
                        pixel_gx = -2;
                    }
                    else if (x == 0 && y == 1)
                    {
                        pixel_gx = 2;
                    }
                    else if ((x == -1 && y == 1) || (x == 1 && y == 1))
                    {
                        pixel_gx = 1;
                    }
                    else
                    {
                        pixel_gx = 0;
                    }
                    // get the Gx matrix 1 by 1 start from Top left to bottom right
                    int row = i + x;
                    int column = j + y;
                    // Ensure no pixel is taken outside the picture
                    if (row >= 0 && row <= (height - 1) && column >= 0 && column <= (width - 1))
                    {
                        // Algorithm of Detect edges
                        Gx_red = Gx_red + (pixel_gx * image[row][column].rgbtRed);
                        Gx_green = Gx_green + (pixel_gx * image[row][column].rgbtGreen);
                        Gx_blue = Gx_blue + (pixel_gx * image[row][column].rgbtBlue);
                    }
                }
            }

            // Gy calculation
            // Get the Gy pixel 1 by 1 from Gy matrix
            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    // Get the value in the matrix with the condition
                    // this come from the Gy formula
                    if ((x == -1 && y == -1) || (x == -1 && y == 1))
                    {
                        pixel_gy = -1;
                    }
                    else if ((x == 1 && y == -1) || (x == 1 && y == 1))
                    {
                        pixel_gy = 1;
                    }
                    else if ((x == -1 && y == 0))
                    {
                        pixel_gy = -2;
                    }
                    else if ((x == 1 && y == 0))
                    {
                        pixel_gy = 2;
                    }
                    else
                    {
                        pixel_gy = 0;
                    }
                    // get the Gx matrix 1 by 1 start from Top left to bottom right
                    int row = i + x;
                    int column = j + y;
                    // Ensure no pixel is taken outside the picture
                    if (row >= 0 && row <= (height - 1) && column >= 0 && column <= (width - 1))
                    {
                        // Algorithm of Detect edges
                        Gy_red = Gy_red + (pixel_gy * image[row][column].rgbtRed);
                        Gy_green = Gy_green + (pixel_gy * image[row][column].rgbtGreen);
                        Gy_blue = Gy_blue + (pixel_gy * image[row][column].rgbtBlue);
                    }
                }
            }
            // Calculation of Gx Gy Algorithm
            // square root of (Gx*Gx) + (Gy*Gy)
            int square_red = round(sqrt((Gx_red * Gx_red) + (Gy_red * Gy_red)));
            int square_green = round(sqrt((Gx_green * Gx_green) + (Gy_green * Gy_green)));
            int square_blue = round(sqrt((Gx_blue * Gx_blue) + (Gy_blue * Gy_blue)));
            if (square_red > 255)
            {
                square_red = 255;
            }
            if (square_green > 255)
            {
                square_green = 255;
            }
            if (square_blue > 255)
            {
                square_blue = 255;
            }
            // Save the calculation result to tmp
            tmp[i][j].rgbtRed = square_red;
            tmp[i][j].rgbtGreen = square_green;
            tmp[i][j].rgbtBlue = square_blue;
        }
    }
    // Get the pixel 1 by 1 from left to right
    // The loop above actually only processes one pixel(e.g pixel 0, 0 then the next is 0, 1)
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Update the current pixel colour
            image[i][j].rgbtRed = tmp[i][j].rgbtRed;
            image[i][j].rgbtGreen = tmp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = tmp[i][j].rgbtBlue;
        }
    }
    return;
}