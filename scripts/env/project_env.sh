#!/usr/bin/env bash

# Project-specific environment configuration.
# This file is meant to be sourced before running Spark, Hadoop or Hive commands.

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# These paths will be completed after downloading and extracting the tools.
export BIGDATA_TOOLS_HOME="$HOME/bigdata-tools"

export SPARK_HOME="$BIGDATA_TOOLS_HOME/spark-3.5.3-bin-hadoop3"
export HADOOP_HOME="$BIGDATA_TOOLS_HOME/hadoop-3.3.6"
export HIVE_HOME="$BIGDATA_TOOLS_HOME/apache-hive-4.0.1-bin"

export PATH="$JAVA_HOME/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HIVE_HOME/bin:$PATH"
