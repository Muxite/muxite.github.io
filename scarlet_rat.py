from selenium import webdriver
import time
from datetime import datetime
import random
import os
import glob

page_div_investigation_time = []  # 2.376628432955061
page_p_investigation_time = []  #
sample = "Battle Royale.txt"  # sample text to get search terms from. Good book.
words_range = [1, 3]
google = 'https://www.google.com/'
html_file_template = r'template_scarlet_rat_pile.html'
block_file_template = r'template_scarlet_rat_block.html'
html_file_index = r'scarlet_rat_pile.html'
pile_location = r"pile/"


def get_search_term(heap_location, word_count):
    heap = ""
    for letter in open(heap_location, encoding="utf8"):
        heap += letter.replace("\n", "").replace("BATTLE ROYALE", "")  # remove these strings
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


def bot(mode, max_runs):
    options = webdriver.ChromeOptions()
    options.add_argument("--mute-audio")
    browser = webdriver.Chrome(r"chromedriver.exe", options=options)
    browser.minimize_window()
    runs = 0
    while True:
        term = get_search_term(sample, words_range)
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
                            return datetime.now().strftime("%Y-%m-%d--%H-%M-%S"), term, link, block
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


def make_text(tag, tag_follower, text):  # make text (add your own tag)
    return str('<%s %s>%s</%s>' % (tag, tag_follower, text, tag))


# def package(time_made, term, link, block):  # make a list of parts to write
#     build = []
#     build.append('<div class="container">')
#     build.append('<div class="row">')
#     build.append('<div class="col">')
#     build.append(make_text('button', 'class="accordion active"', time_made))
#     build.append('<div class="panel" style="display: block;">')
#     build.append(make_text('h2', '', term))
#     build.append(make_text('a', 'href=%s' % link, link))
#     build.append(block)
#     build.append('</div>')
#     build.append('</div>')
#     build.append('</div>')
#     build.append('</div>')
#     return build
#

def html_make_chunk():  # make a html chunk that can be added to the index.html
    time_start = time.time()
    time_made, term, link, block = bot(0, 15)
    title = str(time_made) + ".html"
    with open(block_file_template, 'r', encoding="utf-8") as html_block_template:
        with open(pile_location + title, 'w+', encoding="utf-8") as html_block:
            to_write = str(html_block_template.read())
            to_write = to_write.replace("TITLE", term)
            to_write = to_write.replace("DATE", time_made)
            to_write = to_write.replace("CONTENT", block)
            to_write = to_write.replace("LINK", link)
            html_block.write(to_write)
            print("created " + str(title))
    print("total time: " + str(time.time() - time_start))


def create_index():  # use the template and all chunks to form index.html
    print("creating index")
    time_start = time.time()
    big = ""
    parts = []
    for html_file in glob.glob(os.path.join(pile_location, '*.html')):
        with open(html_file, 'r', encoding="utf8") as f:
            parts.append(str(f.read()))

    for i in range(len(parts)):  # build in reverse order
        big += parts[len(parts)-1-i]

    # now make a new index, and replace the marker with the combined chunks
    with open(html_file_template, 'r', encoding="utf-8") as html_template:
        with open(html_file_index, 'w+', encoding="utf-8") as html_index:
            html_index.truncate(0)  # clear all
            html_index.write(str(html_template.read()).replace("<p>MARKER1</p>", big))
    print("created page")
    print("total time: " + str(time.time() - time_start))


def make():
    for i in range(0, 20):
        html_make_chunk()


create_index()
