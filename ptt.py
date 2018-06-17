import requests, bs4, sys

PTT = 'https://www.ptt.cc'
PTT_BEAUTY = 'https://www.ptt.cc/bbs/Beauty'
PTT_O2 = 'https://www.ptt.cc/bbs/AllTogether'

def parse_web(url):
    res = requests.get(url)
    res.raise_for_status()
    
    bs = bs4.BeautifulSoup(res.text, 'html.parser')
    links = bs.select('.title a')

    print(str(len(links)))

    results = []
    count = 0

    for link in links:
        print(str(link))
        print(link.get('href'))
            
    results.append("{}\n{}{}\n".format(links[0].getText(), PTT, links[0].get('href')))
    results.append("{}\n{}{}\n".format(links[1].getText(), PTT, links[1].get('href')))
    results.append("{}\n{}{}\n".format(links[2].getText(), PTT, links[2].get('href')))

    print('\n')

    for i in results:
        print(i)

    return results
    

def o2():
    url = "{}/search?q={}".format(PTT_O2, '徵男')
    print(url)
    return parse_web(url)

def beauty(keyword):
    url = "{}/search?q={}".format(PTT_BEAUTY, keyword)
    print(url)
    return parse_web(url)
	
if __name__ == '__main__':
    url = ''
    if sys.argv[1] == 'o2':
        o2()
    elif sys.argv[1] == 'beauty':
        beauty(sys.argv[2]);
    else:
        print('command error')
    
