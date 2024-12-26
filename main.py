import clipboard
import logging
import os
import pyautogui
import requests
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

def check_internet_connection(url='https://www.google.com', timeout=5):
    try:
        # Faz uma requisição GET ao URL especificado
        response = requests.get(url, timeout=timeout)
        # Verifica se a resposta foi bem-sucedida (status code 200)
        return True if response.status_code == 200 else False
    except requests.ConnectionError:
        # Captura erros de conexão
        return False

def fillout_routine(data):
    clipboard.copy(data)
    with pyautogui.hold('ctrl'):
        pyautogui.press('v')    
    time.sleep(1)  
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('tab')

def find_and_click_element_by_text(text):
    try:
        # Localizar o elemento pelo texto
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{text}')]"))
        )
        # Clicar no elemento encontrado
        element.click()
        print(f"Elemento com texto '{text}' foi clicado com sucesso.")
        return element
    except Exception as e:
        print(f"Erro: {e}")
        return None

def get_all_messages():
    print("\nGet all messages")
    try:
        messages = WebDriverWait(driver, 30).until( 
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.message-in, div.message-out")) 
        )
        return [message.text for message in messages]
    except StaleElementReferenceException:
        return get_all_messages() # Try again in exception cases

def get_chat():  
    print("\nGet chat")
    while True:
        try:
            search = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, os.getenv("SEARCH"))))
            search.click()
            search.send_keys("My Number")
            chat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="My Number"]')))
            #chat = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//span[@title="ULTRON"]')) #ultron
            chat.click()
            break
        except:
            print("Non clickable element. Trying again")
            time.sleep(1)

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

def multiple_tabs(i):
    aux = 0
    while (aux < i):
        pyautogui.press('tab')
        time.sleep(1)
        aux = aux + 1

def tabs_plus_enter(i):
    multiple_tabs(i)
    pyautogui.press('enter')

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

