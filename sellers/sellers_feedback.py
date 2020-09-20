from datetime import datetime
import selenium
from selenium import webdriver
from dateparser.search import search_dates
import time
from selenium.webdriver.common.by import By


class SellerFeedbackScraper:
    def __init__(self):
        self.driver = webdriver.PhantomJS('C:/Program Files/phantomjs-2.1.1-windows/bin/phantomjs.exe')

    def scrape(self, seller_id):
        self.driver.get("https://www.amazon.com/sp?seller=" + str(seller_id))
        feedback_list = self.parse()

    def parse(self):
        next_page = True
        while next_page:
            try:
                feedback_list = []
                table_id = self.driver.find_element_by_xpath("//*[@id='feedback-table']")
                # get all of the rows in the table
                rows = table_id.find_elements_by_xpath(".//tr[@class='feedback-row']")
                for row in rows:
                    feedback = {}
                    rating_string = row.find_element_by_xpath(".//th/div/i/span").get_attribute("innerHTML")
                    feedback['rating'] = int(rating_string.split(' ')[0])
                    col_2 = row.find_element(By.TAG_NAME, "td")
                    feedback['text'] = col_2.find_element_by_xpath('.//*[@id="-text" or @id="-expanded"]'
                                                                   ).get_attribute("innerHTML")
                    try:
                        div = col_2.find_element_by_xpath(".//*[@class='a-section a-spacing-top-small feedback-suppressed']")
                        value = div.value_of_css_property("display")
                        if value == 'none':
                            feedback['deleted'] = 0
                        else:
                            feedback['deleted'] = 1
                    except selenium.common.exceptions.NoSuchElementException:
                        feedback['deleted'] = 0
                    s = col_2.find_element_by_xpath('.//div/div[2]/span').text
                    date = search_dates(s, settings={'TIMEZONE': 'UTC'})[0][1].date()
                    if date is None or date > datetime.today().date():
                        feedback['date'] = ""
                    else:
                        feedback['date'] = str(date)
                    feedback_list.append(feedback)
                self.driver.find_element_by_xpath("//*[@id='feedback-next-link']").click()
                time.sleep(10)
            except selenium.common.exceptions.ElementNotVisibleException:
                next_page = False
        return feedback_list
