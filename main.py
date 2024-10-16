from selenium import webdriver
import time, os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

auth_token = os.environ['TOKEN']
word = os.environ['TEXT']
tweet_id = os.environ['ID']

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-http2')
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=options)
driver.get('https://x.com/i/flow/login')
driver.maximize_window()
element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, 'text')))

time.sleep(1)
cookie = {
        'name': 'auth_token',
        'value': auth_token,
        'domain': '.x.com',
        'path': '/'
}
driver.add_cookie(cookie)
time.sleep(1)
driver.get('https://x.com/user/status/' + tweet_id)
element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role=textbox]')))
time.sleep(1)

buttons = driver.find_elements(By.TAG_NAME, 'button')
for btn in buttons:
    outer_html = btn.get_attribute('outerHTML')
    client_height = btn.size['height']
    if 'like' in outer_html and client_height > 30 and 'unlike' not in outer_html:
        btn.click()
        time.sleep(2)
    if 'bookmark' in outer_html and client_height > 30:
        btn.click()

actions = ActionChains(driver)
for _ in range(20):
    actions.send_keys(Keys.TAB)
actions.perform()
time.sleep(1)
element_box = driver.find_element(By.CSS_SELECTOR, '[role=textbox]')
element_box.send_keys(word)
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '[data-testid=tweetButtonInline]').click()
time.sleep(8)

driver.quit()
