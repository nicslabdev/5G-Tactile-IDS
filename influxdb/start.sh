export INFLUXDB_TOKEN=sdfbl9YowtCfERWHmjjjq-GXfFoFgZJpZoCe4eMfPmufSXMahDQ2Dvj-yKns6imYFWSvuzy9zmylGG1pyyc6ZQ==

docker run \
    --network host \
    -v "/home/nics/Repos/5G-Tactile-IDS/influxdb/data:/var/lib/influxdb2" \
    -v "/home/nics/Repos/5G-Tactile-IDS/influxdb/config:/etc/influxdb2" \
    influxdb:2
