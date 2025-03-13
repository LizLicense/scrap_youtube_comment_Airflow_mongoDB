import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_data_to_mongodb(**kwargs):
    """
    Load data from JSON file to MongoDB and delete the file
    """
    # Get MongoDB connection string from environment variable
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    
    # Read topic from file
    with open('/Users/lizliao/Downloads/ASSIGNMENT1/topic.txt', 'r') as f:
        topic = f.read().strip()
    
    # JSON file path
    json_file = f'/Users/lizliao/Downloads/ASSIGNMENT1/{topic}.json'
    
    # Check if JSON file exists, if not, fetch the data first
    if not os.path.exists(json_file):
        print(f"JSON file {json_file} not found. Fetching YouTube data first...")
        from fetch_youtube_data import get_youtube_data
        
        # Fetch data
        videos_data = get_youtube_data(topic)
        
        # Save to JSON file
        with open(json_file, 'w') as f:
            json.dump(videos_data, f, indent=2)
        print(f"Created {json_file} with {len(videos_data)} videos")
    
    # Load data from JSON file
    with open(json_file, 'r') as f:
        videos_data = json.load(f)
    
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client['youtube_data']
    collection = db[topic]
    
    # Insert data into MongoDB
    if videos_data:
        # Clear existing data in collection
        collection.delete_many({})
        
        # Insert new data
        collection.insert_many(videos_data)
        print(f"Inserted {len(videos_data)} documents into {topic} collection")
    
    # Delete JSON file
    os.remove(json_file)
    print(f"Deleted file: {json_file}")
    
    # Close MongoDB connection
    client.close()

if __name__ == "__main__":
    load_data_to_mongodb()
