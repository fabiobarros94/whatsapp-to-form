import clipboard
import logging
import os
import pyautogui
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import time

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
current_year = datetime.now().year
current_day = datetime.now().day
current_month = datetime.now().month

# Configurar o logging 
logging.basicConfig(filename='whatsapp_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

load_dotenv()

def click_element_by_label(label_text): 
    print("\nClick element by label")
    while True: 
        try: # Localizar a label pelo texto   
            label = driver.find_element(By.XPATH, "//label[text()='Data Inicial']")
            print("Achou a label!")
            input_element = label.find_element(By.XPATH, ".//input")
            input_element.send_keys("19/12/2024")
            # associated_element_id = label.get_attribute("for") 
            # associated_element_xpath = f"//*[@id='{associated_element_id}']" # Localizar e clicar no elemento de entrada associado 
            # associated_element = WebDriverWait(driver, 10).until( 
            #     EC.element_to_be_clickable((By.XPATH, associated_element_xpath)) 
            # ) 
            # associated_element.click() 
            return label #associated_element_xpath # Retornar o XPath do elemento associado 
        except Exception as e: print(f"Erro: {e}. Tentando novamente...") # Mensagem de erro para depuração 
        time.sleep(1)

def find_and_insert(data): 
    print("\nFind and insert")
    while True: 
        try: # Localizar a label pelo texto
            elements = WebDriverWait(driver, 10).until( 
                EC.presence_of_all_elements_located((By.CLASS_NAME, "mud-input-control-input-container")) 
                )
            elements_vector = [element for element in elements]
            print("\nTamanho do elemento (lá ele): ", len(elements_vector))
            print("\nAchou e clicou!")
            for i in data:
                print("\nDado da vez: ", i)
                for element in elements_vector:
                    print("\nElemento da vez: ", element)
                    element.click()
                    clipboard.copy(i)
                    print("\nTexto copiado")
                    with pyautogui.hold('ctrl'):
                        pyautogui.press('v')
                    print("\nTexto colado!")
                    time.sleep(1)
                    pyautogui.press('tab')
                    next(i)
                    
            
        except Exception as e: print(f"Erro: {e}. Tentando novamente...") # Mensagem de erro para depuração 
        time.sleep(1)

def find_element_by_text(text):
    try:
        # Localizar o elemento pelo texto
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
        )
        return element
    except Exception as e:
        print(f"Erro: {e}")
        return None

def find_group(group_name): 
    print("\nFind group")
    try: 
        group = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, f'//span[@title="{group_name}"]')) ) 
        group.click() 
    except StaleElementReferenceException: 
        return find_group(group_name) # Try again in exception cases
    return group

# Locate and click on the specific group
def get_chat():  
    print("\nGet chat")
    while True:
        try:
            search = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, os.getenv("SEARCH"))))
            search.click()
            search.send_keys("My Number")
            chat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="My Number"]')))
            #ultron = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//span[@title="ULTRON"]'))
            chat.click()
            break
        except:
            print("Non clickable element. Trying again")
            time.sleep(1)
  
def get_all_messages():
    print("\nGet all messages")
    try:
        messages = WebDriverWait(driver, 30).until( 
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.message-in, div.message-out")) 
        )
        return [message.text for message in messages]
    except StaleElementReferenceException:
        return get_all_messages() # Try again in exception cases

def get_police():
    print("\nGet police")
    try:
        police = WebDriverWait(driver, 10).until( 
            EC.element_to_be_clickable((By.XPATH, os.getenv("EFETUAR"))))
        police.click()
    except:
        get_police()

def handle_popup(xpath): 
    print("Handle pop-up")
    try: # Aguardar até que o elemento do pop-up esteja presente e clicável 
        popup_element = WebDriverWait(driver, 10).until( 
            EC.element_to_be_clickable((By.XPATH, xpath)) 
            ) 
        popup_element.click() 
        print("Pop-up detectado e clicado para refrescar a página.") 
    except: print("Pop-up não detectado ou não clicável no momento.")

