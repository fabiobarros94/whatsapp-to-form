import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from process_msg import main as parse_msg
import os

load_dotenv()

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
#options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get('https://web.whatsapp.com/')

time.sleep(20)

print (driver.title) #for debug only
whatsapp_tab = driver.current_window_handle
driver.switch_to.new_window('tab')
driver.get('https://www.invertexto.com/pxqu41')
form_tab = driver.current_window_handle
driver.switch_to.new_window('tab')
driver.get(os.getenv("PROTECTED_URL"))
protected_tab = driver.current_window_handle
time.sleep(30)
input_list = driver.find_elements(by=By.TAG_NAME, value = "input")
login_box = input_list[0]
pass_box = input_list[1]
login_box.send_keys(os.getenv("LOGIN")[::-1])
time.sleep(3)
pass_box.send_keys(os.getenv("PASSWORD"))
time.sleep(3)
#pass_box.send_keys(Keys.RETURN))
driver.switch_to.window(whatsapp_tab)
chat = driver.find_element(by=By.CSS_SELECTOR, value = '[title="+55 81 9648-9577"]').click()
time.sleep(3)

messages = driver.find_elements(by=By.CSS_SELECTOR, value="span.selectable-text.copyable-text > span")

print (f'{len(messages)=}')

for msg in  (messages[-10:]):
    print (msg.text) #show this to the user, save it in a file so the user knows where the program started at

messages = driver.find_elements(by=By.CSS_SELECTOR, value="span.selectable-text.copyable-text")
while (True):
    time.sleep(15)
    new_messages = driver.find_elements(by=By.CSS_SELECTOR, value="span.selectable-text.copyable-text")
    if new_messages[-1].text != messages[-1].text:
        print ("new messages arrived") #inform the user?
        last_msg_txt = messages[-1].text
        new_texts = [m.text for m in new_messages]
        messages = new_messages
        driver.switch_to.window(form_tab)
        time.sleep(2)
        for i, new_txt in enumerate(new_texts[::-1]):
            #print (f'debug, comparing {new_txt} and {last_msg_txt}')
            if new_txt == last_msg_txt:
                break
        for j in range(i):
                idx = -i + j # we were couting backwards from the end
                print (f'Processing this message: {new_texts[idx]}') #Inform the user that this message was processed
                parsed_msg = parse_msg (new_texts[idx])
                driver.find_element(By.CSS_SELECTOR, 'textarea').send_keys(f'{parsed_msg}\n')
        driver.switch_to.window(whatsapp_tab)
    else:
        print ('no new messages') #inform the user?
    #for msg in messages[-10:]:
        #print (msg.text) #for debug only
