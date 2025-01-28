# SI 206 Final Project -- Weather data per city
# Tabassum Chowdhury, Elise Herzog, Jessica Imaz

import requests
import sqlite3 

# Database setup
DB_NAME = "cities.db"
API_KEY = "2fb2957234e69cdb23d53592869cb02e"

def initialize_tables():
    """Create database if it doesn't exist"""

    # Connect to database (create database file if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create 'CityInfo' table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS CityInfo (
            city_id INTEGER PRIMARY KEY,
            city_name TEXT NOT NULL,
            UNIQUE(city_name)  -- Prevent duplicate entries
        )
    """)

    # Create 'CityWeather' table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS CityWeather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            average_temperature REAL NOT NULL,
            FOREIGN KEY(city_id) REFERENCES CityInfo(city_id)
        )
    """)

    # Commit changes to save table structure in database
    conn.commit()
    # Close database
    conn.close()

def fetch_weather_data(city_name):
    """Fetch average temperature for a given city"""

    # Handle special cases for NYC and St. Petersburg
    if city_name.lower() == "new york city":
        city_name = "New York"
    elif city_name.lower() == "st. petersburg":
        city_name = "Saint Petersburg"

    # Construct API request URL
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city_name},US&appid={API_KEY}&units=imperial"
    response = requests.get(URL)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        # Make sure temperature data exists in response
        if "main" in data and "temp" in data["main"]:
            return data["main"]["temp"]
        else:
            raise ValueError(f"Temperature data missing for {city_name}")
    elif response.status_code == 401:
        raise Exception("Unauthorized access. Check your API key.")
    else:
        raise Exception(f"Failed to fetch weather data for {city_name}. Status code: {response.status_code}")

def store_weather_data(limit=25):
    """Fetch and store weather data for cities in the database."""

    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Get city data from Cities table
    cur.execute("""
        SELECT id, city_name
        FROM Cities
        WHERE id NOT IN (SELECT city_id FROM CityWeather)
        LIMIT ?
    """, (limit,))
    cities = cur.fetchall()

    count = 0
    # Iterate over the retrieved cities
    for city_id, city_name in cities:
        try:
            # Insert city info into CityInfo table if not already present
            cur.execute("""
                INSERT OR IGNORE INTO CityInfo (city_id, city_name)
                VALUES (?, ?)
            """, (city_id, city_name))

            # Fetch weather data
            average_temperature = fetch_weather_data(city_name)

            # Insert weather data into CityWeather table
            cur.execute("""
                INSERT INTO CityWeather (city_id, average_temperature)
                VALUES (?, ?)
            """, (city_id, average_temperature))
            count += 1
            print(f"Inserted weather data for {city_name}: {average_temperature}°F")
        except Exception as e:
            print(f"Error fetching/storing data for {city_name}: {e}")

    # Commit to database
    conn.commit()

    # Count total rows in the Weather table
    cur.execute("SELECT COUNT(*) FROM CityWeather")
    total_count = cur.fetchone()[0]

    conn.close()
    print(f"{total_count} rows now in the CityWeather table.")  # Accumulating total
    return count

def join_city_info_and_weather():
    """Join the CityInfo and CityWeather tables and display the results."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Perform an INNER JOIN on CityInfo and CityWeather tables
    cur.execute("""
        SELECT CityInfo.city_id, CityInfo.city_name, CityWeather.average_temperature
        FROM CityInfo
        JOIN CityWeather ON CityInfo.city_id = CityWeather.city_id
    """)
    results = cur.fetchall()

    # Print the joined data
    for row in results:
        print(f"City ID: {row[0]}, Name: {row[1]}, Avg Temp: {row[2]}°F")

    conn.close()

def main():
    """Main function to initialize the weather table and store data."""
    
    initialize_tables()
    try:
        inserted_count = store_weather_data()
        print(f"Inserted {inserted_count} rows into the CityWeather table.")
        join_city_info_and_weather() # Display joined data
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

