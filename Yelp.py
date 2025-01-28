import os
import requests
import sqlite3
from website import fetch_city_data, store_city_data, initialize_database

# Constants 
BATCH_SIZE = 25
DB_NAME = 'cities.db'
YELP_API_KEY = '68bKQvDY-Acok2eoGhj72Hf7XKsJGkijjUqR_8d1jeCVFlnz9S4d9tzTsl7dY8LD7KgNN9XsqNcFPwu0ZuwUoNrCNhVbQNABusZWZkPyN-krg9t_o9ShkJeb3VlPZ3Yx'

def initialize_yelp_table():
    """Create the Yelp table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create IceCreamShops table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS IceCreamShops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            business_name TEXT NOT NULL,
            review_count INTEGER NOT NULL,
            rating REAL NOT NULL,
            FOREIGN KEY(city_id) REFERENCES Cities(id)
        )
    """)

    conn.commit()
    conn.close()

def fetch_yelp_data_for_city(api_key, city):
    """Fetches Yelp data for a given city."""
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.yelp.com/v3/businesses/search"
    params = {
        "term": "ice cream",
        "location": f"{city}",
        "sort_by": "review_count",
        "limit": 10
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch Yelp data for {city}. Status code: {response.status_code}")
    
def store_yelp_data(city_id, yelp_data):
    """Store Yelp data in the IceCreamShops table."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for business in yelp_data.get("businesses", []):
        business_name = business["name"]
        review_count = business["review_count"]
        rating = business["rating"]

        # Insert into IceCreamShops table
        cur.execute("""
            INSERT INTO IceCreamShops (city_id, business_name, review_count, rating)
            VALUES (?, ?, ?, ?)
        """, (city_id, business_name, review_count, rating))

    conn.commit()
    conn.close()

    
def process_yelp_data():
    """Fetch and store Yelp data for 25 cities per run."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Get the next batch of cities (25 cities per run)
    cur.execute("""
        SELECT id, city_name
        FROM Cities
        WHERE id NOT IN (SELECT DISTINCT city_id FROM IceCreamShops)
        LIMIT ?
    """, (BATCH_SIZE,))
    cities = cur.fetchall()

    conn.close()

    # Process each city in the batch
    for city_id, city_name in cities:
        try:
            print(f"Processing city: {city_name}")
            yelp_data = fetch_yelp_data_for_city(YELP_API_KEY, city_name)
            store_yelp_data(city_id, yelp_data)
            print(f"Inserted Yelp data for {city_name}.")
        except Exception as e:
            print(f"Error fetching/storing Yelp data for {city_name}: {e}")

    print("Batch processing complete.")


def main():
    """Main function to initialize the Yelp table and process Yelp data."""
    
    # Make sure Cities table is created 
    initialize_database()
    # Make sure IceCreamShops table is created
    initialize_yelp_table() 
    
    try:
        process_yelp_data()  # Process Yelp data for 25 cities
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()