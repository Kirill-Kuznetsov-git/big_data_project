DROP TABLE IF EXISTS trips;

CREATE TABLE IF NOT EXISTS trips (
    trip_id VARCHAR(120) PRIMARY KEY,
    call_type VARCHAR(10) NOT NULL,
    origin_call DOUBLE PRECISION NULL,
    origin_stand DOUBLE PRECISION NULL,
    taxi_id INTEGER NOT NULL,
    timestamp BIGINT NOT NULL,
    day_type VARCHAR(10) NOT NULL,
    missing_data BOOLEAN NOT NULL,
    polyline TEXT NOT NULL
);

CREATE OR REPLACE RULE "trips_on_duplicate_ignore" AS ON INSERT TO "trips"
  WHERE EXISTS(SELECT 1 FROM trips
                WHERE (trip_id)=(NEW.trip_id))
  DO INSTEAD NOTHING;
