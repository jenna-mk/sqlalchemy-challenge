# Module 10 Challenge: Hawaii Weather Analysis
The purpose of this challenge is use SQLAlchemy and Flask to pull weather information from a sqlite database and perform an analysis find and graph various metrics such as precipitation and temperature.

## Part 1: Data Analysis and Exploration
The first part of this challenge is to perform precipitation and station analyses. First, I used the SQLAlchemy create_engine() function to connect to the provided SQLite database, used the automap_base() function to reflect the tables into classes, and saved these references into classes named Measurement and Station, then created a SQLAlchemy session to link Python to the database

Next, I performed a precipitation analysis over the past year of collected data by finding the most recent date in the dataset and then creating a query to extract the previous 12 months of precipitation data from that date. The results were loaded into a Pandas DataFrame and plotted as a bar graph, which can be found in Starter_Code/climate_starter.ipynb, and the summary statistics printed below.

Next, I performed a station analysis by querying the station class to find the total number of stations included in the dataset. I found the most active station by creating a query that calculated the observation counts for each station and listed them in descending order. Using the listed ids, I created a query that found the maximum, minimum, and average temperatures for the most active station. Using this same station id, I created another query which extracted the previous 12 months of temperature observation data and plotted the results as a histogram with 12 bins, which can be found in Starter_Code/climate_starter.ipynb.

## Part 2: Climate App Design
The second part of this challenge is to design a Flask API using the queries created in Part 1. The routes created for this section are as follows:
* /
  - Starts at the homepage
  - Lists all available routes for navigation
* /api/v1.0/precipitation
  - Returns the JSON representation of a dictionary where date is the key and prcp is the value, using the query results from the previous year of precipitation data
* /api/v1.0/stations
  - Returns a JSON list of the stations
* /api/v1.0/tobs
  - Returns a JSON list of temperature observations for the most active station over the previous year
* /api/v1.0/(start) and /api/v1.0/(start)/(end)
  - Returns a JSON list of the minimum, maximum, and average temperature for a user-specified start or start-end range
The code for these routes are in Starter_Code/app.py.
