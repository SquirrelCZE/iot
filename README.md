
# IoT

This si my simple homegrown IoT system as "weekend project".

The idea is to use postgresql database (initialized by dump.sql) to store data from sensors.
mosquitto to handle transporting data from sensors
mqtt\_daemon.py to move data from mqtt into the database
plot.py to plot the various data pin therminal as TUI

Among sensors is rpi zero with envirohate and script sensors/envirohat.py collectin data in cronjob
