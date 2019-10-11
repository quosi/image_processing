from selenium import webdriver
import time
import numpy as np
import logging
# coordinates (type to terminal):
# while true; do clear; xdotool getmouselocation; sleep 0.1; done

driver = webdriver.Chrome()
driver.get("https://www.soccerstand.com/team/amiens-sc/lKkBAsxF/results/")
#driver.get("https://www.soccerstand.com/team/aumund-vegesack/AJB2Rj20/results/")
element=driver.find_element_by_class_name('padr')
location=element.location
size=element.location
time.sleep(3)
action = webdriver.common.action_chains.ActionChains(driver)
action.move_to_element_with_offset(element, 0, 0)
action.click()
action.perform()
handles = driver.window_handles
size = len(handles)

def get_stats_from_window(handle_number):
    driver.switch_to.window(handle_number)
    new_link = driver.current_url
    statistics1=new_link[:-7]+"statistics;1"
    print(statistics1)
    time.sleep(2)
    try:
        driver.get(statistics1)
        time.sleep(2)
        login_form=driver.find_element_by_xpath('//div[@id="tab-statistics-1-statistic"]')
        statistics1=login_form.text
        print(statistics1)
        f = open('half', 'w')
        f.write(statistics1)
        f.close()

        new_link = driver.current_url
        statistics2=new_link[:-7]+"statistics;0"
        print(statistics2)
        time.sleep(2)
        driver.get(statistics2)
        time.sleep(2)
        login_form=driver.find_element_by_xpath('//div[@id="tab-statistics-0-statistic"]')
        statistics2=login_form.text
        print(statistics2)
        f = open('end', 'w')
        f.write(statistics2)
        f.close()

        new_link = driver.current_url
        goals=new_link[:-12]+"summary"
        print(goals)
        time.sleep(2)
        driver.get(goals)
        time.sleep(2)
        login_form=driver.find_element_by_xpath('//div[@id="summary-content"]')
        goals=login_form.text
        print(goals)
        f = open('goal', 'w')
        f.write(goals)
        f.close()

        new_link = driver.current_url
        info=new_link[:-12]+"summary"
        print(info)
        time.sleep(3)
        driver.get(info)
        time.sleep(3)
        login_form=driver.find_element_by_xpath('//td[@id="flashscore_column"]')
        info=login_form.text
        print(info)
        f = open('info', 'w')
        f.write(info)
        f.close()

    except:
        print("No Statistics for this game!!!")

#"""
for i in range(0,70,23):
    action.move_to_element_with_offset(element, 0, i)
    action.click()
    action.perform()
    last_window=driver.window_handles[-1]
    driver.switch_to_window(last_window)
    time.sleep(3)
    current_window = driver.current_window_handle
    print('LAST WINDOW IS HERE:',last_window)
    print('CURRENT WINDOW IS HERE:',current_window)
    print('\n\n\n')
    print(i)
    time.sleep(4)
    handles=list(driver.window_handles)
    print('NUMBER OF WINDOWS OPEN:',len(handles))
    get_stats_from_window(last_window)
    driver.close()
    handles=list(driver.window_handles)
    print('NUMBER OF WINDOWS OPEN AFTER DRIVER CLOSE:',len(handles))
    driver.switch_to_window(handles[0])
driver.quit()
"""
    for i in reversed(range(len(handles))):
        if i == 0:
            break
        current_window=driver.window_handles[i]
        print('\n\n',i,current_window)
        handles.remove(current_window)
        time.sleep(3)
        driver.close()
"""
