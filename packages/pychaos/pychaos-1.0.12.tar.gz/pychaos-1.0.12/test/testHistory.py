import pyChaos
import sys
import datetime
import json


if len(sys.argv)<2:
    print("You must specify a valid device");
    sys.exit(1);
cnt=0;
end=TimestampMillisec64();
start=end-5000;
print "Query ",sys.argv[1]," from:",start," end:",end;
data=pyChaos.QueryDataset(sys.argv[1],start,end,0,0,100);

decoded=json.loads(data);
print "seqid:",decoded["seqid"]," runid:",decoded["runid"], "len:", len(decoded["data"]);
if(len(decoded["data"])>1) :
    print "first elem:",decoded["data"][0];
    
while len(decoded["data"])>=100 :
    data=pyChaos.QueryDataset(sys.argv[1],start,end,decoded["seqid"],decoded["runid"],100);
    decoded=json.loads(data);
    print cnt,"] seqid:",decoded["seqid"]," runid:",decoded["runid"], "len:", len(decoded["data"]);
    cnt+=1;



