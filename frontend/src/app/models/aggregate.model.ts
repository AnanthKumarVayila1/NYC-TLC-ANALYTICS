export interface DailyAggregate {
  metric_date: string;
  service_type: string;
  total_trips: number;
  total_revenue: number;
  avg_trip_distance: number;
  avg_trip_duration_sec: number;
  avg_fare_amount: number;
}

export interface Pagination {
  page: number;
  page_size: number;
  total_records: number;
  total_pages: number;
}

export interface DailyAggregatesResponse {
  data: DailyAggregate[];
  pagination: Pagination;
}