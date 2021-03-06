from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from pydbus import SystemBus
import re
# import pickle
from threading import Thread
from gi.repository import GLib

whatsappGroup = "Signal test"
bus = SystemBus()
signal = bus.get('org.asamk.Signal')

class WhatsApp:
    last_message = None
    def __init__(self, chat):
        self.driver = webdriver.Firefox()        
        self.driver.get('https://web.whatsapp.com/')
        # try:
        #     cookies = pickle.load(open("cookies.pkl", "rb"))
        #     print("found")
        # except Exception: # so many things could go wrong, can't be more specific.
        #     cookies = []
        #     pass
        # print(cookies)
        # for cookie in cookies:
        #     print("adding")
        #     self.driver.add_cookie(cookie)
        wait_message = "Open WhatsApp on your phone"
        while wait_message in self.driver.page_source:
            pass
        sleep(5)
        self.driver.find_element(By.XPATH, '//*[@title="{}"]'.format(chat)).click()
        # print(self.driver.get_cookies())
        # pickle.dump( self.driver.get_cookies() , open("cookies.pkl","wb"))

    def fetch_information(self, webelement):
        try:
            msg = webelement.find_element(By.XPATH, './/div[contains(@class, "copyable-text")]')
            msg_sender = msg.get_attribute('data-pre-plain-text')
            msg_text = msg.find_elements(By.XPATH, './/span[contains(@class, "selectable-text")]')[-1].text
        except IndexError as e:
            msg_text = ""
            print('[DEBUG1] {}'.format(str(e)))
        except Exception as e:
            msg_sender = ""
            msg_text = ""
            print('[DEBUG2] {}'.format(str(e)))
        return msg_sender, msg_text

    def get_last_message(self):
        try:
            all_msgs = self.driver.find_elements(By.XPATH, '//*[@id="main"]//div[contains(@class, "message")]')
            if len(all_msgs) > 0:
                msg = all_msgs[-1]
                author, msg = self.fetch_information(msg)

                if self.last_message != author + msg:
                    self.last_message = author + msg
                    print('[Received] {}'.format(self.last_message))
                    author = re.sub(r".*] ", "", author)
                    data = author + msg
                    # signal.sendMessage(data, [], ['+31616864918']) # Peter
                    # signal.sendMessage(data, [], ['+31624986088']) # Rick
                    signal.sendMessage(data, [], ['+31652652611'])
                    signal.sendGroupMessage(data, [], [175, 177, 152, 66, 116, 102, 45, 32, 30, 52, 106, 98, 219, 217, 112, 12]) # signal test
                    # signal.sendGroupMessage(data, [], [ 0x71, 0x26, 0x89, 0x4E, 0x50, 0xA8, 0x16, 0xA1, 0x2B, 0x20, 0x42, 0xF8, 0x14, 0x4A, 0x49, 0x4F])

                    return msg
                else:
                    return None
        except Exception as e:
            print('[DEBUG3] {}'.format(str(e)))

    def sendmsg(self, msg):
        input_box = self.driver.find_element(
            By.XPATH, '//*[@id="main"]//footer//div[contains(@contenteditable, "true")]')
        input_box.click()
        msg = msg.split('\n')
        action = ActionChains(self.driver)
        for m in msg:
            action\
                .send_keys(m)\
                .key_down(Keys.SHIFT)\
                .send_keys(Keys.RETURN)\
                .key_up(Keys.SHIFT)
        action.send_keys(Keys.RETURN)
        action.perform()