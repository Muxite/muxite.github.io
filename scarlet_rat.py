from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup  # yeah theres both selenium and bs4 here
import requests
import time
import datetime
import random
import os
sample = "Battle Royale.txt"  # sample text to get search terms from. Good book.
words_range = [2, 4]
google = 'https://www.google.com/'
browser = webdriver.Chrome("D:\Github\muxite.github.io\chromedriver.exe")
browser.minimize_window()
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
    i = random.randint(0, len(heap)-30)
    spaces_found = 0
    builder = ""
    while True:
        # keep advancing until a first space is found
        # then start adding to builder until word count is reached.
        if 0 < spaces_found < wc+1:
            builder += heap[i]
        elif spaces_found >= wc+1:
            break

        if heap[i] == " ":
            spaces_found += 1
        i += 1
    return builder


def bot():
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
            chosen = pages[random.randint(0, len(pages)-1)]  # random webpage
            link = chosen.get_attribute("href")
            browser.get(link)
            time.sleep(1)  # wait a bit for the page to load
            divs = browser.find_elements_by_xpath('//p | //span')  # stuff
            print(len(divs))
            if len(divs) == 0:
                continue
            builder = []
            i = random.randint(0, len(divs))
            end = i+random.randint(2, 8)
            while True:
                if i > end:
                    break
                try:
                    builder.append(divs[i].get_attribute("innerHTML"))
                except IndexError:
                    break
                i += 1
            print(term)
            print(link)
            print(builder)
            browser.close()
            return term, link, builder
        except IndexError:
            print("Index Error")
        if runs > max_runs:
            print("FAILED")
            break
        runs += 1
    browser.close()


def rebuild_html():
    # open file
    with open(html_file) as f:
        soup = BeautifulSoup(f, 'html.parser')
    search_term, link, ppp = bot()
    html_string = html_snippet.replace("DATE", str(datetime.datetime.now()))
    html_string = html_string.replace("URL", link)
    html_string = html_string.replace("TITLE", search_term)
    content = ''
    for part in ppp:
        content += str(part)
    html_string = html_string.replace("CONTENT", content)
    new_div = BeautifulSoup(html_string, 'html.parser')
    scripts_to_remove = soup.find_all("script", src="accordion.js")
    for script in scripts_to_remove:
        script.decompose()
    soup.body.append(new_div)
    # save to file
    with open("index.html", "w") as f:
        f.write(str(soup))


rebuild_html()
