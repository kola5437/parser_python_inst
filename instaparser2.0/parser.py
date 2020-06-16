#!/usr/bin/python
# -*- coding: utf8 -*-
# ЕСЛИ ЭТОТ ЕБУЧИЙ МОЙ КОД КОМУ ТО ДОСТАНЕТЬСЯ, ТО ПИШИТЕ В ТЕЛЕГРАММ @Darimelley
import tkinter as tk
import sqlite3
from selenium import webdriver
import time
import pickle
import re
import sys
import requests
import json
import os
import sqlite3
from threading import Thread
import threading
from selenium.webdriver.common.keys import Keys

active_counter = False


root = tk.Tk()

#----------Параметры окна-------------------
root.geometry('300x450')
root.title('Войти в cиcтему')
root['bg'] = 'white'
label = tk.Label(root, fg="black", bg = 'white')
counter = 0
active_counter = False



#------------------------------------ПАРСЕР-ХУЯСЕР---------------------------------
counter = 0
links_array = []
hashtags = []

def get_driver(proxy = False,headless = False,mobile = False):
    options = webdriver.ChromeOptions()
    if proxy:
        options.add_argument('--proxy-server=http://%s' % proxy)
    if headless == True:
        options.add_argument('headless')
    if mobile == True:
        options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def load_cookie(driver,filename="vartsaba_vasil"):
    driver.get('https://instagram.com')
    filename = "cookies/%s" % filename
    cookies = pickle.load(open(filename, "rb"))
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)
    driver.refresh()

