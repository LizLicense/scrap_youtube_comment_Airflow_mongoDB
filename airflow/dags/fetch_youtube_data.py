import os
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_youtube_data(topic, max_results=100):
    """
    Fetch YouTube data for a given topic
    """
    YOUTUBE_API_KEY = 'AI00000000...' #CHANGE THIS TO YOUR OWN API KEY
    # Get API key from environment variable
    if not YOUTUBE_API_KEY:
        raise ValueError("YouTube API key not found in environment variables")
    
    # Build YouTube API client
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    # Search for videos related to the topic
    video_ids = []
    next_page_token = None
    
    # Keep fetching until we have at least max_results videos or no more results
    while len(video_ids) < max_results:
        search_response = youtube.search().list(
            q=topic,
            part='id,snippet',
            maxResults=50,  # Maximum allowed per request
            type='video',
            pageToken=next_page_token
        ).execute()
        
        # Extract video IDs from the response
        for item in search_response['items']:
            if 'videoId' in item['id']:
                video_ids.append(item['id']['videoId'])
        
        # Check if there are more pages
        next_page_token = search_response.get('nextPageToken')
        if not next_page_token:
            break
        
        # If we've collected enough videos, stop
        if len(video_ids) >= max_results:
            break
    
    # Limit to max_results
    video_ids = video_ids[:max_results]
    
    # Get detailed information for each video
    videos_data = []
    
    # Process videos in batches of 50 (API limit)
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        
        # Get video statistics
        video_response = youtube.videos().list(
            id=','.join(batch_ids),
            part='snippet,statistics,contentDetails'
        ).execute()
        
        # Extract relevant information
        for item in video_response['items']:
            video_info = {
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'upload_date': item['snippet']['publishedAt'],
                'views': int(item['statistics'].get('viewCount', 0)),
                'likes': int(item['statistics'].get('likeCount', 0)),
                'comments': int(item['statistics'].get('commentCount', 0)),
                'url': f"https://www.youtube.com/watch?v={item['id']}"
            }
            videos_data.append(video_info)
    
    print(f"Fetched {len(videos_data)} videos for topic: {topic}")
    return videos_data

def fetch_and_save_youtube_data(**kwargs):
    """
    Airflow task to fetch YouTube data and save to JSON
    """
    try:
        # Read topic from file
        with open('/Users/[username]/.../topic.txt', 'r') as f:
            topic = f.read().strip()
        
        print(f"Successfully read topic: {topic}")
        
        # Fetch data
        videos_data = get_youtube_data(topic)
        
        # Save to JSON file
        output_file = f'/Users/[username]/.../{topic}.json'
        with open(output_file, 'w') as f:
            json.dump(videos_data, f, indent=2)
        
        print(f"Saved {len(videos_data)} videos data to {output_file}")
        
        # Return the output file path for the next task
        return output_file
    except Exception as e:
        print(f"Error in fetch_and_save_youtube_data: {str(e)}")
        raise

if __name__ == "__main__":
    fetch_and_save_youtube_data()
