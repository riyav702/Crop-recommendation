import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("dataset/Crop_recommendation.csv")  # Adjust path if needed

# Separate features and target
X = df.drop(columns=["label"])  # Features
y = df["label"]  # Target variable

# Encode target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save trained model
with open("models/crop_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Save label encoder
with open("models/label_encoder.pkl", "wb") as file:
    pickle.dump(label_encoder, file)

print("Model and label encoder saved successfully!")
