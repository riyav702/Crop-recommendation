import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["CropDatabase"]  # Create a new database
collection = db["CropData"]  # Create a collection

# Load dataset
df = pd.read_csv("dataset/crop_data.csv")  # Ensure filename matches your CSV

# Convert DataFrame to a dictionary format
data_dict = df.to_dict(orient="records")

# Insert into MongoDB
collection.insert_many(data_dict)

print("✅ Data successfully inserted into MongoDB!")
