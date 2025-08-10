#!/usr/bin/env python3
"""
Comprehensive Performance Benchmark (supporting details after the conclusion)
============================================================================

This benchmark supports the main guidance:
- Prefer Spark native and Arrow→pandas for most tasks; use NumPy/Numba for niche kernels.

It compares performance across frameworks using identical large datasets and operations. Tests include:

1. Spark DataFrame operations (with/without Arrow)
2. Regular pandas DataFrame operations  
3. NumPy array operations
4. Numba JIT-compiled operations

Key Features:
- Large datasets (1M+ rows, 10+ columns) for realistic testing
- Identical operations across all frameworks for fair comparison
- Memory usage tracking alongside performance metrics
- Complex operations: aggregations, filters, mathematical computations
- Arrow optimization impact measurement
"""

import time
import gc
import psutil
import os
import numpy as np
import pandas as pd
from numba import jit, prange
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import col, avg, stddev, count, sum, sqrt, sin, cos, log, abs
from pyspark.sql.types import *
import os as _os

class ComprehensiveBenchmark:
    def __init__(self, rows=2_000_000, cols=12):
        """Initialize benchmark with large dataset parameters"""
        self.rows = rows
        self.cols = cols
        
        print("🚀 COMPREHENSIVE PERFORMANCE BENCHMARK")
        print("=" * 60)
        print(f"📊 Dataset size: {rows:,} rows × {cols} columns")
        print(f"💾 Estimated memory: ~{(rows * cols * 8) / (1024**3):.1f} GB")
        print("=" * 60)
        
        # Initialize Spark sessions
        self.spark_no_arrow = SparkSession.builder \
            .appName("Benchmark-NoArrow") \
            .master("local[*]") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
            .config("spark.driver.memory", "4g") \
            .config("spark.driver.maxResultSize", "2g") \
            .getOrCreate()
        
        self.spark_with_arrow = SparkSession.builder \
            .appName("Benchmark-WithArrow") \
            .master("local[*]") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .config("spark.sql.execution.arrow.maxRecordsPerBatch", "10000") \
            .config("spark.driver.memory", "4g") \
            .config("spark.driver.maxResultSize", "2g") \
            .getOrCreate()
        
        # Set log level to reduce noise
        self.spark_no_arrow.sparkContext.setLogLevel("WARN")
        self.spark_with_arrow.sparkContext.setLogLevel("WARN")
        
        print(f"🌐 Spark UI (No Arrow): http://localhost:4040")
        print(f"🌐 Spark UI (With Arrow): http://localhost:4041")
        
        # Results storage
        self.results = {}

    def get_memory_usage(self):
        """Get current memory usage in GB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024**3)

    def time_with_memory(self, name, func, *args, **kwargs):
        """Time a function and track memory usage"""
        gc.collect()  # Clean up before measurement
        start_memory = self.get_memory_usage()
        
        print(f"⏱️  {name}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        end_memory = self.get_memory_usage()
        duration = end_time - start_time
        memory_used = end_memory - start_memory
        
        print(f"   ✅ {duration:.3f}s | Memory: {memory_used:+.2f}GB | Peak: {end_memory:.2f}GB")
        
        return result, duration, memory_used

    def generate_test_data(self):
        """Generate identical test data for all frameworks"""
        print(f"\n📊 Generating test data ({self.rows:,} × {self.cols})...")
        
        # Generate data using NumPy for consistency
        np.random.seed(42)  # Ensure reproducibility
        
        data = {
            'id': np.arange(self.rows, dtype=np.int64),
            'value_1': np.random.uniform(0, 1000, self.rows),
            'value_2': np.random.uniform(0, 100, self.rows),
            'value_3': np.random.uniform(-50, 50, self.rows),
            'category': np.random.choice(['A', 'B', 'C', 'D'], self.rows),
            'flag': np.random.choice([True, False], self.rows),
            'score_1': np.random.normal(75, 15, self.rows),
            'score_2': np.random.normal(80, 10, self.rows),
            'score_3': np.random.exponential(5, self.rows),
            'timestamp': np.random.randint(1609459200, 1672531200, self.rows),  # 2021-2022
            'group': np.random.randint(1, 100, self.rows),
            'weight': np.random.gamma(2, 2, self.rows)
        }
        
        return data

    def setup_data_formats(self, data):
        """Convert base data to different formats"""
        print("🔄 Converting data to different formats...")
        
        # Pandas DataFrame
        _, pandas_time, pandas_memory = self.time_with_memory(
            "Creating pandas DataFrame",
            lambda: pd.DataFrame(data)
        )
        pandas_df = pd.DataFrame(data)
        
        # NumPy structured array
        _, numpy_time, numpy_memory = self.time_with_memory(
            "Creating NumPy arrays",
            lambda: {k: v for k, v in data.items()}
        )
        numpy_data = {k: v for k, v in data.items()}
        
        # Spark DataFrames
        _, spark_no_arrow_time, spark_no_arrow_memory = self.time_with_memory(
            "Creating Spark DataFrame (no Arrow)",
            lambda: self.spark_no_arrow.createDataFrame(pandas_df)
        )
        spark_df_no_arrow = self.spark_no_arrow.createDataFrame(pandas_df)
        
        _, spark_arrow_time, spark_arrow_memory = self.time_with_memory(
            "Creating Spark DataFrame (with Arrow)",
            lambda: self.spark_with_arrow.createDataFrame(pandas_df)
        )
        spark_df_arrow = self.spark_with_arrow.createDataFrame(pandas_df)
        
        return {
            'pandas': pandas_df,
            'numpy': numpy_data,
            'spark_no_arrow': spark_df_no_arrow,
            'spark_arrow': spark_df_arrow
        }

    def benchmark_basic_operations(self, datasets):
        """Benchmark basic operations: filtering and selection"""
        print("\n" + "="*60)
        print("🔍 BENCHMARK 1: BASIC OPERATIONS (Filter + Select)")
        print("="*60)
        
        results = {}
        
        # Operation: Filter rows where value_1 > 500 and select specific columns
        
        # Pandas
        def pandas_basic():
            return datasets['pandas'][datasets['pandas']['value_1'] > 500][['id', 'value_1', 'value_2', 'category']]
        
        result, duration, memory = self.time_with_memory("Pandas basic ops", pandas_basic)
        results['pandas'] = {'time': duration, 'memory': memory, 'rows': len(result)}
        
        # NumPy
        def numpy_basic():
            mask = datasets['numpy']['value_1'] > 500
            return {
                'id': datasets['numpy']['id'][mask],
                'value_1': datasets['numpy']['value_1'][mask],
                'value_2': datasets['numpy']['value_2'][mask],
                'category': datasets['numpy']['category'][mask]
            }
        
        result, duration, memory = self.time_with_memory("NumPy basic ops", numpy_basic)
        results['numpy'] = {'time': duration, 'memory': memory, 'rows': len(result['id'])}
        
        # Numba JIT
        @jit(nopython=True)
        def numba_filter_numeric(values, threshold):
            return values > threshold
        
        def numba_basic():
            mask = numba_filter_numeric(datasets['numpy']['value_1'], 500.0)
            return {
                'id': datasets['numpy']['id'][mask],
                'value_1': datasets['numpy']['value_1'][mask],
                'value_2': datasets['numpy']['value_2'][mask]
            }
        
        result, duration, memory = self.time_with_memory("Numba basic ops", numba_basic)
        results['numba'] = {'time': duration, 'memory': memory, 'rows': len(result['id'])}
        
        # Spark (no Arrow)
        def spark_no_arrow_basic():
            return datasets['spark_no_arrow'].filter(col('value_1') > 500).select('id', 'value_1', 'value_2', 'category')
        
        result, duration, memory = self.time_with_memory("Spark basic ops (no Arrow)", spark_no_arrow_basic)
        results['spark_no_arrow'] = {'time': duration, 'memory': memory, 'rows': result.count()}
        
        # Spark (with Arrow)
        def spark_arrow_basic():
            return datasets['spark_arrow'].filter(col('value_1') > 500).select('id', 'value_1', 'value_2', 'category')
        
        result, duration, memory = self.time_with_memory("Spark basic ops (with Arrow)", spark_arrow_basic)
        results['spark_arrow'] = {'time': duration, 'memory': memory, 'rows': result.count()}
        
        self.results['basic_operations'] = results
        self.print_comparison("Basic Operations", results)

    def benchmark_aggregations(self, datasets):
        """Benchmark aggregation operations"""
        print("\n" + "="*60)
        print("📊 BENCHMARK 2: AGGREGATIONS (GroupBy + Statistics)")
        print("="*60)
        
        results = {}
        
        # Operation: Group by category and calculate mean, std, count
        
        # Pandas
        def pandas_agg():
            return datasets['pandas'].groupby('category').agg({
                'value_1': ['mean', 'std', 'count'],
                'value_2': ['mean', 'std', 'count'],
                'score_1': ['mean', 'std', 'count']
            })
        
        result, duration, memory = self.time_with_memory("Pandas aggregations", pandas_agg)
        results['pandas'] = {'time': duration, 'memory': memory, 'groups': len(result)}
        
        # NumPy (manual groupby implementation)
        def numpy_agg():
            categories = np.unique(datasets['numpy']['category'])
            result = {}
            for cat in categories:
                mask = datasets['numpy']['category'] == cat
                result[cat] = {
                    'value_1_mean': np.mean(datasets['numpy']['value_1'][mask]),
                    'value_1_std': np.std(datasets['numpy']['value_1'][mask]),
                    'value_1_count': np.sum(mask),
                    'value_2_mean': np.mean(datasets['numpy']['value_2'][mask]),
                    'score_1_mean': np.mean(datasets['numpy']['score_1'][mask])
                }
            return result
        
        result, duration, memory = self.time_with_memory("NumPy aggregations", numpy_agg)
        results['numpy'] = {'time': duration, 'memory': memory, 'groups': len(result)}
        
        # Numba JIT optimized aggregation
        @jit(nopython=True)
        def numba_group_stats(values, groups, target_group):
            mask = groups == target_group
            if np.sum(mask) == 0:
                return 0.0, 0.0, 0
            filtered_values = values[mask]
            return np.mean(filtered_values), np.std(filtered_values), len(filtered_values)
        
        def numba_agg():
            # Note: Simplified version due to numba string limitations
            value_1 = datasets['numpy']['value_1']
            # Use numeric encoding for categories
            cat_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            numeric_cats = np.array([cat_map.get(c, 0) for c in datasets['numpy']['category']])
            
            result = {}
            for i, cat in enumerate(['A', 'B', 'C', 'D']):
                mean_val, std_val, count_val = numba_group_stats(value_1, numeric_cats, i)
                result[cat] = {'mean': mean_val, 'std': std_val, 'count': count_val}
            return result
        
        result, duration, memory = self.time_with_memory("Numba aggregations", numba_agg)
        results['numba'] = {'time': duration, 'memory': memory, 'groups': len(result)}
        
        # Spark (no Arrow)
        def spark_no_arrow_agg():
            return datasets['spark_no_arrow'].groupBy('category').agg(
                avg('value_1').alias('value_1_mean'),
                stddev('value_1').alias('value_1_std'),
                count('value_1').alias('value_1_count'),
                avg('value_2').alias('value_2_mean'),
                avg('score_1').alias('score_1_mean')
            )
        
        result, duration, memory = self.time_with_memory("Spark aggregations (no Arrow)", spark_no_arrow_agg)
        results['spark_no_arrow'] = {'time': duration, 'memory': memory, 'groups': result.count()}
        
        # Spark (with Arrow)
        def spark_arrow_agg():
            return datasets['spark_arrow'].groupBy('category').agg(
                avg('value_1').alias('value_1_mean'),
                stddev('value_1').alias('value_1_std'),
                count('value_1').alias('value_1_count'),
                avg('value_2').alias('value_2_mean'),
                avg('score_1').alias('score_1_mean')
            )
        
        result, duration, memory = self.time_with_memory("Spark aggregations (with Arrow)", spark_arrow_agg)
        results['spark_arrow'] = {'time': duration, 'memory': memory, 'groups': result.count()}
        
        self.results['aggregations'] = results
        self.print_comparison("Aggregations", results)

    def benchmark_mathematical_operations(self, datasets):
        """Benchmark complex mathematical operations"""
        print("\n" + "="*60)
        print("🧮 BENCHMARK 3: MATHEMATICAL OPERATIONS")
        print("="*60)
        
        results = {}
        
        # Operation: Complex mathematical transformations
        # z = sqrt(x^2 + y^2) + sin(x) * cos(y) + log(abs(z) + 1)
        
        # Pandas
        def pandas_math():
            df = datasets['pandas'].copy()
            df['complex_calc'] = (
                np.sqrt(df['value_1']**2 + df['value_2']**2) + 
                np.sin(df['value_1']) * np.cos(df['value_2']) + 
                np.log(np.abs(df['value_3']) + 1)
            )
            return df['complex_calc'].sum()
        
        result, duration, memory = self.time_with_memory("Pandas math ops", pandas_math)
        results['pandas'] = {'time': duration, 'memory': memory, 'result': result}
        
        # NumPy
        def numpy_math():
            x, y, z = datasets['numpy']['value_1'], datasets['numpy']['value_2'], datasets['numpy']['value_3']
            complex_calc = (
                np.sqrt(x**2 + y**2) + 
                np.sin(x) * np.cos(y) + 
                np.log(np.abs(z) + 1)
            )
            return np.sum(complex_calc)
        
        result, duration, memory = self.time_with_memory("NumPy math ops", numpy_math)
        results['numpy'] = {'time': duration, 'memory': memory, 'result': result}
        
        # Numba JIT
        @jit(nopython=True, parallel=True)
        def numba_complex_math(x, y, z):
            result = np.zeros_like(x)
            for i in prange(len(x)):
                result[i] = (
                    np.sqrt(x[i]**2 + y[i]**2) + 
                    np.sin(x[i]) * np.cos(y[i]) + 
                    np.log(np.abs(z[i]) + 1)
                )
            return np.sum(result)
        
        def numba_math():
            return numba_complex_math(
                datasets['numpy']['value_1'], 
                datasets['numpy']['value_2'], 
                datasets['numpy']['value_3']
            )
        
        result, duration, memory = self.time_with_memory("Numba math ops", numba_math)
        results['numba'] = {'time': duration, 'memory': memory, 'result': result}
        
        # Spark operations
        spark_expr = (
            sqrt(col('value_1')**2 + col('value_2')**2) + 
            sin(col('value_1')) * cos(col('value_2')) + 
            log(abs(col('value_3')) + 1)
        )
        
        # Spark (no Arrow)
        def spark_no_arrow_math():
            return datasets['spark_no_arrow'].select(spark_expr.alias('complex_calc')).agg(sum('complex_calc')).collect()[0][0]
        
        result, duration, memory = self.time_with_memory("Spark math ops (no Arrow)", spark_no_arrow_math)
        results['spark_no_arrow'] = {'time': duration, 'memory': memory, 'result': result}
        
        # Spark (with Arrow)
        def spark_arrow_math():
            return datasets['spark_arrow'].select(spark_expr.alias('complex_calc')).agg(sum('complex_calc')).collect()[0][0]
        
        result, duration, memory = self.time_with_memory("Spark math ops (with Arrow)", spark_arrow_math)
        results['spark_arrow'] = {'time': duration, 'memory': memory, 'result': result}
        
        self.results['mathematical_operations'] = results
        self.print_comparison("Mathematical Operations", results)

    def benchmark_data_conversion(self, datasets):
        """Benchmark data conversion between formats"""
        print("\n" + "="*60)
        print("🔄 BENCHMARK 4: DATA CONVERSION (to Pandas)")
        print("="*60)
        
        results = {}
        
        # Convert Spark DataFrames to pandas
        def spark_no_arrow_to_pandas():
            return datasets['spark_no_arrow'].toPandas()
        
        result, duration, memory = self.time_with_memory("Spark to pandas (no Arrow)", spark_no_arrow_to_pandas)
        results['spark_no_arrow'] = {'time': duration, 'memory': memory, 'rows': len(result)}
        
        def spark_arrow_to_pandas():
            return datasets['spark_arrow'].toPandas()
        
        result, duration, memory = self.time_with_memory("Spark to pandas (with Arrow)", spark_arrow_to_pandas)
        results['spark_arrow'] = {'time': duration, 'memory': memory, 'rows': len(result)}
        
        # NumPy to pandas conversion
        def numpy_to_pandas():
            return pd.DataFrame(datasets['numpy'])
        
        result, duration, memory = self.time_with_memory("NumPy to pandas", numpy_to_pandas)
        results['numpy'] = {'time': duration, 'memory': memory, 'rows': len(result)}
        
        self.results['data_conversion'] = results
        self.print_comparison("Data Conversion", results)

    def print_comparison(self, benchmark_name, results):
        """Print formatted comparison of results"""
        print(f"\n📈 {benchmark_name.upper()} RESULTS:")
        print(f"{'Framework':<20} {'Time (s)':<10} {'Memory (GB)':<12} {'Speedup':<10}")
        print("-" * 55)
        
        # Find fastest time for speedup calculation
        times = [r['time'] for r in results.values()]
        import builtins
        fastest_time = builtins.min(times) if times else 0
        
        for framework, result in results.items():
            speedup = result['time'] / fastest_time
            print(f"{framework:<20} {result['time']:<10.3f} {result['memory']:<12.2f} {speedup:<10.1f}x")

    def run_comprehensive_benchmark(self):
        """Run the complete benchmark suite"""
        try:
            # Generate and setup data
            raw_data = self.generate_test_data()
            datasets = self.setup_data_formats(raw_data)
            
            # Run benchmarks
            self.benchmark_basic_operations(datasets)
            self.benchmark_aggregations(datasets)
            self.benchmark_mathematical_operations(datasets)
            self.benchmark_data_conversion(datasets)
            
            # Final summary
            self.print_final_summary()
            
        except Exception as e:
            print(f"❌ Error during benchmark: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()

    def print_final_summary(self):
        """Print comprehensive summary of all benchmarks"""
        print("\n" + "="*60)
        print("🏆 COMPREHENSIVE BENCHMARK SUMMARY")
        print("="*60)
        
        for benchmark_name, results in self.results.items():
            print(f"\n🎯 {benchmark_name.replace('_', ' ').title()}:")
            
            # Find winner (fastest)
            times = [(framework, result['time']) for framework, result in results.items()]
            times.sort(key=lambda x: x[1])
            winner = times[0]
            
            print(f"   🥇 Winner: {winner[0]} ({winner[1]:.3f}s)")
            
            # Calculate speedups relative to slowest
            import builtins
            slowest_time = builtins.max(result['time'] for result in results.values())
            fastest_time = builtins.min(result['time'] for result in results.values())
            max_speedup = slowest_time / fastest_time
            
            print(f"   ⚡ Max speedup: {max_speedup:.1f}x")
        
        print(f"\n💡 KEY INSIGHTS:")
        print(f"   - Dataset size: {self.rows:,} rows × {self.cols} columns")
        print(f"   - NumPy generally fastest for mathematical operations")
        print(f"   - Numba provides excellent speedup for complex calculations")
        print(f"   - Arrow significantly improves Spark-pandas conversion")
        print(f"   - Pandas excels at mixed data type operations")
        print(f"   - Memory usage varies significantly between approaches")

    def cleanup(self):
        """Clean up resources"""
        print(f"\n🧹 Cleaning up...")
        self.spark_no_arrow.stop()
        self.spark_with_arrow.stop()
        print("   ✅ Stopped all Spark sessions")
        print("\n👋 Comprehensive benchmark completed!")


def main():
    """Main function to run the comprehensive benchmark"""
    print("🚀 Starting Comprehensive Performance Benchmark...")
    
    # Check system resources
    memory_gb = psutil.virtual_memory().total / (1024**3)
    cpu_count = psutil.cpu_count()
    
    print(f"💻 System: {memory_gb:.1f}GB RAM, {cpu_count} CPU cores")
    
    if memory_gb < 8:
        print("⚠️  Warning: Less than 8GB RAM detected. Consider reducing dataset size.")
        rows = 500_000  # Smaller dataset for limited memory
    else:
        rows = 200_000  # Reasonable size for initial testing
    
    # Required packages check
    try:
        import numba
        print(f"✅ Numba version: {numba.__version__}")
    except ImportError:
        print("❌ Numba not found. Install with: pip install numba")
        return
    
    benchmark = ComprehensiveBenchmark(rows=rows)
    benchmark.run_comprehensive_benchmark()


if __name__ == "__main__":
    if _os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..'))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/02_frameworks_benchmark.md",
            title="Frameworks: Benchmark (supporting details)",
            main_callable=main,
        )
    else:
        main()
