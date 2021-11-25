import requests
import csv
from bs4 import BeautifulSoup as BS
import pandas as pd
import os


def scrape(link, index):
    req_comp = ['CPU', 'CPU Cooler', 'Motherboard', 'Memory', 'Storage', 'Video Card', 'Case', 'Power Supply', 'Monitor']
    cp_type = []
    cp_name = []
    csv_input = {}
    data = requests.get(link).text
    soup = BS(data, "html.parser")
    partlist = soup.find_all("table", class_="partlist partlist--mini")
    for part in partlist:
        c = part.find_all("td", class_="td__component")
        n = part.find_all("td", class_="td__name")
        for x in c:
            if x.find("h4"):
                cp_type.append(x.find("h4").text)
        for y in n:
            if y.find("a"):
                cp_name.append(y.find("a").text)
    for i in range(len(cp_type)):
        if cp_type[i] in req_comp:
            csv_input[cp_type[i]] = cp_name[i]
    f_name = 'scraped_data\\pcbuild' + str(index) + '.csv'
    if not os.path.exists('scraped_data'):
        os.mkdir('scraped_data')
    csv_df = pd.DataFrame.from_dict([csv_input])
    csv_df.transpose()
    csv_df.to_csv(f_name)
    '''with open(f_name, 'x', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Component', 'Name'])
        for key, value in csv_input.items():
            writer.writerow([key, value])'''


if __name__ == "__main__":
    df = pd.read_excel('input.xlsx')
    links = df['links']
    for i in range(len(links)):
        print('Scraping data from: '+links[i]+' Row:'+str(i))
        scrape(links[i], i)
    print('All done!')