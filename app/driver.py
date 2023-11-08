from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

class Driver():

    def __init__(self):
        self.driver = webdriver.Chrome()
        
        self.driver.get("https://www.mercadao.pt/store/pingo-doce")
        self.driver.maximize_window()

        self.reject_cookies()

        self.open_zip_code()

    def return_to_previous_page(self):
        self.driver.back()

    def scroll_down(self):
        self.driver.execute_script("window.scrollBy(0, 400);")

    def scroll_up(self):
        self.driver.execute_script("window.scrollBy(0, -400);")

    def add_to_cart(self, qty=1):
        try:
            add_one_btn = self.driver.find_element(By.CSS_SELECTOR, ".-add > .pdo-inline-block > .ng-star-inserted")
            for _ in range(qty):
                add_one_btn.click()
        except:
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".pdo-add-btn").click()
                time.sleep(1)
                if qty > 1:
                    add_one_btn = self.driver.find_element(By.CSS_SELECTOR, ".-add > .pdo-inline-block > .ng-star-inserted")
                    for _ in range(qty-1):
                        add_one_btn.click()
            except:
                pass

    def search_product(self, product):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".pdo-navbar-search .clear > .pdo-inline-block > .ng-star-inserted").click()
        except:
            pass

        self.driver.find_element(By.ID, "search").send_keys(product)
        time.sleep(1)
        self.driver.find_element(By.ID, "search").send_keys(Keys.ENTER)

    def open_cart(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, "pdo-nav-cart > .pdo-button-cart").click()
        except:
            pass
            
    def close_cart(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".cart-back-icon > .ng-star-inserted").click()
        except:
            pass

    def open_zip_code(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".\_3db0T2TkzhslzgcJWQemKW .\_1c3YrH459HH65NxQxwOE90:nth-child(3) .pdo-svg").click()
        except:
            pass

    def insert_number(self, number):
        if self.driver.find_element(By.XPATH, "//p[contains(.,'Insira o código-postal e comece a comprar!')]"):
            self.insert_zip_code(number)
        else:
            pass

    def clear_text(self):
        if self.driver.find_element(By.XPATH, "//p[contains(.,'Insira o código-postal e comece a comprar!')]"):
            self.clear_zip_code()
        else:
            pass

    def insert_zip_code(self, zip_code):
        try:
            self.driver.find_element(By.ID, "postalCode").send_keys(zip_code)
        except:
            pass

    def clear_zip_code(self):
        try:
            self.driver.find_element(By.ID, "postalCode").clear()
        except:
            pass

    def confirm_zip_code(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        except:
            pass

    def close_zip_code(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".pdo-modal-backdrop").click()
        except:
            pass

    def affirm(self):
        if self.driver.find_element(By.XPATH, "//p[contains(.,'Insira o código-postal e comece a comprar!')]"):
            self.confirm_zip_code()
        elif self.driver.find_element(By.XPATH, "//p[contains(.,'Ao mudar de morada o seu carrinho pode sofrer alterações!')]"):
            self.confirm_zip_code()
        else:
            pass

    def reject_cookies(self):
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id=\'onetrust-button-group\']/div[3]/button"))
            )
            button.click()
            self.driver.find_element(By.XPATH, "//div[@id=\'onetrust-pc-sdk\']/div/div[3]/div/button").click()   
        except TimeoutException:
            pass

    def close(self):
        self.driver.close()