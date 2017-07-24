#!/usr/bin/python
import os
import sys
import json

#read output.json and store all the users that we can't use
def readOutputJson(infolder):
  for (dirpath, dirname, filenames) in os.walk(infolder):
    for file in filenames:
      if "output.json" in file:
        with open(dirpath + "/"+ file, "r") as f:
          data = json.load(f)

  return data


#parsed unload for users and gets userInternalName, userID, lastName, firstName, internalSite and ties with siteName from sitesList
def readunload(infolder, sitesList):
  for (dirpath, dirname, filenames) in os.walk(infolder):
    for file in filenames:
      if "unload-" in file:
        with open(dirpath + "/"+ file, "r") as f:
          userList = []
          userDict = {}
          endofUsers = False

          for line in f:
            # print "This is the current line %i %s" % (i , line)

            if ("Users" in line) and ("XVSET" in line):
              # print "This is the user line %s" %line
              userID = ""
              lastName = ""
              firstName = ""

              for line in f:
                # print "this is the inner line %s " % (line)
                if "Address Book Entry" in line:
                  endofUsers = True #break the outer loop of reading all lines in file
                  break

                if "Internal Name" in line:
                  # print line
                  line = " ".join(line.split()) #remove duplicate spaces
                  line = line.split("=")
                  userInternalName = line[1].strip()
                  # print userInternalName

                if "User ID" in line:
                  # print line
                  line = " ".join(line.split()) #remove duplicate spaces
                  line = line.split("=")
                  userID = line[1].strip()
                  # print userID

                if "Last Name" in line:
                  # print line
                  line = " ".join(line.split()) #remove duplicate spaces
                  line = line.split("=")
                  lastName = line[1].strip()
                  # print lastName

                if "First Name" in line:
                  # print line
                  line = " ".join(line.split()) #remove duplicate spaces
                  line = line.split("=")
                  firstName = line[1].strip()
                  # print firstName

                if "Site" in line and "Local Site" not in line:
                  # print line
                  line = " ".join(line.split()) #remove duplicate spaces
                  line = line.split("=")
                  internalSite = line[1].strip()
                  site = ""
                  # print internalSite
                  # print userID + " " + lastName + " " + firstName
                  for s in sitesList:
                    if internalSite == s["siteInternalName"]:
                      site = s["Name"]

                  userList.append({"userID": userID, "lastName": lastName, "firstName": firstName, "internalName": userInternalName, "internalSite": internalSite, "site":site})

            else:
              if endofUsers == True:
                break
          # print userList
          return userList

#parse unload for sites siteInternalName to tie in with users siteInternalName
def readunloadForSites(infolder):
  for (dirpath, dirname, filenames) in os.walk(infolder):
    for file in filenames:
      if "unload-" in file:
        with open(dirpath + "/"+ file, "r") as f:
          sitesList = []
          endofsites = False

          for line in f:
            # print "This is the current line %i %s" % (i , line)

            if ("Sites" in line) and ("XVSET" in line):
              # print "This is the sites line %s" %line
              siteInternalName = ""
              siteName = ""

              for line in f:
                # print "this is the inner line %s " % (line)
                if "Groups"in line:
                  endofsites = True #break the outer loop of reading all lines in file
                  break

                if "Internal Name" in line:
                  # print line
                  line = " ".join(line.split()) #remove duplicate spaces
                  line = line.split("=")
                  siteInternalName = line[1].strip()
                  #print siteInternalName

                if "Name\t\t\t\t\t=" in line:
                  # print line
                  line = " ".join(line.split()) #remove duplicate spaces
                  line = line.split("=")
                  Name = line[1].strip()
                  #print Name

                  sitesList.append({"siteInternalName": siteInternalName, "Name": Name})

            else:
              if endofsites == True:
                break
          # print sitesList
          return sitesList


def generateDiffLoadList(subsetList, totalList):
  tempList = totalList
  for s in subsetList:
    # print s
    for t in tempList:
      # print t
      # print "this is s %s and t %s" % (s["userID"], t["userID"])
      if str(s["userID"]) == str(t["userID"]):
        #print "removed this user"
        #print t
        tempList.remove(t)

  return tempList

def generateLoadList(numberToGenerate):
  outputList = []
  count = 0

  while count < int(numberToGenerate):
    tempDict = {}
    tempDict["index"] = "0"
    tempDict["timeDelta"] = str(count)
    tempDict["unixtime"] = "0"
    tempDict["userID"] = "tuser" + str(count)
    tempDict["ap"] = "f07f06f3244f"
    tempDict["ABCommands"] = ["UNTIL"]
    tempDict["time"] = "01/01/01 12:00:00.000"
    tempDict["device"] = "aaa0" + str(count).zfill(8)
    tempDict["firstName"] = "Test"
    tempDict["lastName"] = "User" + str(count)
    outputList.append(tempDict)
    count = count + 1
  return outputList

def generateLoadListReal(numberToGenerate, site, inList):
  outputList = []
  count = 0
  while count < int(numberToGenerate):
    count = count + 1
    # print count
    for i in inList:
      if i["site"] == site:
        print i
        tempDict = {}
        tempDict["index"] = "0"
        tempDict["timeDelta"] = str(count)
        tempDict["unixtime"] = "0"
        tempDict["userID"] = i["userID"]
        tempDict["ap"] = "3cce731bf410"
        tempDict["ABCommands"] = ["UNTIL"]
        tempDict["time"] = "01/01/01 12:00:00.000"
        tempDict["device"] = "aaa0" + str(count).zfill(8)
        outputList.append(tempDict)
        inList.remove(i)
        break
  return outputList

def generateUserCSV(inList, outfolder):
  tempList = []
  #first pass go through and find userIDs and devices
  for s in inList:
    tempStr = s["userID"] + ","+ ","+ ","+ "," + s["firstName"][0] + s["lastName"] +'@sollab.local'+ ","+ ","+ ","+ ","+ ","+ ","+ ","+s["device"]+"\n"
    tempList.append(tempStr)

  with open(outfolder + "/userLogins.csv", "w") as out:
    for t in tempList:
      out.write(t)

def printJSON(inList, outfolder):
  with open(outfolder + "/CallLoadAll.json", "w") as fOut:
    fOut.write(str(json.dumps(inList)))

def main():
  #input path
  infolder = sys.argv[1]
  # print infolder

  #output path
  outfolder = sys.argv[2]
  # print outfolder

  #number to generated
  numberToGenerate = sys.argv[3]

  #site name to get users from to compare against
  site = sys.argv[4]

  #SECTION 1: Generate test users for ABLauncher

  ss = generateLoadList(numberToGenerate)

  #generate CallLoadAll.json file for ABLauncher
  printJSON(ss, outfolder)

  #write appropriate fields in Sessions Dict List to CSV
  generateUserCSV(ss, outfolder)

  #SECTION 2: use the functions to take existing CallLoadALL.json file and parse unload to get a diff of users to use for other tests that don't conflict

  #Read in OutputJson file of the list of users that are active
  # oL = readOutputJson(infolder)

  #parse unload for sites for internal and site names
  # sL = readunloadForSites(infolder)

  #parse unload for users so it can associate users with their sites by full site name as seen in SA logs
  # uL = readunload(infolder, sL)

  #get the diff
  # gg = generateDiffLoadList(oL, uL)

  # p = generateLoadListReal(numberToGenerate, site, gg)

  # printJSON(p, outfolder)
  # generateUserCSV(p, outfolder)
if __name__ == '__main__':
  main()
