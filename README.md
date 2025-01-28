# SI206-Final-Project

What the Entire Project Does

This project analyzes whether there is a correlation between the average temperature in a city and the ratings of its ice cream shops. Here’s how the scripts work together:
	1.	Data Collection:
	•	website.py collects information about the top 100 most populated U.S. cities.
	•	weather.py retrieves temperature data for these cities from the OpenWeatherMap API.
	•	yelp.py gathers Yelp data about ice cream shops in these cities, including review counts and ratings.
	2.	Data Organization:
	•	The data is stored in a normalized database structure with tables for city information (Cities), temperature data (CityWeather), and Yelp ice cream shop data (IceCreamShops).
	3.	Analysis:
	•	calculations.py integrates data from the database to compute insights like population statistics, temperature extremes, and average ice cream shop ratings.
	4.	Output:
	•	The results of the analysis are written to a text file (calculations.txt), providing a clear summary of the data and allowing for further investigation of potential correlations.
This cohesive system combines web scraping, API integration, and data analysis to answer the research question: Is there a relationship between temperature and the ratings of ice cream shops in a city?


What Each File Does

website.py
The website.py script is responsible for scraping data about the top 100 most populated cities in the U.S. from the World Population Review website. Using the BeautifulSoup library, it extracts the city names, their states, and population data, then stores this information in a database table called Cities. The script ensures that only unique city and state combinations are added to the database. This forms the foundational dataset, which is used by other scripts to perform further operations.
Key tasks performed by website.py:
	•	Scrapes the names, states, and populations of cities from the website.
	•	Creates a Cities table in the database if it doesn’t already exist.
	•	Stores the scraped data in the database with safeguards to avoid duplicates.
 
weather.py
The weather.py script interacts with the OpenWeatherMap API to retrieve temperature data for each city listed in the Cities table. The script organizes this data into two tables: CityInfo (holding city-specific details like names and states) and CityWeather (storing temperature data linked to cities using a foreign key). This separation ensures normalized and structured data storage. The script processes a batch of 25 cities at a time and records their average temperatures in the database.
Key tasks performed by weather.py:
	•	Queries the OpenWeatherMap API for average temperatures for each city.
	•	Splits data into two tables: CityInfo (city details) and CityWeather (temperature data).
	•	Processes cities in batches of 25 to handle large datasets efficiently.
 
yelp.py
The yelp.py script leverages the Yelp API to fetch information about ice cream shops in the cities listed in the Cities table. For each city, it retrieves data on the top 10 most-reviewed ice cream shops, including their names, review counts, and average ratings. This data is stored in a table called IceCreamShops, which links each shop to its corresponding city using a foreign key.
Key tasks performed by yelp.py:
	•	Queries the Yelp API to gather data about the top 10 most reviewed ice cream shops for each city.
	•	Stores business details (name, review count, and rating) in the IceCreamShops table.
	•	Processes cities in batches of 25 for efficiency.
 
What calculations.py Does
The calculations.py script performs calculations and analysis on the data stored in the database. It uses SQL queries to extract insights and writes the results to a text file for reporting. The script integrates data from the Cities, CityWeather, and IceCreamShops tables to compute metrics such as:
	•	Total and average population of the top 100 cities.
	•	Minimum and maximum temperatures, along with the cities that recorded them.
	•	Average Yelp ratings for most reviewed ice cream shops in each city.
The script then organizes these results and saves them in a text file called calculations.txt, providing a summary of the data and insights derived from the project.
Key tasks performed by calculations.py:
	•	Calculates population statistics from the Cities table.
	•	Fetches and analyzes temperature data from the CityWeather table.
	•	Computes average Yelp ratings for ice cream shops in each city.
	•	Writes the results to a text file for easy access and reporting.
 
What temp_by_city_vis.py does
Gets the list of top 100 US cities from CityInfo table, Joins that with CityWeather on city_id to connect the city names with their average temperature
Creates a bar graph with the city names on the x axis and temperature on the yaxis

What rev_by_city_vis.py does
Gets the list of top 100 US cities from CityInfo table, Joins that with IceCreamShops table on city_id
Groups by the city_id so that the calculation below happens by city
Uses SQL command ‘AVG’ to make the average rating from the rating column
Creates a bar graph with city names on the x axis and average ice cream shop rating for that city on the y axis

What temp_vs_rating_vis.py does
Joins CityInfo with CityWeather and IceCreamShops so that we have city_id connecting the average temperature in that city and the average ice cream shop rating
Creates a scatter plot that shows the average temp on the x axis and average rating on the y axis, with each bubble representing a city


