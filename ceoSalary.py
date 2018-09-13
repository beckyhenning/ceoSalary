import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_soup(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    return soup

def num_pages(url):
    soup = get_soup(url)
    page = soup.find_all('li', class_='pager__item')
    return page

def mult_pages_industry():
    last_page = page[-1].find('a', href=True)["href"]
    last_page_index = last_page.find("page=")
    last_page = int(last_page[last_page_index+5:])
    for pageNum in range(0,last_page+1):
        url = "https://aflcio.org/paywatch/highest-paid-ceos?combine=&industry=" + i + "&state=All&sp500=0&page=" + str(pageNum)
        soup = get_soup(url)
        main_content = soup.find('table', class_ = 'cols-5 responsive-enabled')
        salary = main_content.find_all('td', class_ = 'views-field views-field-total is-active')
        salaries.append([float( x.text.strip().replace('$','').replace(',','')) for x in salary])
        company_ticker = main_content.find_all('a', class_='use-ajax')
        tickers.append([x.text for x in company_ticker][::2])
    return tickers, salaries

def mult_pages_state():
    last_page = page[-1].find('a', href=True)["href"]
    last_page_index = last_page.find("page=")
    last_page = int(last_page[last_page_index+5:])
    for pageNum in range(0,last_page+1):
        url = "https://aflcio.org/paywatch/highest-paid-ceos?combine=&industry=All&state=" + i + "&sp500=0&page=" + str(pageNum)
        soup = get_soup(url)
        main_content = soup.find('table', class_ = 'cols-5 responsive-enabled')
        salary = main_content.find_all('td', class_ = 'views-field views-field-total is-active')
        salaries.append([float( x.text.strip().replace('$','').replace(',','')) for x in salary])
        company_ticker = main_content.find_all('a', class_='use-ajax')
        tickers.append([x.text for x in company_ticker][::2])
    return tickers, salaries

def single_page():
    soup = get_soup(url)
    main_content = soup.find('table', class_ = 'cols-5 responsive-enabled')
    salary = main_content.find_all('td', class_ = 'views-field views-field-total is-active')
    salaries.append([float( x.text.strip().replace('$','').replace(',','')) for x in salary])
    company_ticker = main_content.find_all('a', class_='use-ajax')
    tickers.append([x.text for x in company_ticker][::2])
    return tickers, salaries

def graph_state(salaries, stateCode ):

    df = pd.DataFrame({'Salary in Millions': salaries, 'State': stateCode})
    df.set_index('State',inplace=True)
    df.sort_values(by='Salary in Millions', ascending=False)

    ax = df.plot(kind="bar", title="Average Salary")

    ax.set_ylabel('Salary in Millions')
    ax.legend_.remove()
    ax.axes.get_yaxis().set_visible(True)

    #if i want values on bars

    # for p in ax.patches:
    #     ax.annotate(np.round(p.get_height(),decimals=2), (p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    plt.show()

def graph_industry(salaries, industry ):

    df = pd.DataFrame({'Salary in Millions': salaries, 'Industry': industry})
    df.set_index('Industry',inplace=True)


    ax = df.plot(kind="bar", title="Average Salary")

    ax.set_ylabel('Salary in Millions')
    ax.legend_.remove()
    ax.axes.get_yaxis().set_visible(True)

    plt.show()


factor = input("by industry or state? ")
url = "https://aflcio.org/paywatch/highest-paid-ceos"
soup = get_soup(url)

selection = soup.find_all('option', selected=False)
industry = [x.text.title() for x in selection][:-51]
state = [x.text for x in selection][-51:]
stateCode = [option['value'] for option in selection][-51:]
total_tickers, total_salaries= [], []

if factor.lower() == "industry":
    for i in industry:
        i = i.replace(',','%2C').replace(' ','%20')
        url = "https://aflcio.org/paywatch/highest-paid-ceos?combine=&industry=" + i + "&state=All&sp500=0&page="
        page = num_pages(url)
        salaries = []
        tickers = []
        #if multiple pages
        if len(page) > 0:
            tickers, salaries = mult_pages_industry()
        #if one page only
        else:
            tickers, salaries = single_page()
        tickers = sum(tickers, [])
        salaries = sum(salaries, [])
        avg_salary = round((sum(salaries)/len(salaries))/1000000.00,2)
        total_tickers.append(tickers)
        total_salaries.append(avg_salary)

    graph_industry(total_salaries,industry)

elif factor.lower() == "state":
    for i in stateCode:
        url = "https://aflcio.org/paywatch/highest-paid-ceos?combine=&industry=All&state=" + i + "&sp500=0&page="
        page = num_pages(url)
        salaries = []
        tickers = []
        #if multiple pages
        if len(page) > 0:
            tickers, salaries = mult_pages_state()
        #if one page only
        else:
            tickers, salaries = single_page()
        tickers = sum(tickers, [])
        salaries = sum(salaries, [])
        avg_salary = round((sum(salaries)/len(salaries))/1000000.00,2)
        total_tickers.append(tickers)
        total_salaries.append(avg_salary)

    graph_state(total_salaries,stateCode)

else:
    pass
