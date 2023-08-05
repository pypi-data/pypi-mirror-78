import requests
import json

options = {
    "uri":"localhost:8081",
    "timeout":5000,
}
def setOptions(opt):
    global options
    options = opt

def timestampMillisec64():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


class ChaosException(Exception):
    """ Chaos Error/Exception raised for rest exception.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

def basicPost(func,params):
    """ Basic post for chaos rest calls
    Args:
        func: string that defines the target function (CU or MDS (administration))
        params: dict with parameters
    
    Raises:
        ChaosException in case of error from !CHAOS or other exception if communication error

    """
    srv = options["uri"];
    url = "http://" + srv + "/" + func;
    r = requests.post(url, data=params, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if(r.status_code == requests.codes.ok):
        return json.loads(r.text)
    else:
        raise ChaosException(r.text)
  
def mdsBase(cmd,opt):
    """ base function for MDS administration 

    Arguments:
        cmd {[string]} -- commands
        opt {[dict]} -- parameters

    Returns:
        [dict] -- an object depending from the operation
    """    
    param = "cmd=" + cmd + "&parm=" + json.dumps(opt)
    return basicPost("MDS", param)
