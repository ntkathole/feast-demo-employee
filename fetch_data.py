import pandas as pd
from feast import FeatureStore

# Initialize Feast feature store
store = FeatureStore(repo_path="feature_repo")

# Define the list of employees & timestamps
entity_rows = [
    {"employee_name": "Jitendra", "event_timestamp": "2025-03-01"},
    {"employee_name": "Gaurav", "event_timestamp": "2025-03-02"},
    {"employee_name": "Dipanshu", "event_timestamp": "2025-03-03"},
    {"employee_name": "Abhijeet", "event_timestamp": "2025-03-04"},
]

# Fetch feature vectors from Feast
feature_vector = store.get_historical_features(
    entity_df=pd.DataFrame(entity_rows),
    features=[
        "employee_attendance_aggregated:total_visits",
        "employee_attendance_aggregated:total_visits_per_month",
        "employee_attendance_aggregated:total_visits_per_week",
        "employee_attendance_aggregated:days_since_last_visit",
        "employee_attendance_aggregated:total_tenure",
        "employee_attendance_features:day_of_week",
        "employee_attendance_features:time_to_reach_office",
        "employee_attendance_features:will_attend",  # Target variable (1=present, 0=absent)
    ],
).to_df()

# Preview Data
print(feature_vector.head())
