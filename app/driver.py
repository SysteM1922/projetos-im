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

        self.sendToVoice("Bem-vindo ao Mercadão")
        time.sleep(1)
        self.open_zip_code()

    def return_to_previous_page(self):
        self.driver.back()

    def scroll_down(self):
        self.driver.execute_script("window.scrollBy(0, 400);")

    def scroll_up(self):
        self.driver.execute_script("window.scrollBy(0, -400);")

    def add_to_cart(self, qty=1):
        if "/product/" not in self.driver.current_url:
            self.sendToVoice("Não é possível adicionar o produto que deseja nesta página.")
            return False
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
                self.sendToVoice("Não é possível adicionar o produto que deseja nesta página.")
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
            self.sendToVoice("Não é possível abrir o carrinho aqui.")
            return False
        return True

    def is_cart_open(self):
        if self.driver.find_element(By.XPATH, "//a[contains(text(),'Continuar a comprar')]").is_displayed:
            return True
        return False
            
    def close_cart(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".cart-back-icon > .ng-star-inserted").click()
        except:
            return False
        return True
    
    def clear_cart(self):
        
        if "-open" not in self.driver.find_element(By.TAG_NAME, "aside").get_attribute('class'):
            self.sendToVoice("O carrinho não está aberto")
            return False
        c = False
        while True:
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".pdo-icon-delete").click()
                c = True
            except:
                break
        if c:
            self.sendToVoice("Carrinho limpo com sucesso.")
            return True
        else:
            self.sendToVoice("O carrinho já está vazio.")
            return False
        
    
    def remove_from_cart(self, button, name):
        try:
            button.click()
            self.sendToVoice(f"{name} removido do carrinho com sucesso.")
        except:
            self.sendToVoice(f"Não é possível remover {name} do carrinho.")
            return False
        return True
    
    def change_category(self, name):
        print("Categoria: ", name)
        try:
            if name == "Voltar":
                self.driver.find_element(By.CSS_SELECTOR, ".sidebar-back > .pdo-middle").click()
                return True
            self.driver.find_element(By.XPATH, "//span[contains(.,'"+name+"')]").click()
        except:
            self.sendToVoice(f'Não é possível mudar para a categoria {name}.')
            return False
        return True

    def get_cart_products(self):
        items = []
        for item in self.driver.find_elements(By.TAG_NAME, "pdo-cart-summary-item"):
            if item.find_element(By.CSS_SELECTOR, ".summary-item-name").text not in ["", "Saco de Plástico Reciclado 85%"]:
                items.append([item.find_element(By.CSS_SELECTOR, ".summary-item-name").text.lower(), item.find_element(By.CSS_SELECTOR, ".item-remove-btn")])
        
        return items

    def open_zip_code(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".\_3db0T2TkzhslzgcJWQemKW .\_1c3YrH459HH65NxQxwOE90:nth-child(3) .pdo-svg").click()
            self.sendToVoice("Por favor insira o seu código postal.")
        except:
            self.sendToVoice("Não é possível alterar o código postal nesta página.")
            return False
        return True

    def insert_number(self, numbers):
        if self.driver.find_elements(By.XPATH, "//p[contains(.,'Insira o código-postal e comece a comprar!')]"):
            self.insert_zip_code(numbers)
        else:
            self.sendToVoice("Esta página não permite inserir números.")
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
            self.sendToVoice("Não existe código postal por confirmar.")
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
        if "-open" in self.driver.find_element(By.TAG_NAME, "aside").get_attribute('class'):
            self.sendToVoice("O carrinho já está aberto.")
            return False
        try:
            self.driver.find_element(By.CSS_SELECTOR, "pdo-nav-cart > .pdo-button-cart").click()
        except:
            self.sendToVoice("Não é possível abrir o carrinho aqui.")
            return False
        return True

    def sort_items(self, sort_opt: int = None):
        if sort_opt:
            if self.driver.find_elements(By.CSS_SELECTOR, ".filter-label > .pdo-block"):
                if not self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-item:nth-child(1) .ui-radiobutton-label"):
                    self.driver.find_element(By.CSS_SELECTOR, ".filter-label > .pdo-block").click()
                self.driver.find_element(By.CSS_SELECTOR, f".dropdown-item:nth-child({sort_opt}) .ui-radiobutton-label").click()
            else:
                self.sendToVoice("Não é possível ordernar nesta página.")
                return False
        else:
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".filter-label > .pdo-block").click()
            except:
                self.sendToVoice("Não é possível ordernar nesta página.")
                return False
        return True
            
    def checkout(self):
        if self.driver.find_elements(By.CSS_SELECTOR, ".-cta"):
            try:
                self.driver.find_elements(By.CSS_SELECTOR, ".-cta").click()
                self.sendToVoice("A proceder para o pagamento.")
            except:
                self.sendToVoice("O mínimo de compra para efectuar o checkout é de 60€.")
                return False
        else:
            self.sendToVoice("Não é possível efectuar checkout nesta página.")
            return False
        return True  

    def change_store(self, store: int = None):
        url = None
        msg = None
        if store:
            if store == 1:
                url = "https://www.mercadao.pt/store/pingo-doce"
                msg = "Loja alterada para Pingo Doce."
            elif store == 2:
                url = "https://www.mercadao.pt/store/pingo-doce-madeira"
                msg = "Loja alterada para Pingo Doce Madeira."
            elif store == 3:
                url = "https://www.mercadao.pt/store/solmar-acores"
                msg = "Loja alterada para Solmar Açores."
            elif store == 4:
                url = "https://www.mercadao.pt/store/mercadao-solidario"
                msg = "Loja alterada para Mercadão Solidário."
            elif store == 5:
                url = "https://www.mercadao.pt/store/bem-estar"
                msg = "Loja alterada para Saúde."
            elif store == 6:
                url = "https://www.mercadao.pt/store/medicamentos"
                msg = "Loja alterada para Medicamentos."
            else:
                return False

            self.driver.get(url)
            time.sleep(1)
            if self.driver.current_url == url:
                self.sendToVoice(msg)
            else:
                self.sendToVoice("Esta loja não está disponível para a sua localização.")
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

    def help(self, option = None):
        
        if option:
            if option == "carrinho" or option == "todas":
                self.sendToVoice("Ajuda com o carrinho.")
                self.sendToVoice("Pode adicionar a quantidade de produtos que desejar ao carrinho, desde que não ultrapasse as 30 unidades.")
                self.sendToVoice("Pode remover produtos do carrinho, ou limpar o carrinho todo.")
                self.sendToVoice("Abrir e fechar o carrinho, e efectuar o checkout dentro dele.")
                time.sleep(1)
            if option == "produto" or option == "todas":
                self.sendToVoice("Ajuda com os produtos.")
                self.sendToVoice("Pode pesquisar por produtos, e ordenar os produtos por relevância, promoções, nome, preço mais alto ou preço mais baixo.")
                self.sendToVoice("Pode filtrar os resultados por marca e categoria")
                self.sendToVoice("Pode adicionar a quantidade de produtos que pretende ao carrinho e abrir o carrinho para ver os produtos que lá estão.")
                self.sendToVoice("Pode remover produtos do carrinho, ou limpar o carrinho todo.")
                self.sendToVoice("Pode pesquisar pelo nome do produto ou pela categoria do produto.")
                self.sendToVoice("As categorias dos produtos encontram-se na lateral esquerda da página.")
                time.sleep(1)
            if option == "código postal" or option == "morada" or option == "todas":
                self.sendToVoice("Ajuda com o código postal/morada.")
                self.sendToVoice("Pode adicionar ou alterar o código postal sempre que quiser.")
                self.sendToVoice("Basta pedir para alterar o código postal e dizer o novo código postal.")
                self.sendToVoice("Atenção: a alteração do código postal pode implicar a mudança de loja e a limpeza do carrinho.")
                time.sleep(1)
            if option == "loja" or option == "todas":
                self.sendToVoice("Ajuda com a loja.")
                self.sendToVoice("Pode mudar de loja sempre que quiser.")
                self.sendToVoice("Basta pedir para mudar de loja e dizer o nome da loja.")
                self.sendToVoice("Atenção: algumas lojas não estão disponíveis para a sua localização.")
                time.sleep(1)
            if option == "operações" or option == "todas":
                self.sendToVoice("Ajuda com as operações.")
                self.sendToVoice("Pode voltar para a página anterior pedindo para voltar.")
                self.sendToVoice("Pode confirmar operaçoes pedindo para confirmar.")
                self.sendToVoice("Pode recusar operaçoes pedindo para cancelar.")
                self.sendToVoice("Pode andar para cima e para baixo na página pedindo para subir ou descer.")
                self.sendToVoice("Pode fechar o Mercadão pedindo para sair.")
                self.sendToVoice("Pode pedir pesquisar por voz pedindo para pesquisar.")
                self.sendToVoice("Pode ordenar e filtrar os resultados da pesquisa pedindo para ordenar ou filtrar.")
                self.sendToVoice("Pode navegar pelas categorias e secções pedindo para mudar de categoria ou secção.")
                self.sendToVoice("Pode fazer checkout pedindo para fazer checkout dentro do carrinho.")
                self.sendToVoice("Pode pedir mais ajudas sobre o carrinho, os produtos, o código postal ou morada e sobre as lojas.")
                self.sendToVoice("Pode pedir ajuda com as operações pedindo para ajuda.")
                time.sleep(1)

        else:
            self.sendToVoice("Bem-vindo ao Mercadão. Obrigado por solicitar ajuda.")
            self.sendToVoice("Posso ajudar com questões de interação por voz no site, nomeadamente sobre as lojas, os produtos, o carrinho, o código postal ou morada e com outras operações. Em que posso ajudar?")
        return True

    def close(self):
        self.driver.close()