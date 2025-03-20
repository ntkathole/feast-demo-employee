import pandas as pd
import numpy as np
from feast import FeatureStore
from datetime import datetime
import joblib


# Initialize Feature Store
store = FeatureStore(repo_path="feature_repo")

date_input = input("Enter the date for prediction (YYYY-MM-DD): ")

try:
    prediction_date = pd.to_datetime(date_input)
except ValueError:
    print("❌ Invalid date format! Please enter in 'YYYY-MM-DD' format.")
    exit()

# Prediction data
entity_df = pd.DataFrame({
    "employee_name": ["Jitendra", "Gaurav", "Dipanshu", "Abhijeet", "Nikhil", "Amita", "Claudia"],
    "event_timestamp": pd.to_datetime([prediction_date] * 7)
})

features = [
    "employee_attendance_features:day_of_week",
    "employee_attendance_features:in_office",
    "employee_attendance_features:is_tuesday_or_friday"
]

# Fetch features for prediction
prediction_df = store.get_historical_features(entity_df=entity_df, features=features).to_df()

if prediction_date > datetime.now():
    print("🔮 Future prediction! Converting date to day of week...")
    prediction_df["day_of_week"] = prediction_df["event_timestamp"].dt.day_name()  # Convert to day of week since model can't predict future dates
    prediction_df["is_tuesday_or_friday"] = prediction_df["day_of_week"].apply(lambda x: 1 if x in [1, 4] else 0)

print("Sample Features from feast store:")
print(prediction_df)

# Convert categorical feature to numeric
prediction_df["day_of_week"] = pd.Categorical(prediction_df["day_of_week"]).codes

# Drop non-feature columns to match training phase
feature_columns = [
    'day_of_week', 'is_tuesday_or_friday'
]

# Ensure all required columns are present
missing_columns = [col for col in feature_columns if col not in prediction_df.columns]
for col in missing_columns:
    prediction_df[col] = 0  # Add placeholder if missing

X_pred = prediction_df[feature_columns]

# Load the trained model
model = joblib.load("attendance_model.pkl")

# Ensure the feature columns order matches the model training
feature_columns = [col for col in feature_columns if col != "in_office"]
X_pred = X_pred[feature_columns] 

# Make predictions
predictions = model.predict(X_pred)
try:
    # Check if model is binary classifier or not
    if len(model.classes_) == 2:
        predicted_probs = model.predict_proba(X_pred)[:, 1]  # Probability of being in office (class 1)
    else:
        predicted_probs = model.predict_proba(X_pred)[:, 0]  # Fallback to single-class probability
except AttributeError:
    predicted_probs = np.ones(len(predictions))  # If model lacks predict_proba, assume all 1s

# Show predictions
prediction_df["predicted_in_office"] = predictions
prediction_df["predicted_probability"] = predicted_probs

print("🔹 Prediction Results:")
print(prediction_df[["employee_name", "predicted_in_office", "predicted_probability"]])