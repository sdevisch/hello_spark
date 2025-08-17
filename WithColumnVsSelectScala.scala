import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._

object WithColumnVsSelectScala {
  private def generateDf(spark: SparkSession, numRows: Long): DataFrame = {
    import spark.implicits._
    spark.range(numRows)
      .select(
        col("id"),
        (col("id") % 100).as("a"),
        (col("id") % 50).as("b")
      )
  }

  private def withColumnChain(df: DataFrame): DataFrame = {
    df
      .withColumn("c", col("a") * 2 + 1)
      .withColumn("d", col("b") * col("c"))
      .withColumn("e", when(col("d") % 3 === 0, col("d") + 7).otherwise(col("d") - 7))
      .withColumn("f", col("e") * 3 + col("a"))
      .withColumn("g", col("f") - col("b"))
      .withColumn("h", col("g") * 2)
      .withColumn("i", col("h") + lit(42))
      .withColumn("j", col("i") % 97)
      .select("id", "a", "b", "c", "d", "e", "f", "g", "h", "j")
  }

  private def selectCombined(df: DataFrame): DataFrame = {
    val c = (col("a") * 2 + 1).as("c")
    val dExpr = (col("b") * (col("a") * 2 + 1))
    val d = dExpr.as("d")
    val e = when(dExpr % 3 === 0, dExpr + 7).otherwise(dExpr - 7).as("e")
    val f = (col("e") * 3 + col("a")).as("f")
    val g = (col("f") - col("b")).as("g")
    val h = (col("g") * 2).as("h")
    val j = ((col("h") + lit(42)) % 97).as("j")
    df.select(col("id"), col("a"), col("b"), c, d, e, f, g, h, j)
  }

  private def timeIt[T](label: String)(block: => T): (T, Double) = {
    val start = System.nanoTime()
    val result = block
    val end = System.nanoTime()
    val seconds = (end - start) / 1e9
    println(f"$label%s | time=${seconds}%.2fs")
    (result, seconds)
  }

  private def parseSizesArg(args: Array[String], fast: Boolean): Seq[Long] = {
    val default = if (fast) Seq(100000L, 300000L) else Seq(500000L, 1000000L, 2000000L)
    val sizesArg = args.sliding(2, 1).find(a => a.headOption.contains("--sizes")).flatMap(_.lift(1))
    sizesArg match {
      case Some(raw) =>
        raw.split(",").toSeq.flatMap { t =>
          val s = t.trim.toLowerCase
          if (s.isEmpty) None
          else if (s.endsWith("k")) Some((s.dropRight(1).toDouble * 1e3).toLong)
          else if (s.endsWith("m")) Some((s.dropRight(1).toDouble * 1e6).toLong)
          else Some(s.toDouble.toLong)
        }
      case None => default
    }
  }

  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("WithColumnVsSelectScala")
      .master("local[*]")
      .config("spark.sql.adaptive.enabled", "true")
      .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    val fast = sys.env.getOrElse("FAST", "0") == "1"
    val sizes = parseSizesArg(args, fast)

    println("\n=== Scala: withColumn vs select (Spark) ===")
    println(s"Spark version: ${spark.version}")
    println(s"Row sizes: ${sizes.mkString(", ")}")

    sizes.foreach { rows =>
      println(f"\n--- Running Scala scenarios for rows=$rows%,d ---")
      val base = generateDf(spark, rows)

      val (_, t1) = timeIt("withColumn_chain -> count") {
        withColumnChain(base).count()
      }
      val (_, t2) = timeIt("select_combined -> count") {
        selectCombined(base).count()
      }
      println(f"Summary | rows=$rows%,d | withColumn_chain=${t1}%.2fs | select_combined=${t2}%.2fs")
    }

    spark.stop()
  }
}


