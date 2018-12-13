lazy val root = project
	.in(file("."))
	.settings(
		scalaVersion := "2.10.5",
		name := "Spark notebook",
		libraryDependencies ++= Seq(
			"org.apache.spark" %% "spark-core" % "1.5.0",
			"org.apache.spark" %% "spark-mllib" % "1.5.0"
		)
	)
