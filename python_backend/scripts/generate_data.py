import os
import random
import sys
import time
from pathlib import Path

def get_data_from_file(file_path):
    """Reads lines from a file."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def main():
    """Generates simulated user movement data and prints to stdout."""
    
    # Correctly locate the data directory relative to this script
    data_dir = Path(__file__).parent.parent / 'data'
    
    try:
        user_info_lines = get_data_from_file(data_dir / 'user_info.txt')
        cell_loc_lines = get_data_from_file(data_dir / 'cell_loc.txt')
    except FileNotFoundError as e:
        print(f"Error: Data file not found. Make sure {e.filename} exists.", file=sys.stderr)
        sys.exit(1)

    # 1. Process cell data: sort, index, and create lookup maps
    cells = []
    for line in cell_loc_lines:
        cell_id, lat, lon = line.split('|')
        cells.append({'cell': cell_id, 'lat': lat, 'lon': lon})

    # Sort cells by ID (as integers) to mimic the Java logic
    cells.sort(key=lambda x: int(x['cell']))

    # Assign an index to each cell after sorting
    for i, cell in enumerate(cells):
        cell['index'] = i

    # Create lookup maps for efficient access
    cell_index_map = {c['index']: c for c in cells}
    cell_id_to_index_map = {c['cell']: c['index'] for c in cells}
    
    num_cells = len(cells)
    user_status = {}  # Stores the last known cell_id for each user

    print("Starting Python data generator...", file=sys.stderr)

    # 2. Main loop to generate data
    try:
        while True:
            # Randomly pick a user
            random_user_line = random.choice(user_info_lines)
            imsi = random_user_line.split('|')[0]

            # Get the user's last cell index, or a random one if new
            last_cell_id = user_status.get(imsi)
            last_index = cell_id_to_index_map.get(last_cell_id, random.randint(0, num_cells - 1))

            # Simulate a small step
            step = random.randint(-3, 3)
            if step == 0:
                continue

            # 3. Calculate next position with boundary checks
            next_index = last_index + step
            # If the step takes the user out of bounds, try stepping in the opposite direction
            if not (0 <= next_index < num_cells):
                next_index = last_index - step
            # If still out of bounds, stay put (this is a fallback)
            if not (0 <= next_index < num_cells):
                next_index = last_index

            next_cell = cell_index_map[next_index]
            user_status[imsi] = next_cell['cell']

            # 4. Generate output string and print to stdout
            curr_time_ms = int(time.time() * 1000)
            data = f"{imsi}|{next_cell['cell']}|{next_cell['lat']}|{next_cell['lon']}|{curr_time_ms}"
            
            print(data, flush=True) # flush=True is important when piping output
            
            time.sleep(0.1) # Sleep for 100ms

    except KeyboardInterrupt:
        print("Data generator stopped by user.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred in the data generator: {e}", file=sys.stderr)


if __name__ == "__main__":
    main() 