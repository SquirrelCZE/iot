from envirophat import *
import paho.mqtt.publish as publish

spot_tag = "BCN1";

prefix = "sensors/" + spot_tag + "/";

msgs = [
    (prefix + "temp", weather.temperature(), 0, False),
    (prefix + "light", light.light(), 0, False),
    (prefix + "pressure", weather.pressure(), 0, False),
]

publish.multiple(msgs, "192.168.0.38", client_id="grouchy")

