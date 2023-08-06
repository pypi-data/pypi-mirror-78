from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
from selenium.common.exceptions import NoSuchElementException
import re
import time
import random
import requests
import os
import io
from PIL import Image
import hashlib
import shutil 
import psycopg2
import string
import instabot

class thief:
    def __init__(self):
        self.username = str(input("Enter your instagram username: "))
        self.password = str(input("Enter your instagram password: "))
        self.dbName = str(input("Enter your database name: "))
        self.dbPassword = str(input("Enter your database password: "))
        self.path = str(input("Enter your directory (where to download picture): "))
        self.driver = webdriver.Firefox()
        #open database
        self.db = psycopg2.connect(database=self.dbName,user="postgres",password=self.dbPassword,host="127.0.0.1",port="5432")
        self.cursor = self.db.cursor()
    def login(self):
        self.driver.get("https://www.instagram.com/")
        time.sleep(5)
        username_input = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
        username_input.send_keys(self.username)
        time.sleep(5)
        password_input = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
        password_input.send_keys(self.password)
        time.sleep(5)
        login_button = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button")
        login_button.click()
        time.sleep(20)
        not_now = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button")
        not_now.click()
        time.sleep(10)
        ui.WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.HoLwm"))).click()
        time.sleep(10)
    
    def downloadByHashtags(self,hashtags,number_of_photos):
        for k in range(0,len(hashtags)):
           
            self.driver.get("https://www.instagram.com/explore/tags/"+hashtags[k])
            for i in range(1,number_of_photos):

                #create random Id
                time.sleep(10)
                letters = string.ascii_lowercase
                ID = ''.join(random.choice(letters) for i in range(1,12))

                #click second post
                post = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[2]/a/div[1]")
                ActionChains(self.driver).move_to_element(post).click().perform()
                time.sleep(5)

                #get current url and current url content
                current_Url = self.driver.current_url
                time.sleep(5)
                imageScraping = requests.get(current_Url)

                #get img url
                time.sleep(5)
                soup = BeautifulSoup(imageScraping.content,"html.parser")
                link = soup.select("script")[3]
                time.sleep(5)
                data = link.string
                json_data = data[21:-1]
                start_index = json_data.find("https")
                end_index = json_data.index("\"",start_index)
                raw_url = json_data[start_index:end_index]
                complete_url = re.sub(r'(\\u0026)',"&",raw_url)

                #check if is video or not
                start_index_video = json_data.find("is_video")
                end_index_video = start_index_video+15
                is_video = json_data[start_index_video:end_index_video]
                if len(is_video) == 15:
                    video_bool = is_video[10:15]
                else:
                    video_bool = is_video[10:14]
                time.sleep(10)

                #download picture
                if video_bool == "false":

                    #get owner of post
                    time.sleep(10)
                    first_owner = json_data.find("owner")
                    last_owner = json_data.rfind("owner")
                    owners = json_data[first_owner:last_owner]
                    username_owner = owners.rfind("username")
                    account_owner = owners[username_owner:]
                    first_coma = account_owner.index(",")
                    semicolon = account_owner.index(":")
                    raw_username = account_owner[semicolon+1:first_coma]
                    complete_username = re.sub('"','',raw_username)
                    print("username: "+complete_username)

                    #download picture
                    r = requests.get(complete_url)
                    os.chdir(self.path)
                    if r.status_code == 200:
                        r.raw.decode_content = True
                        with open("instagramSample.jpeg",'wb') as f:
                            f.write(r.content)
                            os.rename("instagramSample.jpeg",ID+".jpeg")
                            address = self.path + ID + ".jpeg"

                        #store it into a database (postgresql)
                        ID = "'" + ID + "'"
                        address = "'"+address+"'"
                        NOTPOSTED = "'NOTPOSTED'"
                        complete_username = "'"+complete_username+"'"
                        print("ID: "+ ID)
                        print("path: "+address)
                        print("status: " + NOTPOSTED)
                        self.cursor.execute("INSERT INTO photos_instagram (id,path,status,owner) \
        VALUES ({},{},{},{});".format(ID,address,NOTPOSTED,complete_username))
                else:
                    continue
                
                time.sleep(40)

                #go to next post
                next_post = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a[2]")
                next_post.click()                   
                time.sleep(10)

            
    def downloadByFeed(self,number_of_photos):
        self.driver.get("https://www.instagram.com/explore/")
        for i in range(1,number_of_photos+1):

            #create random Id
            time.sleep(10)
            letters = string.ascii_lowercase
            ID = ''.join(random.choice(letters) for i in range(1,12))

            #click second post
            post = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/div/div[1]/div[3]/div")
            ActionChains(self.driver).move_to_element(post).click().perform()
            time.sleep(5)

            #get current url and current url content
            current_Url = self.driver.current_url
            time.sleep(5)
            imageScraping = requests.get(current_Url)

            #get img url
            time.sleep(5)
            soup = BeautifulSoup(imageScraping.content,"html.parser")
            link = soup.select("script")[3]
            time.sleep(5)
            data = link.string
            json_data = data[21:-1]
            start_index = json_data.find("https")
            end_index = json_data.index("\"",start_index)
            raw_url = json_data[start_index:end_index]
            complete_url = re.sub(r'(\\u0026)',"&",raw_url)

            #check if is video or not
            start_index_video = json_data.find("is_video")
            end_index_video = start_index_video+20
            is_video = json_data[start_index_video:end_index_video]
            if len(is_video) == 15:
                video_bool = is_video[10:15]
            else:
                video_bool = is_video[10:14]
            time.sleep(10)

            #download picture
            if video_bool == "false":

                #get owner of post
                time.sleep(10)
                first_owner = json_data.find("owner")
                last_owner = json_data.rfind("owner")
                owners = json_data[first_owner:last_owner]
                username_owner = owners.rfind("username")
                account_owner = owners[username_owner:]
                first_coma = account_owner.index(",")
                semicolon = account_owner.index(":")
                raw_username = account_owner[semicolon+1:first_coma]
                complete_username = re.sub('"','',raw_username)
                print("username: "+complete_username)

                #download picture
                r = requests.get(complete_url)
                os.chdir(self.path)
                if r.status_code == 200:
                    r.raw.decode_content = True
                    with open("instagramSample.jpeg",'wb') as f:
                        f.write(r.content)
                        os.rename("instagramSample.jpeg",ID+".jpeg")
                        address = self.path + ID + ".jpeg"

                    #store it into a database (postgresql)
                    ID = "'" + ID + "'"
                    address = "'"+address+"'"
                    NOTPOSTED = "'NOTPOSTED'"
                    complete_username = "'"+complete_username+"'"
                    print("ID: "+ ID)
                    print("path: "+address)
                    print("status: " + NOTPOSTED)
                    self.cursor.execute("INSERT INTO photos_instagram (id,path,status,owner) \
        VALUES ({},{},{},{});".format(ID,address,NOTPOSTED,complete_username))
            else:
                continue
                
            time.sleep(40)

            #go to next post
            next_post = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a[2]")
            next_post.click()                   
            time.sleep(10) 

    def postToAccount(self,description_post):
        databaseName = str(input("Enter database name: "))
        databasePass= str(input("Enter database password: "))
        path = str(input("Enter path of directory of instagram photos: "))
        db = psycopg2.connect(database=databaseName,user="postgres",password=databasePass,host="127.0.0.1",port="5432")

        cursor = db.cursor()
        username = str(input("Enter instagram username: "))
        password = str(input("Enter instagram password: "))
        bot = Bot() 
        os.chdir(path)
        bot.login(username = username,  
                password = password) 
        r = cursor.execute("SELECT * FROM photos_instagram")
        rows = cursor.fetchall()
        for row in rows:
            owner = row[3]
            path = row[1]
            status = row[2]
            ID = row[0]
            caption = "Owner: " + "@"+ owner + "\n" + "If you are the owner of the post and want to remove it, please contact me and I will remove it."
            if status == "NOTPOSTED":
                bot.upload_photo(path,caption=description_post+"\n"+caption)
                time.sleep(10)
                cursor.execute("SELECT * FROM photos_instagram WHERE id = "+"'"+ID+"'"+";")
                cursor.execute("UPDATE photos_instagram SET status = 'POSTED';")
                os.rename(ID+".jpeg.REMOVE_ME",ID+".jpeg")
            else:
                pass

        db.commit()
        db.close()

    def closeDB(self):
        self.db.commit()
        self.db.close()
