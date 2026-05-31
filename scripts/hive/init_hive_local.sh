#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/env/project_env.sh

export HIVE_HOME="$HOME/bigdata-tools/apache-hive-4.0.1-bin"
export HIVE_CONF_DIR="$PROJECT_ROOT/hive/conf"

mkdir -p "$HIVE_CONF_DIR"
mkdir -p "$PROJECT_ROOT/hive"
mkdir -p "$PROJECT_ROOT/hive/warehouse"
mkdir -p "$PROJECT_ROOT/results/tmp/hive"

cat > "$HIVE_CONF_DIR/hive-site.xml" <<EOF
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<configuration>
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:derby:;databaseName=$PROJECT_ROOT/hive/metastore_db;create=true</value>
  </property>

  <property>
    <name>hive.metastore.warehouse.dir</name>
    <value>file://$PROJECT_ROOT/hive/warehouse</value>
  </property>

  <property>
    <name>hive.exec.scratchdir</name>
    <value>$PROJECT_ROOT/results/tmp/hive</value>
  </property>

  <property>
    <name>hive.exec.local.scratchdir</name>
    <value>$PROJECT_ROOT/results/tmp/hive</value>
  </property>

  <property>
    <name>hive.downloaded.resources.dir</name>
    <value>$PROJECT_ROOT/results/tmp/hive/resources</value>
  </property>

  <property>
    <name>hive.server2.thrift.bind.host</name>
    <value>localhost</value>
  </property>

  <property>
    <name>hive.server2.thrift.port</name>
    <value>10000</value>
  </property>

  <property>
    <name>hive.server2.authentication</name>
    <value>NONE</value>
  </property>

  <property>
    <name>hive.server2.enable.doAs</name>
    <value>false</value>
  </property>

  <property>
    <name>hive.query.results.cache.enabled</name>
    <value>false</value>
  </property>
</configuration>
EOF

if [ -d "$PROJECT_ROOT/hive/metastore_db" ] && [ -z "$(ls -A "$PROJECT_ROOT/hive/metastore_db" 2>/dev/null)" ]; then
    echo "Removing empty Hive metastore directory so Derby can initialize it..."
    rmdir "$PROJECT_ROOT/hive/metastore_db"
fi

if [ ! -d "$PROJECT_ROOT/hive/metastore_db" ]; then
    echo "Initializing Hive metastore schema..."
    schematool -dbType derby -initSchema
else
    echo "Hive metastore directory already exists."
fi

echo
echo "Hive local configuration completed."
echo "HIVE_CONF_DIR=$HIVE_CONF_DIR"
