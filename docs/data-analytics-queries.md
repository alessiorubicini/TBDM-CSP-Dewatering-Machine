# Data Analytics Queries

## Moisture Sensor Analysis

### Query 1: Average Moisture Level per Hour
To track the average moisture level per hour, which helps understand the process’s effectiveness over time.

```sql
import "profiler"
option profiler.enabledProfilers = ["query", "operator"]

from(bucket: "dewatering_machine")
  |> range(start: 2024-09-01T00:00:00Z, stop: 2024-10-10T00:00:00Z) // Filter by the date range
  |> filter(fn: (r) => r._measurement == "umidita_fango")
  |> aggregateWindow(every: 1h, fn: mean) // Aggregate by hour and calculate the mean moisture level
  |> yield(name: "avg_moisture_per_hour")
```

Query performance metrics:

| Total Duration	| 5,619708 ms |
| ----------------- | ----------- |
| Compile Duration	| 0,37375 ms | 
| Queue Duration	| 0,020208 ms |
| Execute Duration	| 5,19825 ms |
| Max number of bytes allocated	| 15360 bytes = 15,36 kB |

The query that tracks the average moisture level per hour runs efficiently, with a total duration of 5.62 seconds. The compile duration is minimal (0.37 ms), and the queue duration is very low (0.02 ms), indicating no significant delays or resource contention. Most of the time is spent in the execution phase (5.20 seconds), which is reasonable given the query’s scope (large date range and hourly aggregation). Memory usage is also low, with a maximum allocation of 15.36 KB. While the query performs well, further optimization could be explored, such as parallelizing queries for large datasets or partitioning data to enhance performance as data volume increases.

### Query 2: Trend of Moisture Levels

To track the trend of moisture levels over time. This query calculates the average moisture level for the entire time range, helping you understand the overall trend.

```sql
import "profiler"
option profiler.enabledProfilers = ["query", "operator"]

from(bucket: "dewatering_machine")
  |> range(start: 2024-09-01T00:00:00Z, stop: 2024-10-10T00:00:00Z)
  |> filter(fn: (r) => r._measurement == "umidita_fango")
  |> mean() // Calculate the overall average moisture level over the entire period
  |> yield(name: "moisture_trend")
```

| Total Duration | 6,066 ms |
| --- | --- |
| Compile Duration | 0,260709 ms |
| Queue Duration | 0,017708 ms |
| Execute Duration | 5,767417 ms |
| Max number of bytes allocated | 128 bytes = 0,128 kB |

## Screw Speed Sensor Analysis

Dataset: `velocita_coclea.csv`

The screw speed sensor measures the speed of the screw inside the dewatering machine, which is critical for optimizing the separation process.

### Query 1: Maximum Screw Speed in the Period
To find the highest screw speed recorded during the observation period.

```sql
import "profiler"
option profiler.enabledProfilers = ["query", "operator"]

from(bucket: "dewatering_machine")
  |> range(start: 2024-09-01T00:00:00Z, stop: 2024-10-10T00:00:00Z)
  |> filter(fn: (r) => r._measurement == "velocita_coclea")
  |> max() // Returns the maximum screw speed
  |> yield(name: "max_screw_speed")
```

### Query 2: Average Screw Speed per Hour
To calculate the average screw speed per hour to monitor fluctuations in screw operation.

```sql
import "profiler"
option profiler.enabledProfilers = ["query", "operator"]

from(bucket: "dewatering_machine")
  |> range(start: 2024-09-01T00:00:00Z, stop: 2024-10-10T00:00:00Z)
  |> filter(fn: (r) => r._measurement == "velocita_coclea")
  |> aggregateWindow(every: 1h, fn: mean) // Aggregate by hour and calculate the mean screw speed
  |> yield(name: "avg_screw_speed_per_hour")
```

### Query 3: Detecting Sudden Spikes or Drops (Rate of Change)
Detect large, sudden changes in sensor readings. This can highlight unusual events or failures.

```sql
import "profiler"
option profiler.enabledProfilers = ["query", "operator"]

from(bucket: "dewatering_machine")
  |> range(start: 2024-09-01T00:00:00Z, stop: 2024-10-10T00:00:00Z)
  |> filter(fn: (r) => r._measurement == "velocita_coclea")
  |> difference() // Calculate the difference between consecutive readings
  |> filter(fn: (r) => r._value > 100) // Detect large changes, e.g., greater than 100 units
  |> yield(name: "large_speed_changes")
```

Query performance metrics:

