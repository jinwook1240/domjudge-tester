#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
import csv
import threading
import time
import os

# 테스트 옵션. 디버그 시 테스트 유저 수를 낮추고 --headless 옵션을 없앨 것
options = Options()
options.add_argument("--headless")
USERFORTEST =10 # 톄쓰트할 유저 수
CORES = 10 # 스레드 수

students = []
lock = threading.Lock()
def prepInner(category, login, fullname, email, password):
    data = {'category':category, 'login':login, 'fullname':fullname, 'email':email, 'password':password, 'browser':webdriver.Firefox(firefox_options=options), 'result':[]}
    lock.acquire()
    students.append(data)
    lock.release()
            
def prepare():
    prepThreads = []
    with open('users.csv') as usercsv:
        spamreader = csv.reader(usercsv, delimiter=',', quotechar='|')
        for idx, row in enumerate(spamreader):
            if idx is USERFORTEST:
                break
            category = row[0]
            login = row[1]
            fullname = row[2]
            email = row[3]
            password = row[4]
            print(row)
            prepThreads.append(threading.Thread(target=prepInner, args=(category, login, fullname, email, password)))
            prepThreads[len(prepThreads)-1].start()
            if (idx%CORES) is (CORES-1):
                for t in prepThreads:
                    t.join()
                prepThreads = []
    for t in prepThreads:
        t.join()

def login(user):
    user['browser'].get("http://blockchain.onyah.net:10080/login")
    user['browser'].find_element_by_name('_username').send_keys(user['login'])
    user['browser'].find_element_by_name('_password').send_keys(user['password'])
    user['browser'].find_element_by_xpath('//*[@id="loginform"]/div/form/button').click()

def submit(user):# 파일명 및 문제 제목을 변경하여 다른 문제에 대한 테스트 가능
    user['browser'].get("http://blockchain.onyah.net:10080/team/submit")
    #user['browser'].find_element_by_xpath('/html/body/nav/div/div[1]/a/button').click()
    user['browser'].find_element_by_xpath('//*[@id="submit_problem_code"]').send_keys(os.path.abspath('./HelloWorld.java'))# 파일 선택
    Select(user['browser'].find_element_by_xpath('//*[@id="submit_problem_problem"]')).select_by_visible_text("hello - Hello World")# 문제 선택
    Select(user['browser'].find_element_by_xpath('//*[@id="submit_problem_language"]')).select_by_visible_text("Java")# 언어 선택
    user['browser'].find_element_by_xpath('/html/body/div[2]/div/div/div/form/div[5]/button').click()
    user['browser'].switch_to.alert.accept()

def getResult(user):
    user['browser'].get("http://blockchain.onyah.net:10080/team")
    while user['browser'].find_element_by_xpath("/html/body/div[2]/div/div/div/div[3]/div[1]/table/tbody/tr[1]/td[4]/a/span").text =="pending":
        time.sleep(0.2)
        user['browser'].get("http://blockchain.onyah.net:10080/team")
     



def end():
    endThreads = []
    for user in students:
        print(user['login'], end=' : ')
        for result in user['result']:
            print(result[1]-result[0], end=', ')
        print()
    for idx, user in enumerate(students):
        threading.Thread(target=user['browser'].close).start()
        #endThreads.append(threading.Thread(target=user['browser'].close))
        #endThreads[len(endThreads)-1].start()
        #if (idx%CORES) is (CORES-1):
        #    for t in endThreads:
        #        t.join()
        #    endThreads = []

def testing(idx, user):
    students[idx]['result'].append([time.time()])
    login(user)
    students[idx]['result'][0].append(time.time())
    students[idx]['result'].append([time.time()])
    submit(user)
    students[idx]['result'][1].append(time.time())
    students[idx]['result'].append([time.time()])
    getResult(user)
    students[idx]['result'][2].append(time.time())

#### TEST ####
prepare()
threads = []
for idx, user in enumerate(students):
    t = threading.Thread(target=testing, args=(idx, user))
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()
end()



