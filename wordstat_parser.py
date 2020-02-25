from splinter import Browser
import config
import random
from time import sleep
import pandas as pd

# need to define settings of your account
request_word = 'Культура и религия'

def parse_wordstat(login, password, request_word, number_of_request_pages = 3):
    # открытие страницы wordstat и авторизация 
    browser = Browser()
    url = "https://wordstat.yandex.ru/"
    browser.visit(url)
    browser.click_link_by_href('https://passport.yandex.ru/passport?mode=auth&msg=&retpath=https%3A%2F%2Fwordstat.yandex.ru%2F')
    browser.find_by_id('b-domik_popup-username').fill(login)
    sleep(random.randint(5, 10)/10)
    browser.find_by_id('b-domik_popup-password').fill(password)
    sleep(random.randint(5, 10)/10)
    button = browser.find_by_css('input[class="b-form-button__input"]')[2]
    button.click()
    sleep(random.randint(5, 10)/10)

    # ввод запроса
    word_search_input = browser.find_by_css('input[class="b-form-input__input"]').first
    word_search_input = word_search_input.fill(request_word)
    sleep(random.randint(5, 10)/10)
    span_button = browser.find_by_css('input[class="b-form-button__input"]')[0]
    span_button.click()
    sleep(random.randint(5, 10)/10)
    
    queries = []
    frequency = []
    # обход заданного числа страниц
    for _ in range(number_of_request_pages):
        # получение табличных данных
        iter_element = browser.find_by_css('td[class*="b-word-statistics__td"]')
        word_flag = True
        frequency_current = config.frequency + 1
        for i in range(100):
            if word_flag:
                queries.append(iter_element[i].text)  
            else:
                frequency_current = int(''.join((iter_element[i].text.split())))
                frequency.append(frequency_current)
                if(frequency_current < config.frequency):
                    break
            word_flag = not word_flag
        if (frequency_current < config.frequency):
            break
        browser.click_link_by_href('#next_page')
        sleep(random.randint(5, 10)/10)

    #Поиск рекламы на страницах
    url = "https://yandex.ru/search/?text="
    browser.visit(url)
    advense = []
    count = 0
    for query in queries:
        count += 1
        print(str(count)+'...'+str(len(queries)))
        web_search_input = browser.find_by_css('input[class="input__control mini-suggest__input"]').first
        web_search_input = web_search_input.fill(query)
        sleep(random.randint(5, 10) / 10)
        search_button = browser.find_by_css('.websearch-button').first
        search_button.click()
        sleep(random.randint(5, 10) / 10)
        span_adv = browser.find_by_text('реклама')
        advense.append(len(span_adv))

    result = pd.DataFrame(dict(queries = queries, frequency = frequency, advense = advense))
    result.sort_values(by=['frequency'], ascending=False)
    result.to_excel("output.xlsx", columns=['queries', 'frequency', 'advense'], index=False)
    browser.quit()


parse_wordstat(config.login, config.password, request_word, 10)
