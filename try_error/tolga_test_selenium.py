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
#logging.info(f'{element}')
#print(element)
print('\n\n\n')
size=element.location
#print(location)
time.sleep(3)
action = webdriver.common.action_chains.ActionChains(driver)
action.move_to_element_with_offset(element, 0, 0)
action.click()
action.perform()
handles = driver.window_handles
size = len(handles)
#print(handles)
#print(size)
"""
def get_stats_from_window(num):
    driver.switch_to.window(handles[num])
    new_link = driver.current_url
    statistics1=new_link[:-7]+"statistics;1"
    print(statistics1)
    time.sleep(2)
    try:
        driver.get(statistics1)
        time.sleep(2)
        login_form=driver.find_element_by_xpath('//div[@id="tab-statistics-1-statistic"]')
    #    if login_form:
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
"""
#for i in range(1,size):
#    get_stats_from_window(i)


#"""
for i in range(0,270,23):
    action.move_to_element_with_offset(element, 0, i)
    action.click()
    action.perform()
    last_window=driver.window_handles[-1]
    driver.switch_to_window(last_window)
# FUNCTION GOES HERE
#    for i in range(1,size):
#        get_stats_from_window(i)
    # FUNCTION GOES HERE
    print('LAST WINDOW IS HERE:',last_window)
    print('\n\n\n')
    print(i)
    handles=list(driver.window_handles)
    print(handles)
    for i in reversed(range(len(handles))):
        if i == 0:
            break
        current_window=driver.window_handles[i]
        print('\n\n',i,current_window)
        handles.remove(current_window)
        time.sleep(3)
        driver.close()
    driver.switch_to_window(handles[0])
#    current_window = driver.current_window_handle
#    handles.remove(current_window)
#    driver.close()
#    driver.switch_to_window(handles[0])

#"""
