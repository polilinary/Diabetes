# Diabetes
Big Data

# Анализ медицинских анализов на диабет.

## Описание проекта
Данный проект представляет собой систему, которая использует медицинские данные для предсказания возможности развития диабета.


## Как запустить проект

Нужно запустить 4 вариации приложений (с 1 нодой без оптимизации и с ней и с 3 нодами без оптимизации и с ней)
   ```bash
   bash run.sh --datanodes 1 --optimized False
   ```
   ```bash
   bash run.sh --datanodes 1 --optimized True
   ```
   ```bash
   bash run.sh --datanodes 3 --optimized False
   ```
   ```bash
   bash run.sh --datanodes 3 --optimized True
   ```
   
### Результаты  

  Данные о затраченном времени и памяти сохранятся в log файлы, где их можно посмотреть, визуализацию результатов можно посмотреть в папке results imgs/


   
### Дополнительно

Если вам нужно ознакомиться с предварительной обработкой данных и подбором гиперпараметров модели, вы можете ноутбук EDA + models + visualisation с необходимыми процессами.

## Структура репозитория  
Diabetes/  
├── data/                  # Исходные данные  
│   └── diabetes_012_health_indicators.csv  # Датасет  
│  
├── logs/                  # Логи Spark (создаются при запуске)
│   ├── log_DataNodes_1_opt_False.txt
│   ├── log_DataNodes_1_opt_True.txt
│   ├── log_DataNodes_3_opt_False.txt
│   └── log_DataNodes_3_opt_True.txt
│
├── results imgs/         # р=визуализация результатов  
│  
├── scripts/               # Скрипты для обработки и запуска  
│   ├── HDFS.sh           # Загрузка данных в HDFS  
│   ├── Spark.sh          # Запуск Spark-приложения  
│   └── spark_app.py      # Код Spark-приложения              
│
│── docker-compose.yml          # Композ для 1 DataNode  
│── docker-compose-3.yml        # Композ для 3 DataNode  
├── EDA+models+visual.ipynb     # БЛОКНОТ
├── run.sh                      # bash скрипт для быстрого запуска тест-кейсов
├── hadoop.env                  # файл с переменными окружения для контейнеров
│  
└── README.md             # Описание проекта  

