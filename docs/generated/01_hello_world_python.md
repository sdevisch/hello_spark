# Basics: Spark Hello World (PySpark)

Generated: 2025-08-10 14:13 UTC

## Console output

```text
==================================================
Hello World with Apache Spark!
==================================================

1. Basic RDD Operations:
Original data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Squared numbers: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
Even numbers: [2, 4, 6, 8, 10]
Sum of all numbers: 55
Count: 10

2. Text Processing:
Text data: ['Hello World', 'Apache Spark', 'Big Data Processing', 'Distributed Computing']
Word counts: {'apache': 1, 'data': 1, 'processing': 1, 'hello': 1, 'spark': 1, 'distributed': 1, 'big': 1, 'computing': 1, 'world': 1}

3. DataFrame Operations:
People DataFrame:
+-------+---+-------------+
|   name|age|         city|
+-------+---+-------------+
|  Alice| 25|     New York|
|    Bob| 30|San Francisco|
|Charlie| 35|      Seattle|
|  Diana| 28|       Boston|
+-------+---+-------------+

People older than 27:
+-------+---+-------------+
|   name|age|         city|
+-------+---+-------------+
|    Bob| 30|San Francisco|
|Charlie| 35|      Seattle|
|  Diana| 28|       Boston|
+-------+---+-------------+

Average age:
+--------+
|avg(age)|
+--------+
|    29.5|
+--------+


4. SQL Queries:
People count by city:
+-------------+-----+
|         city|count|
+-------------+-----+
|     New York|    1|
|San Francisco|    1|
|      Seattle|    1|
|       Boston|    1|
+-------------+-----+


==================================================
Spark Hello World completed successfully!
Spark Version: 3.5.0
Spark UI available at: http://localhost:4040
==================================================
```
