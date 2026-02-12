export interface SummaryStats {
  total_trips: number;
  total_revenue: number;
  avg_distance: number;
  avg_duration_minutes: number;
  avg_fare: number;
  by_service_type: {
    service_type: string;
    total_trips: number;
    total_revenue: number;
  }[];
  by_borough: {
    pickup_borough: string;
    trip_count: number;
    avg_distance: number;
  }[];
}
