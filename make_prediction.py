import pandas as pd
import numpy as np
from feast import FeatureStore

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
]

# Fetch features for prediction
prediction_df = store.get_historical_features(entity_df=entity_df, features=features).to_df()
print("Sample Features from feast store:")
print(prediction_df.head())
# Convert categorical feature to numeric
prediction_df["day_of_week"] = pd.Categorical(prediction_df["day_of_week"]).codes

# Drop non-feature columns to match training phase
feature_columns = [
    'day_of_week',
]

# Ensure all required columns are present
missing_columns = [col for col in feature_columns if col not in prediction_df.columns]
for col in missing_columns:
    prediction_df[col] = 0  # Add placeholder if missing

X_pred = prediction_df[feature_columns]

# Load the trained model
import joblib
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

print("\nSample Features for Prediction:")
print(prediction_df.head())

print("🔹 Prediction Results:")
print(prediction_df[["employee_name", "predicted_in_office", "predicted_probability"]])
