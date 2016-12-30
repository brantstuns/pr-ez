import os
import sys
import re
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def getConfigData(configFile):
    r = re.compile("\: (.*)")
    config = []
    with open(configFile) as f:
        for line in f:
            result = r.search(line)
            if result:
                config.append(result.group(1))
            else:
                print '\n\nYou need to completely fill out config.txt for this to be ez :(\n\n'
                sys.exit()
    return config

def loginToGithub (u, p, driver):
    driver.get('https://github.com/login')
    driver.find_element_by_id('login_field').send_keys(u)
    driver.find_element_by_id('password').send_keys(p)
    driver.find_element_by_class_name('btn-primary').click()

def openNewPr(driver, githubRepo, assignees, branch):
    driver.get(githubRepo)
    driver.find_element_by_class_name('new-pull-request-btn').click()
    compareBranch = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[button//i[contains(text(), 'compare')]]"))
    )
    driver.find_element_by_xpath("//div[button//i[contains(text(), 'compare')]]").click()
    driver.find_elements_by_xpath("//*[contains(@id, 'commitish-filter-field')]")[1].send_keys(branch)
    driver.find_elements_by_xpath("//div[contains(text(), {0})]".format(branch))[1].click()
    for dev in assignees:
        print dev
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, '.sidebar-assignee'))
        )
        driver.find_elements_by_class_name('.sidebar-assignee')[1].click()
        print 'ok were here'
        driver.find_element_by_id('assignee-filter-field').send_keys(dev)
        driver.find_element_by_class_name('.navigation-focus').send_keys(Keys.RETURN)

def browserStuff(driver, gitCredentials, branch, configData):
    githubRepo = configData[0]
    assignees = configData[1].split(', ')
    print assignees
    try:
        loginToGithub(gitCredentials[0], gitCredentials[1], driver)
        openNewPr(driver, githubRepo, assignees, branch)
    except Exception as e:
        print 'Exception: ' + e.message

def main():
    config = getConfigData('config.txt')
    if len(sys.argv) == 1:
        branch = raw_input('\nEnter the name of the remote branch you want to open a Pull Request for (case matters): ')
    else:
        branch = sys.argv[1]

    gitEmail = raw_input('\nEnter your github email: ').lower().strip()
    gitPass = getpass.getpass(prompt = '\npassword (dont worry, this isnt stored anywhere and wont get echoed to the console): ')
    chromedriver = '/usr/local/bin/chromedriver'
    os.environ['webdriver.chrome.driver'] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    try:
        browserStuff(driver, [gitEmail, gitPass], branch, config)
    except Exception as err:
        print '\nException: ' + err.message
        driver.close()

main()