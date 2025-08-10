#!/usr/bin/env python3
"""
Conclusion first: After Arrow→NumPy, stay in C; avoid Python crossings
======================================================================

Conclusion: Once data is in NumPy, keep work vectorized in C. Avoid scalar
extraction, `.tolist()`, and Python loops that cross back into Python objects.

Why: Vectorized NumPy runs in optimized C; Python object creation is slow and
memory-heavy.

What: Identify boundaries where C→Python happens and how to avoid them.

How: Build realistic data in Spark, convert with Arrow, then profile NumPy ops.
"""

import time
import numpy as np
import psutil
import os
import pickle
import sys
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import col

class NumPySerializationNuances:
    def __init__(self, rows=100_000):  # Smaller for detailed analysis
        """Initialize with focus on serialization nuances"""
        self.rows = rows
        
        print("🔬 NUMPY SERIALIZATION NUANCES DEMO")
        print("=" * 50)
        print(f"📊 Dataset size: {rows:,} rows (smaller for detailed analysis)")
        print("🎯 Focus: When does serialization happen within NumPy?")
        print("=" * 50)
        
        # Initialize Spark for comparison
        self.spark = SparkSession.builder \
            .appName("NumPy-Serialization-Nuances") \
            .master("local[*]") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        print(f"🌐 Spark UI: http://localhost:4040")

    def get_memory_usage(self):
        """Get current memory usage in GB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024**3)

    def time_operation(self, name, func, *args, **kwargs):
        """Time an operation with memory tracking"""
        start_memory = self.get_memory_usage()
        print(f"⏱️  {name}")
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        end_memory = self.get_memory_usage()
        duration = end_time - start_time
        memory_delta = end_memory - start_memory
        
        print(f"   ✅ {duration:.6f}s | Memory: {memory_delta:+.3f}GB")
        return result, duration

    def create_test_data(self):
        """Create test data starting in Spark - REALISTIC SCENARIO"""
        print("\n" + "="*50)
        print("📊 CREATING TEST DATA IN SPARK - REALISTIC STARTING POINT")
        print("="*50)
        
        print("💡 REAL-WORLD SCENARIO:")
        print("   - Data starts in Spark (from files, databases, etc.)")
        print("   - We'll convert to NumPy to demonstrate serialization boundaries")
        print("   - Focus: When does serialization happen within NumPy operations?")
        
        def create_spark_and_convert():
            # STEP 1: Create data in Spark (realistic starting point)
            # This simulates reading from files, databases, etc.
            spark_df = self.spark.range(self.rows).select(
                col("id"),
                # Spark's built-in random functions - computed in JVM
                (F.rand() * 200 - 100).alias("float_data"),     # Uniform(-100, 100)
                (F.rand() * 2000 - 1000).cast("int").alias("int_data"),  # Random(-1000, 1000)
                (F.rand() > 0.5).alias("bool_data"),            # Random boolean
                (F.rand()).alias("float32_data"),               # For dtype analysis
                (F.rand() + F.rand()).alias("complex_real")     # For complex analysis
            ).cache()
            
            # Force materialization
            spark_df.count()
            
            # STEP 2: Convert to pandas/NumPy (this is where serialization happens)
            # This demonstrates the realistic scenario: Spark → NumPy conversion
            print("   📤 Converting Spark → pandas → NumPy (SERIALIZATION)")
            pdf = spark_df.toPandas()
            
            # STEP 3: Extract NumPy arrays (no additional serialization)
            arrays = {
                'float_data': pdf['float_data'].values.astype(np.float64),
                'int_data': pdf['int_data'].values.astype(np.int32), 
                'bool_data': pdf['bool_data'].values,
                'float32_data': pdf['float32_data'].values.astype(np.float32),
                'complex_data': (pdf['complex_real'].values + 1j * pdf['complex_real'].values).astype(np.complex128),
                
                # Additional arrays for testing
                'large_array': np.random.random((1000, 100)),  # Extra for matrix ops
                'small_array': np.array([1, 2, 3, 4, 5])       # Tiny for demos
            }
            
            return arrays, spark_df
        
        (arrays, spark_df), duration = self.time_operation("Creating Spark DF and converting to NumPy", create_spark_and_convert)
        
        print(f"\n✅ Started with Spark DataFrame, converted to {len(arrays)} NumPy arrays")
        print(f"💾 Total NumPy size: {sum(arr.nbytes for arr in arrays.values()) / (1024**2):.1f} MB")
        print(f"🎯 Now we'll analyze serialization boundaries within NumPy operations")
        
        return arrays, spark_df

    def demo_no_serialization_operations(self, arrays):
        """Demonstrate NumPy operations that stay in C - NO SERIALIZATION"""
        print("\n" + "="*50)
        print("✅ NUMPY OPERATIONS - NO SERIALIZATION")
        print("="*50)
        
        print("💡 THESE OPERATIONS STAY IN C (NO SERIALIZATION):")
        print("   - Array arithmetic and math functions")
        print("   - Array slicing and views")
        print("   - Aggregations (sum, mean, etc.)")
        print("   - Boolean indexing and masking")
        print("   - Array reshaping and transposing")
        
        float_data = arrays['float_data']
        int_data = arrays['int_data']
        bool_data = arrays['bool_data']
        large_array = arrays['large_array']
        
        # 1. Basic arithmetic operations - Pure C
        def arithmetic_operations():
            """All operations stay in compiled C code"""
            # WHAT HAPPENS: All operations vectorized in C
            # - No Python objects created for intermediate results
            # - SIMD instructions used for parallel computation
            # - Memory stays in contiguous C arrays
            result1 = float_data * 2.5 + 10.0          # Vectorized: C multiplication & addition
            result2 = np.sqrt(np.abs(float_data))       # Vectorized: C sqrt and abs functions
            result3 = np.sin(float_data) ** 2           # Vectorized: C sin function + power
            result4 = (float_data > 0) & (float_data < 50)  # Vectorized: C comparison + bitwise AND
            
            return result1, result2, result3, result4
        
        arith_results, arith_time = self.time_operation(
            "Arithmetic operations (*, +, sqrt, sin, comparisons)",
            arithmetic_operations
        )
        
        # 2. Array slicing and views - Memory views, not copies
        def slicing_operations():
            """Array slicing creates views, not copies - NO SERIALIZATION"""
            # WHAT HAPPENS: Creates new array objects but shares underlying memory
            # - No data copying or serialization
            # - Just pointer arithmetic and stride calculations
            # - Views maintain reference to original C memory block
            
            slice1 = float_data[1000:2000]          # View: shares memory with original
            slice2 = float_data[::10]               # Strided view: every 10th element
            slice3 = float_data[bool_data]          # Boolean mask: creates copy but in C
            slice4 = large_array[:, 10:20]          # 2D slice: view of columns 10-19
            
            # Reshaping - just changes metadata, same memory
            reshaped = large_array.reshape(-1)      # 1D view of 2D array
            transposed = large_array.T              # Transpose: just swaps strides
            
            return slice1, slice2, slice3, slice4, reshaped, transposed
        
        slice_results, slice_time = self.time_operation(
            "Slicing & reshaping (views, boolean indexing)",
            slicing_operations
        )
        
        # 3. Aggregation operations - Optimized C reductions
        def aggregation_operations():
            """Statistical aggregations use optimized C algorithms"""
            # WHAT HAPPENS: Highly optimized reduction algorithms in C
            # - Single pass through data for most operations
            # - SIMD vectorization for parallel computation
            # - May use specialized algorithms (e.g., Kahan summation)
            # - Results are Python scalars but computation is pure C
            
            mean_val = np.mean(float_data)           # C implementation: sum/count
            std_val = np.std(float_data)             # C implementation: Welford's algorithm
            median_val = np.median(float_data)       # C implementation: quickselect
            percentile_val = np.percentile(float_data, 95)  # C implementation: interpolation
            
            # Multi-axis aggregations on 2D array
            col_means = np.mean(large_array, axis=0)  # Mean of each column (vectorized)
            row_sums = np.sum(large_array, axis=1)    # Sum of each row (vectorized)
            
            return mean_val, std_val, median_val, percentile_val, col_means, row_sums
        
        agg_results, agg_time = self.time_operation(
            "Aggregations (mean, std, median, percentile)",
            aggregation_operations
        )
        
        # 4. Advanced array operations - Still in C
        def advanced_operations():
            """Advanced NumPy operations that stay in C"""
            # WHAT HAPPENS: Complex operations but still vectorized in C
            # - Linear algebra uses BLAS/LAPACK (highly optimized)
            # - FFT uses optimized algorithms (FFTW)
            # - Sorting uses efficient C implementations
            
            # Linear algebra - BLAS/LAPACK
            # large_array is (1000, 100), so we take (100,50) × (50,30) = (100,30)
            A = large_array[:100, :50]    # Shape: (100, 50)
            B = large_array[:50, 50:80]   # Shape: (50, 30) 
            matrix_mult = np.dot(A, B)    # Shape: (100, 30)
            
            # Sorting - optimized C sorting algorithms
            sorted_data = np.sort(float_data[:10000])  # Smaller subset for demo
            
            # Element-wise functions - vectorized
            complex_calc = np.exp(float_data[:1000] / 100) * np.log1p(np.abs(float_data[:1000]))
            
            # Conditional operations - vectorized (avoid sqrt of negative numbers)
            conditional = np.where(float_data > 0, 
                                 np.sqrt(np.abs(float_data)), 
                                 -np.sqrt(np.abs(float_data)))
            
            return matrix_mult, sorted_data, complex_calc, conditional
        
        adv_results, adv_time = self.time_operation(
            "Advanced operations (dot, sort, exp, log, where)",
            advanced_operations
        )
        
        print(f"\n🎯 NO-SERIALIZATION OPERATIONS PERFORMANCE:")
        print(f"   Arithmetic operations:     {arith_time:.6f}s")
        print(f"   Slicing & reshaping:       {slice_time:.6f}s")
        print(f"   Aggregations:              {agg_time:.6f}s")
        print(f"   Advanced operations:       {adv_time:.6f}s")
        print(f"   💡 All operations stay in C - blazing fast!")
        
        return {
            'arithmetic': arith_results,
            'slicing': slice_results,
            'aggregations': agg_results,
            'advanced': adv_results
        }

    def demo_serialization_boundaries(self, arrays):
        """Demonstrate where serialization boundaries occur"""
        print("\n" + "="*50)
        print("⚠️  SERIALIZATION BOUNDARIES - WHERE PYTHON KICKS IN")
        print("="*50)
        
        print("💡 SERIALIZATION HAPPENS WHEN:")
        print("   - Extracting individual scalar values")
        print("   - Converting to Python lists/tuples")
        print("   - Pickling for inter-process communication")
        print("   - String representations and printing")
        print("   - Some NumPy functions that return Python objects")
        
        float_data = arrays['float_data']
        small_array = arrays['small_array']
        
        # 1. Scalar extraction - Forces Python object creation
        def scalar_extraction():
            """Extracting scalars creates Python objects - SERIALIZATION"""
            # WHAT HAPPENS: C array elements → Python objects
            # - Memory copying from C array to Python heap
            # - Type conversion (C double → Python float)
            # - Python object creation with reference counting
            # - This is where NumPy "crosses the boundary" to Python
            
            # These operations force Python object creation:
            first_element = float_data[0]           # C double → Python float
            last_element = float_data[-1]           # Array access + conversion
            middle_element = float_data[len(float_data)//2]  # Index calc + conversion
            
            # Multiple scalar extractions
            scalars = [float_data[i] for i in [10, 100, 1000]]  # List of Python floats
            
            # Array element assignment from Python
            temp_array = float_data.copy()
            temp_array[0] = 99.99  # Python float → C double (reverse serialization)
            
            return first_element, last_element, middle_element, scalars, temp_array[0]
        
        scalar_results, scalar_time = self.time_operation(
            "Scalar extraction (array[0], array[-1]) - SERIALIZATION",
            scalar_extraction
        )
        
        # 2. List/tuple conversion - Mass serialization
        def list_conversion():
            """Converting arrays to Python lists - MASS SERIALIZATION"""
            # WHAT HAPPENS: Every array element → Python object
            # - Iterates through entire C array
            # - Creates Python object for each element
            # - Allocates Python list with object references
            # - Memory usage explodes (Python objects are larger)
            
            # Convert small array to list (manageable size)
            small_list = small_array.tolist()       # NumPy → Python list
            small_tuple = tuple(small_array)        # NumPy → Python tuple
            
            # Convert subset of large array (avoid memory explosion)
            subset_list = float_data[:100].tolist() # 100 elements → Python list
            
            # This would be very expensive for large arrays:
            # large_list = float_data.tolist()  # DON'T DO THIS - 100k Python objects!
            
            return small_list, small_tuple, subset_list
        
        list_results, list_time = self.time_operation(
            "Array to list conversion (.tolist()) - MASS SERIALIZATION",
            list_conversion
        )
        
        # 3. String representation - Complex serialization
        def string_operations():
            """String operations require full serialization"""
            # WHAT HAPPENS: Array → human-readable text
            # - Iterates through array elements
            # - Converts each number to string representation
            # - Formats according to NumPy's display rules
            # - Concatenates into final string (memory intensive)
            
            # These operations serialize the entire array:
            small_str = str(small_array)            # Full array → string
            small_repr = repr(small_array)          # Full array → repr string
            
            # Large array string representation (truncated but still expensive)
            large_str = str(float_data[:10])        # Just first 10 elements
            
            return small_str, small_repr, large_str
        
        str_results, str_time = self.time_operation(
            "String representation (str, repr) - FULL SERIALIZATION",
            string_operations
        )
        
        # 4. Pickling - Serialization for storage/transmission
        def pickling_operations():
            """Pickling serializes arrays for storage or IPC"""
            # WHAT HAPPENS: Array → byte stream
            # - Serializes array metadata (shape, dtype, strides)
            # - Serializes the underlying C data buffer
            # - Creates portable byte representation
            # - Can be transmitted or stored, then deserialized
            
            # Pickle small array
            small_pickled = pickle.dumps(small_array)
            
            # Pickle larger array (more expensive)
            subset_pickled = pickle.dumps(float_data[:1000])
            
            # Unpickling (deserialization)
            small_unpickled = pickle.loads(small_pickled)
            
            return len(small_pickled), len(subset_pickled), small_unpickled
        
        pickle_results, pickle_time = self.time_operation(
            "Pickling operations (serialize/deserialize) - SERIALIZATION",
            pickling_operations
        )
        
        # 5. Memory vs computation analysis
        def memory_analysis():
            """Analyze memory implications of different operations"""
            # WHAT HAPPENS: Different memory patterns
            
            # NO SERIALIZATION: Views share memory
            view = float_data[1000:2000]            # Memory view - shares buffer
            view_size = view.nbytes                 # Same memory, different metadata
            
            # COPY: New memory allocation but still in C
            copy_array = float_data.copy()          # New C buffer allocation
            copy_size = copy_array.nbytes           # Same size, different memory location
            
            # SERIALIZATION: Python objects
            python_list = float_data[:100].tolist() # 100 Python float objects
            python_size = sys.getsizeof(python_list) + sum(sys.getsizeof(x) for x in python_list)
            
            return view_size, copy_size, python_size
        
        memory_results, memory_time = self.time_operation(
            "Memory analysis (views vs copies vs Python objects)",
            memory_analysis
        )
        
        # Show the results
        view_size, copy_size, python_size = memory_results
        
        print(f"\n💾 MEMORY USAGE COMPARISON (for 100 float64 elements):")
        print(f"   NumPy view:        {view_size//100:,} bytes per element")
        print(f"   NumPy copy:        {copy_size//100:,} bytes per element") 
        print(f"   Python objects:    {python_size//100:,} bytes per element")
        if copy_size > 0:
            print(f"   Python overhead:   {(python_size/copy_size - 1)*100:.0f}% more memory!")
        else:
            print(f"   Python overhead:   Cannot calculate (copy_size is 0)")
        
        print(f"\n⚠️  SERIALIZATION BOUNDARIES PERFORMANCE:")
        print(f"   Scalar extraction:     {scalar_time:.6f}s")
        print(f"   List conversion:       {list_time:.6f}s")
        print(f"   String operations:     {str_time:.6f}s")
        print(f"   Pickling operations:   {pickle_time:.6f}s")
        print(f"   Memory analysis:       {memory_time:.6f}s")
        print(f"   💡 These operations cross the C/Python boundary!")
        
        return {
            'scalars': scalar_results,
            'lists': list_results,
            'strings': str_results,
            'pickle': pickle_results,
            'memory': memory_results
        }

    def demo_spark_serialization_comparison(self, arrays):
        """Compare NumPy boundaries with Spark serialization"""
        print("\n" + "="*50)
        print("🔄 SPARK SERIALIZATION VS NUMPY BOUNDARIES")
        print("="*50)
        
        print("💡 COMPARISON OF SERIALIZATION COSTS:")
        print("   - NumPy scalar extraction: Minimal (single value)")
        print("   - NumPy list conversion: Moderate (all elements)")
        print("   - Spark toPandas(): Heavy (inter-process + format conversion)")
        
        float_data = arrays['float_data']
        
        # Create comparable Spark DataFrame
        def create_spark_data():
            # Convert NumPy to Spark (for comparison)
            data_list = [(float(x),) for x in float_data[:1000]]  # Small subset
            return self.spark.createDataFrame(data_list, ['value'])
        
        spark_df, spark_creation_time = self.time_operation(
            "Create Spark DataFrame from NumPy",
            create_spark_data
        )
        
        # NumPy operations for comparison
        def numpy_boundary_operations():
            # Light serialization: few scalars
            scalars = [float_data[i] for i in range(0, 1000, 100)]  # 10 scalars
            
            # Medium serialization: small list
            small_list = float_data[:100].tolist()  # 100 elements
            
            # Heavy serialization: large list
            large_list = float_data[:1000].tolist()  # 1000 elements
            
            return scalars, small_list, large_list
        
        numpy_results, numpy_boundary_time = self.time_operation(
            "NumPy boundary operations (scalars + lists)",
            numpy_boundary_operations
        )
        
        # Spark serialization for comparison
        def spark_serialization():
            # Spark → pandas conversion (heavy serialization)
            pandas_df = spark_df.toPandas()
            
            # pandas → NumPy (light operation)
            numpy_array = pandas_df['value'].values
            
            return pandas_df, numpy_array
        
        spark_results, spark_serialization_time = self.time_operation(
            "Spark → pandas → NumPy conversion",
            spark_serialization
        )
        
        print(f"\n⚖️  SERIALIZATION COST COMPARISON:")
        print(f"   NumPy boundaries (1000 elements):   {numpy_boundary_time:.6f}s")
        print(f"   Spark serialization (1000 elements): {spark_serialization_time:.6f}s")
        print(f"   Spark overhead factor:               {spark_serialization_time/numpy_boundary_time:.1f}x")
        print(f"   💡 Spark serialization is much heavier than NumPy boundaries!")
        
        return {
            'numpy_boundary_time': numpy_boundary_time,
            'spark_serialization_time': spark_serialization_time,
            'overhead_factor': spark_serialization_time/numpy_boundary_time
        }

    def demo_practical_guidelines(self, arrays):
        """Demonstrate practical guidelines for avoiding unnecessary serialization"""
        print("\n" + "="*50)
        print("💡 PRACTICAL GUIDELINES - AVOIDING UNNECESSARY SERIALIZATION")
        print("="*50)
        
        float_data = arrays['float_data']
        
        print("✅ GOOD PRACTICES (Avoid serialization):")
        print("   - Use vectorized operations instead of loops")
        print("   - Extract scalars only when necessary")
        print("   - Use array slicing instead of list conversion")
        print("   - Keep computations in NumPy as long as possible")
        print("   - Use views instead of copies when possible")
        
        # Good vs bad examples
        def good_practices():
            """Examples of avoiding unnecessary serialization"""
            
            # ✅ GOOD: Vectorized operation (stays in C)
            result1 = np.sum(float_data > 0)  # Count positive values - vectorized
            
            # ✅ GOOD: Boolean indexing (creates C array copy)
            positive_values = float_data[float_data > 0]  # Filter in C
            
            # ✅ GOOD: Aggregation on filtered data (stays in C)
            mean_positive = np.mean(positive_values)  # C computation
            
            # ✅ GOOD: Use array slicing for ranges
            subset = float_data[1000:2000]  # Memory view - no copy
            
            return result1, positive_values, mean_positive, subset
        
        good_results, good_time = self.time_operation(
            "Good practices (vectorized, stay in NumPy)",
            good_practices
        )
        
        def bad_practices():
            """Examples that force unnecessary serialization"""
            
            # ❌ BAD: Loop with scalar extraction (use same subset as good method)
            count = 0
            test_data = float_data  # Use full array to match good method
            for i in range(min(10000, len(test_data))):  # Limit for demo
                if test_data[i] > 0:  # Scalar extraction each iteration
                    count += 1
            
            # ❌ BAD: Convert to list for filtering  
            data_list = test_data[:10000].tolist()  # Mass serialization
            positive_list = [x for x in data_list if x > 0]  # Python loop
            
            # ❌ BAD: Convert back to NumPy
            positive_array = np.array(positive_list)  # Rebuild array
            
            return count, positive_list, positive_array
        
        bad_results, bad_time = self.time_operation(
            "Bad practices (loops, lists, conversions)",
            bad_practices
        )
        
        print(f"\n📊 PRACTICE COMPARISON:")
        print(f"   Good practices (vectorized):    {good_time:.6f}s")
        print(f"   Bad practices (serialization):  {bad_time:.6f}s")
        print(f"   Performance difference:         {bad_time/good_time:.1f}x slower")
        print(f"   💡 Vectorized operations are much faster!")
        
        # Memory efficiency comparison
        good_count, good_positive, good_mean, good_subset = good_results
        bad_count, bad_positive_list, bad_positive_array = bad_results
        
        print(f"\n🎯 RESULTS VERIFICATION:")
        print(f"   Good method count: {good_count}")
        print(f"   Bad method count:  {bad_count}")
        print(f"   Results match:     {good_count == bad_count}")
        print(f"   💡 Same results, but vastly different performance!")
        
        return {
            'good_time': good_time,
            'bad_time': bad_time,
            'speedup': bad_time/good_time
        }

    def run_comprehensive_demo(self):
        """Run the complete NumPy serialization nuances demonstration"""
        try:
            # Create test data starting from Spark (realistic scenario)
            arrays, original_spark_df = self.create_test_data()
            
            # Show operations that don't serialize
            no_serial_results = self.demo_no_serialization_operations(arrays)
            
            # Show serialization boundaries
            boundary_results = self.demo_serialization_boundaries(arrays)
            
            # Compare with Spark serialization
            spark_comparison = self.demo_spark_serialization_comparison(arrays)
            
            # Practical guidelines
            practical_results = self.demo_practical_guidelines(arrays)
            
            # Final summary
            self.print_final_summary(no_serial_results, boundary_results, 
                                   spark_comparison, practical_results)
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()

    def print_final_summary(self, no_serial_results, boundary_results, 
                          spark_comparison, practical_results):
        """Print comprehensive summary of serialization nuances"""
        print("\n" + "="*50)
        print("🏆 NUMPY SERIALIZATION NUANCES SUMMARY")
        print("="*50)
        
        print("\n🎯 KEY LEARNINGS:")
        
        print("\n✅ NO SERIALIZATION (Stay in C):")
        print("   • Array arithmetic and math functions")
        print("   • Slicing, reshaping, transposing (views)")
        print("   • Aggregations (sum, mean, std, median)")
        print("   • Boolean indexing and masking")
        print("   • Advanced operations (dot, sort, where)")
        print("   💡 These operations are blazing fast!")
        
        print("\n⚠️  SERIALIZATION OCCURS (C → Python):")
        print("   • Scalar extraction: array[0], array[-1]")
        print("   • List conversion: array.tolist()")
        print("   • String representation: str(array)")
        print("   • Pickling for storage/transmission")
        print("   • Individual element assignment from Python")
        print("   💡 These cross the C/Python boundary!")
        
        print("\n🔄 SERIALIZATION HIERARCHY (lightest → heaviest):")
        print("   1. NumPy scalar extraction     (single element)")
        print("   2. NumPy list conversion       (all elements)")
        print("   3. Spark → pandas conversion   (inter-process + format)")
        print(f"   📊 Spark overhead: {spark_comparison['overhead_factor']:.1f}x vs NumPy boundaries")
        
        print("\n💡 PRACTICAL GUIDELINES:")
        print("   ✅ DO: Use vectorized operations")
        print("   ✅ DO: Keep computations in NumPy")
        print("   ✅ DO: Extract scalars sparingly")
        print("   ✅ DO: Use array slicing over list conversion")
        print("   ❌ AVOID: Python loops over arrays")
        print("   ❌ AVOID: Unnecessary .tolist() conversions")
        print(f"   📊 Performance difference: {practical_results['speedup']:.1f}x")
        
        print("\n🎯 DECISION FRAMEWORK:")
        print("   • Single values needed → Use scalar extraction")
        print("   • Multiple operations → Stay vectorized")
        print("   • Data exchange needed → Consider format carefully")
        print("   • Performance critical → Profile boundary crossings")
        
        print("\n💎 GOLDEN RULE:")
        print("   'Stay in NumPy's C layer as long as possible'")
        print("   'Cross boundaries only when absolutely necessary'")

    def cleanup(self):
        """Clean up resources"""
        print(f"\n🧹 Cleaning up...")
        self.spark.stop()
        print("   ✅ Stopped Spark session")
        print("\n👋 NumPy serialization nuances demo completed!")


def main():
    """Main function to run the NumPy serialization nuances demonstration"""
    print("🚀 Starting NumPy Serialization Nuances Demo...")
    print("📚 Docs index: docs/index.md")
    
    # Check system resources
    memory_gb = psutil.virtual_memory().total / (1024**3)
    print(f"💻 System: {memory_gb:.1f}GB RAM")
    
    # Use smaller dataset for detailed analysis
    rows = 100_000  # Smaller for nuanced analysis
    
    demo = NumPySerializationNuances(rows=rows)
    demo.run_comprehensive_demo()


if __name__ == "__main__":
    if os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys, os as _os
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..'))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/ser_03_numpy_serialization_nuances.md",
            title="Serialization 03: NumPy boundaries and best practices",
            main_callable=main,
        )
    else:
        main()
