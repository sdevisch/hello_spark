# Performance 02: Data types and efficiency

Generated: 2025-08-10 16:54 UTC

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
   Load time: 3.030s
   Operation time: 0.517s
   Total time: 3.547s
   Estimated DataFrame size: 85.8 MB
🟢 Correct types approach:
   Load time: 2.518s
   Operation time: 0.504s
   Total time: 3.022s
   Estimated DataFrame size: 29.1 MB
⚡ Speedup with correct types: 1.17x

🔸 SCENARIO 2: 64-bit vs Right-sized Data Types
----------------------------------------
Creating optimized datasets for fair comparison...
Testing: OVERSIZED 64-bit types...
Testing: RIGHT-SIZED data types...
🔴 Oversized 64-bit types:
   Load time: 0.375s
   Operation time: 0.424s
   Total time: 0.799s
   Estimated DataFrame size: 32.9 MB
🟢 Right-sized types:
   Load time: 0.268s
   Operation time: 0.323s
   Total time: 0.591s
   Estimated DataFrame size: 17.2 MB
⚡ Speedup with right-sized types: 1.35x
💾 Memory savings: 47.8%

🔸 SCENARIO 3: Join Performance Impact
----------------------------------------
📋 Creating sample datasets...
Testing: STRING-based join...
Testing: INTEGER-based join...
🔴 String-based join: 1.606s
🟢 Integer-based join: 1.428s
⚡ Join speedup: 1.12x

📊 Creating performance visualizations...

============================================================
📋 SPARK DATA TYPES PERFORMANCE SUMMARY REPORT
============================================================

🔸 STRINGS vs CORRECT TYPES:
   Performance improvement: 1.17x faster
   Time saved: 0.525s
   Memory difference: 56.7MB

🔸 64-BIT vs RIGHT-SIZED TYPES:
   Performance improvement: 1.35x faster
   Time saved: 0.208s
   Memory saved: 47.8%

🔸 JOIN PERFORMANCE:
   Integer vs String join speedup: 1.12x faster

💡 KEY TAKEAWAYS:
   • Use correct data types instead of strings for significant performance gains
   • Right-size your data types to save memory and improve cache efficiency
   • Integer joins are much faster than string joins
   • Type casting during operations adds unnecessary overhead
   • Memory efficiency directly impacts Spark's ability to cache and process data

============================================================

🧹 Cleaning up Spark session...
```
