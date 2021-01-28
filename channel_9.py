from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time

HOME_PAGE = "https://channel9.msdn.com"
URL = HOME_PAGE + "/Series/Javascript-Fundamentals-Development-for-Absolute-Beginners?page=2"

if __name__=="__main__":
    opts = webdriver.ChromeOptions()
    binary_location = r"C:/chromium/chrome.exe"
    opts.binary_location = binary_location
    driver = webdriver.Chrome(options = opts)
    driver.get(URL)
    html = driver.page_source
    data = BeautifulSoup(html, "lxml")
    series_link = lambda tag: tag.has_attr("href") and tag.get("href").startswith("/Series")
    links = data.find_all(series_link)
    all_links = set()
    for link in links:
        link = link.get("href")
        driver.get(HOME_PAGE+link)
        time.sleep(3)

        try:
            download_div = driver.find_element_by_xpath("//section[@data-ch9tab_name='download']/h2")
            download_div.click()
            download_link = driver.find_element_by_partial_link_text("High Quality WMV")
            caption_link = driver.find_element_by_partial_link_text("English")
            all_links.add(caption_link.get_attribute("href"))
            all_links.add(download_link.get_attribute("href"))
            print(download_link.get_attribute("href"), caption_link.get_attribute("href"))
        except Exception as ex:
            print(ex)
            continue
    with open("links.txt",'w') as link_file:
        for i in all_links:
            link_file.write("%s\n" %(i))