from influxdb import InfluxDBClient
import config

client = InfluxDBClient(host=config.influx_ip, port=config.influx_port, database=config.influx_database)

print("< connected to influx!")
print("> checking if database 'telegraf' exists ...")

database_list = client.get_list_database()
smarthome_exists = False

for s in range(0, len(database_list)):
    if database_list[s]['name'] == config.influx_database:
        smarthome_exists = True

        print("< database 'telegraf' exists")

if not smarthome_exists:

    print("< database 'telegraf' does not exist!")
    print("> creating database 'telegraf' ...")

    client.create_database('telegraf')

    print("< created database 'telegraf'!")
