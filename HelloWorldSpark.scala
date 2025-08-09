import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.{StructType, StructField, StringType, IntegerType}
import org.apache.spark.sql.Row
import org.apache.spark.sql.functions.avg

/**
 * Hello World example using Apache Spark (Scala)
 * This application demonstrates basic Spark operations including RDD creation, transformations, and actions.
 */
object HelloWorldSpark {
  
  def main(args: Array[String]): Unit = {
    // Initialize Spark Session
    val spark = SparkSession.builder()
      .appName("HelloWorldSpark")
      .master("local[*]")
      .getOrCreate()
    
    // Import implicits for DataFrame operations
    import spark.implicits._
    
    println("=" * 50)
    println("Hello World with Apache Spark!")
    println("=" * 50)
    
    // Example 1: Basic RDD operations
    println("\n1. Basic RDD Operations:")
    val data = Seq(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    val rdd = spark.sparkContext.parallelize(data)
    
    // Transformations
    val squaredRdd = rdd.map(x => x * x)
    val evenRdd = rdd.filter(_ % 2 == 0)
    
    // Actions
    println(s"Original data: ${rdd.collect().mkString(", ")}")
    println(s"Squared numbers: ${squaredRdd.collect().mkString(", ")}")
    println(s"Even numbers: ${evenRdd.collect().mkString(", ")}")
    println(s"Sum of all numbers: ${rdd.sum()}")
    println(s"Count: ${rdd.count()}")
    
    // Example 2: Working with text data
    println("\n2. Text Processing:")
    val textData = Seq("Hello World", "Apache Spark", "Big Data Processing", "Distributed Computing")
    val textRdd = spark.sparkContext.parallelize(textData)
    
    // Word count example
    val wordsRdd = textRdd.flatMap(_.split(" "))
    val wordPairsRdd = wordsRdd.map(word => (word.toLowerCase, 1))
    val wordCounts = wordPairsRdd.reduceByKey(_ + _)
    
    println(s"Text data: ${textData.mkString(", ")}")
    println(s"Word counts: ${wordCounts.collect().map(p => s"${p._1}: ${p._2}").mkString(", ")}")
    
    // Example 3: Using DataFrame API (Spark SQL)
    println("\n3. DataFrame Operations:")
    
    // Create a DataFrame
    val peopleData = Seq(
      ("Alice", 25, "New York"),
      ("Bob", 30, "San Francisco"),
      ("Charlie", 35, "Seattle"),
      ("Diana", 28, "Boston")
    )
    
    val df = peopleData.toDF("name", "age", "city")
    
    println("People DataFrame:")
    df.show()
    
    println("People older than 27:")
    df.filter($"age" > 27).show()
    
    println("Average age:")
    df.agg(avg($"age").alias("average_age")).show()
    
    // Example 4: SQL queries
    println("\n4. SQL Queries:")
    df.createOrReplaceTempView("people")
    
    val result = spark.sql("SELECT city, COUNT(*) as count FROM people GROUP BY city ORDER BY count DESC")
    println("People count by city:")
    result.show()
    
    // Example 5: Functional programming style operations
    println("\n5. Functional Programming Style:")
    val numbers = (1 to 20).toList
    val numbersRdd = spark.sparkContext.parallelize(numbers)
    
    val processedData = numbersRdd
      .filter(_ % 2 == 0)  // Keep only even numbers
      .map(x => x * x)     // Square them
      .filter(_ > 50)      // Keep only those greater than 50
      .collect()
    
    println(s"Original numbers: ${numbers.mkString(", ")}")
    println(s"Even numbers squared > 50: ${processedData.mkString(", ")}")
    
    println("\n" + "=" * 50)
    println("Spark Hello World completed successfully!")
    println(s"Spark Version: ${spark.version}")
    println("Spark UI available at: http://localhost:4040")
    println("=" * 50)
    
    // Stop the Spark session
    spark.stop()
  }
}
