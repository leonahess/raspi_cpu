from influxdb import InfluxDBClient
import config

client = InfluxDBClient(host=config.influx_ip, port=config.influx_port, database=config.influx_database)

print("< connected to influx!")
print("> checking if database 'telegraf' exists ...")

database_list = client.get_list_database()
smarthome_exists = False
retention_exits = False

for s in range(0, len(database_list)):
    if database_list[s]['name'] == 'telegraf':
        smarthome_exists = True
        print("< database 'telegraf' exists")


if not smarthome_exists:

    print("< database 'smarthome' does not exist!")
    print("> creating database 'telegraf' ...")

    client.create_database('telegraf')

    print("< created database 'telegraf'!")

retention_list = client.get_list_retention_policies("telegraf")
database_list = client.get_list_database()

print("> checking retention policy")
for s in range(0, len(database_list)):
    if database_list[s]['name'] == 'telegraf':
        for rp in range(0, len(retention_list)):
            if retention_list[rp]['name'] == config.influx_retention_policy:
                print("< correct retention policy exists")
                retention_exits = True


if not retention_exits:
    print("< correct retention policy does not exists")
    print("> creating correct retention policy")

    client.create_retention_policy(config.influx_retention_policy, config.influx_retention_policy, 1,
                                   database="telegraf")

    print("< created correct retention policy")
