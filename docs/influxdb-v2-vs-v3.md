# InfluxDB: V2 vs V3

InfluxDB is one of the most popular time series databases (TSDB) for managing and analyzing temporal data. With the release of **InfluxDB V3 Core** (currently in **alpha**), InfluxData has introduced several new features and optimizations compared to the previous version, **InfluxDB V2**.

Currently, **InfluxDB V3 is only available in the Core version**, while the **Enterprise** version is under development and will offer advanced features for historical data, high availability and security. The alpha version of InfluxDB V3 Core has already removed some initial limitations, such as support for recent data only, now allowing you to write and query data from any period.

This paper analyzes the main differences between the two versions, comparing **architecture, performance, data management and query languages**.

## **1. Architectural Differences**

### **InfluxDB V2**

- Based on the **TSM (Time-Structured Merge Tree)** engine.
- Supports data storage, compression, and management with InfluxDB's own internal format.
- Uses **Flux** as the primary query language, allowing for more complex queries than InfluxQL V1.

### **InfluxDB V3**

- Introduces a new storage engine based on **Apache Arrow and Parquet**, optimized for fast analytical queries and scalability.
- Improves query optimization, especially for large datasets.
- **Removed the concept of buckets**: data is now organized in **databases and tables** instead of buckets with retention policies.
- **There is no longer a fixed retention policy**, data is no longer automatically deleted based on time, giving users more control.
- Introduced a **columnar storage** model, more efficient than the traditional row structure.

**Conclusion**: InfluxDB V3 improves scalability and performance with a completely revised architecture, while V2 remains based on a more traditional TSDB model.

## **2. Data Management: Bucket vs Database/Table**

A significant change in InfluxDB V3 is data management.

| Feature	    | InfluxDB V2 | InfluxDB V3|
| ------------- | ----------- | -------------------- |
| **Storage units**	| Bucket      |	Databases and table  |
| **Data structure**| Time series with predefined buckets | SQL-like organization with tables |
| **Retention Policy**	| Set per bucket (e.g. 30 days) | No default limitation, manual management |
| **Optimization**	| Based on TSM	| Based on Apache Arrow and Parquet |

### **InfluxDB V2: Using Buckets**

In V2, data is written by specifying a **bucket**, with a retention policy:

```bash
influx write --bucket "sensors" --org "my-org" --token "my-token" "temperature,location=room1 value=23.5"
```

Queries in Flux require you to specify a bucket:

```sql
from(bucket: "sensors")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "temperature")
  |> mean()
```

### **InfluxDB V3: Databases and Tables**

In V3, data is organized in **tables** inside a **database**, approaching a SQL-like model. Queries can now be executed in SQL:

```sql
SELECT * FROM "temperature_data"
WHERE time >= now() - interval '1 hour';
```

**Conclusion**: InfluxDB V3 abandons buckets in favor of a model closer to relational databases, making it easier to integrate with SQL tools.

## **3. Performance Comparison**

| Feature	    | InfluxDB V2 | InfluxDB V3|
| ------------- | ----------- | -------------------- |
| **Storage Engine**	| TSM (Time-Structured Merge Tree)      |	Apache Arrow + Parquet  |
| **Query Optimization**| Good, but less efficient on large datasets | Much improved, especially for large datasets |
| **Data compression**	| Good, but less optimized for long time series queries | Better thanks to Parquet and Arrow |
| **Query on historical data**	| Slower on very large datasets	| Much faster and scalable |

**Conclusion**: InfluxDB V3 offers a huge speed improvement, especially for complex analytical queries on large datasets, thanks to the use of Apache Arrow and Parquet.

## **4. Query Languages: Flux vs SQL Hook**

### **InfluxDB V2: Flux Language**

- Declarative language specific to InfluxDB.
- Powerful for complex analysis and advanced data manipulation.
- Syntax similar to a combination of SQL and functional programming functions.

Example query in Flux (InfluxDB V2):

```sql
from(bucket: "sensors")
 |> range(start: -1h)
 |> filter(fn: (r) => r._measurement == "temperature")
 |> mean()
```

### **InfluxDB V3: Introducing SQL Hook**

- Improved support for SQL, thanks to the new storage architecture.
- Maintains Flux support, but allows users to query SQL.
- **Deeper integration with existing SQL-based tools**.

```sql
SELECT time, mean(value)
FROM "temperature"
WHERE time >= now() - interval '1 hour'
GROUP BY time(10m);
```

**Conclusion**: InfluxDB V3 expands query capabilities by introducing SQL support, making it easier to adopt for those coming from relational databases.

## **5. Conclusion**

- **InfluxDB V3 represents a significant step forward** in performance and scalability compared to InfluxDB V2.
- The new storage engine **improves queries on large datasets**, optimizing reading and compression.
- **The bucket structure has been eliminated**, now data is organized in **databases and tables**, making the model closer to relational databases.
- The introduction of **SQL Hook** makes InfluxDB V3 more accessible to SQL users, while maintaining support for Flux.
- **Currently, InfluxDB V3 Core is still in alpha**, so it may not be ready for production environments yet, but it promises significant improvements in future releases.

If your focus is on performance, advanced analytics, and fast queries on large datasets, InfluxDB V3 is clearly a better choice than V2. However, it is still in alpha, so use in production requires caution.