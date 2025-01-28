import matplotlib.pyplot as plt
import sqlite3

DB_NAME = 'cities.db'
#fetch the cities and their average Yelp ratings 
def fetch_city_yelp_data():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # SQL query to join CityInfo and IceCreamShops on city_id and get city_name and average rating
    cur.execute("""
        SELECT CityInfo.city_name, AVG(IceCreamShops.rating) AS average_rating
        FROM IceCreamShops
        JOIN CityInfo ON IceCreamShops.city_id = CityInfo.city_id
        GROUP BY IceCreamShops.city_id
        ORDER BY average_rating DESC
        LIMIT 100
    """)

    cities_yelp_data = cur.fetchall()
    conn.close()
    return cities_yelp_data

# get city names and their average Yelp ratings
cities_yelp_data = fetch_city_yelp_data()
# get the first element of cities_yelp_data, which is the city name
city_names = [city[0] for city in cities_yelp_data]
# get the second element of cities_yelp_data, which is the city name
yelp_ratings = [city[1] for city in cities_yelp_data]

#create a bar graph with city_name on the x-axis and average Yelp rating on the y-axis
plt.figure(figsize=(20, 8))
plt.bar(city_names, yelp_ratings, color='lightpink')

# axis labels and titles
plt.xlabel('City', fontsize=20)
plt.ylabel('Average Ice Cream Shop Yelp Rating From Top 10 Most Reviewed Shops', fontsize=11)
plt.title('Top 100 Most Populated U.S. Cities and Their Average Ice Cream Shop Yelp Ratings', fontsize=25)

plt.xticks(rotation=90, fontsize=8)

# display the plot

plt.show()