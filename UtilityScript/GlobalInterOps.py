"""  This module would contains all the global variable related to interops"""

# Include Session 
import os
import sys
import time
import datetime
import requests
global VMPGlobalEnv
global VSTGlobalEnv
import logging
from LoadLogicCalculate import *


PYTHON_PATH = "C:\\Python27\\python.exe "
HOME_DIR = str(os.path.dirname(os.path.realpath(__file__))).split("VMPScalability")[0]+"VMPScalability\\"
INTERGRATION_PY_DIR_PATH = HOME_DIR+"PyScriptForInterOps\\"
TESTDATA = HOME_DIR+"TestData\\"
INTERGRATION_TEST_DATA_PATH = TESTDATA + "IntegrationTestData\\"
STAF_INI = HOME_DIR+"STAF.ini"




class VMPEnv(object):
    
    VmpEndpoint = None
    headers = {}
    
    def __init__(self):
        """ Assign the parameter"""
        
        self.VmpEndpoint = "http://10.37.225.2"    
        headers = {
                    'Referer': self.VmpEndpoint,
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Origin': self.VmpEndpoint,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
            }

        
class VSTEnv(object):
    
    VSTEndpoint = None
    headers = {}
    
    def __init__(self):
        """ Assign the parameter"""
        
        self.VSTEndpoint = 'https://load-vst-api.vocera.com'   
        headers = {}
  


# Example of Use 

# Create VMP Env Object as global Object
VMPGlobalEnv = VMPEnv()

# Create VST Env Object as global Object
VSTGlobalEnv = VSTEnv()

