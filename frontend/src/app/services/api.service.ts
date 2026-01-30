import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { DailyAggregatesResponse } from '../models/aggregate.model';
import { TripsResponse } from '../models/trip.model';
import { SummaryStats } from '../models/summary.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getDailyAggregates(
    startDate: string,
    endDate: string,
    serviceType?: string,
    page: number = 1,
    pageSize: number = 100
  ): Observable<DailyAggregatesResponse> {
    let params = new HttpParams()
      .set('start_date', startDate)
      .set('end_date', endDate)
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    if (serviceType) {
      params = params.set('service_type', serviceType);
    }

    return this.http.get<DailyAggregatesResponse>(
      `${this.apiUrl}/api/aggregates/daily`,
      { params }
    );
  }

  getSummary(
    startDate: string,
    endDate: string,
    serviceType?: string
  ): Observable<SummaryStats> {
    let params = new HttpParams()
      .set('start_date', startDate)
      .set('end_date', endDate);

    if (serviceType) {
      params = params.set('service_type', serviceType);
    }

    return this.http.get<SummaryStats>(
      `${this.apiUrl}/api/summary`,
      { params }
    );
  }

  getTrips(
    startDate: string,
    endDate: string,
    serviceType?: string,
    borough?: string,
    page: number = 1,
    pageSize: number = 100
  ): Observable<TripsResponse> {
    let params = new HttpParams()
      .set('start_date', startDate)
      .set('end_date', endDate)
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    if (serviceType) {
      params = params.set('service_type', serviceType);
    }
    if (borough) {
      params = params.set('borough', borough);
    }

    return this.http.get<TripsResponse>(
      `${this.apiUrl}/api/trips`,
      { params }
    );
  }

  getStatistics(): Observable<any> {
    return this.http.get(`${this.apiUrl}/api/statistics`);
  }
}