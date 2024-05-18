from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  # yeah theres both selenium and bs4 here
import requests
import time
from datetime import datetime
import random
import os


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
        print("too many iterations")
        return None
    else:
        test = random.choice(div_iter)
        div_childs = test.find_elements_by_xpath('.//div')
        if not div_childs:
            if len(test.find_elements_by_xpath('.//*')) > 0 and len(str(test.get_attribute('innerHTML'))) > 2000:
                print(test.get_attribute('innerHTML'))
                return test
            else:
                print("no content, no sub-divs")
                return None
        else:
            return div_min(div_childs, iteration+1)


def bot():
    browser = webdriver.Chrome("D:\Github\muxite.github.io\chromedriver.exe")
    browser.minimize_window()
    max_runs = 10
    runs = 0
    while True:
        term = get_search_term(sample, words_range)
        browser.get(google)
        time.sleep(2)
        search_bar = browser.find_element_by_xpath('//*[@id="APjFqb"]')  # get the search bar
        search_bar.send_keys(term)  # input the word
        search_bar.send_keys(u'\ue007')  # press enter
        time.sleep(2)  # wait a bit for the page to load
        try:
            pages = browser.find_elements_by_xpath('//a[contains(@jsname, "UWckNb")]')
            chosen = pages[random.randint(0, len(pages) - 1)]  # random webpage
            link = chosen.get_attribute("href")
            browser.get(link)
            time.sleep(2)  # wait a bit for the page to load
            divs = browser.find_elements_by_xpath('//div')
            print(len(divs))
            if len(divs) == 0:
                continue
            # now investigate the list of divs to find a lowest level div
            for i in range(0, 10):  # 10 tries max
                try:
                    response = div_min(divs, 0)
                    if response is not None:
                        block = response.get_attribute('innerHTML')
                        browser.close()
                        return datetime.now().strftime("%Y-%m-%d-%H%M%S"), term, link, block
                except IndexError:
                    print("div attempt error")
            else:
                continue

        except IndexError:
            print("Index Error")
        if runs > max_runs:
            print("FAILED")
            break
        runs += 1


def html_make_chunk():
    time_made, term, link, block = bot()
    title = str(time_made) + " " + str(term) + ".html"
    with open(title, 'w+', encoding="utf-8") as html_block:
        html_block.write(block)
    print(link)


for i in range(0, 30):
    html_make_chunk()