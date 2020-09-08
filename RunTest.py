from Action.PageAction import *
from appium import webdriver
from Utils.GetDesiredcaps import getDesiredcaps
import time

desired_caps = getDesiredcaps()
#driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
open_app()
#driver.find_element_by_id("com.xsteach.appedu:id/content_rb_mine").click()
click("id","com.xsteach.appedu:id/content_rb_mine")
time.sleep(2)
#assert "我的学习轨迹" in driver.page_source
assert_string_in_pagesource("我的学习轨迹")
#driver.find_element_by_id("com.xsteach.appedu:id/tvLogin").click()
click("id","com.xsteach.appedu:id/tvLogin")
print("success")
