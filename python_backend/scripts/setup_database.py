import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    """Creates the database if it doesn't exist."""
    try:
        # Connect without specifying database
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        
        # Create database
        db_name = os.getenv("DB_NAME")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created successfully.")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
        return False
    
    return True

def create_tables():
    """Creates all necessary tables."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        
        # Create user_profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                imsi VARCHAR(255) PRIMARY KEY,
                gender INT COMMENT '0: female, 1: male',
                age_group INT COMMENT '1: <10, 2: 10-20, 3: 20-40, 4: >40'
            )
        """)
        
        # Create cells table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cells (
                cell_id VARCHAR(255) PRIMARY KEY,
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8)
            )
        """)
        
        # Create regions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regions (
                region_id VARCHAR(255) PRIMARY KEY,
                region_name VARCHAR(255),
                center_latitude DECIMAL(10, 8),
                center_longitude DECIMAL(11, 8),
                boundary TEXT COMMENT 'Polygon boundary points'
            )
        """)
        
        # Create region_cells table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS region_cells (
                region_id VARCHAR(255),
                cell_id VARCHAR(255),
                PRIMARY KEY (region_id, cell_id),
                FOREIGN KEY (region_id) REFERENCES regions(region_id),
                FOREIGN KEY (cell_id) REFERENCES cells(cell_id)
            )
        """)
        
        # Create user_events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                imsi VARCHAR(255),
                cell_id VARCHAR(255),
                event_time DATETIME,
                INDEX idx_event_time (event_time),
                INDEX idx_imsi_time (imsi, event_time)
            )
        """)
        
        # Create hourly_region_users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hourly_region_users (
                produce_hour DATETIME,
                region_id VARCHAR(255),
                imsi VARCHAR(255),
                PRIMARY KEY (produce_hour, region_id, imsi)
            )
        """)
        
        # Create daily_region_flow table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_region_flow (
                analysis_date DATE,
                region_id VARCHAR(255),
                flow_type ENUM('inflow', 'outflow'),
                gender INT,
                age_group INT,
                user_count INT,
                PRIMARY KEY (analysis_date, region_id, flow_type, gender, age_group)
            )
        """)
        
        conn.commit()
        print("All tables created successfully.")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")
        return False
    
    return True

if __name__ == "__main__":
    print("Setting up database...")
    if create_database():
        if create_tables():
            print("Database setup completed successfully!")
        else:
            print("Failed to create tables.")
    else:
        print("Failed to create database.") 