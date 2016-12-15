import os
import sys
import re
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getConfigData(configFile):
    r = re.compile("\: (.*)")
    config = [r.search(config.rstrip('\n')).group(1) for config in open(configFile)]
    print config
    if None in config:
        print '\n\nYou need to completely fill out config.txt for this to be ez :(\n\n'
        sys.exit()
    else:
        return config

def loginToGithub (u, p, driver):
    driver.get('https://github.com/login')
    driver.find_element_by_id('login_field').send_keys(u)
    driver.find_element_by_id('password').send_keys(p)
    driver.find_element_by_class_name('btn-primary').click()

def openNewPr(driver, githubRepo, assignees):
    driver.get(githubRepo)
    driver.find_element_by_class_name('new-pull-request-btn').click()
    compareBranch = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'compare'))
    )
    driver.find('compare').click()
    print 'yo2'

def browserStuff(driver, gitCredentials):
    configData = getConfigData('config.txt')
    githubRepo = configData[0]
    assignees = configData[1].split(', ')
    try:
        loginToGithub(gitCredentials[0], gitCredentials[1], driver)
        openNewPr(driver, githubRepo, assignees)
    except Exception as e:
        print 'Exception: ' + e.message


def main():
    if raw_input('\nWant to make this PR really easy? ').lower().startswith('n'):
        sys.exit()
    gitEmail = raw_input('\nEnter your github email: ').lower().strip()
    gitPass = getpass.getpass(prompt = 'password (dont worry, this isnt stored anywhere and wont get echoed to the console): ')
    chromedriver = '/usr/local/bin/chromedriver'
    os.environ['webdriver.chrome.driver'] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    try:
        browserStuff(driver, [gitEmail, gitPass])
    except Exception as err:
        print 'Exception: ' + err.message
        driver.close()

main()