def insert_data_into_textbox(xpath, data): 
    print("\nInsert data into textbox")
    while True: 
        try: # Aguarda até que a caixa de texto esteja presente e clicável 
            textbox = WebDriverWait(driver, 10).until( 
                EC.presence_of_element_located((By.XPATH, xpath)) 
            ) 
            textbox.clear() # Limpa qualquer texto existente na caixa 
            textbox.send_keys(data) # Insere o dado na caixa de texto 
            break # Sai do loop quando o dado é inserido com sucesso 
        except Exception as e: 
            print(f"Erro: {e}. Tentando novamente...") # Mensagem de erro para depuração 
            time.sleep(1) # Espera um segundo antes de tentar novamente

#message parsing
def process_message(message):
    print("\nProcess message")
    if '\n\n' in message:
        groups = message.split('\n\n')
    else:
        groups = [message]
    processed_groups = []
    for group in groups:
        linhas = group.split('\n')
        for i in range(len(linhas)):
            if i == 1 or i == 2 or i == 10:
                linhas[i] = linhas[i].split(' ')
        processed_groups.append(linhas)
    return processed_groups

def report_fillout(groups):
    print("\nReport fillout")
    driver.switch_to.window(protected_tab)
    get_police()
    for group in groups:
        print("\nGroup = ", group)
        data_inicial = str((group[1])[0]) + '/' + str(current_year)
        print("\nData inicial = ", data_inicial) #for debug purposes
        data_final = str((group[1])[1]) + '/' + str(current_year)
        print("\nData final = ", data_final) #for debug purposes
        hora_inicial = str((group[2])[0]).replace(":","")
        print("\nHora inicial = ", hora_inicial) #for debug purposes
        hora_final = str((group[2])[1]).replace(":","")
        print("\nHora final = ", hora_final) #for debug purposes
        first_page = [data_inicial, data_final, hora_inicial, hora_final]
        find_and_insert(first_page)  
        # xpath_data_inicial = click_element_by_label("Data Inicial")
        # xpath_data_final = click_element_by_label("Data Final")
        # insert_data_into_textbox(data_inicial, xpath_data_inicial)
        # insert_data_into_textbox(data_final, xpath_data_final)

# Function to detect new messages
def detect_new_messages(old_message):
    print("\nDetect new messages")
    messages = get_all_messages()
    new_message = messages[-1] if messages else None
    log_message(new_message)
    if new_message and new_message != old_message: 
        print("Nova mensagem detectada: ", new_message)
        groups = process_message(new_message)
        report_fillout(groups)
        return new_message 
    else: 
        print("Nenhuma nova mensagem.") 
        return old_message    
  
def log_writer(messages):
    counter = 0
    for msg in  (messages.text[-10:]):
        f = open("log.txt", "a", encoding="utf-8")
        if counter == 0:
            inicio_str = "Início de sessão realizado no dia " + str(current_day) + " do " + str(current_month) + " de " + str(current_year)
            f.write(inicio_str)
            f.write("\nMensagem inicial:\n")
        f.write(msg)
        counter = counter + 1     

# Function to record messages on log file
def log_message(message): 
    logging.info(f"Mensagem analisada: {message}")

#function to star the log file
def start_log(): 
    logging.info("Script iniciado")

#start log file
start_log()

#open whatsapp web
driver.get('https://web.whatsapp.com/')
whatsapp_tab = driver.current_window_handle
time.sleep(30)

driver.switch_to.new_window('tab')
driver.get(os.getenv("PROTECTED_URL"))
protected_tab = driver.current_window_handle
#wait until user inputs valid credentials
time.sleep(90)


# Locate and click on the specific group
#find_group("ULTRON")
driver.switch_to.window(whatsapp_tab)
get_chat()

# Wait for complete load on group messages
time.sleep(5)

#get last message in group
#old_message = get_all_messages()[-1] if get_all_messages() else None
#last_message = get_last_message()
old_message = get_all_messages()[-1] if get_all_messages() else None


while (True):
    handle_popup(os.getenv("REFRESH"))
    time.sleep(1)
    new_message = detect_new_messages(old_message)
    time.sleep(5)
