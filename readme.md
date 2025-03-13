# YouTube Data ETL Pipeline with Airflow and MongoDB

## Overview

This project implements a data pipeline that extracts YouTube video data based on a specified topic, processes it, and loads it into MongoDB. The pipeline is orchestrated using Apache Airflow.

## Project Structure

```
ASSIGNMENT1/
├── airflow/
│   ├── dags/
│   │   ├── youtube_dag.py         # Main DAG definition file
│   │   ├── fetch_youtube_data.py  # Script to fetch YouTube data
│   │   └── load_data_to_mongo.py  # Script to load data into MongoDB
│   └── topic.txt                  # Contains the topic to search for
├── README.md                      # This file
└── .env                           # Environment variables (API keys, MongoDB URI)
```

## Requirements

- Python 3.7+
- Apache Airflow 2.0+
- MongoDB (local installation or MongoDB Atlas)
- YouTube Data API key

## Setup Instructions

### 1. Install Required Packages

```bash
pip install apache-airflow pymongo python-dotenv google-api-python-client
```

### 2. Configure Environment Variables

Create a `.env` file in the ASSIGNMENT1 directory with the following content:

```
YOUTUBE_API_KEY=your_youtube_api_key_here (default is 27017)
MONGO_URI=mongodb://localhost:27017/
```

Replace the values with your actual YouTube API key and MongoDB connection string.

### 3. Set Up Airflow

Set the Airflow home directory to point to your project:

change the directory to the airflow folder

```bash
export AIRFLOW_HOME=/Users/[username]/.../airflow
```

Initialize the Airflow database:

```bash
airflow db init
```

Create an admin user (first time only):

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

### 4. Configure Topic

Edit the `topic.txt` file to contain your desired search topic (e.g., "earthquake").

## Running the Pipeline

### 1. Start Airflow Services

Start the Airflow webserver:

change the directory to the airflow folder

```bash
export AIRFLOW_HOME=/Users/[username]/.../airflow
airflow webserver --port 8080
```

In a new terminal, start the Airflow scheduler:

```bash
export AIRFLOW_HOME=/Users/[username]/.../airflow
airflow scheduler
```

### 2. Access the Airflow UI

Open your browser and navigate to:

```
http://localhost:8080
```

Log in with the admin credentials you created earlier.

### 3. Run the DAG

In the Airflow UI:
1. Find the DAG named `is459_assignment_youtube`
2. Click the "Play" button to trigger the DAG manually

Alternatively, you can trigger the DAG from the command line:

```bash
export AIRFLOW_HOME=/Users/[username]/.../airflow   
airflow dags trigger is459_assignment_youtube
```

### 4. Verify Results in MongoDB

After the DAG completes successfully, connect to MongoDB to verify the data:

```bash
mongosh
use youtube_data
db.earthquake.find().limit(5)  # Replace "earthquake" with your topic
```

## Pipeline Workflow

1. **Start**: The DAG begins execution
2. **Fetch YouTube Data**: 
   - Reads the topic from `topic.txt`
   - Retrieves information for 100+ videos related to the topic
   - Saves the data to a JSON file named `{topic}.json`
3. **Load Data to MongoDB**:
   - Reads the JSON file
   - Inserts the data into a MongoDB collection named after the topic
   - Deletes the JSON file after successful loading
4. **End**: The DAG completes execution

## Troubleshooting

### DAG Not Visible in Airflow UI

If your DAG doesn't appear in the Airflow UI:

1. Ensure your DAG files are in the correct location:
   ```bash
   ls -la $AIRFLOW_HOME/dags
   ```

2. Check for syntax errors in your DAG files:
   ```bash
   python $AIRFLOW_HOME/dags/youtube_dag.py
   ```

3. Restart the Airflow scheduler:
   ```bash
   pkill -f "airflow scheduler"
   airflow scheduler
   ```

### MongoDB Connection Issues

If you encounter MongoDB connection issues:

1. Verify that MongoDB is running:
   ```bash
   mongosh
   ```

2. Check your connection string in the `.env` file
3. Ensure the pymongo package is installed:
   ```bash
   pip install pymongo
   ```

### YouTube API Issues

If you encounter issues with the YouTube API:

1. Verify your API key is correct in the `.env` file
2. Check that your API key has the YouTube Data API v3 enabled
3. Monitor your API quota usage in the Google Cloud Console

## Notes

- The DAG is configured to run daily, but you can modify the schedule in `youtube_dag.py`
- The MongoDB collection name will match your topic (e.g., "earthquake")
- At least 100 videos related to the topic will be retrieved and stored

