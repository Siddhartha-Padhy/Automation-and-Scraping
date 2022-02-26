# Flipkart_scraper
It is a python program that scrapes all the data about a book from the [Flipkart](https://www.flipkart.com/) Website and stores them in a csv file named by the book name.<br>
Max limit and min limit of price can be set.

## Known improvements to be made
- Takes a lot of time to scrape the data. Multi-threading can be used.
- Just gives the data, doesn't select the best product. Auto **add to cart** feature can be added.

## Setup and Run
Ensure that [selenium](https://pypi.org/project/selenium/) package is installed.
In order to run the program from Command Line Interface use the following command in windows:<br>
```
set PATH=%PATH%;C:path-to-your-folder
```
Now run the program and enter required information as prompted.<br>
The CSV file will be found in the same directory.
