from html.parser import HTMLParser
import re
import requests

class MyHTMLParser(HTMLParser):

    def handle_data(self, data):
        m_GB = re.search(r'[0123456789].*[G]', data)
        m_MB = re.search(r'[0123456789].*[M]', data)
        m_KB = re.search(r'[0123456789].*[K]', data)
        date = re.search(r'.*-.*-.*',data)
        gameTitle = re.search(r'.*7z',data)
        
        try:
            if date:
                pass
            elif gameTitle:
                list_gameTitles.append(data)
            elif m_GB:
                data = data[:-1]
                data = float(data)
                size_B = data*1000000000
                list_bytes.append(size_B)
            elif m_MB:
                data = data[:-1]
                if ',' in data:
                    data = data.replace(',','')
                data = float(data)
                size_B = data*1000000
                list_bytes.append(size_B)
            elif m_KB:
                data = data[:-1]
                data = float(data)
                size_B = data*1000
                list_bytes.append(size_B)
        except:
            print(f"ERROR: encountered invalid file size: {data}")

websites = ['https://archive.org/download/RedumpSonyPS2NTSCU','https://archive.org/download/RedumpSonyPS2NTSCUPart2']
list_bytes = []
total_fileSize = [] # total file size of all the games in GB

for website in websites:
    list_gameTitles = []
    
    r = requests.get(website) # get site
    parser = MyHTMLParser() 
    parser.feed(r.text) # feed html to parser

    sum_bytes = sum(list_bytes) # total file size
    
    total_gb = sum_bytes * .0000000009
    total_mb = sum_bytes * .0000009
    total_fileSize.append(total_gb)
    print(f'Website: {website}\nTotal file size: {total_gb} GB\nTotal games: {len(list_gameTitles)}\n')

print(f'Total file size of all games: {sum(total_fileSize)} GB')