from feast import Entity, FeatureView, Field
from feast.types import Int32, String
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import PostgreSQLSource

# Define Employee Entity
employee = Entity(name="employee_name", join_keys=["employee_name"])

# Data Source
attendance_source = PostgreSQLSource(
    name="employee_attendance",
    query="""
        SELECT 
            timestamp AS timestamp,
            employee_name, 
            day_of_week,
            in_office
        FROM employee_attendance
    """,
    timestamp_field="timestamp"
)

# Feature View Definition (Raw Features)
employee_attendance_fv = FeatureView(
    name="employee_attendance_features",
    entities=[employee],
    ttl=None,
    schema=[
        Field(name="day_of_week", dtype=String),
        Field(name="in_office", dtype=Int32)
    ],
    online=True,
    source=PostgreSQLSource(
        name="employee_attendance_features",
        query="""
        SELECT 
            timestamp,
            employee_name,
            day_of_week,
            in_office
        FROM employee_attendance
        """,
        timestamp_field="timestamp"
    ),
    tags={}
)
