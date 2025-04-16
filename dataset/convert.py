import pandas as pd
import json

# Load CSV file
df = pd.read_csv("dataset/Crop_recommendation.csv")

# Convert DataFrame to JSON
json_data = df.to_dict(orient="records")

# Save as JSON file
with open("dataset/Crop_recommendation.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)

print("CSV converted to JSON successfully!")
