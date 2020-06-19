import math
import nltk
import selenium.common.exceptions
from random import randint as rand
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from tkinter import *
import json

URLS = json.load(open('URLS.json'))


class Browser:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ['enable-automation'])

        self.driver = webdriver.Chrome(options=self.options)

        self.actions = ActionChains(self.driver)

    def open_random_page(self, bank):
        sites = URLS[f'{bank}']
        r = rand(0, len(sites) - 1)
        print(f'Opening random page: {sites[r]}...')
        self.driver.get(f'{sites[r]}')

    def aggregator(self, tag_name):
        text = []
        elements = self.driver.find_elements_by_tag_name(tag_name)

        print('Aggregating elements...')
        [text.append(element.text) for element in elements if (len(element.text) > 3) if element.is_displayed()]

        print(f'Elements: {text}')
        return text

    def google_search(self):
        print('Google search...')
        headlines = []
        [headlines.append(item) for item in self.aggregator(tag_name='h2')]
        [headlines.append(item) for item in self.aggregator(tag_name='h3')]

        text = self.keyword_extraction(headlines[rand(0, len(headlines) - 1)])
        print(f'Query: {text}')

        self.driver.get("https://google.com")
        self.driver.get(f"http://www.google.com/search?q={text}")

    def youtube_search(self):
        print('YouTube search...')
        headlines = ['world news']
        [headlines.append(item) for item in self.aggregator(tag_name='h2')]
        [headlines.append(item) for item in self.aggregator(tag_name='h3')]

        r = rand(0, len(headlines) - 1)
        print(f'Selected text: {headlines[r]}')
        text = self.keyword_extraction(headlines[r])

        print(f'Query: {text}')
        self.driver.get("https://youtube.com")
        self.driver.get(f"https://www.youtube.com/results?search_query={text}")

    def click_random_link(self):
        print('Trying to click random link...')
        links = [link for link in self.driver.find_elements_by_tag_name("a") if link.is_displayed()]

        if links:
            l = links[rand(0, len(links) - 1)]
            self.driver.execute_script('arguments[0].scrollIntoView();', l)
            print(f'Selected link: {l.text}')
            sleep(1)
            try:
                self.driver.execute_script("arguments[0].click();", l)
            except selenium.common.exceptions.StaleElementReferenceException:
                print('Link no longer visible...')
        else:
            print('No links collected...')
            pass

    def scroll(self):
        sleep(3)

        i = rand(3, 6)
        j = rand(2, 4)
        print(f'Scrolling down {i} times, and up {j} times...')

        while i > 0:
            self.actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.3)
            i = (i - 1)

        sleep(2)

        while j > 0:
            self.actions.send_keys(Keys.ARROW_UP).perform()
            sleep(0.3)
            j = (j - 1)

    def new_tab(self, bank):
        print('Opening new tab...')
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        print('Opening random page in new tab...')
        self.open_random_page(f"{bank}")

    def typer(self, text):
        for character in text:
            self.actions.send_keys(character).perform()
            sleep(0.1)

    @staticmethod
    def keyword_extraction(text):
        print('Extracting keywords...')

        text = word_tokenize(text)
        text = [term for term in text if term not in stopwords.words('english') or stopwords.words('german')]
        text = [word for word in text if len(word) > 2]
        text = nltk.pos_tag(text)
        text = [term for term in text if ('NN' or 'RB' or 'PR' or 'JJ' or 'FW') in term[1]]

        if len(text) > 3:
            i = math.ceil(len(text) * .6)
        else:
            i = len(text)

        text = [term[0].lower() for term in text]
        text = text[0:i]

        final = " ".join([str(item) for item in text])

        return final

    @staticmethod
    def wait():
        time = rand(3, 8)
        print(f"Sleeping for {time} seconds...")
        sleep(time)


class Runner:
    def __init__(self):
        self.go = Browser()
        self.bank = ''
        self.root = Tk()
        self.language = ''

    def menu(self):
        Button(self.root, text='US - Liberal', command=lambda: self.set_bank('english-us-liberal')).pack()
        Button(self.root, text='US - Conservative', command=lambda: self.set_bank('english-us-conservative')).pack()
        Button(self.root, text='UK - Liberal', command=lambda: self.set_bank('english-uk-liberal')).pack()
        Button(self.root, text='UK - Conservative', command=lambda: self.set_bank('english-uk-conservative')).pack()
        Button(self.root, text='Germany - Liberal', command=lambda: self.set_bank('german-liberal')).pack()
        Button(self.root, text='Germany - Conservative', command=lambda: self.set_bank('german-conservative')).pack()
        self.root.mainloop()

    def set_bank(self, selection):
        self.bank = selection
        self.set_language(selection)
        self.root.destroy()

    def set_language(self, bank_name):
        self.language = bank_name.split('-')[0]
        print(f'Language: {self.language}')
        return self.language

    def standard_run(self):
        run = self.go
        run.open_random_page(self.bank)
        run.scroll()
        run.click_random_link()
        run.wait()
        run.click_random_link()
        run.scroll()
        run.new_tab(self.bank)
        run.scroll()
        run.wait()
        run.click_random_link()
        run.scroll()
        run.google_search()
        run.wait()
        run.click_random_link()
        run.scroll()
        run.wait()
        run.youtube_search()
        run.scroll()
        run.google_search()
        run.scroll()


runner = Runner()
runner.menu()
runner.standard_run()
