#!/bin/bash

# по умолчанию:
DATANODES_COUNT=1  
OPTIMIZED=False 


while [[ $# -gt 0 ]] # условие цикла (пока есть параметры, больше нуля — $# -gt 0), двойные скобки лучше поддерживают работу с переменными и операторами
do
    case "$1" in 
        --optimized) 
            OPTIMIZED="$2"
            shift 2 
            ;; 
        --datanodes) 
            DATANODES_COUNT="$2" 
            shift 2
            ;; 
        *) 
            echo "Неизвестный параметр: $1" 
            exit 1
            ;;
    esac
done
echo "Количество DataNode: $DATANODES_COUNT, оптимизированный запуск Spark: $OPTIMIZED."


# определяем со сколькими DataNode запускать контейнер
if [[ $DATANODES_COUNT -eq 1 ]]
then
    docker-compose -f docker-compose.yml up -d
elif [[ $DATANODES_COUNT -eq 3 ]]
then
    docker-compose -f docker-compose-3.yml up -d
else
    echo "Переданное количество DataNode=$DATANODES_COUNT не поддерживается!"
    exit 1
fi


# отправляем данные в Hadoop
docker cp ./data/diabetes_012_health_indicators.csv namenode:/
docker cp ./scripts/HDFS.sh namenode:/
docker exec -it namenode bash HDFS.sh


# отправляем приложение в контейнер со Spark и запускаем его
docker cp ./scripts/spark_app.py spark-master:/
docker cp ./scripts/Spark.sh spark-master:/
docker exec -it spark-master bash Spark.sh ${OPTIMIZED}
docker cp spark-master:/log.txt ./logs/log_DataNodes_${DATANODES_COUNT}_opt_${OPTIMIZED}.txt


# выключаем запущенные контейнеры
if [[ $DATANODES_COUNT -eq 1 ]]
then
    docker-compose -f docker-compose.yml down
else
    docker-compose -f docker-compose-3.yml down
fi