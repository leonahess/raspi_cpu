import subprocess
from app import client
import config
import datetime
import time


class RaspiTemp:

    def __init__(self):
        while True:

            self.write(self.read())


            time.sleep(10)

    def read(self):
        jsons = []
        result = subprocess.run("cat /sys/class/thermal/thermal_zone0/temp", shell=True, capture_output=True)
        temp_cpu_raw = int(result.stdout)
        temp_cpu = temp_cpu_raw / 1000

        freq0_cpu = int(subprocess.run("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", shell=True, capture_output=True).stdout)
        freq1_cpu = int(subprocess.run("cat /sys/devices/system/cpu/cpu1/cpufreq/scaling_cur_freq", shell=True, capture_output=True).stdout)
        freq2_cpu = int(subprocess.run("cat /sys/devices/system/cpu/cpu2/cpufreq/scaling_cur_freq", shell=True, capture_output=True).stdout)
        freq3_cpu = int(subprocess.run("cat /sys/devices/system/cpu/cpu3/cpufreq/scaling_cur_freq", shell=True, capture_output=True).stdout)

        utcnow = datetime.datetime.utcnow()

        jsons.append({
            "measurement": "cpu",
            "tags": {
                "host": config.hostname,
                "cpu": "cpu-total"
            },
            "fields": {
                "temp": temp_cpu
            },
            "time": utcnow
        })

        jsons.append({
            "measurement": "cpu",
            "tags": {
                "host": config.hostname,
                "cpu": "cpu0"
            },
            "fields": {
                "freq": freq0_cpu
            },
            "time": utcnow
        })

        jsons.append({
            "measurement": "cpu",
            "tags": {
                "host": config.hostname,
                "cpu": "cpu1"
            },
            "fields": {
                "freq": freq1_cpu
            },
            "time": utcnow
        })

        jsons.append({
            "measurement": "cpu",
            "tags": {
                "host": config.hostname,
                "cpu": "cpu2"
            },
            "fields": {
                "freq": freq2_cpu
            },
            "time": utcnow
        })

        jsons.append({
            "measurement": "cpu",
            "tags": {
                "host": config.hostname,
                "cpu": "cpu3"
            },
            "fields": {
                "freq": freq3_cpu
            },
            "time": utcnow
        })

        return jsons

    def write(self, jsons):

        try:
            client.write_points(jsons, protocol="json")
        except Exception as e:
            print("Write exception: {}".format(e))



