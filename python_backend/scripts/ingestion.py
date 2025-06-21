import sys
import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def insert_event(imsi, cell_id, timestamp_ms):
    """Inserts a user event into the database."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        
        # Convert timestamp from milliseconds to datetime
        event_time = datetime.fromtimestamp(int(timestamp_ms) / 1000)
        
        cursor.execute(
            "INSERT INTO user_events (imsi, cell_id, event_time) VALUES (%s, %s, %s)",
            (imsi, cell_id, event_time)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}", file=sys.stderr)
    except Exception as e:
        print(f"Error processing event: {e}", file=sys.stderr)

def main():
    """Main ingestion loop."""
    print("Starting data ingestion...", file=sys.stderr)
    
    for line in sys.stdin:
        try:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split('|')
            if len(parts) == 5:
                imsi, cell_id, lat, lon, curr_time = parts
                insert_event(imsi, cell_id, curr_time)
            else:
                print(f"Invalid data format: {line}", file=sys.stderr)
                
        except KeyboardInterrupt:
            print("Ingestion stopped by user.", file=sys.stderr)
            break
        except Exception as e:
            print(f"Error processing line: {e}", file=sys.stderr)

if __name__ == "__main__":
    main() 