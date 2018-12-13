import org.apache.spark.SparkContext
import org.apache.spark.mllib.clustering.{LDA, LDAModel, DistributedLDAModel, LocalLDAModel}

object Main {
  val msg = "Hello, world!"

  def main(args: Array[String]): Unit = {
    println(msg)
  }
}