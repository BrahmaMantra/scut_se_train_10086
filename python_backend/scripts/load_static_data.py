import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def load_cell_data():
    """Loads cell location data from cell_loc.txt"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'cell_loc.txt')
        
        with open(data_file, 'r') as f:
            for line in f:
                cell_id, lat, lon = line.strip().split('|')
                cursor.execute(
                    "INSERT IGNORE INTO cells (cell_id, latitude, longitude) VALUES (%s, %s, %s)",
                    (cell_id, float(lat), float(lon))
                )
        
        conn.commit()
        print("Cell data loaded successfully.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error loading cell data: {e}")

def load_region_data():
    """Loads region data from region_center_loc.txt"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'region_center_loc.txt')
        
        with open(data_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                region_id = parts[0]
                center_coords = parts[1]
                boundary = parts[2]
                
                # Parse center coordinates
                center_lat, center_lon = center_coords.split(',')
                
                cursor.execute(
                    """INSERT IGNORE INTO regions 
                       (region_id, center_latitude, center_longitude, boundary) 
                       VALUES (%s, %s, %s, %s)""",
                    (region_id, float(center_lat), float(center_lon), boundary)
                )
        
        conn.commit()
        print("Region data loaded successfully.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error loading region data: {e}")

def load_region_cell_data():
    """Loads region-cell relationships from region_cell.txt"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'region_cell.txt')
        
        with open(data_file, 'r') as f:
            for line in f:
                region_id, cell_id = line.strip().split('|')
                cursor.execute(
                    "INSERT IGNORE INTO region_cells (region_id, cell_id) VALUES (%s, %s)",
                    (region_id, cell_id)
                )
        
        conn.commit()
        print("Region-cell relationships loaded successfully.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error loading region-cell data: {e}")

def load_user_data():
    """Loads user profile data from user_info.txt"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_info.txt')
        
        with open(data_file, 'r') as f:
            for line in f:
                imsi, gender, age_group = line.strip().split('|')
                cursor.execute(
                    "INSERT IGNORE INTO user_profiles (imsi, gender, age_group) VALUES (%s, %s, %s)",
                    (imsi, int(gender), int(age_group))
                )
        
        conn.commit()
        print("User data loaded successfully.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error loading user data: {e}")

if __name__ == "__main__":
    print("Loading static data...")
    load_cell_data()
    load_region_data()
    load_region_cell_data()
    load_user_data()
    print("All static data loaded!") 