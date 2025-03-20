import pandas as pd
from feast import FeatureStore
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from datetime import datetime

# Initialize Feature Store
store = FeatureStore(repo_path="feature_repo")

start_date = datetime(2025, 2, 18)
end_date = datetime(2025, 3, 20)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

employee_names = ["Jitendra", "Gaurav", "Dipanshu", "Abhijeet", "Nikhil", "Amita", "Claudia"]

# Define entity_df with actual timestamps (e.g., multiple dates)
entity_df = pd.DataFrame({
    "employee_name": [name for name in employee_names for _ in date_range],
    "timestamp": [date for date in date_range for _ in employee_names]
})

# Specify features
features = [
    "employee_attendance_features:day_of_week",
    "employee_attendance_features:in_office",
    "employee_attendance_features:is_tuesday_or_friday"
]

# Fetch historical features
training_df = store.get_historical_features(entity_df=entity_df, features=features).to_df()

print("Sample Features from Feature Store:")
print(training_df.head())  # Check if the data has the features you expect

# Label extraction and preprocessing
X = training_df.drop(columns=["employee_name", "timestamp", "in_office"])  # Drop 'in_office' here

# Check if the features are correctly loaded
print("Feature columns:", X.columns)

# Convert 'day_of_week' to encoding
X["day_of_week"] = pd.Categorical(X["day_of_week"]).codes
# Define the target variable
y = training_df["in_office"]

# Label distribution
print("Label Distribution in Training Data:")
print(training_df["in_office"].value_counts())

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
print("Model saved successfully!")
print("Feature Importances:", model.feature_importances_)
print("Model feature names:", model.feature_names_in_)

