# Performance: Data types and efficiency

Generated: 2025-08-10 13:58 UTC

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
   Load time: 3.053s
   Operation time: 0.453s
   Total time: 3.506s
   Estimated DataFrame size: 85.8 MB
🟢 Correct types approach:
   Load time: 2.492s
   Operation time: 0.574s
   Total time: 3.065s
   Estimated DataFrame size: 29.1 MB
⚡ Speedup with correct types: 1.14x

🔸 SCENARIO 2: 64-bit vs Right-sized Data Types
----------------------------------------
Creating optimized datasets for fair comparison...
Testing: OVERSIZED 64-bit types...
Testing: RIGHT-SIZED data types...
🔴 Oversized 64-bit types:
   Load time: 0.452s
   Operation time: 0.430s
   Total time: 0.882s
   Estimated DataFrame size: 32.9 MB
🟢 Right-sized types:
   Load time: 0.387s
   Operation time: 0.305s
   Total time: 0.692s
   Estimated DataFrame size: 17.2 MB
⚡ Speedup with right-sized types: 1.27x
💾 Memory savings: 47.8%

🔸 SCENARIO 3: Join Performance Impact
----------------------------------------
📋 Creating sample datasets...
Testing: STRING-based join...
Testing: INTEGER-based join...
🔴 String-based join: 1.773s
🟢 Integer-based join: 1.476s
⚡ Join speedup: 1.20x

📊 Creating performance visualizations...

============================================================
📋 SPARK DATA TYPES PERFORMANCE SUMMARY REPORT
============================================================

🔸 STRINGS vs CORRECT TYPES:
   Performance improvement: 1.14x faster
   Time saved: 0.441s
   Memory difference: 56.7MB

🔸 64-BIT vs RIGHT-SIZED TYPES:
   Performance improvement: 1.27x faster
   Time saved: 0.189s
   Memory saved: 47.8%

🔸 JOIN PERFORMANCE:
   Integer vs String join speedup: 1.20x faster

💡 KEY TAKEAWAYS:
   • Use correct data types instead of strings for significant performance gains
   • Right-size your data types to save memory and improve cache efficiency
   • Integer joins are much faster than string joins
   • Type casting during operations adds unnecessary overhead
   • Memory efficiency directly impacts Spark's ability to cache and process data

============================================================

🧹 Cleaning up Spark session...
```