# Function to record messages on log file
def log_message(message): 
    logging.info(f"Mensagem analisada: {message}")

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
        hsh_vector = str(group[0]).split(' ')
        if (len(hsh_vector) > 1):
            HSH = hsh_vector[0] + ' ' + hsh_vector[1]
        else:
            HSH = ''
        data_inicial = str((group[1])[0]) + '/' + str(current_year)
        print("\nData inicial = ", data_inicial) #for debug purposes
        data_final = str((group[1])[1]) + '/' + str(current_year)
        print("\nData final = ", data_final) #for debug purposes
        hora_inicial = str((group[2])[0]).replace("H",":00")
        print("\nHora inicial = ", hora_inicial) #for debug purposes
        hora_final = str((group[2])[1]).replace("H",":00")
        print("\nHora final = ", hora_final) #for debug purposes
        tipo_emprego = str(group[3])
        print("\nTipo de emprego = ", tipo_emprego) #for debug purposes
        tipo_acao = str(group[4])
        print("\nTipo de ação = ", tipo_acao) #for debug purposes
        tipo_operacao = str(group[5])
        print("\nTipo de operação = ", tipo_operacao) #for debug purposes
        unidade_operacional = str(group[6])
        print("\nUnidade operacional = ", unidade_operacional) #for debug purposes
        popup = str(group[7])
        print("\npopup = ", popup) #for debug purposes
        pop_up = str(group[7]).split(" ")
        if 'VIATURA' in pop_up:
            pref = pop_up[2]
            patr = pop_up[4]
        if 'POG' in pop_up:
            pref = ''
            patr = ''
        cidade = group[8]
        bairro = group[9]
        matriculas = str(group[10]).split(' ')
        
        tipo_viatura = pref[:2]
        prefixo = pref[2:]

        elements = WebDriverWait(driver, 10).until( 
            EC.presence_of_all_elements_located((By.CLASS_NAME, "mud-input-control-input-container")) 
        )
        elements_vector = [element for element in elements]

        ##INÍCIO

        print("\nTamanho do elemento (lá ele): ", len(elements_vector))
        print("\nAchou e clicou!")
        
        time.sleep(10)
        element = elements_vector[0]
        element.click()

        time.sleep(2)

        clipboard.copy(data_inicial)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')

        time.sleep(2)
        element = elements_vector[1]
        element.click()

        clipboard.copy(data_final)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')

        time.sleep(2)
        element = elements_vector[2]
        element.click()
            
        clipboard.copy(hora_inicial)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')

        time.sleep(2)
        element = elements_vector[3]
        element.click()
            
        clipboard.copy(hora_final)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')

        time.sleep(2)
        element = elements_vector[4]
        element.click()
            
        clipboard.copy(tipo_emprego)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')
        time.sleep(1)  
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')

        time.sleep(2)
        pyautogui.press('tab')
            
        clipboard.copy(tipo_acao)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')    
        time.sleep(1)  
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')

        time.sleep(2)
        pyautogui.press('tab')
            
        clipboard.copy(tipo_operacao)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')    
        time.sleep(1)  
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

        pyautogui.press('tab')
            
        clipboard.copy(unidade_operacional)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')    
        time.sleep(1)  
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

        tabs_plus_enter(2)

        time.sleep(5)
        if('VIATURA' in popup):
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.press('enter')

        elif('POG'in popup):
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.press('enter')


        button = WebDriverWait(driver, 10).until( 
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]/div[2]/button')) 
            ) 
        button.click()

        time.sleep(2)

        pyautogui.press('tab')

        clipboard.copy(cidade)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')
        time.sleep(1)  
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

        pyautogui.press('tab')

        clipboard.copy(bairro)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')
        time.sleep(1)  
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

        if (HSH != ''):
            find_and_click_element_by_text(HSH)
            tabs_plus_enter(2)
            time.sleep(2)
            multiple_tabs(2)

        button2 = WebDriverWait(driver, 5).until( 
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'mud-button-root mud-button mud-button-filled mud-button-filled-primary mud-button-filled-size-medium mud-ripple')]")) 
            )
        button2.click()

        time.sleep(2)

        if(pop_up == 'VIATURA'):
            multiple_tabs(5)
            clipboard.copy(tipo_viatura)
            with pyautogui.hold('ctrl'):
                pyautogui.press('v')
            time.sleep(1)
            pyautogui.press('down')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('tab')

            clipboard.copy(patr)
            with pyautogui.hold('ctrl'):
                pyautogui.press('v')
            time.sleep(1)
            pyautogui.press('down')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('tab')    

            clipboard.copy(prefixo)
            with pyautogui.hold('ctrl'):
                pyautogui.press('v')
            time.sleep(1)
            pyautogui.press('down')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('tab')    

        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.press('enter')

        time.sleep(5)

        tabs_plus_enter(4)

        multiple_tabs(2)

        for matricula in matriculas:
            matri_form = str(matricula).replace("-", "")
            clipboard.copy(matri_form)
            
            with pyautogui.hold('ctrl'):
                pyautogui.press('v')
            time.sleep(1)
            pyautogui.press('down')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            with pyautogui.hold('ctrl'):
                pyautogui.press('a')
            time.sleep(1)
            pyautogui.press('delete')

        tabs_plus_enter(2)

        tabs_plus_enter(5)

        ##FIM        


#function to star the log file
def start_log(): 
    logging.info("Script iniciado")

#open whatsapp web
driver.get('https://web.whatsapp.com/')
whatsapp_tab = driver.current_window_handle
time.sleep(30)

driver.switch_to.new_window('tab')
driver.get(os.getenv("PROTECTED_URL"))
protected_tab = driver.current_window_handle
#wait until user inputs valid credentials

time.sleep(20)

# Locate and click on the specific group
driver.switch_to.window(whatsapp_tab)
get_chat()

# Wait for complete load on group messages
time.sleep(5)

old_message = get_all_messages()[-1] if get_all_messages() else None

while (check_internet_connection()):  #always check if the internet connection is ok
    handle_popup(os.getenv("REFRESH"))
    time.sleep(1)
    new_message = detect_new_messages(old_message)
    time.sleep(5)
    old_message = new_message


