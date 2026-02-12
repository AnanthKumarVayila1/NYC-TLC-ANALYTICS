# NYC TLC Trip Analytics Platform

[![Backend](https://img.shields.io/badge/Backend-FastAPI-green)](https://github.com/AnanthKumarVayila1/NYC-TLC-ANALYTICS)
[![Frontend](https://img.shields.io/badge/Frontend-Angular-red)](https://github.com/AnanthKumarVayila1/NYC-TLC-ANALYTICS)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](https://github.com/AnanthKumarVayila1/NYC-TLC-ANALYTICS)

**End-to-end analytics solution for NYC Taxi & Limousine Commission trip data covering 5 years (2020-2024).**

![Architecture](https://img.shields.io/badge/Architecture-Star_Schema-blue)
![Data](https://img.shields.io/badge/Records-159.5M-green)
![Tech](https://img.shields.io/badge/Stack-Azure_PySpark_FastAPI_Angular-orange)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Testing](#testing)
- [Project Structure](#project-structure)

---

## 🎯 Overview

This platform processes and analyzes 5 years of NYC TLC trip record data (2020-2024), providing:

- **Data Ingestion**: Automated processing of 1.26 billion trip records from Parquet files
- **Data Enrichment**: Geographic enrichment using NYC Taxi Zone lookup data
- **Analytics API**: RESTful API with JWT authentication, pagination, and filtering
- **Interactive Dashboard**: Real-time visualizations with time-series charts and tabular views
- **Azure Cloud Deployment**: Fully containerized with CI/CD pipeline

### Key Metrics

| Metric | Value |
|--------|-------|
| **Total Trip Records** | 159,557,896 |
| **Date Range** | 2020-01-01 to 2024-12-31 |
| **Service Types** | Yellow, Green, FHV, FHVHV |
| **Daily Aggregates** | 7,306 records |
| **Database Size** | ~450 GB |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Layer                               │
│  ┌──────────────┐      ┌─────────────────┐                     │
│  │ NYC TLC Data │─────▶│ Azure Data Lake │                     │
│  │  (Parquet)   │      │   Storage Gen2  │                     │
│  └──────────────┘      └────────┬────────┘                     │
│                                  │                               │
│                         ┌────────▼────────┐                     │
│                         │   Databricks    │                     │
│                         │   (PySpark)     │                     │
│                         └────────┬────────┘                     │
│                                  │                               │
│                         ┌────────▼────────┐                     │
│                         │  Azure SQL DB   │                     │
│                         │ (159.5M rows)   │                     │
│                         └────────┬────────┘                     │
└──────────────────────────────────┼──────────────────────────────┘
                                   │
┌──────────────────────────────────┼──────────────────────────────┐
│                      Application Layer                          │
│                         ┌────────▼────────┐                     │
│                         │   FastAPI       │                     │
│                         │  (Backend API)  │                     │
│                         │   + JWT Auth    │                     │
│                         └────────┬────────┘                     │
│                                  │                               │
│                         ┌────────▼────────┐                     │
│                         │   Angular 17    │                     │
│                         │   (Frontend)    │                     │
│                         │  + Chart.js     │                     │
│                         └─────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
                                   │
┌──────────────────────────────────┼──────────────────────────────┐
│                    Deployment Layer                             │
│  ┌────────────────┐   ┌──────────────┐   ┌─────────────────┐  │
│  │ Azure Container│   │ App Service  │   │  Static Web App │  │
│  │   Registry     │──▶│  (Backend)   │   │   (Frontend)    │  │
│  └────────────────┘   └──────────────┘   └─────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           GitHub Actions (CI/CD)                         │  │
│  │  • Automated Testing  • Docker Build  • Azure Deploy    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### Data Processing
- ✅ Ingest 1.26 billion trip records from Parquet files
- ✅ Data validation and quality checks
- ✅ Geographic enrichment with NYC borough and zone data
- ✅ Derived metrics: trip duration, total fare calculations
- ✅ Daily aggregations for fast querying

### Backend API
- ✅ **Authentication**: JWT-based secure authentication
- ✅ **Daily Aggregates**: Get trip metrics by date range and service type
- ✅ **Trip Records**: Paginated trip data with filtering
- ✅ **Statistics**: Summary statistics across all data
- ✅ **Pagination**: Efficient data retrieval with configurable page sizes
- ✅ **CORS**: Configured for frontend integration
- ✅ **API Docs**: Auto-generated Swagger/OpenAPI documentation

### Frontend Dashboard
- ✅ **Authentication**: Secure login with JWT tokens
- ✅ **Time-Series Charts**: Daily trip volume visualizations
- ✅ **Tabular Views**: Sortable, paginated trip records
- ✅ **Filters**: Date range and service type filtering
- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **Real-Time Data**: Dynamic data loading from API

### DevOps
- ✅ **Docker**: Containerized backend and frontend
- ✅ **CI/CD**: GitHub Actions for automated testing and deployment
- ✅ **Azure Deployment**: App Service + Static Web Apps
- ✅ **Testing**: 11 automated backend tests (100% passing)
- ✅ **Infrastructure as Code**: ARM templates for Azure resources

---

## 🛠️ Technology Stack

### Data Processing
- **Azure Data Lake Storage Gen2**: Raw data storage
- **Databricks (Apache Spark)**: Distributed data processing
- **Azure Data Factory**: ETL orchestration
- **Python 3.12**: Data processing scripts

### Backend
- **FastAPI 0.109.0**: High-performance Python API framework
- **PyODBC 5.3.0**: SQL Server connectivity
- **Azure SQL Database**: Data warehouse
- **JWT Authentication**: Secure API access
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server

### Frontend
- **Angular 17**: Modern web framework
- **TypeScript**: Type-safe JavaScript
- **Chart.js**: Data visualizations
- **RxJS**: Reactive programming
- **Zone.js**: Change detection

### DevOps & Infrastructure
- **Docker**: Containerization
- **GitHub Actions**: CI/CD automation
- **Azure Container Registry**: Docker image storage
- **Azure App Service**: Backend hosting (Linux)
- **Azure Static Web Apps**: Frontend hosting
- **Nginx**: Frontend reverse proxy

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- Azure CLI (for deployment)
- Git

### Local Development

#### 1. Clone Repository

```bash
git clone https://github.com/AnanthKumarVayila1/NYC-TLC-ANALYTICS.git
cd NYC-TLC-ANALYTICS
```

#### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run backend
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000
API Docs: http://localhost:8000/docs

#### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install --legacy-peer-deps

# Run development server
npm start
```

Frontend will be available at: http://localhost:4200

#### 4. Using Docker (Recommended)

```bash
# From project root
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:80
- API Docs: http://localhost:8000/docs

### Test Credentials

- **Username**: `admin`
- **Password**: `secret`

---

## 🗄️ Database Schema

### Star Schema Design

```sql
-- Dimension Table: Taxi Zones (263 rows)
dim_taxi_zone (
    location_id INT PRIMARY KEY,
    borough VARCHAR(50),
    zone_name VARCHAR(100),
    service_zone VARCHAR(50)
)

-- Fact Table: Trip Records (159.5M rows)
fact_trip (
    trip_id BIGINT PRIMARY KEY,
    service_type VARCHAR(10),           -- yellow, green, fhv, fhvhv
    pickup_datetime DATETIME2,
    dropoff_datetime DATETIME2,
    pickup_location_id INT,             -- FK to dim_taxi_zone
    dropoff_location_id INT,            -- FK to dim_taxi_zone
    pickup_borough VARCHAR(50),         -- Denormalized for performance
    pickup_zone VARCHAR(100),
    dropoff_borough VARCHAR(50),
    dropoff_zone VARCHAR(100),
    trip_distance DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    trip_duration_sec INT,
    pickup_date DATE,                   -- Partition key
    is_valid BIT
)

-- Aggregate Table: Daily Metrics (7.3K rows)
agg_daily_metrics (
    metric_date DATE,
    service_type VARCHAR(10),
    total_trips INT,
    total_revenue DECIMAL(18,2),
    avg_trip_distance DECIMAL(10,2),
    avg_trip_duration_sec DECIMAL(10,2),
    avg_fare_amount DECIMAL(10,2),
    PRIMARY KEY (metric_date, service_type)
)
```

### Schema Rationale

1. **Star Schema**: Optimized for analytical queries
2. **Denormalization**: Borough/zone names duplicated for query performance
3. **Indexing**: Covering indexes on date, service type, and locations
4. **Partitioning**: Date-based partitioning for large fact table
5. **Aggregates**: Pre-computed daily metrics for dashboard performance

---

## 📡 API Documentation

### Authentication

```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=admin&password=secret
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Daily Aggregates

```http
GET /api/aggregates/daily?start_date=2020-05-01&end_date=2020-05-31&page=1&page_size=100
Authorization: Bearer {token}
```

**Response:**
```json
{
  "data": [
    {
      "metric_date": "2020-05-31",
      "service_type": "yellow",
      "total_trips": 3055,
      "total_revenue": 55796.83,
      "avg_trip_distance": 4.56,
      "avg_trip_duration_sec": 982,
      "avg_fare_amount": 18.26
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 100,
    "total_records": 124,
    "total_pages": 2
  }
}
```

### Get Trip Records

```http
GET /api/trips?start_date=2020-05-01&end_date=2020-05-31&service_type=yellow&page=1&page_size=100
Authorization: Bearer {token}
```

**Full API documentation available at:** `http://localhost:8000/docs`

---

## 🚢 Deployment

### Azure Deployment (Automated)

#### Quick Deploy

```bash
chmod +x deployment/azure-deploy.sh
./deployment/azure-deploy.sh
```

#### Manual Deployment

See [deployment/AZURE_DEPLOYMENT.md](deployment/AZURE_DEPLOYMENT.md) for detailed instructions.

#### GitHub Secrets Required

Configure these in GitHub repository settings (Settings → Secrets → Actions):

| Secret | Description |
|--------|-------------|
| `ACR_LOGIN_SERVER` | Azure Container Registry URL |
| `ACR_USERNAME` | ACR admin username |
| `ACR_PASSWORD` | ACR admin password |
| `AZURE_CREDENTIALS` | Service Principal JSON |
| `AZURE_STATIC_WEB_APPS_API_TOKEN` | Static Web App deployment token |
| `DB_SERVER` | SQL Server hostname |
| `DB_NAME` | Database name |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |
| `SECRET_KEY` | JWT secret key (generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`) |
| `ALLOWED_ORIGINS` | CORS allowed origins |

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

**Test Coverage:**
- ✅ Authentication endpoints (3 tests)
- ✅ Daily aggregates API (3 tests)
- ✅ Trip records API (3 tests)
- ✅ Statistics API (1 test)
- ✅ Database connectivity (1 test)

**Total: 11/11 tests passing (100%)**

### Docker Testing

```bash
# Build and test containers
docker-compose up --build

# Verify services
curl http://localhost:8000/health
curl http://localhost/health
```

---

## 📁 Project Structure

```
NYC_TLC_Analytics/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── auth.py            # JWT authentication
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # Database connection
│   │   ├── models.py          # Pydantic models
│   │   └── routers/           # API endpoints
│   │       ├── aggregates.py  # Daily metrics API
│   │       ├── trips.py       # Trip records API
│   │       └── statistics.py  # Statistics API
│   ├── tests/                 # Automated tests
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                   # Angular Frontend
│   ├── src/app/
│   │   ├── components/
│   │   │   ├── dashboard/     # Main dashboard
│   │   │   └── login/         # Login page
│   │   ├── services/          # API services
│   │   └── models/            # TypeScript models
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── deployment/                 # Deployment configurations
│   ├── azure-deploy.sh        # Azure deployment script
│   ├── azure-template.json    # ARM template
│   ├── azure-parameters.json  # ARM parameters
│   └── AZURE_DEPLOYMENT.md    # Deployment guide
│
├── .github/workflows/          # CI/CD pipelines
│   ├── backend-ci-cd.yml      # Backend pipeline
│   ├── frontend-ci-cd.yml     # Frontend pipeline
│   └── tests.yml              # Automated tests
│
├── docker-compose.yml          # Local Docker setup
├── README.md                   # This file
└── 01_Data_Processing_Notebook.ipynb  # Data processing
```

---

## 📊 Data Processing Workflow

1. **Data Ingestion**: Download 60 monthly Parquet files (2020-2024)
2. **Data Validation**: Filter invalid records, check quality
3. **Enrichment**: Join with NYC Taxi Zone lookup table
4. **Loading**: Bulk load to Azure SQL using Data Factory
5. **Optimization**: Create indexes, partitions, and aggregates

---

## 🔒 Security

- **JWT Authentication**: Secure API access with token-based auth
- **HTTPS Only**: All production traffic encrypted
- **CORS Configuration**: Restricted to allowed origins
- **SQL Injection Protection**: Parameterized queries
- **Environment Variables**: Sensitive data in .env files
- **Docker Security**: Non-root containers, minimal base images

---

## 👤 Author

**NYC TLC Analytics Platform**
- Repository: [NYC-TLC-ANALYTICS](https://github.com/AnanthKumarVayila1/NYC-TLC-ANALYTICS)
- Owner: [@AnanthKumarVayila1](https://github.com/AnanthKumarVayila1)

---

## 🙏 Acknowledgments

- NYC Taxi & Limousine Commission for providing open data
- Azure Cloud Platform for hosting infrastructure
- FastAPI and Angular communities

---

**⭐ Star this repository if you find it helpful!**