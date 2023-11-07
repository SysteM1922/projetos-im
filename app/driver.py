from colorclass import is_enabled
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

class Driver():

    def __init__(self):
        self.driver = webdriver.Chrome()
        
        self.driver.get("https://www.mercadao.pt/store/pingo-doce")
        self.driver.maximize_window()

        self.reject_cookies()

    def return_to_previous_page(self):
        self.driver.back()

    def scroll_down(self):
        self.driver.execute_script("window.scrollBy(0, 400);")

    def scroll_up(self):
        self.driver.execute_script("window.scrollBy(0, -400);")

    def add_to_cart(self, qty=1):
        add_to_cart_btn = self.driver.find_element(By.CSS_SELECTOR, ".pdo-add-btn")
        add_to_cart_btn.click()

    def search_product(self, product):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".pdo-navbar-search .clear > .pdo-inline-block > .ng-star-inserted").click()
        except:
            pass
        self.driver.find_element(By.ID, "search").send_keys(product)
        time.sleep(1)
        self.driver.find_element(By.ID, "search").send_keys(Keys.ENTER)

    def see_cart(self):
        check_cart_btn = self.driver.find_element(By.CSS_SELECTOR, "pdo-nav-cart > .pdo-button-cart")
        check_cart_btn.click()


    def filter_items(self, filter):
        if filter == "":
            self.driver.find_element(By.CSS_SELECTOR, ".filter-label > .pdo-block").click()
        else: 
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".dropdown-item:nth-child(2) .ui-radiobutton-label")
            except NoSuchElementException:
                print("No Such Element Exception")
                self.driver.find_element(By.CSS_SELECTOR, ".filter-label > .pdo-block").click()

            self.driver.find_element(By.CSS_SELECTOR, ".dropdown-item:nth-child({}) .ui-radiobutton-label".format(filter)).click()
            
    def checkout(self):
        checkout_btn = self.driver.find_element(By.CSS_SELECTOR, ".-cta")

        if not checkout_btn.is_enabled():
            print("Checkout button is not enabled")
            return

        checkout_btn.click()   

    def change_store(self, store: int):
        if store == "":
            self.driver.get("https://www.mercadao.pt")
        else:
            if store == 1:
                self.driver.get("https://www.mercadao.pt/store/pingo-doce")
            elif store == 2:
                self.driver.get("https://www.mercadao.pt/store/pingo-doce-madeira")
            elif store == 3:
                self.driver.get("https://www.mercadao.pt/store/solmar-acores")
            elif store == 4:
                self.driver.get("https://www.mercadao.pt/store/mercadao-solidario")
            elif store == 5:
                self.driver.get("https://www.mercadao.pt/store/bem-estar")
            elif store == 6:
                self.driver.get("https://www.mercadao.pt/store/medicamentos")


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