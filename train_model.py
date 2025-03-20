import pandas as pd
from imblearn.over_sampling import SMOTE
import numpy as np
from feast import FeatureStore
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Initialize Feature Store
store = FeatureStore(repo_path="feature_repo")

# Fetch historical features
entity_df = pd.DataFrame({
    "employee_name": ["Jitendra", "Gaurav", "Dipanshu", "Abhijeet", "Nikhil", "Amita", "Claudia"],
    "timestamp": pd.to_datetime(["2025-03-18"] * 7),
    "in_office": [1, 0, 1, 0, 1, 0, 1]  # Manually added in_office as label
})

features = [
    "employee_attendance_features:day_of_week",
]

training_df = store.get_historical_features(entity_df=entity_df, features=features).to_df()

print("Sample Features from Feature Store:")
print(training_df.head())
# Label extraction and preprocessing
X = training_df.drop(columns=["employee_name", "timestamp", "in_office"])  # Drop 'in_office' here


# Convert categorical day_of_week to numeric encoding
X["day_of_week"] = pd.Categorical(X["day_of_week"]).codes
y = training_df["in_office"]

print("Label Distribution in Training Data:")
print(training_df["in_office"].value_counts())

print("Sample Features for Training:")
print(training_df.head())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Model training
model = RandomForestClassifier(
    n_estimators=200, 
    max_depth=10, 
    min_samples_split=5, 
    random_state=42,
    class_weight="balanced"
)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy Score:", accuracy_score(y_test, y_pred))
# Save the model
joblib.dump(model, "attendance_model.pkl")