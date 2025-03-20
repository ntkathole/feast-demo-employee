from feast import FeatureStore
import pandas as pd
from datetime import datetime

# Initialize Feast FeatureStore
store = FeatureStore(repo_path="feature_repo")

# Prepare an entity dataframe with required columns
entity_df = pd.DataFrame({
    "employee_name": ["Jitendra", "Gaurav", "Dipanshu"],
    "event_timestamp": pd.to_datetime(["2025-03-20", "2025-03-19", "2025-03-18"])
})

# Specify the features you want to fetch
feature_refs = [
    "employee_attendance_features:day_of_week",
]

# Fetch historical features
historical_features = store.get_historical_features(
    entity_df=entity_df,
    features=feature_refs
).to_df()

print(historical_features)
