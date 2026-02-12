export interface Trip {
  trip_id: number;
  service_type: string;
  pickup_datetime: string;
  dropoff_datetime: string;
  pickup_borough: string;
  pickup_zone: string;
  dropoff_borough: string;
  dropoff_zone: string;
  trip_distance: number;
  total_amount: number;
  trip_duration_sec: number;
}

export interface TripsResponse {
  data: Trip[];
  pagination: Pagination;
}

export interface Pagination {
  page: number;
  page_size: number;
  total_records: number;
  total_pages: number;
}