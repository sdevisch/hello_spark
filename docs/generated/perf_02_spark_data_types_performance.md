# Performance 02: Data types and efficiency

Generated: 2025-08-10 22:50 UTC

## Scope

Cross-cutting performance practices: IO formats, UDF vs native, caching, partitioning, broadcast, and data types.

## Console output

```text
📚 Docs index: docs/index.md
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
   Load time: 2.966s
   Operation time: 0.521s
   Total time: 3.487s
   Estimated DataFrame size: 85.8 MB
🟢 Correct types approach:
   Load time: 2.636s
   Operation time: 0.544s
   Total time: 3.180s
   Estimated DataFrame size: 29.1 MB
⚡ Speedup with correct types: 1.10x

🔸 SCENARIO 2: 64-bit vs Right-sized Data Types
----------------------------------------
Creating optimized datasets for fair comparison...
Testing: OVERSIZED 64-bit types...
Testing: RIGHT-SIZED data types...
🔴 Oversized 64-bit types:
   Load time: 0.357s
   Operation time: 0.453s
   Total time: 0.810s
   Estimated DataFrame size: 32.9 MB
🟢 Right-sized types:
   Load time: 0.165s
   Operation time: 0.321s
   Total time: 0.486s
   Estimated DataFrame size: 17.2 MB
⚡ Speedup with right-sized types: 1.67x
💾 Memory savings: 47.8%

🔸 SCENARIO 3: Join Performance Impact
----------------------------------------
📋 Creating sample datasets...
Testing: STRING-based join...
Testing: INTEGER-based join...
🔴 String-based join: 1.568s
🟢 Integer-based join: 1.574s
⚡ Join speedup: 1.00x

📊 Creating performance visualizations...

============================================================
📋 SPARK DATA TYPES PERFORMANCE SUMMARY REPORT
============================================================

🔸 STRINGS vs CORRECT TYPES:
   Performance improvement: 1.10x faster
   Time saved: 0.308s
   Memory difference: 56.7MB

🔸 64-BIT vs RIGHT-SIZED TYPES:
   Performance improvement: 1.67x faster
   Time saved: 0.324s
   Memory saved: 47.8%

🔸 JOIN PERFORMANCE:
   Integer vs String join speedup: 1.00x faster

💡 KEY TAKEAWAYS:
   • Use correct data types instead of strings for significant performance gains
   • Right-size your data types to save memory and improve cache efficiency
   • Integer joins are much faster than string joins
   • Type casting during operations adds unnecessary overhead
   • Memory efficiency directly impacts Spark's ability to cache and process data

============================================================

🧹 Cleaning up Spark session...
```
