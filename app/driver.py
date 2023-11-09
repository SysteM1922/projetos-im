from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

def do_nothing(message):
    pass

class Driver():

    def __init__(self, speak_func=do_nothing):
        self.driver = webdriver.Chrome()
        self.sendToVoice = speak_func

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
        if qty > 30:
            self.sendToVoice("Não é possível adicionar mais de 30 unidades de um produto ao carrinho.")
            return False
        try:
            add_one_btn = self.driver.find_element(By.CSS_SELECTOR, ".-add > .pdo-inline-block > .ng-star-inserted")
            for _ in range(qty):
                add_one_btn.click()
            self.sendToVoice(f"Produtos adicionados ao carrinho com sucesso.")
        except:
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".pdo-add-btn").click()
                time.sleep(1)
                if qty > 1:
                    add_one_btn = self.driver.find_element(By.CSS_SELECTOR, ".-add > .pdo-inline-block > .ng-star-inserted")
                    for _ in range(qty-1):
                        add_one_btn.click()
                    self.sendToVoice(f"Produtos adicionados ao carrinho com sucesso.")
                else:
                    self.sendToVoice(f"Produto adicionado ao carrinho com sucesso.")
            except:
                return False
        return True

    def search_product(self, product):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".pdo-navbar-search .clear > .pdo-inline-block > .ng-star-inserted").click()
        except:
            pass

        self.driver.find_element(By.ID, "search").send_keys(product)
        time.sleep(1)
        self.driver.find_element(By.ID, "search").send_keys(Keys.ENTER)
        return True

    def open_cart(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, "pdo-nav-cart > .pdo-button-cart").click()
        except:
            return False
        return True
            
    def close_cart(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".cart-back-icon > .ng-star-inserted").click()
        except:
            return False
        return True
    
    def clear_cart(self):
        if self.open_cart():
            time.sleep(1)
        while True:
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".pdo-icon-delete").click()
                self.sendToVoice("Carrinho limpo com sucesso.")
            except:
                break
        return self.close_cart()
    
    def remove_from_cart(self):
        items = self.driver.find_elements(By.CSS_SELECTOR, ".pdo-icon-delete")

    def open_zip_code(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".\_3db0T2TkzhslzgcJWQemKW .\_1c3YrH459HH65NxQxwOE90:nth-child(3) .pdo-svg").click()
            self.sendToVoice("Insira o seu código postal.")
        except:
            return False
        return True

    def insert_number(self, numbers):
        if self.driver.find_elements(By.XPATH, "//p[contains(.,'Insira o código-postal e comece a comprar!')]"):
            self.insert_zip_code(numbers)
        else:
            return False
        return True

    def clear_text(self):
        if self.driver.find_elements(By.XPATH, "//p[contains(.,'Insira o código-postal e comece a comprar!')]"):
            self.clear_zip_code()
        else:
            try:
                self.driver.find_element(By.ID, "search").clear()
            except:
                return False
        return True

    def insert_zip_code(self, numbers):
        try:
            for number in numbers:
                self.driver.find_element(By.ID, "postalCode").send_keys(number)
        except:
            return False
        return True

    def clear_zip_code(self):
        try:
            self.driver.find_element(By.ID, "postalCode").clear()
        except:
            return False
        return True

    def confirm_zip_code(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
            self.sendToVoice("Código postal atualizado com sucesso.")
        except:
            return False
        return True

    def close_zip_code(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".pdo-dismiss").click()
        except:
            try:
                if self.driver.find_element(By.XPATH, "//p[contains(.,'Ao mudar de morada o seu carrinho pode sofrer alterações!')]"):
                    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
                    time.sleep(1)
                    self.driver.find_element(By.CSS_SELECTOR, ".pdo-dismiss").click()
                else:
                    return False
            except:
                return False
        return True

    def affirm(self):
        if self.driver.find_elements(By.XPATH, "//p[contains(.,'Insira o código-postal e comece a comprar!')]"):
            self.confirm_zip_code()
        elif self.driver.find_elements(By.XPATH, "//p[contains(.,'Ao mudar de morada o seu carrinho pode sofrer alterações!')]"):
            self.confirm_zip_code()
        elif self.driver.find_elements(By.XPATH, "//p[contains(.,'A marca actual não existe para entrega nesta localização!')]"):
            self.confirm_zip_code()
        else:
            return False
        return True

    def open_cart(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, "pdo-nav-cart > .pdo-button-cart").click()
        except:
            return False
        return True

    def filter_items(self, filter: int = None):
        if filter:
            if self.driver.find_elements(By.CSS_SELECTOR, ".filter-label > .pdo-block"):
                if not self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-item:nth-child(1) .ui-radiobutton-label"):
                    self.driver.find_element(By.CSS_SELECTOR, ".filter-label > .pdo-block").click()
                self.driver.find_element(By.CSS_SELECTOR, f".dropdown-item:nth-child({filter}) .ui-radiobutton-label").click()
            else:
                return False
        else:
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".filter-label > .pdo-block").click()
            except:
                return False
        return True
            
    def checkout(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".-cta").click()
            self.sendToVoice("A iniciar checkout.")
        except:
            return False
        return True  

    def change_store(self, store: int = None):
        if store:
            print(store)
            if store == 1:
                self.driver.get("https://www.mercadao.pt/store/pingo-doce")
                self.sendToVoice("Loja alterada para Pingo Doce.")
            elif store == 2:
                self.driver.get("https://www.mercadao.pt/store/pingo-doce-madeira")
                self.sendToVoice("Loja alterada para Pingo Doce Madeira.")
            elif store == 3:
                self.driver.get("https://www.mercadao.pt/store/solmar-acores")
                self.sendToVoice("Loja alterada para Solmar Açores.")
            elif store == 4:
                self.driver.get("https://www.mercadao.pt/store/mercadao-solidario")
                self.sendToVoice("Loja alterada para Mercadão Solidário.")
            elif store == 5:
                self.driver.get("https://www.mercadao.pt/store/bem-estar")
                self.sendToVoice("Loja alterada para Saúde.")
            elif store == 6:
                self.driver.get("https://www.mercadao.pt/store/medicamentos")
                self.sendToVoice("Loja alterada para Medicamentos.")
            else:
                return False
        else:
            self.driver.get("https://www.mercadao.pt")
            self.sendToVoice("Por favor escolha uma loja.")
        return True

    def quit(self):
        if self.close_cart() or self.close_zip_code():
            self.sendToVoice("A sair do Mercadão.")
            return False
        return True

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