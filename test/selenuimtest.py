from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.layui.com/demo/admin.html")

# span = driver.find_element_by_xpath(".//span[contains(text(),'aaaa')]")
ss=driver.find_elements_by_class_name("layui-nav-item")[0]#
print(ss)