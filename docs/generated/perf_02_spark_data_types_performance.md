# Performance 02: Data types and efficiency

Generated: 2025-08-10 16:23 UTC

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
   Load time: 3.109s
   Operation time: 0.460s
   Total time: 3.569s
   Estimated DataFrame size: 85.8 MB
🟢 Correct types approach:
   Load time: 2.690s
   Operation time: 0.530s
   Total time: 3.220s
   Estimated DataFrame size: 29.1 MB
⚡ Speedup with correct types: 1.11x

🔸 SCENARIO 2: 64-bit vs Right-sized Data Types
----------------------------------------
Creating optimized datasets for fair comparison...
Testing: OVERSIZED 64-bit types...
Testing: RIGHT-SIZED data types...
🔴 Oversized 64-bit types:
   Load time: 0.466s
   Operation time: 0.503s
   Total time: 0.970s
   Estimated DataFrame size: 32.9 MB
🟢 Right-sized types:
   Load time: 0.204s
   Operation time: 0.298s
   Total time: 0.502s
   Estimated DataFrame size: 17.2 MB
⚡ Speedup with right-sized types: 1.93x
💾 Memory savings: 47.8%

🔸 SCENARIO 3: Join Performance Impact
----------------------------------------
📋 Creating sample datasets...
Testing: STRING-based join...
Testing: INTEGER-based join...
🔴 String-based join: 1.754s
🟢 Integer-based join: 1.575s
⚡ Join speedup: 1.11x

📊 Creating performance visualizations...

============================================================
📋 SPARK DATA TYPES PERFORMANCE SUMMARY REPORT
============================================================

🔸 STRINGS vs CORRECT TYPES:
   Performance improvement: 1.11x faster
   Time saved: 0.348s
   Memory difference: 56.7MB

🔸 64-BIT vs RIGHT-SIZED TYPES:
   Performance improvement: 1.93x faster
   Time saved: 0.468s
   Memory saved: 47.8%

🔸 JOIN PERFORMANCE:
   Integer vs String join speedup: 1.11x faster

💡 KEY TAKEAWAYS:
   • Use correct data types instead of strings for significant performance gains
   • Right-size your data types to save memory and improve cache efficiency
   • Integer joins are much faster than string joins
   • Type casting during operations adds unnecessary overhead
   • Memory efficiency directly impacts Spark's ability to cache and process data

============================================================

🧹 Cleaning up Spark session...
```
