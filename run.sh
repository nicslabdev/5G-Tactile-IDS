export INFLUXDB_TOKEN=sdfbl9YowtCfERWHmjjjq-GXfFoFgZJpZoCe4eMfPmufSXMahDQ2Dvj-yKns6imYFWSvuzy9zmylGG1pyyc6ZQ==

#start influxdb
docker run \
    -d \
    --network host \
    -v "/home/nics/Repos/5G-Tactile-IDS/influxdb/data:/var/lib/influxdb2" \
    -v "/home/nics/Repos/5G-Tactile-IDS/influxdb/config:/etc/influxdb2" \
    influxdb:2

# start grafana
docker run -d --network host --name=grafana \
  --volume grafana-storage:/var/lib/grafana \
  grafana/grafana-enterprise

# start ids
# docker build -t ids-main .
docker run --network=host ids-main


