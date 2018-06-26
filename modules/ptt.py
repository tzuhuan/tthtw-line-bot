import requests, bs4, sys
import random

PTT = 'https://www.ptt.cc'
PTT_BBS = 'https://www.ptt.cc/bbs/'
PTT_WORLDCUP = 'https://www.ptt.cc/bbs/WorldCup'

def send_request(url):
    res = requests.get(url)
    try:
        res.raise_for_status()
    except:
        return url
        
    return res.text
    
def get_html_tag_elements(html_source, pattern):
    bs = bs4.BeautifulSoup(html_source, 'html.parser')
    return bs.select(pattern)

def parse_web(url):
    res = send_request(url)
    links = get_html_tag_elements(res, '.title a')
    
    if len(links) == 0:
        return 'Not found.'
	
    results = ""

    #for link in links:
    #    print(str(link))
    #    print(link.get('href'))

    count = len(links)
    if count > 3:
        count = 3
        
    for i in range(count):
        results = results + "{}\n{}{}\n".format(links[i].getText(), PTT, links[i].get('href'))

    return results
    
def get_imgur_url(url):
    res = send_request(url)
    web_links = get_html_tag_elements(res, '.richcontent a')
    
    url_candidates = []
    for link in web_links:
        url = link.get('href')
        if url.find('imgur.com'):
            url = 'https:' + url
            url_candidates.append(url)
            
    count = len(url_candidates)
    if count > 0:
        url = url_candidates[random.randint(0, count-1)]
        return get_photo(url)
    
    return url
    
def get_photo(url):
    res = requests.get(url)
    try:
        res.raise_for_status()
    except:
        return url
        
    bs = bs4.BeautifulSoup(res.text, 'html.parser')
    tags = bs.select('meta[name="twitter:image"]')
    return tags[0].get('content')
    
def random_beauty():
    url = '{}{}/search?q={}'.format(PTT_BBS, 'beauty', '正妹')
    res = send_request(url)
    articles = get_html_tag_elements(res, '.title a')
    chosen = articles[random.randint(0, len(articles) -1)];
    return get_imgur_url(PTT + chosen.get('href'))
    
def fifa():
    return 'WorldCup 2018 賽程表\n{}\n'.format('https://www.ptt.cc/bbs/WorldCup/M.1528816712.A.BB1.html')
	
def query(commands):
    commands = commands.split()
    length = len(commands)
    if length < 2: # ptt
        return ""
    
    if length == 2: # ptt Stock
        if commands[1] == 'allTogether':
            url = '{}{}/search?q={}'.format(PTT_BBS, commands[1], '徵男')
        elif commands[1] == 'pic': # ptt pic
            return random_beauty();
        else:
            url = '{}{}'.format(PTT_BBS, commands[1])
    else: # ptt Stock 0050
        url = '{}{}/search?q={}'.format(PTT_BBS, commands[1], commands[2])
    
    return parse_web(url)
    
def test():
    #print("-----ptt fifa-----")
    #print(fifa())
    
    #print("-----ptt AllTogether-----")
    #print(query('ptt AllTogether'))

    #print("-----ptt allTogether 台北-----")
    #print(query('ptt allTogether 台北'))
    
    #print("-----ptt Stock-----")
    #print(query('ptt Stock'))
    
    #print("-----ptt stock 0050-----")
    #print(query('ptt stock 0050'))
    
    #print("-----ptt Beauty-----")
    #print(query('ptt Beauty'))
    
    #print("-----ptt beauty 高中-----")
    #print(query('ptt beauty 高中'))

    print(query('ptt pic'))
    
if __name__ == '__main__':
    test()
    
