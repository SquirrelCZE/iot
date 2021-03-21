import paho.mqtt.client as mqtt
from conn import conn

conn.autocommit = True


def on_connect(client, userdata, flags, rc):
    print("Connected: " + str(rc))

    client.subscribe("sensors/+/+")


def on_message(client, userdata, msg):

    topc = msg.topic.split("/")
    if topc[0] != "sensors":
        return
    _, spot, vtype = topc

    ## SQL injection much
    with conn.cursor() as cur:
        sql = "INSERT INTO {}(value, spot_tag) VALUES(%s,%s)".format(vtype)
        cur.execute(sql, (float(msg.payload), spot))
        conn.commit()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

while True:
    client.loop()
