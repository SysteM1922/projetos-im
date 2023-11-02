from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class Driver():

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.page = self.driver.get("https://www.mercadao.pt/store/pingo-doce")
        self.driver.maximize_window()

        self.reject_cookies()

    def close(self):
        self.driver.close()

    def reject_cookies(self):
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id=\'onetrust-button-group\']/div[3]/button"))
            )
            button.click()
            self.driver.find_element(By.XPATH, "//div[@id=\'onetrust-pc-sdk\']/div/div[3]/div/button").click()   
        except TimeoutException:
            pass