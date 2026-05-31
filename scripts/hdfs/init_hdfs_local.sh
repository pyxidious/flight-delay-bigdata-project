#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/env/project_env.sh

export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"

mkdir -p "$HADOOP_CONF_DIR"
mkdir -p "$PROJECT_ROOT/hadoop/hdfs/namenode"
mkdir -p "$PROJECT_ROOT/hadoop/hdfs/datanode"
mkdir -p "$PROJECT_ROOT/results/tmp/hadoop"

if [ -f "$HADOOP_HOME/etc/hadoop/log4j.properties" ]; then
    cp "$HADOOP_HOME/etc/hadoop/log4j.properties" "$HADOOP_CONF_DIR/log4j.properties"
fi

cat > "$HADOOP_CONF_DIR/core-site.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>

    <property>
        <name>hadoop.tmp.dir</name>
        <value>$PROJECT_ROOT/results/tmp/hadoop</value>
    </property>
</configuration>
EOF

cat > "$HADOOP_CONF_DIR/hdfs-site.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>

    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file://$PROJECT_ROOT/hadoop/hdfs/namenode</value>
    </property>

    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file://$PROJECT_ROOT/hadoop/hdfs/datanode</value>
    </property>
</configuration>
EOF

cat > "$HADOOP_CONF_DIR/mapred-site.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>local</value>
    </property>
</configuration>
EOF

cat > "$HADOOP_CONF_DIR/yarn-site.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
</configuration>
EOF

echo "HDFS local configuration generated."
echo "HADOOP_CONF_DIR=$HADOOP_CONF_DIR"
echo
echo "Formatting NameNode if needed..."

if [ ! -d "$PROJECT_ROOT/hadoop/hdfs/namenode/current" ]; then
    hdfs namenode -format -force -nonInteractive
else
    echo "NameNode already formatted."
fi

echo
echo "HDFS local initialization completed."
