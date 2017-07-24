"""   This module is developed to hold all the common os and system level functionality """

# Import Session 
import sys
import os


MAIN_DIR = "Autoclient"
HOME_DIR = str(os.path.dirname(os.path.realpath(__file__))).split(MAIN_DIR)[0]+MAIN_DIR+"\\"
TOOL_DIR = HOME_DIR +"TOOL\\"

class test(object):    
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        print "I am constructor"
    #----------------------------------------------------------------------
    def __del__(self):
        """"""
        print "I am destructor"
        
        
########################################################################
class RemeberPID(object):
    """"""
    FileName = None    
    AllData = []
    PID = None

    
    def __init__(self,PID):
        """Constructor"""
        
        # Intialize the PID         
        self.PID = str(PID)
        
        # Initialize the File name
        self.FileName = TOOL_DIR+"ProcessID.txt"
        
    #----------------------------------------------------------------------
    def AppendMe(self):
        """"""
        try:            
            self.GetAll()
            
            # check if PID already exists in the file 
            val = self.PID+"\n"
            if val in self.AllData:
                return True
            else:
                self.__AddMe()
                
        except IOError:
            
            # Create the new file
            self.__AddMe()
            
            sys.exc_clear()
            
    def __AddMe(self):
        """"""
        with open(self.FileName, "a") as myfile:            
            myfile.write(self.PID)
            myfile.write("\n")
        
    def GetAll(self):
        """"""
        with open(self.FileName, "r") as myfile:            
            self.AllData  = myfile.readlines()  
            
        for item in self.AllData:
            if (str(item).strip() == ""):
                self.AllData.remove(item)
            
        
    #----------------------------------------------------------------------
    
    def GetAllPIDList(self):
        """"""
        self.GetAll()
        return list(map(lambda temp:temp.strip(),self.AllData))
        
    def WriteAllData(self):
        """"""
        with open(self.FileName, "w") as myfile:
            for item in self.AllData:
                myfile.write(item)
        
   
    def RemoveMe(self):
        """"""
        self.GetAll()
        val = self.PID+"\n"
        print "all data in all data "
        print self.AllData
        if val in self.AllData:
            #print val
            temp = self.PID+"\n"
            #print temp
            self.AllData.remove(temp)          
        
        self.WriteAllData()
   

### Example of use 
##Test1 = RemeberPID(76789)
##Test1.AppendMe()
##print Test1.GetAllPIDList()

##Test = RemeberPID(7679)
##Test.AppendMe()
##print Test.GetAllPIDList()


##Test8 = RemeberPID(3445)
##Test8.AppendMe()
##print Test8.GetAllPIDList()

##Test.RemoveMe()

##print Test8.GetAllPIDList()



