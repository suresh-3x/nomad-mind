import chromadb
from chromadb.utils import embedding_functions
from geopy.geocoders import Nominatim
import re

client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("videos")

def store_transcript(video_id, transcript):
    chunks = [transcript[i:i+500] for i in range(0, len(transcript), 500)]
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{video_id}-{i}"]
        )

def search_similar(query):
    results = collection.query(query_texts=[query], n_results=5)
    return [doc for doc in results['documents'][0]]

def extract_locations(text):
    # Use a crude regex to catch likely place names
    matches = re.findall(r'\b(?:in|at|to|near|from)\s([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)', text)
    geolocator = Nominatim(user_agent="nomadmind")
    locations = {}
    for place in set(matches):
        try:
            loc = geolocator.geocode(place)
            if loc:
                locations[place] = (loc.latitude, loc.longitude)
        except:
            pass
    return locations
