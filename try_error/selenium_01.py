from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import logging
# coordinates (type to terminal):
# while true; do clear; xdotool getmouselocation; sleep 0.1; done

driver = webdriver.Firefox()
driver.get("https://film-grab.com/category/1-851/")
# assert "Python" in driver.title

elements=driver.find_elements_by_tag_name('a')
img_elements = driver.find_elements_by_xpath("//figure[@class='entry-thumb-content']")
ele = []
ele = [x.text for x in list(elements)]# print out all the titles.print('titles:')
img_ele = [x.text for x in list(img_elements)]
print(ele, '\n')
len(ele)
ele


element.send_keys(Keys.ARROW_DOWN)
element.clear()

location=element.location
action = webdriver.common.action_chains.ActionChains(driver)
action.move_to_element_with_offset(element, 960, 300)   # 280, 610 first image-click
action.click()
action.perform()
handles = driver.window_handles
size = len(handles)

# driver.switch_to.window(handle_number)
# new_link = driver.current_url
# statistics1=new_link[:-7]+"statistics;1"
# print(statistics1)

time.sleep(2)
driver.quit()
