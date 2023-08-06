#!/usr/bin/env python3
# -fire CLI
from fire import Fire
from notifator.version import __version__
import requests
import os


"""
The trick:  In Fatherbot, create /newbot, select a name
1- remember the API key
from API on web https://.../getUpdates
2- remember the chat_id
3- put APIkey and chat_id to ~/.telegram.token
...
markdown doesnt work with multiline
YES, just give double \n\n
"""


print("i... module notifator/telegram is being run")

def func():
    print("D... function defined in notifator:telegram")
    return True

def test_func():
    print("D... test function ... run pytest")
    assert func()==True









def get_token():
    tokenpath="~/.telegram.token"
    try:
        with open( os.path.expanduser(tokenpath) ) as f:
            res=f.readlines()
    except:
        print("X... cannot read",tokenpath)
        quit()
    res=[ x.strip() for x in res]
    token,chat_id=res
    print( token, chat_id)
    return token, chat_id


def bot_send(bot_message, bot_photo="" ):
    if bot_message=="":
        print("X... zero message")
        quit()
    bot_token, bot_chatID= get_token()
    #    bot_token = ''
    #    bot_chatID = ''

    if (bot_photo==""): #======= NO PHOTO =============
        url='https://api.telegram.org/bot' + bot_token + '/sendMessage'
        payload = {'chat_id':bot_chatID,
                   "parse_mode": "markdown",
                   'text':bot_message}
#        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=MarkdownV2&text=' + bot_message

        print(url)
        print(payload)
        response = requests.post(url,  data=payload, verify=False)
        #response = requests.get(send_text)


    else: #====================YES PHOTO================
        if not os.path.isfile(bot_photo):
            print("X... cannot find picture", bot_photo)
            quit()

        files = {'photo': open(bot_photo, 'rb')}
        payload = {'chat_id':bot_chatID, "parse_mode": "markdown",
                   'caption':bot_message}
        url='https://api.telegram.org/bot' + bot_token + '/sendPhoto'
        print(url)
        print(payload)
        response = requests.post(url, files=files, data=payload, verify=False)
        print( response )
    #----------------------

    return response.json()














if __name__=="__main__":
    print("D... in main of project/module:  notifator/telegram ")
    print("D... version :", __version__ )
    #Fire(  )
    Fire({"bot_send":bot_send,
          "get_token":get_token
    }
    )
