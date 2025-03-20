import random
import psycopg2
from datetime import datetime, timedelta

# Database connection settings
DB_SETTINGS = {
    "dbname": "employee",
    "user": "postgres",
    "password": "nikhil",
    "host": "localhost",
    "port": "5432"
}

# Employees list
employees = ["Jitendra", "Gaurav", "Dipanshu", "Abhijeet", "Nikhil", "Amita", "Claudia"]

# Weather conditions
weather_conditions = ["Clear", "Rainy", "Snowy", "Cloudy", "Stormy"]

# Function to generate random commute time (minutes)
def random_commute_time():
    return random.randint(25, 60)

# Generate attendance data with daily timestamp focus
def generate_attendance_data():
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
    data = []

    current_date = start_date
    while current_date <= end_date:
        daily_weather = random.choice(weather_conditions)  # Consistent weather for the day
        is_holiday = current_date.weekday() >= 5  # Saturday (5) and Sunday (6)

        for employee in employees:
            day_of_week = current_date.strftime("%A")
            in_office = 1 if current_date.weekday() in [1, 4] and not is_holiday else 0  # Only Tue & Fri, not holidays
            commute_time = random_commute_time() if in_office else 0
            month = current_date.month

            # Add formatted date (YYYY-MM-DD) to the data
            formatted_date = current_date.strftime("%Y-%m-%d")
            
            data.append((formatted_date, employee, day_of_week, commute_time, month, is_holiday, daily_weather, in_office))

        current_date += timedelta(days=1) 

    # Ensure data is ordered by timestamp
    data.sort(key=lambda x: x[0])

    return data

# Insert data into PostgreSQL
def insert_data_into_db(data):
    conn = psycopg2.connect(**DB_SETTINGS)
    cur = conn.cursor()

    # Create table if not exists (timestamp now as date)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employee_attendance (
            timestamp DATE,
            employee_name TEXT,
            day_of_week TEXT,
            time_to_reach_office INT,
            month INT,
            is_holiday BOOLEAN,
            weather_condition TEXT,
            in_office INT,
            PRIMARY KEY (timestamp, employee_name)
        );
    """)

    # Insert data
    insert_query = """
        INSERT INTO employee_attendance (timestamp, employee_name, day_of_week, time_to_reach_office, month, is_holiday, weather_condition, in_office)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (timestamp, employee_name) DO NOTHING;
    """

    cur.executemany(insert_query, data)
    conn.commit()
    cur.close()
    conn.close()

# Generate and insert data
if __name__ == "__main__":
    dataset = generate_attendance_data()
    insert_data_into_db(dataset)
    print("✅ Dataset with full attendance info successfully inserted into PostgreSQL")
