"""
Development database module with mock data
Used when real SQL Server is not available
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import random
import re
from collections import defaultdict
from app.mock_data import generate_realistic_trips, generate_realistic_aggregates, generate_statistics

class Database:
    """Mock database for development/testing"""
    
    def __init__(self):
        self.connection_string = "dev://mock"
        random.seed(42)  # Seed for consistent data
        self._init_mock_data()
    
    def _init_mock_data(self):
        """Initialize sample data"""
        print("🔄 Initializing enhanced mock data for interview demo...")
        print(f"   Generating aggregates...")
        self.mock_aggregates = generate_realistic_aggregates()
        print(f"   ✅ Generated {len(self.mock_aggregates)} aggregate records")
        
        print(f"   Generating trips...")
        self.mock_trips = generate_realistic_trips(5000)
        print(f"   ✅ Generated {len(self.mock_trips)} trip records")
        
        print(f"   Generating statistics...")
        self.mock_stats = generate_statistics()
        print(f"✅ Mock data initialized:")
        print(f"   - {len(self.mock_aggregates)} aggregate records (5 years of daily metrics)")
        print(f"   - {len(self.mock_trips)} trip records")
        print(f"   - Statistics for {len(self.mock_stats['service_types'])} service types")
        print(f"\n   First aggregate:  {self.mock_aggregates[0] if self.mock_aggregates else 'NONE'}")
        print(f"   Last aggregate:   {self.mock_aggregates[-1] if self.mock_aggregates else 'NONE'}")
        print(f"   First trip:       {self.mock_trips[0] if self.mock_trips else 'NONE'}\n")
    
    def _generate_mock_aggregates(self) -> List[Dict]:
        """Generate mock daily aggregate data (deprecated - use generate_realistic_aggregates)"""
        return generate_realistic_aggregates()
    
    def _generate_mock_trips(self, limit: int = 5000) -> List[Dict]:
        """Generate mock trip records (deprecated - use generate_realistic_trips)"""
        return generate_realistic_trips(limit)
    
    def _generate_mock_stats(self) -> Dict:
        """Generate mock statistics (deprecated - use generate_statistics)"""
        return generate_statistics()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict]:
        """Execute a SELECT query against mock data"""
        query_upper = query.upper()
        
        # Determine which table
        if 'agg_daily_metrics' in query_upper or 'AGG_DAILY' in query_upper:
            data = self.mock_aggregates
            table_name = "agg_daily_metrics"
        elif 'fact_trip' in query_upper or 'FACT_TRIP' in query_upper:
            data = self.mock_trips
            table_name = "fact_trip"
        else:
            print(f"❌ ERROR: No table matched in query: {query_upper}")
            return []
        
        print(f"\n📝 QUERY EXECUTION:")
        print(f"   Table: {table_name}")
        print(f"   Query: {query[:100]}...")
        print(f"   Params: {params}")
        print(f"   Initial data count: {len(data)}")
        
        # Apply WHERE filtering
        if params:
            filtered = self._filter_by_params(data, query, params)
        else:
            filtered = data
        
        print(f"   After WHERE filter: {len(filtered)} records")
        
        # Parse and apply SELECT columns with aggregates
        result = self._apply_select_aggregate(filtered, query)
        
        print(f"   After SELECT/aggregate: {len(result) if isinstance(result, list) else 1} item(s)")
        
        # Apply GROUP BY
        if 'GROUP BY' in query_upper:
            result = self._apply_group_by(result, query, filtered)
            print(f"   After GROUP BY: {len(result)} item(s)")
        
        # Apply ORDER BY
        if 'ORDER BY' in query_upper:
            result = self._apply_order_by(result, query)
            print(f"   After ORDER BY: {len(result)} item(s)")
        
        # Apply OFFSET and FETCH (SQL Server pagination syntax)
        if 'OFFSET' in query_upper and isinstance(result, list):
            result = self._apply_pagination(result, query, params)
            print(f"   After OFFSET/FETCH: {len(result) if isinstance(result, list) else 1} item(s)")
        
        print(f"   ✅ Returning {len(result) if isinstance(result, list) else 1} result(s)\n")
        return result
    
    def execute_scalar(self, query: str, params: Optional[tuple] = None) -> Any:
        """Execute a query and return a single scalar value (e.g., COUNT, SUM, MAX)"""
        result = self.execute_query(query, params)
        if result and isinstance(result, list) and len(result) > 0:
            row = result[0]
            if isinstance(row, dict):
                # Get the first value from the dict
                return next(iter(row.values()))
            return row
        return 0
    
    def _filter_by_params(self, data: List[Dict], query: str, params: tuple) -> List[Dict]:
        """Filter data based on WHERE clause parameters"""
        filtered = data
        params_copy = list(params)  # Work with a copy
        query_upper = query.upper()
        
        print(f"DEBUG _filter_by_params: query contains 'CAST(pickup_date AS DATE) >=' ? {'CAST(pickup_date AS DATE) >=' in query_upper}")
        print(f"DEBUG _filter_by_params: params_copy = {params_copy}, len = {len(params_copy)}")
        
        # Handle BETWEEN for metric_date or pickup_date
        if 'BETWEEN' in query_upper and len(params_copy) >= 2:
            start_date, end_date = params_copy[0], params_copy[1]
            # Convert date objects to strings if needed
            start_str = start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else str(start_date)
            end_str = end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else str(end_date)
            print(f"DEBUG: Filtering by date BETWEEN {start_str} AND {end_str}")
            
            # Check for both metric_date and pickup_date
            date_col = 'metric_date' if 'metric_date' in query else 'pickup_date'
            filtered = [r for r in filtered if start_str <= r.get(date_col, '') <= end_str]
            print(f"DEBUG: After date filter: {len(filtered)} records")
            params_copy = params_copy[2:]
        
        # Handle CAST(pickup_date AS DATE) >= ? AND CAST(pickup_date AS DATE) <= ? syntax
        elif 'CAST(pickup_date AS DATE) >=' in query_upper and len(params_copy) >= 2:
            start_date, end_date = params_copy[0], params_copy[1]
            start_str = start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else str(start_date)
            end_str = end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else str(end_date)
            print(f"DEBUG: Filtering by pickup_date CAST between {start_str} AND {end_str}")
            
            filtered = [r for r in filtered if start_str <= r.get('pickup_date', '') <= end_str]
            print(f"DEBUG: After date filter: {len(filtered)} records")
            params_copy = params_copy[2:]
        
        # Handle service_type = ? (only if it's actually in WHERE clause with = ?)
        if 'service_type = ?' in query and len(params_copy) > 0:
            service_type = params_copy[0]
            print(f"DEBUG: Filtering by service_type = {service_type}")
            filtered = [r for r in filtered if r.get('service_type') == service_type]
            print(f"DEBUG: After service_type filter: {len(filtered)} records")
            params_copy = params_copy[1:]
        
        # Handle borough filter if it exists
        if 'pickup_borough = ?' in query and len(params_copy) > 0:
            borough = params_copy[0]
            print(f"DEBUG: Filtering by borough = {borough}")
            filtered = [r for r in filtered if r.get('pickup_borough') == borough]
            print(f"DEBUG: After borough filter: {len(filtered)} records")
        
        return filtered
    
    def _apply_select_aggregate(self, data: List[Dict], query: str) -> List[Dict]:
        """Apply SELECT with aggregates like SUM, AVG"""
        select_match = re.search(r'SELECT\s+(.*?)\s+FROM', query, re.IGNORECASE | re.DOTALL)
        if not select_match:
            print(f"DEBUG: No SELECT match found")
            return data
        
        select_part = select_match.group(1)
        print(f"DEBUG: select_part = {select_part}")
        
        # If no aggregates, return selected columns
        if 'SUM(' not in select_part and 'AVG(' not in select_part and 'COUNT(' not in select_part:
            print(f"DEBUG: No aggregates found, returning data")
            return data
        
        # Calculate aggregates
        result = {}
        print(f"DEBUG: Data has {len(data)} rows for aggregation")
        
        # SUM(total_trips)
        if 'SUM(total_trips)' in select_part:
            result['total_trips'] = sum(r.get('total_trips', 0) for r in data)
            print(f"DEBUG: total_trips = {result['total_trips']}")
        
        # SUM(total_revenue)
        if 'SUM(total_revenue)' in select_part:
            result['total_revenue'] = sum(r.get('total_revenue', 0) for r in data)
            print(f"DEBUG: total_revenue = {result['total_revenue']}")
        
        # AVG(avg_trip_distance)
        if 'AVG(avg_trip_distance)' in select_part:
            vals = [r.get('avg_trip_distance', 0) for r in data]
            result['avg_distance'] = sum(vals) / len(vals) if vals else 0
            print(f"DEBUG: avg_distance = {result['avg_distance']}")
        
        # AVG(avg_trip_duration_sec)
        if 'AVG(avg_trip_duration_sec)' in select_part:
            vals = [r.get('avg_trip_duration_sec', 0) for r in data]
            result['avg_duration_sec'] = sum(vals) / len(vals) if vals else 0
            print(f"DEBUG: avg_duration_sec = {result['avg_duration_sec']}")
        
        # AVG(avg_fare_amount)
        if 'AVG(avg_fare_amount)' in select_part:
            vals = [r.get('avg_fare_amount', 0) for r in data]
            result['avg_fare'] = sum(vals) / len(vals) if vals else 0
            print(f"DEBUG: avg_fare = {result['avg_fare']}")
        
        # COUNT(*)
        if 'COUNT(*)' in select_part:
            result['count'] = len(data)
        
        print(f"DEBUG: Final result = {result}")
        return [result] if result else []
    
    def _apply_group_by(self, data: List[Dict], query: str, original_data: List[Dict]) -> List[Dict]:
        """Apply GROUP BY logic"""
        group_match = re.search(r'GROUP BY\s+(\w+)', query, re.IGNORECASE)
        if not group_match:
            return data
        
        group_col = group_match.group(1)
        
        # Rebuild with grouping on original data
        groups = defaultdict(list)
        for row in original_data:
            key = row.get(group_col)
            groups[key].append(row)
        
        result = []
        for key, group_rows in groups.items():
            new_row = {group_col: key}
            
            # Sum for all groups
            new_row['total_trips'] = sum(r.get('total_trips', 0) for r in group_rows)
            new_row['total_revenue'] = sum(r.get('total_revenue', 0) for r in group_rows)
            
            result.append(new_row)
        
        return result
    
    def _apply_order_by(self, data: List[Dict], query: str) -> List[Dict]:
        """Apply ORDER BY"""
        order_match = re.search(r'ORDER BY\s+(\w+)(?:\s+(ASC|DESC))?', query, re.IGNORECASE)
        if not order_match:
            return data
        
        col = order_match.group(1)
        desc = 'DESC' in (order_match.group(2) or '').upper()
        
        return sorted(data, key=lambda x: x.get(col, 0), reverse=desc)
    
    def _apply_pagination(self, data: List[Dict], query: str, params: Optional[tuple]) -> List[Dict]:
        """Apply OFFSET and FETCH NEXT pagination"""
        # Extract OFFSET value
        offset_match = re.search(r'OFFSET\s+(\?|\d+)\s+ROWS', query, re.IGNORECASE)
        fetch_match = re.search(r'FETCH\s+NEXT\s+(\?|\d+)\s+ROWS\s+ONLY', query, re.IGNORECASE)
        
        print(f"   [PAGINATION] offset_match: {bool(offset_match)}, fetch_match: {bool(fetch_match)}")
        print(f"   [PAGINATION] data length: {len(data) if isinstance(data, list) else 'not-a-list'}")
        print(f"   [PAGINATION] params: {params}")
        
        if not offset_match or not fetch_match or not params:
            print(f"   [PAGINATION] No valid pagination config, returning data as-is")
            return data
        
        # Get offset and fetch size from params
        # Params come in order: WHERE params..., then OFFSET value, then FETCH size
        if len(params) >= 2:
            offset = int(params[-2]) if isinstance(params[-2], int) else 0
            fetch_size = int(params[-1]) if isinstance(params[-1], int) else 100
            
            print(f"   [PAGINATION] offset={offset}, fetch_size={fetch_size}")
            print(f"   [PAGINATION] Will return data[{offset}:{offset+fetch_size}]")
            
            # Apply pagination
            end_index = offset + fetch_size
            result = data[offset:end_index] if isinstance(data, list) else []
            
            print(f"   [PAGINATION] Returning {len(result)} records")
            return result
        
        print(f"   [PAGINATION] Not enough params ({len(params)}), returning data as-is")
        return data
