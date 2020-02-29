# bs4 reference https://www.dataquest.io/blog/web-scraping-beautifulsoup/
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import bs4
import time
import json

# returns the content(string) from the given url using selenium
def get_html_source(url):
    html_source = ""

    # *******CHANGE THIS VALUE ACCORDINGLY*********
    # chrome webdriver path (https://chromedriver.chromium.org/)
    path = '/Users/vidyadhari/Downloads/chromedriver' 

    driver = webdriver.Chrome(executable_path=path)
    driver.get(url)

    # allow the page to populate/ get info from API's/ XHR
    time.sleep(5)

    # set number of items per page as 100
    select = Select(driver.find_element_by_name('pagination-length'))
    select.select_by_visible_text("100")
    time.sleep(5)

    # get total number of pages to run through
    pagination_items = driver.find_element_by_class_name(
        'pagination').find_elements_by_tag_name('li')
    pagination_length = int(pagination_items[-3].text)
    # next page button/ link
    pagination_next = pagination_items[-2]
    print(pagination_length)

    # read the current page and click the next page button until all pages are read
    for _ in range(pagination_length):
        html_source += driver.page_source
        # clicking the next page button/link
        driver.find_element_by_class_name(
            'pagination').find_elements_by_tag_name('li')[-2].click()
        time.sleep(5)
    driver.quit()
    return html_source



# parses the html_source and returns json with each entry of the format
# {
#   rank: rank,
#   username: username,
#   score: score,
#   time: time
# }
# using bs4
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

    # print(leaderboard_list, file=open("output.txt", "w"))
    print(len(leaderboard_list))
    return json.dumps(leaderboard_list)


url = 'https://www.hackerrank.com/contests/middle1/leaderboard/'
print(get_json(get_html_source(url)))