import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
#   https://coinmarketcap.com/all/views/all/
import cx_Oracle        # sample


def get_html(url):
    r = requests.get(url)   # return response object
    return r.text   # return html object


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('table', id='currencies-all').find_all('td', class_='currency-name')
    links = []
    for td in tds:
        a = td.find('a').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1', class_='details-panel-item--name').text.split()
    except:
        name = ''
    try:
        price = soup.find('span', id='quote_price').text.split()
    except:
        price = ''
    data = {'name': name, 'price': price}
    return data

def write_csv(data):
    with open('currency.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'],
                         data['price']))
        print(data['name'], data['price'])

def get_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    url = 'https://coinmarketcap.com/all/views/all/'
    all_links = get_all_links(get_html(url))
#    for url_1 in all_links:
#        html = get_html(url_1)
#        data = get_page_data(html)
#        write_csv(data)
    with Pool(20) as p:
        p.map(get_all, all_links)


if __name__ == '__main__':
    main()
