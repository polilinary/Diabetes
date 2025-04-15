#!/bin/bash

hdfs dfs -mkdir /data/
hdfs dfs -D dfs.block.size=32M -put /diabetes_012_health_indicators.csv /data/
hdfs dfsadmin -setSpaceQuota 4g 
exit
