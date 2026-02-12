import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { NgChartsModule } from 'ng2-charts';
import { ChartConfiguration, ChartType } from 'chart.js';
import { ApiService } from '../../services/api.service';
import { AuthService } from '../../services/auth.service';
import { DailyAggregate } from '../../models/aggregate.model';
import { Trip } from '../../models/trip.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, NgChartsModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  // Date filters
  startDate: string = '';
  endDate: string = '';
  serviceType: string = '';
  
  // Data
  aggregates: DailyAggregate[] = [];
  trips: Trip[] = [];
  
  // Loading states
  loadingChart = false;
  loadingTable = false;
  
  // Error states
  chartError: string = '';
  tripError: string = '';
  
  // Pagination
  currentPage = 1;
  pageSize = 50;
  totalRecords = 0;
  totalPages = 0;
  
  // Chart configuration
  public lineChartData: ChartConfiguration['data'] = {
    datasets: [],
    labels: []
  };
  
  public lineChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top'
      },
      title: {
        display: true,
        text: 'Daily Trip Volume - Time Series'
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Date'
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Total Trips'
        }
      }
    }
  };
  
  public lineChartType: ChartType = 'line';

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private router: Router
  ) {
    // Set default date range to show data from 2020-05 (where we have data)
    this.startDate = '2020-05-01';
    this.endDate = '2020-05-31';
  }

  ngOnInit(): void {
    this.loadData();
  }

  formatDate(date: Date): string {
    return date.toISOString().split('T')[0];
  }

  loadData(): void {
    this.loadAggregates();
    this.loadTrips();
  }

  loadAggregates(): void {
    this.loadingChart = true;
    this.chartError = '';
    
    this.apiService.getDailyAggregates(
      this.startDate,
      this.endDate,
      this.serviceType || undefined,
      1,
      1000  // Get all for chart
    ).subscribe({
      next: (response) => {
        this.aggregates = response.data;
        this.updateChart();
        this.loadingChart = false;
        
        if (this.aggregates.length === 0) {
          this.chartError = 'No data available for selected date range.';
        }
      },
      error: (err) => {
        console.error('Error loading aggregates:', err);
        this.chartError = 'Failed to load chart data. Please try again.';
        this.loadingChart = false;
        if (err.status === 401) {
          this.authService.logout();
          this.router.navigate(['/login']);
        }
      }
    });
  }

  loadTrips(): void {
    this.loadingTable = true;
    this.tripError = '';
    
    this.apiService.getTrips(
      this.startDate,
      this.endDate,
      this.serviceType || undefined,
      undefined,
      this.currentPage,
      this.pageSize
    ).subscribe({
      next: (response) => {
        this.trips = response.data;
        this.totalRecords = response.pagination.total_records;
        this.totalPages = response.pagination.total_pages;
        this.loadingTable = false;
      },
      error: (err) => {
        console.error('Error loading trips:', err);
        this.tripError = err.status === 504 || err.status === 0 
          ? 'Request timeout. Try selecting a smaller date range.'
          : 'Failed to load trip records. Please try again.';
        this.loadingTable = false;
        this.trips = [];
      }
    });
  }

  updateChart(): void {
    // Group by service type
    const serviceTypes = [...new Set(this.aggregates.map(a => a.service_type))];
    
    // Get unique dates
    const dates = [...new Set(this.aggregates.map(a => a.metric_date))]
      .sort();
    
    // Create datasets for each service type
    const datasets = serviceTypes.map(serviceType => {
      const data = dates.map(date => {
        const agg = this.aggregates.find(
          a => a.metric_date === date && a.service_type === serviceType
        );
        return agg ? agg.total_trips : 0;
      });
      
      return {
        label: serviceType.charAt(0).toUpperCase() + serviceType.slice(1),
        data: data,
        fill: false,
        tension: 0.4,
        borderColor: this.getColorForServiceType(serviceType),
        backgroundColor: this.getColorForServiceType(serviceType)
      };
    });
    
    this.lineChartData = {
      labels: dates,
      datasets: datasets
    };
  }

  getColorForServiceType(serviceType: string): string {
    const colors: any = {
      'yellow': '#FFD700',
      'green': '#32CD32',
      'fhv': '#4169E1',
      'fhvhv': '#FF6347'
    };
    return colors[serviceType] || '#999';
  }

  onFilterChange(): void {
    this.currentPage = 1;
    this.loadData();
  }

  onPageChange(page: number): void {
    this.currentPage = page;
    this.loadTrips();
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}