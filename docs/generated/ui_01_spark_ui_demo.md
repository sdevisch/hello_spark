# UI: Spark UI demo (jobs and exploration)

Generated: 2025-08-10 17:02 UTC

## Scope

Tooling: use the Spark UI to connect code to execution (jobs/stages/SQL).

## Console output

```text
🚀 Starting Spark session for UI exploration...
📚 Docs index: docs/index.md
============================================================
🎉 Spark Session Started Successfully!
🌐 Spark UI: http://localhost:4040
🆔 Application ID: local-1754845363818
📊 Spark Version: 3.5.0
============================================================
📊 Creating sample jobs for UI demonstration...
  • Running Job 1: RDD Operations
    Result: 500 even squares
  • Running Job 2: DataFrame Operations
    Result: 5000 even squares in DataFrame
  • Running Job 3: SQL Operations
    Result: Total=5000, Avg=33343334.00, Max=100000000

🎯 Sample jobs completed! Now you can explore the Spark UI:
   📋 Jobs Tab: See the 3 jobs we just ran
   📊 Stages Tab: View task execution details
   🔧 SQL Tab: Check the SQL query execution plan
   ⚙️  Environment Tab: View Spark configuration
   💻 Executors Tab: Monitor resource usage

⏰ Keeping session alive indefinitely...
💡 Press Ctrl+C to stop when you're done exploring
🌐 Spark UI: http://localhost:4040
⏳ Skipping long keep-alive for docs generation
```
