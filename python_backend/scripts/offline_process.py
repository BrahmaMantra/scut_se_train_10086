import argparse
import mysql.connector
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def aggregate_hourly_users(hour_to_process):
    """Aggregates user events into hourly region summaries."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        
        # Calculate time range for the hour
        start_time = hour_to_process
        end_time = hour_to_process + timedelta(hours=1)
        
        # Aggregate users by region for the specified hour
        query = """
            INSERT IGNORE INTO hourly_region_users (produce_hour, region_id, imsi)
            SELECT
                %s,
                rc.region_id,
                ue.imsi
            FROM user_events ue
            JOIN region_cells rc ON ue.cell_id = rc.cell_id
            WHERE ue.event_time >= %s AND ue.event_time < %s
            GROUP BY rc.region_id, ue.imsi
        """
        
        cursor.execute(query, (hour_to_process, start_time, end_time))
        affected_rows = cursor.rowcount
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Aggregated {affected_rows} user-region records for hour {hour_to_process}")
        return True
        
    except mysql.connector.Error as err:
        print(f"Database error during aggregation: {err}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Process offline data aggregation')
    parser.add_argument('--hour', type=str, help='Hour to process (YYYY-MM-DD HH:MM:SS format)')
    
    args = parser.parse_args()
    
    if args.hour:
        try:
            hour_to_process = datetime.strptime(args.hour, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Invalid hour format. Use YYYY-MM-DD HH:MM:SS")
            return
    else:
        # Default to previous hour
        hour_to_process = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    
    print(f"Processing data for hour: {hour_to_process}")
    
    if aggregate_hourly_users(hour_to_process):
        print("Offline processing completed successfully!")
    else:
        print("Offline processing failed!")

if __name__ == "__main__":
    main() 