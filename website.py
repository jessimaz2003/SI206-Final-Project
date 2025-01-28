# SI 206 Final Project -- Website Scraping using BeautifulSoup
# Elise Herzog, Jessica Imaz, Tabassum Chowdhury
# in this file we gather information from worldpopulationreview.com to find the top 100 ciites in the US by population

import requests 
from bs4 import BeautifulSoup
import sqlite3


# set up database
DB_NAME = 'cities.db'

# create database and table if it doesn't exist already
def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Cities (
            id INTEGER PRIMARY KEY, 
            city_name TEXT NOT NULL,
            rank INTEGER NOT NULL,
            population_2024 INTEGER NOT NULL,
            UNIQUE(city_name)  -- Prevent duplicate entries
        )
    """)
    conn.commit()
    conn.close()

# scrape city data from the website
def fetch_city_data():
    URL = "https://worldpopulationreview.com/us-cities"
    response = requests.get(URL)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch the webpage. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")

    # find the table
    table = soup.find("table", {"class": "wpr-table"})
    if not table:
        # if the table can't be found, the class name is probably wrong
        raise ValueError("Table not found. Verify class name.")
    
    tbody = table.find("tbody")
    if not tbody:
        raise ValueError("<tbody> section not found in the table")
    
    rows = tbody.find_all("tr")
    data = []
    for row in rows:
        #find rank, city, population columns in the row
        rank_cell = row.find("td")
        city_cell = row.find("th")
        population_cell = row.find_all("td")[2] if len(row.find_all("td")) > 1 else None
    
        if rank_cell and city_cell:
            rank = rank_cell.text.strip()
            city_name = city_cell.text.strip()
            population_2024 = population_cell.text.strip().replace(',','')
            try:
                data.append({"rank": int(rank), "city_name": city_name, "population_2024": population_2024})
            except ValueError:
                continue  # skip rows if they have invalid rank data

    return data

# fill the database with the information from the website
def store_city_data(data, limit=25): #limit to 25 items per run
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # count existing rows
    cur.execute("SELECT COUNT(*) FROM Cities")
    existing_count = cur.fetchone()[0]

    count = 0
    for item in data:
        try:
            cur.execute("""
                INSERT OR IGNORE INTO Cities (rank, city_name, population_2024)
                VALUES (?, ?, ?)
            """, (item["rank"], item["city_name"], item["population_2024"]))
            if cur.rowcount > 0:  # if a row was inserted
                count += 1 #increase the count of rows
            if count >= limit:
                break  # stop once limit of 25 items is reached
        except sqlite3.IntegrityError:
            continue  #skip if there's duplicate entries

    conn.commit()
    conn.close()
    print(f"{existing_count + count} rows now in the table.") #keep track of how many rows are in the database so far
    return count



def main():
    initialize_database()
    try:
        city_data = fetch_city_data()
        inserted_count = store_city_data(city_data) #keep track of how many rows were inserted each time
        print(f"Insterted {inserted_count} rows into the table.") #shows if the store_city_data function is working
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
    