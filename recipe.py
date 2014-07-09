import praw
import os
import sys

class NetNavi:
    #####
    ##NetNavi is the wrapper class for navigation-related responsibilities. It contains the user agent and a list of subreddits to which it is linked.
    #####
    
    def __init__(self, Username, Password, subs=[]):
        ###
        ##userAgent string is required in the terms for API use.
        ##navigator is returned when the script is connected to Reddit. It then logs in with the name and password provided through the command line
        ##subredditPortals is a list of subreddits to which the bot is linked
        ###
        userAgent= ("Machine Learning Research TestBot [Recipe Scraper] - contact: Dr.LanHikari@gmail.com")
        self.navigator= praw.Reddit(user_agent=userAgent)
        self.navigator.login(username=Username, password=Password)
        self.subredditPortals= subs #subreddits and/or comment permalinks
        

def Recipe_Searcher(subReddit,bookHandle, idListHandle, idList=[]): #takes in a string that is the subreddit to search, a handle to an open file to store the recipe in, a handle to an open file to prevent duplication upon relaunch, and the local visited list
    ##########
    ###Recipe_Searcher is a function that searches a given subreddit for instances of user-submitted recipes in the comments of a submission
    ###It takes in a subreddit object, a open file (book) handle in which to record found files, a visited list, and an open file (idList) handle to record submissions that have been previously parsed. 
    ##########
    
    topSubs=subReddit.get_top_from_week()   
  
    for submission in topSubs:
        ####Loop through the top submissions for the week
        submissionVars = vars(submission)
        ####getting access to information about it (specifically id)
        if submissionVars['id'] not in idList:
            ###if 'id' is not present, this submission has not been previously evaluated
            idList.append(submissionVars['id'])
            idListHandle.write(submissionVars['id'])
            idListHandle.write("\n")
            theAuthor=submissionVars['author']
            #######in which case the id is recorded in both list and file, and the author is stored locally
            for comment in submission.comments:
                potentialMatch=vars(comment)
                ##go through all the comments in the submission in detail
                if potentialMatch['author']== theAuthor: # we can here use a more stringent restriction (i.e. also check to make sure it has no children)                
                    ##checking to make sure we are getting the recipe directly from the author
                    bodyString=potentialMatch['body']
                    if bodyString.find("Recipe") != -1 or bodyString.find("recipe") !=-1:
                        #And that they use the word recipe in their comment
                        print "Potential User submitted recipe found!"
                        print "!!!", submissionVars['author']                 
                        bookHandle.write("\n------" + str(submissionVars['author']) + "------\n")
                        bodyString=bodyString.encode('ascii', 'ignore')
                        bookHandle.write(bodyString)
                        bookHandle.write("\n***********************************************")
                        ##if one is found, write it into the book for this subreddit
                        break
                    


def main():
    if (len(sys.argv) < 3):
        print "Usage:   python", sys.argv[0], "<PATH>", " <USERNAME>", "<PASSWORD>"
    else:
  
        cookbookNames= next(os.walk(sys.argv[1]))[2] #should return a list of all files in (but not subdirectories) in the path specified by the user upon launch. These are used to determine which subreddits to scan as well as to write to the files
        cookbookHandles={}   
    #need to add  graceful error handling for non existent subreddits, failed user logins, etc
    
        for entry in xrange(len(cookbookNames)):
            cookbookNames[entry]=cookbookNames[entry][:-4] # this line is used to strip the extension out of the list so it can be used to search for reddits     
            cookbookHandles[cookbookNames[entry]]=open((sys.argv[1]+"\\"+cookbookNames[entry]+".txt"), "a+") #Open the file and add the open handle to the bookhandle
        if "IDList" in cookbookNames:
            cookbookNames.remove("IDList")
        netizen=NetNavi(sys.argv[2], sys.argv[3], subs=cookbookNames)            
           
        localIDList= cookbookHandles["IDList"].read().splitlines()
       
        
        print localIDList
        cookbookHandles["IDList"].seek(0,2)
        for Subreddit in netizen.subredditPortals:
            subreddit=netizen.navigator.get_subreddit(Subreddit)
            Recipe_Searcher(subreddit,cookbookHandles[Subreddit], cookbookHandles["IDList"], localIDList)
        for handle in cookbookHandles:
            cookbookHandles[handle].flush()
            cookbookHandles[handle].close()            
        

if __name__ == '__main__':
    main()