import sqlite3
import matplotlib.pyplot as plt

# connect to the database
DB_NAME = 'cities.db'

# fetch the top 100 most populated cities and their average temperatures
def fetch_city_temperature_data():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    #ORDER BY CityInfo.city_id
    # SQL query to join CityInfo and CityWeather on city_id and get city_name and average_temperature
    cur.execute("""
        SELECT CityInfo.city_name, CityWeather.average_temperature
        FROM CityInfo
        JOIN CityWeather ON CityInfo.city_id = CityWeather.city_id
        ORDER BY CityWeather.average_temperature DESC
        LIMIT 100
    """)

    cities_data = cur.fetchall()
    conn.close()
    return cities_data

# get the city names and average temperatures
#list of tuples with a city's name and average temp
cities_data = fetch_city_temperature_data()
# iterates over the cities_data list and grabs the first element, which is the city name
city_names = [city[0] for city in cities_data]
# iterates over the cities_data list and grabs the first element, which is the temperature
temperatures = [city[1] for city in cities_data]

# create a bar graph with city_name on the x-axis and average_temperature on the y-axis
plt.figure(figsize=(20, 8))
plt.bar(city_names, temperatures, color='lightgreen')

#labels and axis titles
plt.xlabel('City', fontsize=20)
plt.ylabel('Average Temperature (°F)', fontsize=20)
plt.title('Top 100 Most Populated U.S. Cities and Their Average Temperatures', fontsize=25)
plt.xticks(rotation=90, fontsize=9)  # rotate x-axis labels for readability

# display the plot
plt.show()