#!python

# import pychaos
import sys
import time
import os
import bson
import json
from kafka import KafkaProducer


if len(sys.argv)<4:
    print("You must specify a <broker:port [9092]> <NodeUID> <cmdname> [JSON VALUE]");
    sys.exit(1);

topic=sys.argv[2].replace('/','.')
topic=topic+"_cmd"
print("sending to:"+sys.argv[1]+" topic:"+topic)
cmd={}


producer = KafkaProducer(bootstrap_servers=sys.argv[1],acks='all',batch_size=0)

if producer.bootstrap_connected():
    print("Connected")
else:
    print("cannot connect to:"+sys.argv[1])
    sys.exit(1)

if len(sys.argv)==5:
    cmd=json.loads(sys.argv[4])

if 'bc_alias' not in cmd.keys():
    cmd['bc_alias'] = sys.argv[3]
        
print("command:",cmd)

encoded=bson.dumps(cmd)
producer.send(topic,encoded)
#producer.send(topic,b'ciao')
#producer.flush()

future = producer.send(topic,encoded)
result=future.get(timeout=60)

if result:
    print("sent ok")
else:
    print("## error sending "+cmd )

sys.exit(0)
