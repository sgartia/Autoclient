"""  This module is to populate and retrive data from SQL server"""
# Include Section 
import os
import sys
import pypyodbc
import string
import random
import ConfigParser


PYTHON_PATH = "C:\\Python27\\python.exe "
HOME_DIR = str(os.path.dirname(os.path.realpath(__file__))).split("Autoclient")[0]+"Autoclient\\"
STAF_INI = HOME_DIR+"UserConfig.ini"



class GlobalDBVariable:
    """  this would contain all the DB related Variable """
    IDAndUserName = {}
    VSUserNameAndID = {}    

        

        

class SQLServer(object):

    Handle = None
    SqlServer = None
    User = None 
    Password = None
    connection = None
    cursor = None
    SqlQueryCommand = None
    results = None
    DataFile = None
    
    

    #----------------------------------------------------------------------
    def __init__(self):
        """  This constructor initialize all database related parameter """


        self.Handle = ConfigParser.ConfigParser()
        self.Handle.optionxform = str
        self.Handle.read(STAF_INI)        
        print STAF_INI

        self.SqlServer = str(self.Handle.get('VMPSQLServerSetting',"SQLServer")).strip()
        self.DB = str(self.Handle.get("VMPSQLServerSetting","DB")).strip()
        self.User= str(self.Handle.get("VMPSQLServerSetting","User")).strip()
        self.Password = str(self.Handle.get("VMPSQLServerSetting","Password")).strip()
        
        print self.SqlServer
        print self.DB
        print self.User
        print self.Password
        
        
      
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
        time.sleep(1)
        self.cursor.commit()


        return 0
    def ExecuteSqlQueryAndFetch (self):
        """   This would execute SQL query """


        self.cursor.execute(self.SqlQueryCommand) 
        self.results = self.cursor.fetchall()

        return 0

    def CloseConnection (self):
        """   This would execute SQL query """
        self.cursor.close()
        self.connection.close() 


        return 0

    def GetUserAndID(self):
        """ This method would initialize all the user and ID"""


        # Expected Sql Query 
        self.SqlQueryCommand = "select ID ,Login From WICMASTER.dbo.Users Where Active='Y' and id>=1 and Login is not null and vstid is null"


        # Execute the SQL query 
        self.ExecuteSqlQueryAndFetch()        


        # Initialize the VSUserAndID
        for item in self.results:
            #print item
            ID = item[0]
            UserName = str(item[1])           
            GlobalDBVariable.VSUserNameAndID[UserName] = ID
            GlobalDBVariable.IDAndUserName[ID]=UserName
       
    
            
            
# Example of use 
SQLAgent = SQLServer()
SQLAgent.ConnectToDB()

#SQLAgent.GetSenderIDRecipentIDAndConvID()
#SQLAgent.GetVSTUserAndID()
SQLAgent.GetUserAndID()
#SQLAgent.GetLastConvID()
SQLAgent.CloseConnection()

#print GlobalDBVariable.VSTUserAndID
print GlobalDBVariable.VSUserNameAndID
print GlobalDBVariable.IDAndUserName