def parser_thread(url,link):
    database = sqlite3.connect('parser_db.sqlite')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
    }
    try:
        html = requests.get(url, headers=headers ).text
        json_page = json.loads(html)
        text = json_page["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]['node']["text"]
        phonePattern = re.compile("\(\d{3}\)\d{9}|\d{3}-\d{3}-\d{4}|\d{12}|\d{3}-\d{3}-\d{2}-\d{2}|0\d{9}|\d{1} \d{2} \(\d{2}\) \d{3} \d{2} \d{2}")
        numbers = phonePattern.findall(text)
        print(numbers)
        if numbers:
            print("Find numbers")
            for number in numbers:
                print(number)
                username = json_page["graphql"]["shortcode_media"]["owner"]["username"]
                try:
                    sql = 'insert into numbers (number,link,username) values ("%s","%s","%s")' % (number,link,username)
                    database.execute(sql)
                    database.commit()
                except: pass
    except: pass
    sql = 'delete from links where link = "%s"'% link
    database.execute(sql)
    database.commit()

def parser():
    global counter
    database = sqlite3.connect('parser_db.sqlite')
    while active_counter:
            sql = 'select link from links where active = 1'
            data_arr = database.execute(sql)
            data_arr = data_arr.fetchall()
            LIMIT = 300
            counter += 1
            if data_arr:
                for link in data_arr:
                    link = link[0]
                    url = "%s?__a=1" % link
                    if threading.active_count() >= LIMIT:
                        time.sleep(3)
                    Thread(target=parser_thread , args=(url,link)).start()

def loader_thread(driver,hashtag):
    database = sqlite3.connect('parser_db.sqlite')
    driver.get("https://www.instagram.com/explore/tags/%s/" % hashtag)
    time.sleep(3)
    html = driver.find_element_by_tag_name('html')
    while active_counter:
        try:
            for _ in range(3):
                html.send_keys(Keys.END)
                html.send_keys(Keys.END)
                html.send_keys(Keys.END)
                time.sleep(1)
            links = driver.find_elements_by_class_name("Nnq7C")
            for link in links:
                link = driver.find_elements_by_class_name("v1Nh3")
                for l in link:
                    l = l.find_element_by_css_selector('a').get_attribute('href')
                    links_array.append(l)
            array_links = list(set(links_array))
            for l in array_links:
                try:
                    sql = 'insert into links (link) values ("%s")' % l
                    database.execute(sql)
                except: pass
            database.commit()
        except: pass


def loader():
    file = ""
    for root, dirs, files in os.walk("cookies/."):
        for filename in files:
            file = filename
    if file:
        for hashtag in hashtags:
            driver = get_driver(headless = True)
            load_cookie(driver,filename=file)
            Thread(target=loader_thread , args=(driver,hashtag)).start()


def save_login_data(login,password):
    driver = get_driver(headless = True)
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(1)
    elem = driver.find_element_by_name("username")
    elem.clear()
    elem.send_keys(login)
    elem = driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(password)
    elem.send_keys(Keys.ENTER)
    time.sleep(10)
    cookies = driver.get_cookies()
    with open('cookies\%s' % login, 'wb') as filehandler:
        pickle.dump(cookies, filehandler)
    driver.quit()

def starter():
    Thread(target=loader).start()
    Thread(target=parser).start()





#------------------------------------ПАРСЕР-ХУЯСЕР---------------------------------



def check_inst(event):# INSTAGRAM
    global login
    global password


    login = login2.get()
    password = password_inst.get()

    if login and password:

        destroy_object = [text_inst,text_login2,login_inst,password_inst,enter2,text_password2,text_not_ok_login1,text_not_ok_password1,text_not_ok_login,reg_insta]
        for object_name in destroy_object:
            object_name.destroy()

        parc.pack()
        text_hesh.pack()
        hash.pack()
        enter_run.pack()
        parc.place(x = 20, y = 5)
        text_hesh.place(x = 20, y = 50)
        hash.place(x = 20, y = 70)
        enter_run.place(x = 20, y = 100)
        label.pack()
        label.place(x = 100, y = 110)
        save_login_data(login,password)

        enter_run.bind('<Button - 1>',start_stop)

    if not password and login:
        text_not_ok_password1.pack()
        text_not_ok_password1.place(x = 20, y = 165)

    elif not login and password:
        text_not_ok_login1.pack()
        text_not_ok_login1.place(x = 20, y = 100)






def check_inst(event):# INSTAGRAM
    global login
    global password


    login = login2.get()
    password = password_inst.get()

    if login and password:

        destroy_object = [text_inst,text_login2,login_inst,password_inst,enter2,text_password2,text_not_ok_login1,text_not_ok_password1,text_not_ok_login,reg_insta]
        for object_name in destroy_object:
            object_name.destroy()

        parc.pack()
        text_hesh.pack()
        hash.pack()
        enter_run.pack()
        parc.place(x = 20, y = 5)
        text_hesh.place(x = 20, y = 50)
        hash.place(x = 20, y = 70)
        enter_run.place(x = 20, y = 100)
        label.pack()
        label.place(x = 100, y = 110)

        enter_run.bind('<Button - 1>',start_stop)

    if not password and login:
        text_not_ok_password1.pack()
        text_not_ok_password1.place(x = 20, y = 165)

    elif not login and password:
        text_not_ok_login1.pack()
        text_not_ok_login1.place(x = 20, y = 100)
def count():
    if active_counter:
        label.config(text=counter)
        label.after(1000, count)


def start_stop(event):
    global active_counter
    for hash1 in hash.get().split():
        hashtags.append( str(hash1) )
    if not hash1:
        active_counter = False
        return

    if enter_run['text'] == 'Старт':
        starter()
        active_counter = True
        count()
        enter_run.config(text="Стоп")
        hashtags.clear()
    else:
        hashtags.clear()

        active_counter = False
        enter_run.config(text="Старт")


def pars_stop(event):
    running = False



text_not_ok_login = tk.Label(text = 'Вы не ввели логин ', font = 'Consalas 7', fg = 'red', bg = 'white')
text_not_ok_password1 = tk.Label(text = 'Пароль или логин не совподают', font = 'Consalas 7', fg = 'red', bg = 'white')

#---------------------------------INSTAGRAM--------------------------------------#
text_inst = tk.Label(text = 'Вход в instagram', font = 'Consalas 25', fg = 'black', bg = 'white')


text_login2 = tk.Label(text = 'Логин от instagram', font = 'Consalas 10', fg = 'black', bg = 'white')
login2 = tk.Entry(root, font = 'Consalas 15', fg = 'black', bg = 'white')

password2 = tk.Entry(root, font = 'Consalas 15', fg = 'black', bg = 'white',show = '*')


login_inst = tk.Entry(root, font = 'Consalas 15', fg = 'black', bg = 'white')

text_password2 = tk.Label(text = 'Пароль от instagram', font = 'Comfortaa 10', fg = 'black', bg = 'white')
password_inst = tk.Entry(root, font = 'Consalas 15', fg = 'black', bg = 'white',show = '*')

enter2 = tk.Button(text='Войти ', font = 'Consalas 15', fg = 'white', bg = '#0000FF')
enter2.bind('<Button - 1>',check_inst)

reg_insta = tk.Label(text = 'После нажатия подожди 15 сек', font = 'Consalas 7', fg = 'red', bg = 'white')

parc = tk.Label(text = 'Парсер', font = 'Consalas 25', fg = 'black', bg = 'white')
text_hesh = tk.Label(text = 'Введите хештег(без #)', font = 'Consalas 10', fg = 'black', bg = 'white')
hash = tk.Entry(root, font = 'Consalas 15', fg = 'black', bg = 'white')

enter_run = tk.Button(text='Старт', font = 'Consalas 15', fg = 'white', bg = '#0000FF')


text_not_ok_login1 = tk.Label(text = 'Вы не ввели логин ', font = 'Consalas 7', fg = 'red', bg = 'white')
text_not_ok_password1 = tk.Label(text = 'Пароль или логин не совподают', font = 'Consalas 7', fg = 'red', bg = 'white')



reg_insta.pack()
reg_insta.place(x = 100, y = 200)
text_inst.pack()
text_login2.pack()
text_inst.place(x = 20, y = 5)
text_login2.place(x = 20, y = 50)
login2.pack()
login2.place(x = 20, y = 70)
text_password2.pack()
password_inst.pack()
text_password2.place(x = 20, y = 115)
password_inst.place(x = 20, y = 135)
enter2.pack()
enter2.place(x = 20, y = 190)

root.mainloop()
