#!/usr/bin/env python
# encoding: utf-8
"""
skype2prowl.py

Created by Kohichi Aoki on 2009-08-05.
Copyright (c) 2009 drikin.com. All rights reserved.
"""

import sys
import os
import time
import codecs
import getopt
import datetime
import Skype4Py
import prowlpy
import pyRijndael
import base64
import urllib

# force utf-8 to workaround unicode problem
reload(sys)
sys.setdefaultencoding('utf-8')

PROWL_API_KEY     = ""
ENCRYPT_KEY       = ""
OWN_DISPLAY_NAME  = ""
lastTime          = datetime.datetime.now()
deltaTime         = datetime.timedelta(minutes=1)
#deltaTime         = datetime.timedelta(seconds=30)

skype       = Skype4Py.Skype()

verbose     = False
isDebug     = False
help_message = '''
The help message goes here.
'''

def encryptText(text):
  s = pyRijndael.EncryptData(ENCRYPT_KEY, text.encode('utf-8'))
  return base64.b64encode(s)
  
def decryptText(text):
  data = base64.b64decode(text)
  d = pyRijndael.DecryptData(ENCRYPT_KEY, data)
  return d

def uploadMessageToGAE(Message, Status):
  postdata = {}
  postdata['status']          = Status
  postdata['id']              = Message.Id
  postdata['user']            = OWN_DISPLAY_NAME
  postdata['fromdisplayname'] = Message.FromDisplayName.encode('utf-8')
  postdata['fromhandle']      = Message.FromHandle.encode('utf-8')
  postdata['chatname']        = Message.ChatName.encode('utf-8')
  postdata['body']            = encryptText(Message.Body.encode('utf-8'))
  postdata['datetime']        = Message.Datetime
  topic = Message.Chat.Topic
  if( topic == '(null)' ):
    topic = None
  else :
    postdata['topic']         = topic.encode('utf-8')
    
  params = urllib.urlencode(postdata)
  if (isDebug):
    up = urllib.urlopen("http://127.0.0.1:8080/api/skype/putchatmessage", params)
  else:
    up = urllib.urlopen("http://labs.drikin.com/api/skype/putchatmessage", params)
  # print up.read()

# ----------------------------------------------------------------------------------------------------
# Fired on attachment status change. Here used to re-attach this script to Skype in case attachment is lost. Just in case.
def OnAttach(status):
  print 'API attachment status: ' + skype.Convert.AttachmentStatusToText(status)
  
  if status == Skype4Py.apiAttachAvailable:
    skype.Attach();
  
  if status == Skype4Py.apiAttachSuccess:
    print('******************************************************************************');

def OnCall(call, status):
  if status == 'RINGING':
    displayName = call.PartnerDisplayName
    message = u"You received a call from " + displayName + u"."
    sendNotification('Skype', displayName, message)
  
def OnMessageStatus(Message, Status):
  global lastTime
  if Status == 'RECEIVED' or Status == 'SENT':
    if (ENCRYPT_KEY != ''):
      uploadMessageToGAE(Message, Status)
    
    time        = Message.Datetime
    if (time - lastTime > deltaTime):
      topic       = Message.Chat.Topic[:20]
      displayName = Message.FromDisplayName
      if (topic == '(null)'):
        topic = displayName

      if Status == 'RECEIVED' and displayName != OWN_DISPLAY_NAME:
        message = displayName + ': ' + Message.Body
        sendNotification('Skype', topic, message)
      if Status == 'SENT':
        message = 'Myself: ' + Message.Body
        if( verbose ):
          print message
    lastTime = time

def sendNotification(appname, event, description):
  if (PROWL_API_KEY != ''):
    return
  try:
    if (verbose):
      print appname + ' ' + event + ': ' + description
    prowl.add(unicode(appname).encode('utf8'), unicode(event).encode('utf8'), unicode(description).encode('utf8'))
  except Exception,msg:
    print msg

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "hu:k:i:p:vd", ["help", "user=", "api_key=", "password=", "interval="])
    except getopt.error, msg:
      raise Usage(msg)
    
    # option processing
    for option, value in opts:
      if option == "-v":
        global verbose
        verbose = True
      if option == "-d":
        global isDebug
        isDebug = True
      if option in ("-h", "--help"):
        raise Usage(help_message)
      if option in ("-u", "--user"):
        global OWN_DISPLAY_NAME
        OWN_DISPLAY_NAME = value
      if option in ("-k", "--api_key"):
        global PROWL_API_KEY
        PROWL_API_KEY = value
      if option in ("-p", "--password"):
        global ENCRYPT_KEY
        ENCRYPT_KEY = value
      if option in ("-i", "--interval"):
        global deltaTime
        deltaTime = datetime.timedelta(seconds=int(value))
  
  except Usage, err:
    print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
    print >> sys.stderr, "\t for help use --help"
    return 2
  
  skype.OnAttachmentStatus  = OnAttach;
  skype.OnMessageStatus     = OnMessageStatus;
  skype.OnCallStatus        = OnCall;
  print('******************************************************************************');
  print 'Username      : ' + OWN_DISPLAY_NAME
  print 'Prowl API Key : ' + PROWL_API_KEY
  print 'Encrypt Key   : ' + ENCRYPT_KEY
  print 'Interval(sec) : ' + str(deltaTime.seconds)
  print 'Encodeing     : ' + sys.getdefaultencoding()
  print 'Verbose mode  : ' + str(verbose)
  print 'Debug mode    : ' + str(isDebug)
  print 'Connecting to Skype..'
  
  skype.Attach(Wait=False);
  global prowl
  prowl = prowlpy.Prowl(PROWL_API_KEY)

  
  # ----------------------------------------------------------------------------------------------------
  # Looping
  while 1:
    time.sleep(0.1)

if __name__ == '__main__':
  main()

