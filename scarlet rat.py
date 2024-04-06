from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import random
import os
sample = "Battle Royale.txt"  # sample text to get search terms from. Good book.
search_bar_xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input'
words_range = [2, 4]
browser = webdriver.Chrome("D:\Github\muxite.github.io\chromedriver.exe")


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


def run():
    term = get_search_term(sample, words_range)
    browser.get(term)  # open google images search
    time.sleep(1)  # wait a bit for the page to load
    try:
        pages = browser.find_elements_by_xpath('//a[contains(@jsname, "UWckNb")]')
        chosen = pages[0, len(pages)-1]

    except IndexError:
        print("Index Error")
        return
    browser.close
