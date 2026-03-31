import json
import boto3

iot = boto3.client('iot-data')

def lambda_handler(event, context):
print (event)
  distance = event.get("distance", 999)
  if distance < 100:
    action = "pause"
  elif distance > 120:
    action = "resume"
  else:
    return
    
  payload = {
    "action": action
  }

  iot.publish(
    topic="kids/command",
    qos=0,
    payload=json.dumps(payload)
  )
  return payload