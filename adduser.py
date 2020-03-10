#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import csv

# set address
f = open("./address.txt", 'r')
ADDR = f.readline().replace("\n","")
print("server address is "+ADDR)
f.close()

# set admin
f = open("./admin.txt", 'r')
admin_id = f.readline().replace("\n","")
admin_pw = f.readline().replace("\n","")
f.close()
print("admin id/pw loaded")

browser = webdriver.Firefox()
#browser.get("https://naver.com")


# Admin login
browser.get(ADDR+"/login")
browser.find_element_by_name('_username').send_keys(admin_id)
browser.find_element_by_name('_password').send_keys(admin_pw)
browser.find_element_by_xpath('//*[@id="loginform"]/div/form/button').click()

# Go to Users menu
#browser.find_element_by_xpath('/html/body/div/div/div/div/div[1]/div[1]/div[2]/ul/li[7]/a').click()


categories = {}
teams = {}

###
# Get Information from webpage
###

def team_update():
    browser.get(ADDR+"/jury/teams")
    tbody = browser.find_element_by_xpath('//*[@id="DataTables_Table_0"]/tbody')
    trs=tbody.find_elements_by_tag_name('tr')
    for tr in trs:
        tds = tr.find_elements_by_tag_name('td')
        name = tds[2].text
        teams[name] = {}
        teams[name]["ID"]=tds[0].text
        teams[name]["externalid"]=tds[1].text
        teams[name]["category"]=tds[3].text
        teams[name]["NumOfContents"]=tds[5].text
    print(teams)


def category_update():
    browser.get(ADDR+"/jury/categories")
    tbody = browser.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/table/tbody')
    trs=tbody.find_elements_by_tag_name('tr')
    for tr in trs:
        tds = tr.find_elements_by_tag_name('td')
        name = tds[2].text
        categories[name] = {}
        categories[name]["ID"]=tds[0].text
        categories[name]["sort"]=tds[1].text
        categories[name]["NumOfTeams"]=tds[3].text
        categories[name]["visible"]=tds[4].text
    print(categories)


###
# automatically add to domjudge
###

# Add Category
def add_category(name):
    browser.get(ADDR+"/jury/categories/add")
    browser.find_element_by_xpath('//*[@id="team_category_name"]').send_keys(name)
    browser.find_element_by_xpath('//*[@id="team_category_save"]').click()
    category_update()


# Add Team
def add_team(externalid, name, category):
    browser.get(ADDR+"/jury/teams/add")
    browser.find_element_by_name('team[externalid]').send_keys(externalid)
    browser.find_element_by_name('team[name]').send_keys(name)
    Select(browser.find_element_by_xpath('//*[@id="team_category"]')).select_by_visible_text(category)# 카테고리 선택
    browser.find_element_by_xpath('/html/body/div/div/div/div/div/form/div[10]/div/label').click()
    browser.find_element_by_xpath('/html/body/div/div/div/div/div/form/div[12]/button').click()
    #team_update()


# Add User
def add_user(username, name, email, plainPassword, team):
    browser.get(ADDR+"/jury/users/add")
    browser.find_element_by_name('user[username]').send_keys(username)
    browser.find_element_by_name('user[name]').send_keys(name)
    browser.find_element_by_name('user[email]').send_keys(email)
    browser.find_element_by_name('user[plainPassword]').send_keys(plainPassword)
    Select(browser.find_element_by_xpath('//*[@id="user_team"]')).select_by_visible_text(team)
    browser.find_element_by_xpath('//*[@id="user_user_roles"]/div[3]/label').click()
    browser.find_element_by_xpath('//*[@id="user_save"]').click()

print("Category Update")
category_update()
print("Team Update")
team_update()
#add_category('aaa')
#add_team('aaa','aaa','aaa')
#add_user('aaa','aaa','a@a.a', 'aaa','aaa')


# Open csv file which contains user information
with open('users.csv') as usercsv:
    spamreader = csv.reader(usercsv, delimiter=',', quotechar='|')
    for row in spamreader:
        print(row)
        category = row[0]
        login = row[1]
        fullname = row[2]
        email = row[3]
        password = row[4]
        # Check Category exists
        if category not in categories.keys():
            add_category(category)

        # Go to Add team
        add_team(login, fullname, category)
        
        # Go to Add user
        add_user(login, fullname, email, password, fullname)
browser.close()
