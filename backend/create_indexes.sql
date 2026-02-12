-- Performance optimization indexes for NYC TLC Analytics

-- Index on daily aggregates for date range and service type filtering
CREATE NONCLUSTERED INDEX idx_agg_daily_metrics_date_service 
ON agg_daily_metrics (metric_date DESC, service_type)
INCLUDE (total_trips, total_revenue, avg_trip_distance, avg_trip_duration_sec, avg_fare_amount);

-- Index on fact_trips for date range filtering (pickup)
CREATE NONCLUSTERED INDEX idx_fact_trips_pickup_datetime 
ON fact_trips (pickup_datetime DESC)
INCLUDE (service_type, trip_distance, trip_duration_sec, total_amount);

-- Index on fact_trips for service type filtering
CREATE NONCLUSTERED INDEX idx_fact_trips_service_type 
ON fact_trips (service_type, pickup_datetime DESC);

-- Composite index for common query pattern (date + service type)
CREATE NONCLUSTERED INDEX idx_fact_trips_date_service 
ON fact_trips (pickup_datetime DESC, service_type)
INCLUDE (pickup_location_id, dropoff_location_id, trip_distance, trip_duration_sec, fare_amount, total_amount);

-- Check index usage statistics (run after some time)
-- SELECT 
--     OBJECT_NAME(s.object_id) AS TableName,
--     i.name AS IndexName,
--     s.user_seeks,
--     s.user_scans,
--     s.user_lookups,
--     s.last_user_seek,
--     s.last_user_scan
-- FROM sys.dm_db_index_usage_stats s
-- INNER JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
-- WHERE OBJECT_NAME(s.object_id) IN ('fact_trips', 'agg_daily_metrics')
-- ORDER BY s.user_seeks + s.user_scans + s.user_lookups DESC;
