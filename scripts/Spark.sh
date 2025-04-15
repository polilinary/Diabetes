#!/bin/bash

# Установка системных зависимостей
apk add --update make automake gcc g++ python3-dev linux-headers libstdc++ openblas-dev

# Установка Python-пакетов
pip install --upgrade pip
pip install numpy psutil lightgbm lightgbm-spark

# 20 запусков Spark-приложения
for ((i=1; i<=20; i++)); do
    /spark/bin/spark-submit /spark_app.py "$1"
done

exit 0