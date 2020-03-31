from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import bs4
import time
import json
from selenium.common.exceptions import NoSuchElementException
# for codeforces
import requests

# input username, output set/list of successful submissions
def codeforces_profile_submissions(username):
    response = requests.get("https://codeforces.com/api/user.status", params={"handle":username})
    response_json = response.json()
    if response_json["status"] == "OK":
        solved_problems = set()
        verdict = set()
        for item in response_json['result']:
            if item['verdict'] == "OK":
                solved_problems.add(item['problem']['name'])
            verdict.add(item['verdict'])
        return "solved_problems"
    else:
        return response_json

def get_html_source(url):
    html_source = ""
    path = '/Users/vidyadhari/Downloads/chromedriver' 
    chrome_options = Options()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    chrome_options.add_argument("--headless") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(options=chrome_options, executable_path=path)
    driver.get(url)
    time.sleep(5)
    driver.get_screenshot_as_file("capture.png")

    # check if pagination-length exists 
    pagination_dropdown = checkIfElementExists(driver, 'pagination-length', 'name')
    # if pagination_dropdown is not None
    if pagination_dropdown:
        select = Select(pagination_dropdown)
        select.select_by_visible_text("100")
        time.sleep(5)

        # check if pagination exists
        pagination = checkIfElementExists(driver, 'pagination', 'class_name')
        # if pagination is not None
        if pagination:
            pagination_items = pagination.find_elements_by_tag_name('li')
            pagination_length = int(pagination_items[-3].text)
        else:
            pagination_length = 1

        # loop changed to pagination_length - 1 since last page has no next button
        for i in range(pagination_length - 1):
            html_source += driver.page_source
            driver.find_element_by_class_name(
                'pagination').find_elements_by_tag_name('li')[-2].click()
            time.sleep(5)
        # get last page data
        html_source += driver.page_source
    # if pagination-length not found
    else:
        html_source += driver.page_source
    driver.quit()
    return html_source

# METHOD TO CHECK IF ELEMENT EXISTS, IF EXISTS RETURN ELEMENT
# func_type: element locating method used
# name: name of the locator
def checkIfElementExists(driver, name, func_type):
    elem = None
    if func_type == "name":
        try:
            elem = driver.find_element_by_name(name)
        except NoSuchElementException:
            return None
    elif func_type == "class_name":
        try:
            elem = driver.find_element_by_class_name(name)
        except NoSuchElementException:
            return None
    return elem




def get_json(html_source):
    soup = bs4.BeautifulSoup(html_source, 'html.parser')
    leaderboard = soup.find_all('div', class_='leaderboard-list-view')
    leaderboard_list = []
    for item in leaderboard:
        row_raw = item.find_all('p')
        row_dict = {
            "rank": row_raw[0].text.strip(),
            "username": row_raw[1].a.text.strip(),
            "score": row_raw[3].text.strip(),
            "time": row_raw[4].text.strip(),
        }
        leaderboard_list.append(row_dict)

    print(len(leaderboard_list))
    return json.dumps(leaderboard_list)


url = 'https://www.hackerrank.com/contests/middle1/leaderboard/1'
# print(get_json(get_html_source(url)))
print(codeforces_profile_submissions("navya570"))
