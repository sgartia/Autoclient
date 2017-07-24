"""  This script would send message to DL """

from VMP_Device_Utility import *
from GlobalVariable_Utility import *

# Sample code to create data set for this script run -- sending external message to Dl 

## Get the DL and User login ID 
#from SQLDB_Utility import *
#SQLAgent = SQLServer()
#SQLAgent.ConnectToDB()


## Get the DL and UserLogin 
#SQLAgent.GetVCSUserLoginAndDLName()

## Close the connection
#SQLAgent.CloseConnection()

## Print the result 
#MasterRun.Agent.Log.info("Getting DL and User Information")
#print GlobalDBVariable.DLAndPublicID
#print GlobalDBVariable.DLAndVCSLogin

## Create a data file for the run 
#DataFile = TEST_DATA + "SampleDataSendingMessageToDL.csv"
#FH = open(DataFile,'w')
## Add the header 
#FH.writelines("DL Name"+","+"DL_ID"+","+"UsersInDL"+",\n")
#for key in GlobalDBVariable.DLAndPublicID:
    #temp = ""
    #for item in GlobalDBVariable.DLAndVCSLogin[key]:
        #temp = temp + str(item)+ "_"
    ## Delete the Last "_" in from the string 
    #temp = str(temp).rstrip("_")
    #record = str(key)+","+ str(GlobalDBVariable.DLAndPublicID[key])+","+ temp +","
    #FH.writelines(record)
    #FH.write("\n")


## End of the Sample code to create data set for this script run -- sending external message to Dl 
#exit()

# create VMP agent to act as external agent to send external Message
VMPAgent = VMP()
DLName = sys.argv[1]
DLPublicID = sys.argv[2]
UserInDL = sys.argv[3]

print DLName
print DLPublicID
print UserInDL

UserNameListInDL = str(UserInDL).split("_")


print UserNameListInDL

# login to all user 
for loop in UserNameListInDL:
       
    
    MasterRun.Agent.Log.info("Authenticate The VCS device with Usename :" +loop+"")
    cmdline = "start " + PYTHON_PATH +" "+SCRIPT_DIR+"UserLoggingWithNoVoiceLogging_Utility.py" + " "+loop
    print cmdline
    
    # Open the Python Script in single process
    os.system(cmdline)
    
    
# Send a number of Message from DL 
time.sleep(10)  # Login Delay
MasterRun.Agent.Log.info("Sending Message to the DL  :" +DLName+"")
VMPAgent.Send3rdPartyMessageToUserToDL(DLPublicID)
MasterRun.Agent.Log.info("Subject of the Message   :" +VMPAgent.ExternalMessageSubject+"")
MasterRun.Agent.Log.info("Text Message   :" +VMPAgent.ExternalMessageText+"")


# Wait 10 sec for iteration delay 
time.sleep(10)  # Login Delay
    
    
