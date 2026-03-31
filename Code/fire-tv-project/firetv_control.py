import paho.mqtt.client as mqtt
import ssl
import subprocess
import json

ENDPOINT = "IOT CORE ENDPOINT"
TOPIC = "kids/command"
FIRE_TV_IP = "FIRE-TV STATIC IP"

ROOT_CA = "certs/rootCA.pem"
CERT = "certs/cert.pem.crt"
KEY = "certs/private.pem.key"

def run(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
    except Exception as e:
        print("Error:", e)

def connect_adb():
    print("Connecting to Fire TV...")
    run(f"adb connect {FIRE_TV_IP}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("Received:", data)
        connect_adb()
        if data["action"] == "pause":
            run("adb shell input keyevent 85")
        elif data["action"] == "resume":
            run("adb shell input keyevent 126")
    except Exception as e:
        print("Error processing message:", e)

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT:", rc)
    client.subscribe(TOPIC)

def on_disconnect(client, userdata, rc):
    print("Disconnected. Reconnecting...")
    client.reconnect()

client = mqtt.Client()

client.tls_set(
    ca_certs=ROOT_CA,
    certfile=CERT,
    keyfile=KEY,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

print("Connecting to AWS IoT...")
client.connect(ENDPOINT, 8883)

client.loop_forever()