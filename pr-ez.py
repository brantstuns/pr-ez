import os
import sys
import re
import getpass
from selenium import webdriver

def getConfigData(configFile):
    r = re.compile("\: (.*)")
    config = [r.search(config.rstrip('\n')).strip() for config in open(configFile)]
    if '' in config:
        print '\n\nYou need to completely fill out config.txt :( for this to be ez\n\n'
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
    driver.find_element_by_link_text('compare:').click()


def browserStuff(driver, gitCredentials):
    configData = getConfigData('config.txt')
    githubRepo = configData[0]
    assignees = configData[1]
    loginToGithub(gitCredentials[0], gitCredentials[1], driver)
    openNewPr(driver, githubRepo, assignees)

def main():
    if raw_input('\nWant to make this PR really easy? ').lower() in ['n', 'no', 'nope', 'maybe?', 'not this time']:
        sys.exit()
    print '\nEnter your github email: '
    gitCreds = getpass.getuser()
    print "\nEnter you github password (don't worry, this isn't stored anywhere and it wont echo to your shell): "
    gitCreds.append(getpass.getpass(prompt = ': '))

    chromedriver = '/usr/local/bin/chromedriver'
    os.environ['webdriver.chrome.driver'] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    try:
        browserStuff(driver, gitCreds)
    except Exception as err:
        print 'Exception: ' + err
        driver.close()

main()
