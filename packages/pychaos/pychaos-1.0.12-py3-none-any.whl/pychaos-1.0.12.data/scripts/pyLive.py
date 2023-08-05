#!python

import pychaos
import sys


if len(sys.argv)<2:
    print("You must specify a <server:port>");
    sys.exit(1);
else:
    pychaos.setOptions({"uri":sys.argv[1]})
lst=pychaos.search("","cu",True)
print("list of  Alive CU:")
print(lst)

print("channel of:"+lst[0])
lst=pychaos.getChannel(lst[0],-1);
print(lst[0])


'''
cnt=0;

QUESTA DA ERRORE ULTIMA ITERAZIONE?
dnames = ['output','input','custom','system','health','devalarm','cualarm']

dnames = ['output']
for dataset in dnames :
    data=pyChaos.GetJsonDataset(sys.argv[1],cnt);
    cnt+=1
    print data;
'''
sys.exit(0);

