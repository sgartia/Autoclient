"""  This module is to populate and retrive data from SQL server"""
# Include Section 
from GlobalVariable_Utility import *


class GlobalDBVariable:
    """  this would contain all the DB related Variable """
    IDAndVCSUserName = {}
    VCSUserNameAndID = {}   
    VmpIdVSIdVCSLogin = {}
    DLAndVCSLogin = {}
    DLAndPublicID = {}

        

        

class SQLServer(object):

    SqlServer = None
    User = None 
    Password = None
    connection = None
    cursor = None
    SqlQueryCommand = None
    results = None
    DataFile = None
    
    # Vmp User details
    VMPUserFirstName = None
    VMPUserLastNamePrefix = None
    NumberOfRowNeedToUpdate = None
    VMPUserIDList = None
    ALreadyExistVmpIDVsPermission = None
    ExpectedAllUserPermissionTable = None
    PermissionList = None
    
    

    #----------------------------------------------------------------------
    def __init__(self):
        """  This constructor initialize all database related parameter """



        self.SqlServer = VMP_DB_SERVER_IP
        self.DB = VMP_SQL_DB_NAME
        self.User= VMP_SQL_DB_USER
        self.Password = VMP_SQL_DB_USER_PASSWORD
        
        print self.SqlServer
        print self.DB
        print self.User
        print self.Password
	
	# Initialize VMP parameter
	self.VMPUserIDList = []
        self.ALreadyExistVmpIDVsPermission = []
	self.ExpectedAllUserPermissionTable = []
        self.PermissionList = ['Chat','Contacts','Documents','Pager']
        
        
      
        # connect the DB 
        self.ConnectToDB()

    @property
    def Id_Generator(self):
        """ Create the device ID randomly"""
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range (31))

    def ConnectToDB (self):
        """   This connects to Db """

        self.connection = pypyodbc.connect("Driver={SQL Server};SERVER="+self.SqlServer+";Database="+self.DB+";uid="+self.User+";pwd="+self.Password+";")
        time.sleep(1)
        self.cursor = self.connection.cursor() 

        return 0

    def ExecuteSqlQueryAndCommit (self):
        """   This would execute SQL query """



        self.cursor.execute(self.SqlQueryCommand) 
        time.sleep(.2)
        self.cursor.commit()


        return 0
    def ExecuteSqlQueryAndFetch (self):
        """   This would execute SQL query """


        self.cursor.execute(self.SqlQueryCommand) 
        self.results = self.cursor.fetchall()

        return 0
    def ExecuteSqlInsertQuery (self):
        """   This would execute Insert Query """


        self.cursor.execute(self.SqlQueryCommand) 
       

        return 0

    def CloseConnection (self):
        """   This would execute SQL query """
        self.cursor.close()
        self.connection.close() 


        return 0
    
    def CreateVMPLogin (self):
        """   This would create the VMP login for all the VS sync user """
        
        for x in range(0,self.NumberOfRowNeedToUpdate,1):
	    SqlQueryPart1 = "UPDATE dbo.Users SET Login='"+self.VMPUserFirstName+self.VMPUserLastNamePrefix+str(x)+"', Password='8123B5AD12FAFAC5EAAB1EA9FDAD3A4AA1CF1A22', EnforceAppPIN='N',\
	    DesktopEnabled='Y', DeviceEnabled='Y', WebEnabled='Y', NotificationsEnabled='Y', OverrideNotificationsEnabled='Y' " 
	    SqlQueryPart2 = "WHERE DisplayName= '"+self.VMPUserFirstName+" "+self.VMPUserLastNamePrefix+str(x)+"';" 
	    FinalSqlQuery = SqlQueryPart1 + ' ' + SqlQueryPart2
    
	    print(FinalSqlQuery)
	    self.SqlQueryCommand = FinalSqlQuery
	    
	    # Executes and commits changes to table after each iteration
	    self.ExecuteSqlQueryAndCommit()

        

        return 0

    def GetVCSUserAndID(self):
        """ This method would initialize all the user and ID"""


        # Expected Sql Query 
        self.SqlQueryCommand = "select ID ,Login From WICMASTER.dbo.Users Where Active='Y' and id>=1 and Login like '"+self.VMPUserFirstName+"%'"


        # Execute the SQL query 
        self.ExecuteSqlQueryAndFetch()        


        # Initialize the VSUserAndID
        for item in self.results:
            #print item
            ID = item[0]
	    self.VMPUserIDList.append(ID)
            UserName = str(item[1])           
            GlobalDBVariable.VCSUserNameAndID[UserName] = ID
            GlobalDBVariable.IDAndVCSUserName[ID]=UserName
	
       
	    
    def UpdateChatMsgNotificationCallPermission(self):
        """ This method would set the permission for chat call, notification and alram"""
	
	# Delete all the rows 	 
        self.SqlQueryCommand = "select * from dbo.ApplicationsInUser"


        # Execute the SQL query 
        self.ExecuteSqlQueryAndFetch() 
	
	
	
	for item in self.results:
	    temp = str(item[0])+"_"+str(item[1])
	    self.ALreadyExistVmpIDVsPermission.append(temp)
	    
	 
	# Get all the VMP Id by calling the GetVCSUserAndID method
	
	self.GetVCSUserAndID()
	
	#print self.VMPUserIDList
	
	
	# Exepected Permission Table 	
	for loop in self.VMPUserIDList:
	    for value in self.PermissionList:
		self.ExpectedAllUserPermissionTable.append(str(loop)+"_"+value)
	
	
	ListDiffer = []
	
	ListDiffer = list_difference(self.ExpectedAllUserPermissionTable,self.ALreadyExistVmpIDVsPermission)

	print ListDiffer
	# Create the insert query to the table dbo.ApplicationsInUser in SQL server of VMP for ListDiffer
	for item in ListDiffer:
	    temval = str(item).split("_")
	    IDval = temval[0]
	    value = temval[1]
	    
	    self.SqlQueryCommand = "INSERT INTO dbo.ApplicationsInUser VALUES ("+IDval+",'"+value+"')"
	    print self.SqlQueryCommand
	    
	    # Execute the SQL query 
	    self.ExecuteSqlQueryAndCommit()
	    
	    
	       
	    
	    
    def GetVCSUserLoginVSIDAndVMPIDForCalling(self):
        """ This method would initialize all the user and ID"""


        # Expected Sql Query 
        self.SqlQueryCommand = "select ID,Login, VoceraID  From WICMASTER.dbo.Users Where Active='Y' and id>=1 and Login like '"+self.VMPUserFirstName+"%' and vstid is null"


        # Execute the SQL query 
        self.ExecuteSqlQueryAndFetch()        


        # Initialize the VSUserAndID
	count = 0
        for item in self.results:
            #print item
            VMPID = item[0]
            VCSUserLogin = str(item[1])  
	    VSUser = str(item[2])
            GlobalDBVariable.VmpIdVSIdVCSLogin[count] = {}
	    

	    GlobalDBVariable.VmpIdVSIdVCSLogin[count]['VMPID'] = VMPID
	    GlobalDBVariable.VmpIdVSIdVCSLogin[count]['VCSlogin'] = VCSUserLogin
	    GlobalDBVariable.VmpIdVSIdVCSLogin[count]['VSID'] = VSUser
	    
	    # Increase the counter
	    count = count + 1
	    
    def GetVCSUserLoginAndDLName(self):
	""" This method would provide login name  and Associated Dl name"""
	
	# Expected Sql Query 
        self.SqlQueryCommand = "select DL.Name, DL.PublicID,UDL.UserID, U.Login from dbo.DistLists DL,dbo.UsersInDistList UDL,dbo.users U where UDL.DistListID = DL.ID and U.ID = UDL.UserID and DL.PublicID != 'NULL'"
          
	# Execute the SQL query 
        self.ExecuteSqlQueryAndFetch() 
	
	
	for item in self.results:
	    dlName = str(item[0])
	    dlPublicId = str(item[1])
	    vcsLoginUser = str(item[3])
	    if (GlobalDBVariable.DLAndVCSLogin.has_key(dlName) == False):
		GlobalDBVariable.DLAndVCSLogin[dlName] = []
	    
	    # Add the user 
	    GlobalDBVariable.DLAndVCSLogin[dlName].append(vcsLoginUser)
	    
	    # Add the Public ID 
	    GlobalDBVariable.DLAndPublicID[dlName] = dlPublicId
            
            
## Example of use 
#SQLAgent = SQLServer()
#SQLAgent.ConnectToDB()

## Initialize the user first name and number of user
#SQLAgent.VMPUserFirstName = "MsgUser"
#SQLAgent.NumberOfRowNeedToUpdate = 300

## call this method after sync the data 
## Method to creae VMP Login After VS user got sync
##SQLAgent.CreateVMPLogin ()

##time.sleep(10)
## Method to create the Update Chat Msg Notification Call Permission

#SQLAgent.UpdateChatMsgNotificationCallPermission()

### method to create the messaging data 
#SQLAgent.GetVCSUserAndID()

###SQLAgent.GetVCSUserLoginVSIDAndVMPIDForCalling()
##print GlobalDBVariable.VmpIdVSIdVCSLogin

#fh = open("VMPUserName.csv",'w')
    
#for keys in  GlobalDBVariable.VCSUserNameAndID:
    #fh.write(keys+","+str(GlobalDBVariable.VCSUserNameAndID[keys])+"\n")
#fh.close()

#SQLAgent.CloseConnection()

#print GlobalDBVariable.DLAndVCSLogin
#print GlobalDBVariable.DLAndPublicID