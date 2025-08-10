# Performance 02: Data types and efficiency

Generated: 2025-08-10 16:30 UTC

## Console output

```text
🔢 SPARK DATA TYPES PERFORMANCE DEMO
==================================================
📊 Dataset size: 500,000 rows
🎯 Focus: Data type impact on performance & memory
==================================================
🚀 Starting comprehensive Spark data types performance analysis...

🔸 SCENARIO 1: Strings vs Correct Data Types
----------------------------------------
📋 Creating sample datasets...
Testing: Everything as STRING types...
Testing: CORRECT data types...
🔴 Strings approach:
   Load time: 3.127s
   Operation time: 0.458s
   Total time: 3.586s
   Estimated DataFrame size: 85.8 MB
🟢 Correct types approach:
   Load time: 2.458s
   Operation time: 0.655s
   Total time: 3.113s
   Estimated DataFrame size: 29.1 MB
⚡ Speedup with correct types: 1.15x

🔸 SCENARIO 2: 64-bit vs Right-sized Data Types
----------------------------------------
Creating optimized datasets for fair comparison...
Testing: OVERSIZED 64-bit types...
Testing: RIGHT-SIZED data types...
🔴 Oversized 64-bit types:
   Load time: 0.368s
   Operation time: 0.450s
   Total time: 0.818s
   Estimated DataFrame size: 32.9 MB
🟢 Right-sized types:
   Load time: 0.342s
   Operation time: 0.298s
   Total time: 0.640s
   Estimated DataFrame size: 17.2 MB
⚡ Speedup with right-sized types: 1.28x
💾 Memory savings: 47.8%

🔸 SCENARIO 3: Join Performance Impact
----------------------------------------
📋 Creating sample datasets...
Testing: STRING-based join...
Testing: INTEGER-based join...
🔴 String-based join: 1.722s
🟢 Integer-based join: 1.513s
⚡ Join speedup: 1.14x

📊 Creating performance visualizations...

============================================================
📋 SPARK DATA TYPES PERFORMANCE SUMMARY REPORT
============================================================

🔸 STRINGS vs CORRECT TYPES:
   Performance improvement: 1.15x faster
   Time saved: 0.472s
   Memory difference: 56.7MB

🔸 64-BIT vs RIGHT-SIZED TYPES:
   Performance improvement: 1.28x faster
   Time saved: 0.178s
   Memory saved: 47.8%

🔸 JOIN PERFORMANCE:
   Integer vs String join speedup: 1.14x faster

💡 KEY TAKEAWAYS:
   • Use correct data types instead of strings for significant performance gains
   • Right-size your data types to save memory and improve cache efficiency
   • Integer joins are much faster than string joins
   • Type casting during operations adds unnecessary overhead
   • Memory efficiency directly impacts Spark's ability to cache and process data

============================================================

🧹 Cleaning up Spark session...
```
