from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  # yeah theres both selenium and bs4 here
import requests
import time
from datetime import datetime
import random
import os

page_div_investigation_time = []  # 2.376628432955061
page_p_investigation_time = []  #
sample = "Battle Royale.txt"  # sample text to get search terms from. Good book.
words_range = [1, 3]
google = 'https://www.google.com/'

html_file = 'D:\Github\muxite.github.io\index.html'
html_snippet = '''
<div class="container">
    <div class="row">
        <div class="col">
            <button class="accordion"> DATE </button>
            <div class="panel"> 
                <a href="URL">TITLE</a> <br>

                CONTENT
            </div>
        </div>
    </div>
</div>
<script src="accordion.js"></script>
'''


def get_search_term(heap_location, word_count):
    heap = ""
    for l in open(heap_location, encoding="utf8"):
        heap += l.replace("\n", "").replace("BATTLE ROYALE", "")  # remove these strings
    wc = random.randint(word_count[0], word_count[1])  # how many words will be selected.
    i = random.randint(0, len(heap) - 30)
    spaces_found = 0
    builder = ""
    while True:
        # keep advancing until a first space is found
        # then start adding to builder until word count is reached.
        if 0 < spaces_found < wc + 1:
            builder += heap[i]
        elif spaces_found >= wc + 1:
            break

        if heap[i] == " ":
            spaces_found += 1
        i += 1
    return builder


def div_min(div_iter, iteration):
    if iteration > 10:
        return None
    else:
        div_childs = div_iter.find_elements_by_xpath('.//div')
        if not div_childs:
            if len(str(div_iter.get_attribute('innerHTML'))) > 3000:
                return div_iter
            else:
                return None
        else:
            return div_min(random.choice(div_childs), iteration+1)


def bot():
    mode = 1
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")
    browser = webdriver.Chrome("D:\Github\muxite.github.io\chromedriver.exe", chrome_options=chrome_options)
    browser.minimize_window()
    max_runs = 15
    runs = 0
    while True:
        term = get_search_term(sample, words_range) + "how to"
        browser.get(google)
        time.sleep(1)
        search_bar = browser.find_element_by_xpath('//*[@id="APjFqb"]')  # get the search bar
        search_bar.send_keys(term)  # input the word
        search_bar.send_keys(u'\ue007')  # press enter
        time.sleep(1)  # wait a bit for the page to load
        try:
            pages = browser.find_elements_by_xpath('//a[contains(@jsname, "UWckNb")]')
            chosen = pages[random.randint(0, len(pages) - 1)]  # random webpage
            link = chosen.get_attribute("href")
            browser.get(link)
            time.sleep(1)  # wait a bit for the page to load
            if mode == 0:
                page_investigate_start_time = time.time()
                divs = browser.find_elements_by_xpath('//div')
                if len(divs) == 0:
                    continue
                # now investigate the list of divs to find a lowest level div
                for i in range(0, max(len(divs), 20)):  # 20 tries max
                    try:
                        response = div_min(random.choice(divs), 0)
                        if response is not None:
                            block = response.get_attribute('outerHTML')
                            browser.close()
                            page_div_investigation_time.append(time.time() - page_investigate_start_time)
                            return datetime.now().strftime("%Y-%m-%d-%H%M%S"), term, link, block
                        else:
                            pass
                    except IndexError:
                        print("div attempt error")
                else:
                    page_div_investigation_time.append(time.time() - page_investigate_start_time)
                    continue
            else:
                page_investigate_start_time = time.time()
                ps = browser.find_elements_by_xpath('//p')
                if len(ps) == 0:
                    continue
                # now investigate the list of p to find good p
                for i in range(0, len(ps)):  # as many tries as there are paragraphs
                    try:
                        response = random.choice(ps)
                        block = response.get_attribute('outerHTML')
                        if (response is not None and
                           len(block) > 2000):
                            browser.close()
                            page_p_investigation_time.append(time.time() - page_investigate_start_time)
                            return datetime.now().strftime("%Y-%m-%d-%H%M%S"), term, link, block
                        else:
                            ps.remove(response)  # strike this p out
                    except IndexError:
                        pass
                else:
                    page_p_investigation_time.append(time.time() - page_investigate_start_time)
                    continue

        except IndexError:
            print("Index Error")
        if runs > max_runs:
            print("FAILED")
            break
        runs += 1


def html_make_chunk():
    start_time = time.time()
    time_made, term, link, block = bot()
    title = str(time_made) + ".html"
    with open(title, 'w+', encoding="utf-8") as html_block:
        html_block.write(block)
        print("created " + str(title))
    print("total time: " + str(time.time() - start_time))


for i in range(0, 10):
    print(i)
    html_make_chunk()
    print(page_p_investigation_time)
    print(page_div_investigation_time)
