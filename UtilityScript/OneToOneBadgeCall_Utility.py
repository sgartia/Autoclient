# Import session 
from  AB_Utility_Newformat import *


# Do login in One badge 

badge1 = AutoBadge()
badge1.BadgeIP = "172.30.26.141"
badge1.AbCmd.UserName = "0.wav+0.wav+0.wav+0.wav"
badge1.AbCmd.PromptForUserName = "u-00_0"

# Do log out if its already login then do login and Wait for some time 
badge1.ListOfABScriptCmd = badge1.AbCmd.LogOut + badge1.AbCmd.Login + badge1.AbCmd.UntillPrompt(Prompt.dummy_foo1,100) + badge1.AbCmd.LogOut 


badge1.StartABRun()

badge2 = AutoBadge()
badge2.BadgeIP = "172.30.26.142"
badge2.AbCmd.UserName = "1.wav+1.wav+1.wav+1.wav"
badge2.AbCmd.PromptForUserName = "u-11_1"

# Do log out if its already login then do login   make call to another user and Wait for some time 
badge2.ListOfABScriptCmd = badge2.AbCmd.LogOut + badge2.AbCmd.Login + badge2.AbCmd.CallUser("0.wav+0.wav+0.wav+0.wav") + badge2.AbCmd.LogOut 

badge2.StartABRun()
