"""  This module would contains all the Ab cmd used in libary and script"""


class WavfileFor(object):
    """ This class contains all web files needed for AB"""
    
    A = "a.wav"
    AcceptAllCalls = "accept_all_calls.wav" 
    AcceptCallsOnlyFrom = "accept_calls_only_from.wav"
    Add = "add.wav"
    AddMetoGroup = "add_me_to_group.wav"
    All = "all.wav"
    AnOutsidePhone = "an_outside_phone_number.wav"
    And = "and.wav"
    AnotherNumber = "anothernumber"
    B = "b.wav"
    BlockAllCalls = "block_all_calls"
    BlockAllCallsExcept  = "block_all_calls_except.wav"
    BlockAllCallsFrom = "block_calls_from.wav"    
    BlockCallsOnlyFrom = "block_calls_only_from.wav"
    Broadcast = "broadcast"
    Buddies = "buddies"
    C = "c.wav"
    Call = "call"
    Cellphone = "cellphone"
    Conference = "Conference"    
    ConnectToSiteVocera = "connect_to_site_vocera.wav"
    ConnectToSite   = "connect_to_site.wav"
    ConnectToSiteOne     = "connect_to_site.wav+1"
    Delete = "delete.wav"
    DeleteAllMessages = "delete_all_messages.wav"
    DeleteAllTextMessages = "delete_all_text_messages.wav"
    DeleteMessageFrom = "delete_message_from.wav"
    DepartmentOne = "departmentone"
    DeskPhone =  "deskphone" 
    DialExtension = "dial_extension.wav"    
    DialAnOutsideNumber = "DialAnOutsideNumber.wav"   
    DisablePages = "disable_pages.wav"   
    DoctorKevinColwell = "doctor_kevin_colwell.wav"
    EnablePages = "enable_pages.wav"
    EraseGreetingFor  = "erase_greeting_for.wav"  
    EraseMyGreeting = "erase_my_greeting.wav"
    Everyone = "everyone"
    EveryoneEverywhere = "everyone_everywhere.wav"
    ForwardMyCallsTo =  "forward_my_calls_to"   
    From = "from"
    Greeting = "Greeting.wav"    
    Group = "group"
    GroupOneSpell  = "group_one_spell.wav"   
    Invite = "invite.wav"    
    InviteUser2 = "invite.wav+2+2+2+2"
    JoinConferenceFor  = "join_conference_for.wav"
    JoinMeToGroup = "join_me_to_group.wav"
    LearnAGroupName = "learn_a_group_name.wav"
    LearnAName = "learn_a_name.wav"
    LearnCommands  = "learn_commands.wav" 
    LeaveConferenceFor = "leave_conference_for.wav"
    Locate = "locate.wav"
    LocateMembersOf = "locate_members_of.wav"    
    Logout = "logout"
    Message = "Message.wav"
    NearLocation = "near_location.wav"
    No           = "no.wav"
    OffLine  = "off_line.wav"  
    Only = "only"
    OutsideBuddy = "outsidebuddy"
    Page = "page.wav"
    PlayGreetingFor = "play_greeting_for.wav"
    PlayMessages = "play_messages.wav"
    PlayMyGreeting = "play_my_greeting.wav"
    PlayOldMessages    = "play_old_messages.wav"  
    PlayTextMessages   = "play_text_messages.wav"  
    PlayWelcomeTutorial = "play_welcome_tutorial.wav"
    PlayLongMsg = "PlayLongMsg.wav"
    PlayMessage = "play_messages.wav"
    PlayMyGreeting = "play_my_greeting.wav"
    PoisonControl  = "Poison_Control.wav" 
    RecordAGreeting = "record_a_greeting.wav"
    RecordAGreetingFor  = "record_a_greeting_for.wav"
    RecordAMessageFor = "record_a_message_for.wav"
    RecordANameFor   = "record_a_name_for.wav "
    RecordAnUrgentMessageFor = "record_an_urgent_message_for.wav"
    RecordMyVoicePrint = "record_my_voice_print.wav"
    RecordAGreeting ="record_a_greeting.wav"
    RecordMyName = "record_my_name.wav"
    RedialNumber  = "RedialNumber.wav"    
    Remove = "remove.wav"
    RemoveMeFromGroup = "remove_me_from_group.wav"
    Sanfrancisco = "san_francisco.wav"
    StopForwarding = "stop_forwarding"
    Supervisors = "Supervisors.wav"
    TechSupport = "tech_support.wav"
    To = "to" 
    Transfer = "transfer"
    Unanswered = "unanswered.wav"
    UnlearnGroupName = "unlearn_group_name.wav"
    UnlearnName = "unlearn_name.wav"
    UnLearnAName = "UnLearn-a-Name.wav"
    Urgent = "urgent"
    UrgentlyInvite = "urgently_invite.wav"
    WelcomeTutorial = "play_welcome_tutorial.wav"
    WhatConferenceAmIIn  = "what_conference_am_i_in.wav"  
    WhatGroupsDoIBelongTo  = "what_groups_do_i_belong_to.wav"   
    WhatTimeIsIt = "Whattimeisit"
    WhereAmI = "where_am_i.wav"
    WhoIsBlocked = "who_is_blocked"
    WhoIsInConferenceFor = "who_is_in_conference_for.wav"
    WhoIsInGroup = "who_is_in_group.wav"
    WhoIsInMyConference = "who_is_in_my_conference.wav"
    WhoAmI = "whoami"
    Yes = "yes.wav"

    
    

class Signal(object):
    """ This class contains all Signal for AB"""
    
    EndCall = "EndCall"
    StartAudio = "StartAudio"
    

class ABCmdSet(object):
    """  This class contains all the ab cmd for server version 4.3 """
    CmdList = []
    UserName = None
    PromptForUserName = None
    UserFullNameAppearInVSLog = None
    CalleeName = None
    CalleeNameAppearInVSLog = None    
    WaitTime = None
    WaitTimeAfterCall = None
    
        
    # initiate the constructor 
    def __init__(self):
	self.__Restore ()
 
    def __Restore(self):		
	self.PromptName = None
	self.SignalName = None
	self.WaitTime = 120
	
    
	
    # -        ###  Set of possible action   #####
    @property
    def WaitUntill(self):
        #self.CmdList = [ 'UNTIL  Prompt MainMenu_prompt_completed   wait   '+str(self.WaitTime)+'']
	self.CmdList = [ 'UNTIL']
        return self.CmdList
    
    @property
    def CallAndWait(self):
        self.CmdList = [ 'UNTIL  Prompt MainMenu_prompt_completed   wait   '+str(self.WaitTimeAfterCall)+'','CALL   wait   3','UNTIL  Prompt MainMenu_prompt_completed   wait  2']
        return self.CmdList
