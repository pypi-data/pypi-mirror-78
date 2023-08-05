#!python

# import pychaos
import sys
import time
import os
import bson
from kafka import KafkaConsumer


if len(sys.argv)<3:
    print("You must specify a <broker:port [9092]> <NodeUID> [groupid]");
    sys.exit(1);

gid="pyexporter"
if len(sys.argv)>3:
    gid=sys.argv[4]
topic=sys.argv[2].replace('/','.')
topic=topic+"_o"
print("subscribing to:"+topic)

consumer = KafkaConsumer(topic, bootstrap_servers=sys.argv[1], group_id=gid)
for msg in consumer:
            decoded = bson.loads(msg.value)
            if "FRAMEBUFFER" in decoded:
                ''' is an image
                '''
                bin=decoded["FRAMEBUFFER"]
                name=decoded['ndk_uid']
                ext=decoded["FMT"]
                seq=decoded['dpck_seq_id']
                ts=decoded['dpck_ats']
                runid=decoded['cudk_run_id']
                dd=time.strftime("%m-%d-%Y", time.localtime(ts/1000))
                name=name+"/"+dd+"/"   
                if not os.path.exists(name):
                    try:
                        os.makedirs(name)
                    except OSError:
                        print ("Creation of the directory %s failed" % name)
                    else:
                        print ("Successfully created the directory %s " % name)

                hr=time.strftime("%H:%M:%S%Z", time.localtime(ts/1000))

                fname=name+str(runid)+"_"+str(seq)+"_"+hr+ext
                f = open(fname, 'w+b')
                f.write(bin)
                f.close
                print("created:"+fname)
            else:    
                print(decoded)
sys.exit(0);

