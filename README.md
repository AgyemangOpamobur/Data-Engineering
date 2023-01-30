# Real-Time-Environmental-Sensor-Readings-with-Pyspark-Kafka-and-PostgreSQL
![sensor-pipeline](sensor-pipeline.jpg)

## Deployment Instructions for a Standalone Deployment on a Local Machine in a Docker Environment

#### Before you deploy, please ensure you have a stable internet connection to build and download maven packages for the deployment.
#### Also, if you have a local instance of Zookeeper running on port 2181, please consider shutting it down first.
For Linux users, you can do that by running the command systemctl stop <nameofzookeeperinstant>. example
```
systemctl stop zookeeper
```
For Windows users, you need to run the zookeeper-server-stop.bat script.

#### You may now deploy using the following commands:
```
git clone https://github.com/AgyemangOpamobur/Real-Time-Environmental-Sensor-Readings-With-Kafka-Pyspark-and-Postgresql.git 
cd Real-Time-Environmental-Sensor-Readings-With-Kafka-Pyspark-and-Postgresql/producer
```
Unzip iot_telemetry_data.zip
```
unzip iot_telemetry_data.zip -d .
```
Change directory back to the base of the repository and edit the .env_config to provide the environment variable you wish to deploy your application with.
```
cd ..
vi .env_config
``` 
```text
DATABASE_HOSTNAME=
DATABASE_PORT=
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_USERNAME=
```
Finally, at the base of the repository, deploy the application by running 

```
docker-compose --env-file .env_config up 
```
or for detach 
```
docker-compose --env-file .env_config up -d
```
To check how your data is published to the Kafka broker open a new terminal and run:
```
docker exec --interactive --tty <kafka container name> kafka-console-consumer.sh --topic Environment-Readings --bootstrap-server kafka:9092
```
```text
{"id": "1", "ts": "1595162570", "device": "00:0f:00:70:91:0a", "co": "0", "humidity": "57", "light": "True", "lpg": "0", "motion": "False", "smoke": "0", "temp": "27"}
{"id": "2", "ts": "1594682448", "device": "b8:27:eb:bf:9d:51", "co": "0", "humidity": "72", "light": "False", "lpg": "0", "motion": "False", "smoke": "0", "temp": "20"}
{"id": "3", "ts": "1595013088", "device": "00:0f:00:70:91:0a", "co": "0", "humidity": "62", "light": "False", "lpg": "0", "motion": "False", "smoke": "0", "temp": "22"}
{"id": "4", "ts": "1594850360", "device": "b8:27:eb:bf:9d:51", "co": "0", "humidity": "55", "light": "False", "lpg": "0", "motion": "False", "smoke": "0", "temp": "22"}
{"id": "5", "ts": "1595040990", "device": "1c:bf:ce:15:ec:4d", "co": "0", "humidity": "79", "light": "True", "lpg": "0", "motion": "False", "smoke": "0", "temp": "22"}
{"id": "6", "ts": "1594836724", "device": "b8:27:eb:bf:9d:51", "co": "0", "humidity": "61", "light": "False", "lpg": "0", "motion": "False", "smoke": "0", "temp": "23"}
{"id": "7", "ts": "1594751409", "device": "00:0f:00:70:91:0a", "co": "0", "humidity": "62", "light": "False", "lpg": "0", "motion": "False", "smoke": "0", "temp": "23"}
```
Docker exec into the PostgreSQL database container and run SQL queries  in new terminal 
```
docker exec -ti  <PostgreSQL container name> psql -U <PostgreSQL user> 
```
```text
-------------------------------------------
Batch: 2
-------------------------------------------
+----+-------------------+-------------------+-----------------+----------+---------+
|  Id|       window_start|         window_end|        device_id|Fahrenheit| humidity|
+----+-------------------+-------------------+-----------------+----------+---------+
|2352|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 77.000000|41.000000|
|2353|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 75.200000|43.000000|
|2354|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 75.200000|51.000000|
|2355|2023-01-30 07:26:00|2023-01-30 07:27:00|00:0f:00:70:91:0a| 75.200000|60.000000|
|2356|2023-01-30 07:26:00|2023-01-30 07:27:00|1c:bf:ce:15:ec:4d| 69.800000|64.000000|
|2357|2023-01-30 07:26:00|2023-01-30 07:27:00|00:0f:00:70:91:0a| 71.600000|52.000000|
|2358|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 69.800000|68.000000|
|2359|2023-01-30 07:26:00|2023-01-30 07:27:00|1c:bf:ce:15:ec:4d| 80.600000|60.000000|
|2360|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 73.400000|50.000000|
|2361|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 73.400000|49.000000|
|2362|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 69.800000|54.000000|
|2363|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 68.000000|77.000000|
|2364|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 68.000000|58.000000|
|2365|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 71.600000|62.000000|
|2366|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 71.600000|53.000000|
|2367|2023-01-30 07:26:00|2023-01-30 07:27:00|00:0f:00:70:91:0a| 71.600000|70.000000|
|2368|2023-01-30 07:26:00|2023-01-30 07:27:00|00:0f:00:70:91:0a| 78.800000|55.000000|
|2369|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 69.800000|50.000000|
|2370|2023-01-30 07:26:00|2023-01-30 07:27:00|b8:27:eb:bf:9d:51| 68.000000|64.000000|
|2371|2023-01-30 07:26:00|2023-01-30 07:27:00|00:0f:00:70:91:0a| 78.800000|54.000000|
+----+-------------------+-------------------+-----------------+----------+---------+
only showing top 20 rows

```

