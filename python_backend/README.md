# Mobile User Data Analysis API

This project provides a backend system to process and analyze mobile user data, based on the requirements in `api.md`. It includes scripts for database setup, data loading, real-time ingestion, offline data processing, and a FastAPI-based API server.

## Directory Structure

```
python_backend/
├── api/
│   ├── __init__.py
│   ├── database.py       # Database connection utilities
│   ├── main.py           # FastAPI application and endpoints
│   └── models.py         # Pydantic models for API
├── data/                 # Data files
│   ├── cell_loc.txt
│   ├── region_cell.txt
│   ├── region_center_loc.txt
│   └── user_info.txt
├── scripts/
│   ├── __init__.py
│   ├── setup_database.py   # Creates database and tables
│   ├── load_static_data.py # Loads data from .txt files into DB
│   ├── ingestion.py        # Ingests real-time data from the Java app
│   └── offline_process.py  # Runs periodic offline aggregation tasks
├── env.example          # Example environment config
└── requirements.txt      # Python dependencies
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- MySQL Server
- Java (to run the data generator)

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
Create a `.env` file by copying the example and edit it with your MySQL credentials.
```bash
cp env.example .env
# Now, edit the .env file with your MySQL credentials
```

### 5. Setup Database Schema
Run the setup script to create the database and all necessary tables.
```bash
python scripts/setup_database.py
```

### 6. Load Static Data
Load the data from all `.txt` files into the newly created database tables.
```bash
python scripts/load_static_data.py
```

## Running the System

### 1. Start the Data Pipeline
The entire pipeline is now in Python. Run the data generator and pipe its output to the ingestion script. Make sure your virtual environment is active.

From the `python_backend` directory:
```bash
source venv/bin/activate
python scripts/generate_data.py | python scripts/ingestion.py
```
This process will run continuously, feeding live user events into the `user_events` table.

### 2. Run the Offline Processing
This script should be run periodically (e.g., every hour via a cron job). It aggregates the raw event data into summary tables to speed up API queries.

To run it manually for a specific hour:
```bash
python scripts/offline_process.py --hour "2025-06-11 10:00:00"
```

Without arguments, it will process data for the previous hour:
```bash
python scripts/offline_process.py
```

### 3. Start the API Server
Finally, start the FastAPI server.
```bash
uvicorn api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000/docs`.

## API Endpoints

The system provides the following API endpoints as specified in `api.md`:

1. `GET /v1/userCountByRegionAndTime` - Count users by region, time, and portrait
2. `GET /v1/userListByRegionAndTime` - Get user list by region, time, and portrait  
3. `GET /v1/regionPortrait` - Get region portrait statistics
4. `GET /v1/regionInflowOutflow` - Get region inflow/outflow analysis

## Database Schema

The system uses the following main tables:
- `user_profiles` - User demographic information
- `cells` - Cell tower locations
- `regions` - Geographic regions
- `region_cells` - Region-cell relationships
- `user_events` - Raw user movement events
- `hourly_region_users` - Aggregated hourly user counts by region
- `daily_region_flow` - Daily inflow/outflow statistics 