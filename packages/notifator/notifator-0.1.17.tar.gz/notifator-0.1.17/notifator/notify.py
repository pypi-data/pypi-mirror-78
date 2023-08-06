#!/usr/bin/python3
#myservice_description: global notificator/in development
#
#   I need to combine with the advanced RPIHAT (running invisibly in screen)
#
#
import notify2
#sudo aptitude install python3-notify2

import time
#from multiprocessing import Queue
from queue import LifoQueue, Queue, Empty, Full
import os

import glob
import subprocess

from fire import Fire


class ScreenTool:
    servlist=[]
    def __init__(self):
        res=self.check_myservice()
        print("i... "+str(len(res))+" screens seen for the user")
        print( "i... : {}\n".format(res ) )


    def check_myservice(self):
        #### CMD="screen -ls "+self.screenname
        user_name = os.getenv('USER')
        res=glob.glob( "/var/run/screen/S-"+user_name+"/*" )
        res=[os.path.basename(x) for x in res] # 4321.myservice_
        shortres=["".join(x.split(".")[1:]) for x in res]
        self.servlist=res
        return res


    def run_screen(self, name, cmd):
        self.screenname=name
        print("i... starting screen")
        CMD=cmd
        print("D...  --- ",CMD)
        CMD='/usr/bin/screen -dmS '+self.screenname+' bash -c  "'+CMD+'"'
        print( CMD )
        ok=False
        #try:
        subprocess.check_call( CMD, shell=True )
        ok=True
        print("i...      run ok ")
        print("i...  screen STARTED")
        #except:
        #print("X...      xxx... screen  PROBLEM")






class NotifyClass(object):

    def __init__(self, dest, message):
        print("D... notifator target/message:",dest,"/",message)
        self.dest = dest
        self.message = message


    def audio(self):
        #print("@"+self.audio.__name__, end='')
        return self.message

    def dbus(self):
        #print("@"+self.dbus.__name__+' ', end='')
        notify2.init("--Title--")
        #notice = notify2.Notification(self.dest, self.message)
        notice = notify2.Notification( self.message )
        notice.show()
        time.sleep(0.1)
        return self.message

    def hat(self):
        #print("@"+self.hat.__name__+'  ', end='')
        return self.message


    def web(self):
        #print("@"+self.web.__name__+'  ', end='')
        return self.message

    def term(self):
        """
        add the user to tty group to be able to listen
        usermod -a -G tty  user
        """

        #print("@"+self.term.__name__+' ', end='')
        msg=self.message
        print(msg)
        msg=msg.replace('"',' ')
        msg=msg.replace('\\',' ')
        msg=msg.replace('|',' ')
        msg=msg.replace('$',' ')
        msg=msg.replace('#',' ')
        msg=msg.replace('`',' ')
        msg=msg.replace("'",' ')
        os.system('echo "'+msg+'" | wall')
        return self.message

#============
    def do( self ):
        return getattr(NotifyClass, self.dest)(self)




def issueall(message):
    """Issues message to all destinations defined in this function
    """
    q = Queue(6)   # how does this work?

    #q.put( NotifyClass('audio','Using google talk') )
    #q.put( NotifyClass('dbus' ,'notify-send way - works with gtk') )
    q.put( NotifyClass('dbus' ,   message  ) )
    q.put( NotifyClass('hat'  , 'Init sense hat and display') )
    #q.put( NotifyClass('web'  , 'connect to webpy.py') )
    q.put( NotifyClass('term' , message) )

    #for i in range(5):
    #    if q.full(): break
    ###############
    # MAIN PART- accept and queue messages
    ###############

    #================== RPIHAT PART
    #s=ScreenTool()
    #s.run_screen("sleeptest","sleep 10") # this can contain rpihat...

    while not q.empty():
        res=q.get().do()
        #print("   ", res)


#============================================================
#============================================================
#============================================================
#============================================================
#============================================================

if __name__=="__main__":
    Fire( issueall )





    ######################## END END END END END END #################
    ######################## END END END END END END #################
    ######################## END END END END END END #################

    #########################
    # TASK:
    #   local and ip applications need to display stuff. messages.
    #   myservice could work as ip port for receiving messages
    #      and everything else is local...
    #  PLAN:
    #  queue external - via -
    # * notify
    # * sense-hat - small num, rolling number
    # * audio - mp3 or voice
    # * webpage
    #https://pymotw.com/2/multiprocessing/communication.html
    #http://askubuntu.com/questions/108764/how-do-i-send-text-messages-to-the-notification-bubbles
    #====== first attempt  d-bus:
    #
    #https://askubuntu.com/questions/38733/how-to-read-dbus-monitor-output/142888
    ############################
