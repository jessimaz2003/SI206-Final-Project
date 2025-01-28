import sqlite3
import matplotlib.pyplot as plt 

# connect to the database
DB_NAME = 'cities.db'

# fetch the cities, their average temperature, and average Yelp rating
def fetch_city_weather_yelp_data():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # SQL query to join CityInfo, CityWeather, and IceCreamShops
    cur.execute("""
        SELECT CityInfo.city_name, CityWeather.average_temperature, AVG(IceCreamShops.rating) AS average_rating
        FROM IceCreamShops
        JOIN CityInfo ON IceCreamShops.city_id = CityInfo.city_id
        JOIN CityWeather ON CityInfo.city_id = CityWeather.city_id
        GROUP BY CityInfo.city_id
        ORDER BY CityWeather.average_temperature
    """)

    city_weather_yelp_data = cur.fetchall()
    conn.close()
    return city_weather_yelp_data

# get the average temperature and average Yelp rating for each city
city_weather_yelp_data = fetch_city_weather_yelp_data()
# get the average temperature from city_weather_yelp_data
average_temperatures = [data[1] for data in city_weather_yelp_data]
# get the average yelp ratings
average_yelp_ratings = [data[2] for data in city_weather_yelp_data]

#create a scatter plot with average temperature on the x-axis and average Yelp rating on the y-axis
plt.figure(figsize=(10, 6))
plt.scatter(average_temperatures, average_yelp_ratings, color='blue', alpha=0.4)

#labels and title
plt.xlabel('Average Temperature (°F)', fontsize=12)
plt.ylabel('Average Yelp Rating for Top 10 Most Reviewed Ice Cream Shops', fontsize=10)
plt.title("Average Temperature vs. Average Yelp Rating in America's 100 Most Populated Cities", fontsize=14)

# x and y axis limits
plt.xlim(0, 100)  #from 0 to 100°F for temperature
plt.ylim(0, 5)    #from 0 to 5 stars for Yelp rating

# Show the plot
plt.show()