| Total Duration | 256,666083 ms |
| --- | --- |
| Compile Duration | 0,214208 ms |
| Queue Duration | 0,0165 ms |
| Execute Duration | 256,378541 ms |
| Max number of bytes allocated | 2726784 bytes = 2.726 kB = 2.73 MB |

The query for detecting sudden spikes or drops in sensor readings takes 256.67 seconds to execute, which is significantly longer than the other queries. The compile duration (0.21 ms) and queue duration (0.02 ms) are both minimal, indicating that the query’s initial setup and waiting times are efficient. However, the execution time of 256.38 seconds is unusually high, suggesting that the `difference` function, which computes the difference between consecutive readings, may be computationally intensive, especially over the large date range (one month). Additionally, the memory allocation is higher at 2.73 MB, which could be a result of processing a large volume of data while calculating the differences and filtering for large changes.

The high execution time and memory usage could be justified by the complexity of calculating the difference for each data point across a large time range. Optimizing this query might involve breaking it into smaller time ranges or applying pre-aggregation to reduce the number of operations.


## Drum Speed Sensor Analysis
Dataset: `velocita_tamburo.csv`

The drum speed sensor measures the speed of the drum in the dewatering machine.

### Query 1: Average Drum Speed per Hour

To monitor the average drum speed every hour, which is important for ensuring that the drum is operating at an optimal speed.

```sql
import "profiler"
option profiler.enabledProfilers = ["query", "operator"]

from(bucket: "dewatering_machine")
  |> range(start: 2024-09-01T00:00:00Z, stop: 2024-10-10T00:00:00Z)
  |> filter(fn: (r) => r._measurement == "velocita_tamburo")
  |> aggregateWindow(every: 1h, fn: mean)
  |> yield(name: "avg_drum_speed_per_hour")
```


## Sludge Inlet Flow
Dataset: `portata_fanghi.csv`

The sludge inlet flow measures the volume of sludge entering the dewatering machine.

### Query 1: Average Sludge Inlet Flow per Hour

To calculate the average flow of sludge entering the machine every hour.

This query helps track the average volume of sludge entering the machine every hour.

```sql
import "profiler"
option profiler.enabledProfilers = ["query", "operator"]

from(bucket: "dewatering_machine")
  |> range(start: 2024-09-01T00:00:00Z, stop: 2024-10-10T00:00:00Z)
  |> filter(fn: (r) => r._measurement == "portata_fanghi")
  |> aggregateWindow(every: 1h, fn: mean)
  |> yield(name: "avg_sludge_inlet_flow_per_hour")
```


## Sludge Inlet Turbidity
Dataset: `torbidita_fango.csv`

This sensor measures the turbidity (suspended particles) of the incoming sludge.

### Query 1: Max Sludge Inlet Turbidity

To determine the maximum turbidity (maximum level of suspended particles) observed in the inlet sludge.

```sql
import "profiler"
option profiler.enabledProfilers = ["query", "operator"]

from(bucket: "dewatering_machine")
  |> range(start: 2024-09-01T00:00:00Z, stop: 2024-10-10T00:00:00Z)
  |> filter(fn: (r) => r._measurement == "torbidita_fango")
  |> max() // Maximum value of turbidity
  |> yield(name: "max_sludge_inlet_turbidity")
```


## Polyelectrolyte Inlet Flow
Dataset: `portata_poly.csv`

This sensor measures the flow rate of polyelectrolyte entering the treatment process.

### Query 1: Polyelectrolyte Flow Analysis

To calculate the average flow of polyelectrolyte in the system every hour.

```sql
import "profiler"
option profiler.enabledProfilers = ["query", "operator"]

from(bucket: "dewatering_machine")
  |> range(start: 2024-09-01T00:00:00Z, stop: 2024-10-10T00:00:00Z)
  |> filter(fn: (r) => r._measurement == "portata_poly")
  |> aggregateWindow(every: 1h, fn: mean)
  |> yield(name: "avg_polyelectrolyte_flow_per_hour")
```


## Clarified Water Turbidity
Dataset: `torbidita_chiarificato.csv`

This sensor measures the turbidity of the clarified water after the treatment process.

### Query 1: Turbidity Trend of Clarified Water
To understand the trend of clarified water turbidity over time.

```sql
import "profiler"
option profiler.enabledProfilers = ["query", "operator"]

from(bucket: "dewatering_machine")
  |> range(start: 2024-09-01T00:00:00Z, stop: 2024-10-10T00:00:00Z)
  |> filter(fn: (r) => r._measurement == "torbidita_chiarificato")
  |> mean() // Calculate the mean turbidity over time
  |> yield(name: "clarified_water_turbidity_trend")
```