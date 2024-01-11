from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
from enums import CategoryPage, Direction
from selenium.webdriver.common.action_chains import ActionChains

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

        # Gesture variables

        self.current_side_bar_index = None
        self.last_category = CategoryPage.MAIN
        self.last_element = None

        self.current_product_index = None
        self.current_product_row = 0
        self.last_product = None

        self.last_timestamp = str(time.time())
        self.last_url = ""

        self.on_categories = False
        self.on_products = False

    def return_to_previous_page(self):
        self.driver.back()

    def scroll_down(self):
        for _ in range(8):
            self.driver.execute_script("window.scrollBy(0, 50);")

    def scroll_up(self):
        for _ in range(8):
            self.driver.execute_script("window.scrollBy(0, -50);")

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

    def confirm(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
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
            if self.confirm():
                self.sendToVoice("Código postal atualizado com sucesso.")
                return True
            else:
                self.sendToVoice("Não existe código postal por confirmar.")
                return False
        elif self.driver.find_elements(By.XPATH, "//p[contains(.,'Ao mudar de morada o seu carrinho pode sofrer alterações!')]"):
            return self.confirm()
        elif self.driver.find_elements(By.XPATH, "//p[contains(.,'A marca actual não existe para entrega nesta localização!')]"):
            return self.confirm()
        return False

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

    def choose_position(self, position: int = None):
        if position:
            try:
                self.driver.find_element(By.CSS_SELECTOR, f".dropdown-item:nth-child({position}) .ui-chkbox-icon").click()
            except:
                self.sendToVoice("Essa opção não existe.")
                return False
        else:
            self.sendToVoice("Desculpe, não entendi a opção.")
            return False
        return True
    
    def filter_products(self, filter_opt: int = None, position: int = None):
        if filter_opt:
            if filter_opt == "marca":
                try:
                    self.driver.find_element(By.CSS_SELECTOR, ".pdo-block > .pdo-dropdown-filter .pdo-block").click()
                    if position:
                        time.sleep(1)
                        self.choose_position(position)
                except:
                    self.sendToVoice("Não é possível filtrar nesta página.")
                    return False
            elif filter_opt == "categoria":
                try:
                    self.driver.find_element(By.CSS_SELECTOR, ".filter-column:nth-child(3) .pdo-block").click()
                except:
                    self.sendToVoice("Não é possível filtrar nesta página.")
                    return False
        else:
            self.sendToVoice("Por favor escolha um filtro entre Marca e Categoria")
            
    def checkout(self):
        if "-open" in self.driver.find_element(By.TAG_NAME, "aside").get_attribute('class'):
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".-cta").click()
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
                msg = "Loja alterada para Pingo Doce Solmar Açores."
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
            time.sleep(2)
            if self.driver.current_url == url:
                self.sendToVoice(msg)
            else:
                self.sendToVoice("Esta loja não está disponível para a sua localização.")
                return False
        else:
            self.driver.get("https://www.mercadao.pt")
            self.sendToVoice("Por favor escolha uma loja.")
        return True
    
    def get_visible_products(self):
        # Execute um script JavaScript para obter os elementos visíveis
        script = """
            var elements = document.querySelectorAll('{}');
            var visibleElements = [];
            for (var i = 0; i < elements.length; i++) {{
                var element = elements[i];
                var rect = element.getBoundingClientRect();
                var isVisible = (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
                );
                if (isVisible) {{
                    visibleElements.push(element);
                }}
            }}
            return visibleElements;
        """.format("pdo-product-item")

        elements = self.driver.execute_script(script)
        return [element.find_element(By.TAG_NAME, "h3") for element in elements]
    
    def open_product(self, product, button):
        try:
            button.click()
            self.sendToVoice(f"A abrir {product}.")
        except:
            self.sendToVoice(f"Não é possível abrir {product}.")
            return False
        return True

    def quit(self):
        if self.close_cart() or self.close_zip_code():
            return False
        self.sendToVoice("A sair do Mercadão.")
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
                self.sendToVoice("Ajuda com o carrinho."+
                                "Pode adicionar a quantidade de produtos que desejar ao carrinho, desde que não ultrapasse as 30 unidades."+
                                "Pode remover produtos do carrinho, ou limpar o carrinho todo."+
                                "Abrir e fechar o carrinho, e efectuar o checkout dentro dele.")
                time.sleep(1)
            if option == "produto" or option == "todas":
                self.sendToVoice("Ajuda com os produtos."+
                                "Pode pesquisar por produtos, e ordenar os produtos por relevância, promoções, nome, preço mais alto ou preço mais baixo."+
                                "Pode filtrar os resultados por marca e categoria"+
                                "Pode adicionar a quantidade de produtos que pretende ao carrinho e abrir o carrinho para ver os produtos que lá estão."+
                                "Pode remover produtos do carrinho, ou limpar o carrinho todo."+
                                "Pode pesquisar pelo nome do produto ou pela categoria do produto."+
                                "As categorias dos produtos encontram-se na lateral esquerda da página.")
                time.sleep(1)
            if option == "código postal" or option == "morada" or option == "todas":
                self.sendToVoice("Ajuda com o código postal/morada."+
                                "Pode adicionar ou alterar o código postal sempre que quiser."+
                                "Basta pedir para alterar o código postal e dizer o novo código postal."+
                                "Atenção: a alteração do código postal pode implicar a mudança de loja e a limpeza do carrinho.")
                time.sleep(1)
            if option == "loja" or option == "todas":
                self.sendToVoice("Ajuda com a loja."+
                                "Pode mudar de loja sempre que quiser."+
                                "Basta pedir para mudar de loja e dizer o nome da loja."+
                                "Atenção: algumas lojas não estão disponíveis para a sua localização.")
                time.sleep(1)
            if option == "operações" or option == "todas":
                self.sendToVoice("Ajuda com as operações."+
                                "Pode voltar para a página anterior pedindo para voltar."+
                                "Pode confirmar operaçoes pedindo para confirmar."+
                                "Pode recusar operaçoes pedindo para cancelar."+
                                "Pode andar para cima e para baixo na página pedindo para subir ou descer."+
                                "Pode fechar o Mercadão pedindo para sair."+
                                "Pode pedir pesquisar por voz pedindo para pesquisar."+
                                "Pode ordenar os resultados da pesquisa pedindo para ordenar."+
                                "Pode filtrar os resultados da pesquisa pedindo para filtrar pela posição da marca ou categoria."+
                                "Pode navegar pelas categorias e secções pedindo para mudar de categoria ou secção."+
                                "Pode fazer checkout pedindo para fazer checkout dentro do carrinho."+
                                "Pode pedir mais ajudas sobre o carrinho, os produtos, o código postal ou morada e sobre as lojas."+
                                "Pode pedir ajuda com as operações pedindo para ajuda.")
                time.sleep(1)

        else:
            self.sendToVoice("Bem-vindo ao Mercadão. Obrigado por solicitar ajuda."+
                             "Posso ajudar com questões de interação por voz no site, nomeadamente sobre as lojas, os produtos, o carrinho, o código postal ou morada e com outras operações."+
                             "Em que posso ajudar?")
        return True

    def close(self):
        self.driver.close()

    def get_categories(self):
        sidebar = self.driver.find_elements(By.CLASS_NAME, "pdo-store-sidebar")
        if any([element.text for element in sidebar[2].find_elements(By.TAG_NAME, "a")]):
            return CategoryPage.SECONDARY, sidebar[2].find_elements(By.TAG_NAME, "a")
        else:
            return CategoryPage.MAIN, sidebar[1].find_elements(By.TAG_NAME, "a")
        
    def unmark_element(self):
        if self.last_element:
            try:
                self.driver.execute_script("arguments[0].style.border='0px solid red'", self.last_element)
                self.last_element = None
            except:
                return False
        return True
    
    def unmark_product(self):
        if self.last_product:
            try:
                self.driver.execute_script("arguments[0].style.border='0px solid red'", self.last_product)
                self.last_product = None
            except:
                return False
        return True
        
    def navigate_to_element(self, element, direction):
        try:
            if direction == Direction.LEFT or direction == Direction.RIGHT:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
            else:
                window_height = self.driver.get_window_size()['height']
                element_y = element.location['y']
                scroll_position = element_y - window_height/4
                self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        except:
            return False
        return True

    def check_page_change(self):
        self.on_categories = False
        self.on_products = False
        stored_timestamp = self.driver.execute_script("return window.control_timestamp")
        if stored_timestamp != self.last_timestamp or self.last_url != self.driver.current_url:
            self.current_side_bar_index = None
            self.current_product_index = None
            self.current_product_row = 0
            self.unmark_element()
            self.unmark_product()
        self.last_url = self.driver.current_url
        self.last_timestamp = str(time.time())
        self.driver.execute_script("window.control_timestamp = arguments[0]", self.last_timestamp)
    
    def get_products(self):
        rows = self.driver.find_elements(By.CLASS_NAME, "pdo-products-slider")
        products = []
        if len(rows) > 1:
            for row in rows:
                products.append(row.find_elements(By.TAG_NAME, "pdo-product-item"))
        else:
            products.append(self.driver.find_elements(By.TAG_NAME, "pdo-product-item"))
        return products
    
    def change_category_gestures(self, direction: Direction):
        self.check_page_change()
        self.on_categories = True
        try:
            self.unmark_element()
            page, sidebar = self.get_categories()
            if page == self.last_category:
                if self.current_side_bar_index == None:
                    self.current_side_bar_index = 0
                elif self.current_side_bar_index == 0 and direction == Direction.UP:
                    self.current_side_bar_index = None
                    self.on_categories = False
                    return True
                elif self.current_side_bar_index == len(sidebar)-1 and direction == Direction.DOWN:
                    pass
                else:
                    if direction == Direction.UP:
                        self.current_side_bar_index -= 1
                    elif direction == Direction.DOWN:
                        self.current_side_bar_index += 1
            else:
                self.current_side_bar_index = 0
                self.last_category = page
            self.last_element = sidebar[self.current_side_bar_index]
            self.driver.execute_script("arguments[0].style.border='3px solid red'", self.last_element)
        except:
            self.sendToVoice("Não foi possível mudar de categoria.")
            return False
        return True
    
    def change_product_gestures(self, direction: Direction):
        self.check_page_change()
        self.on_products = True
        try:
            self.unmark_product()
            products = self.get_products()
            if self.current_product_index == None:
                self.current_product_index = 0
            elif direction == Direction.LEFT and self.current_product_index == 0:
                self.current_product_index = None
                self.on_products = False
                return True
            elif direction == Direction.RIGHT and self.current_product_index == len(products[self.current_product_row])-1:
                pass
            elif len(products) == 1:
                if direction == Direction.UP and self.current_product_index - 5 < 0:
                    self.current_product_index = None
                    self.on_products = False
                    return True
                elif direction == Direction.DOWN and self.current_product_index + 5 > len(products[self.current_product_row])-1:
                    pass
                else:
                    if direction == Direction.LEFT:
                        self.current_product_index -= 1
                    elif direction == Direction.RIGHT:
                        self.current_product_index += 1
                    elif direction == Direction.UP:
                        self.current_product_index -= 5
                    elif direction == Direction.DOWN:
                        self.current_product_index += 5
            elif len(products) > 1:
                if direction == Direction.LEFT:
                    self.current_product_index -= 1
                elif direction == Direction.RIGHT:
                    self.current_product_index += 1
                elif direction == Direction.UP:
                    if self.current_product_row == 0:
                        self.current_product_index = None
                        self.on_products = False
                        return True
                    else:
                        self.current_product_row -= 1
                        self.current_product_index = 0
                elif direction == Direction.DOWN:
                    if self.current_product_row == len(products)-1:
                        pass
                    else:
                        self.current_product_row += 1
                        self.current_product_index = 0
            self.last_product = products[self.current_product_row][self.current_product_index]
            self.navigate_to_element(self.last_product, direction)
            self.driver.execute_script("arguments[0].style.border='3px solid red'", self.last_product)
        except:
            if self.last_product == None:
                self.unmark_product()
                self.on_products = False
                self.current_product_index = None
                self.current_product_row = 0
            else:
                self.sendToVoice("Não foi possível mudar de produto.")

            return False
        return True
        
    def help_gestures(self):
        self.sendToVoice("Bem-vindo ao Mercadão. Obrigado por solicitar ajuda."+
                        "Pode utilizar o braço esquerdo para navegar pelas categorias e o braço direito para navegar pelos produtos e pela página deslizando para cima e para baixo"+
                        "Pode navegar pela lista de produtos abrindo ligeiramente os braços para os lados"+
                        "Com o braço direito pode simular um trasnporte da esquerda para a direita para adicionar ao carrinho"+
                        "Pode empurrar para a frente para abrir uma categoria ou para abrir um produto"+
                        "Pode bater continência para sair do Mercadão"+
                        "Pode levantar colocar a mão esquerda na orelha e levantar o braço direito novamente se precisar de ajuda novamente")
        
    def press(self):
        if self.on_categories:
            try:
                self.last_element.click()
                self.sendToVoice("A abrir a categoria.")
            except:
                self.sendToVoice("Não foi possível abrir a categoria.")
                return False
        elif self.on_products:
            try:
                self.last_product.click()
                self.sendToVoice("A abrir o produto.")
            except:
                self.sendToVoice("Não foi possível abrir o produto.")
                return False
        else:
            self.sendToVoice("Não existe nada selecionado para abrir.")
            return False
        time.sleep(1)
        self.check_page_change()
        return True
        
    def scroll_down_gestures(self):
        if self.on_products or self.last_product != None:
            return self.change_product_gestures(Direction.DOWN)
        else:
            self.scroll_down()
            return True
    
    def scroll_up_gestures(self):
        if self.on_products or self.last_product != None:
            return self.change_product_gestures(Direction.UP)
        else:
            self.scroll_up()
            return True
        

            
        
    