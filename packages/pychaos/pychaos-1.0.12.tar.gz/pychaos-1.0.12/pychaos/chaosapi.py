from pychaos.chaoslib import *
import json


def search(_name,_what,_alive,opts={}):
    """ Search information aboud a !CHAOS node

    Arguments:
        _name : str -- is the substring of what you want search
        _what : str -- one of these: "cu"|"us"|"agent"|"cds"|"webui"|"variable"|"snapshotsof"|"snapshots"|"script"|"zone"|"class" 
        _alive : bool  -- search among alive (true) or all(false)

    Keyword Arguments:
        opts {dict} -- optional parameters (default: {{}})

    Returns:
        dict -- return an array of objects depending on the search
    """    
    opt = {
        "what": _what,
        "alive": _alive
         }
    if isinstance(_name, list): 
        opt["names"]=_name
    else:
        opt['name']=_name
    return mdsBase("search",opt)

def getChannel(_name,channel_id):
    """ Retrive the specified dataset correspoding to a given CU

    Arguments:
        _name (str): devs CU or array of CU
        channel_id (int): channel_id (-1: all,0: output, 1: input, 2:custom,3:system, 4: health, 5 cu alarm, 6 dev alarms,128 status)

    Returns:
        [dict] -- the specified dataset
    """
    if isinstance(_name, list): 
        dev_array=dev_array = ','.join(_name)

    else:
        dev_array=_name


    str_url_cu = "dev=" + dev_array + "&cmd=channel&parm=" + str(channel_id);

    return basicPost("CU",str_url_cu)


def sendCUCmd(_name,cmd,param={}):
    """ Send a command to a specified CU

    Arguments:
        _name : str -- CU unique name
        cmd : str -- command name

    Keyword Arguments:
        param : dict -- Parameters of the command if any (default: {{}})

    Returns:
        dict: -- depending on the command
    """    
    if isinstance(_name, list): 
        dev_array=dev_array = ','.join(_name)

    else:
        dev_array=_name


    str_url_cu = "dev=" + dev_array
    if( isinstance(cmd,dict)):
         str_url_cu += "&cmd="+cmd["cmd"];
         if("mode" in cmd):
            str_url_cu += "&mode="+str(cmd["mode"])
         if("prio" in cmd):
            str_url_cu += "&prio="+str(cmd["prio"]);
         if("sched" in cmd):
            str_url_cu += "&sched="+str(cmd["sched"]);
    else:
        str_url_cu += "&cmd="+cmd;
 

    if(param):
        str_url_cu+= "&parm="+json.dumps(param)
        

    return basicPost("CU",str_url_cu)

def setAttribute(devs,attr,value):
    """ Set an input attribute to the specified value


    Arguments:
        devs : str -- CU name of list of CU names
        attr : str -- name of the input attribute to se
        value : str -- the value of attribute

     
    """    
    parm={}
    parm[attr]=str(value)
    return sendCUCmd(devs,"attr",parm)
       