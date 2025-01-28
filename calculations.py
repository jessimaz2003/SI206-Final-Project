import sqlite3

#connect to database 
DB_NAME = 'cities.db'


### CALCULATIONS FROM THE WEBSITE FILE (CITIES TABLE) ###
#calculate the total population of the top 100 cities
def total_population():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT SUM(population_2024) FROM Cities")
    result = cur.fetchone()[0]
    conn.close()
    return result

# calculate the average population
def average_population():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT AVG(population_2024) FROM Cities")
    result = cur.fetchone()[0]
    conn.close()
    return result

### CALCULATIONS FROM THE WEATHER FILE (CITYWEATHER TABLE) ###
# get all city names and temperatures from the CityWeather table
def fetch_all_city_weather():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    #select the city_name from the CityInfo table, and the average_temperature from the CityWeather table
    #JOIN operation connects the CityWeather table with the CityInfo table by matching rows where the city_id in CityWeather equals the city_id in CityInfo
    cur.execute("SELECT CityInfo.city_name, CityWeather.average_temperature FROM CityWeather JOIN CityInfo ON CityWeather.city_id = CityInfo.city_id")
    
    # make a list of tuples (city_name, temperature)
    city_weather = cur.fetchall()  
    conn.close()
    return city_weather

# calculate the min temp and its city
def min_temperature():
    city_weather = fetch_all_city_weather()
    if not city_weather:  #check if the list is empty
        return None, None  # return None for both city and temperature if no data
    
    # initially, the minimum should be the first city's temp
    min_temp = city_weather[0][1]
    min_temp_city = f"{city_weather[0][0]}, {city_weather[0][1]}"
    
    # iterate through the list and track the smallest value and its city
    for city_name, temp in city_weather:
        if temp < min_temp:
            min_temp = temp
            min_temp_city = f"{city_name}"
    
    return min_temp, min_temp_city

#calculate the max temp and its city
def max_temperature():
    city_weather = fetch_all_city_weather()
    if not city_weather:  #if the list is empty
        return None, None  # return None for both city and temperature if no data
    
    # initially, maximum will be the first city's temp
    max_temp = city_weather[0][1]
    max_temp_city = f"{city_weather[0][0]}, {city_weather[0][1]}"
    
    #track the largest value and its city
    for city_name, temp in city_weather:
        if temp > max_temp:
            max_temp = temp
            max_temp_city = f"{city_name}"
    
    return max_temp, max_temp_city

### CALCULATIONS FROM THE YELP FILE (ICECREAMSHOPS table) ###
#calculate average rating for ice cream shops in each city
def fetch_all_yelp_data():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # select the columns we want from the tables: city_name from CityInfo table, rating from the IceCreamShops table:
    # AVG(IceCreamShops.rating) AS average rating: finds average rating of ice cream shops in that city
    #   calculated from the rating column in IceCreamShops table
    # JOIN CityInfo and IceCreamShops on the city_id column
    #   for every ice cream shop in the table, JOIN makes sure we also have the city info from CityInfo table
    # group it by the city_id so all shops located in the same city are together
    #   then, average is calculated per group (city)
    cur.execute("""
        SELECT CityInfo.city_name, AVG(IceCreamShops.rating) AS average_rating
        FROM IceCreamShops
        JOIN CityInfo ON IceCreamShops.city_id = CityInfo.city_id
        GROUP BY IceCreamShops.city_id
    """)

    yelp_data = cur.fetchall() #tuples containing city_name, average_rating
    conn.close()
    return yelp_data


# write the results to a text file
def write_to_file(filename):
    with open(filename, 'w') as f:
        f.write("Website Calculations\n")
        f.write(f"Total Population: {total_population()}\n")
        f.write(f"Average Population: {average_population()}\n")
        f.write("\n\n")
        f.write("Weather Calculations\n")
        # write min and max temperature with their respective cities
        min_temp, min_city = min_temperature()
        max_temp, max_city = max_temperature()
        
        f.write(f"Minimum Temperature: {min_temp}°F, {min_city}\n")
        f.write(f"Maximum Temperature: {max_temp}°F, {max_city}\n")

        f.write("\n\n")
        f.write("Yelp Calculations\n")
        
        # average ratings for ice cream shops in each city
        for city_name, avg_rating in fetch_all_yelp_data():
            f.write(f"Average rating for ice cream shops in {city_name}: {avg_rating:.1f}\n")


# main to write the calculations to a file
def main():
    filename = "calculations.txt"
    write_to_file(filename)
    print(f"Calculations have been written to {filename}")

if __name__ == "__main__":
    main()
