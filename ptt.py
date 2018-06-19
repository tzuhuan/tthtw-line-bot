import requests, bs4, sys

PTT = 'https://www.ptt.cc'
PTT_BEAUTY = 'https://www.ptt.cc/bbs/Beauty'
PTT_O2 = 'https://www.ptt.cc/bbs/AllTogether'
PTT_WORLDCUP = 'https://www.ptt.cc/bbs/WorldCup'
PTT_STOCK = 'https://www.ptt.cc/bbs/Stock'

def parse_web(url):
    res = requests.get(url)
    try:
        res.raise_for_status()
    except:
        return url
    
    bs = bs4.BeautifulSoup(res.text, 'html.parser')
    links = bs.select('.title a')
    
    if len(links) == 0:
        return 'Not found.'
	
    results = ""

    #for link in links:
    #    print(str(link))
    #    print(link.get('href'))

    try:	
        for i in range(3):
            results = results + "{}\n{}{}\n".format(links[i].getText(), PTT, links[i].get('href'))
    except:
        return 'Not found.'

    return results
    

def o2():
    url = "{}/search?q={}".format(PTT_O2, '徵男')
    print(url)
    return parse_web(url)  

def fifa():
    return 'FIFA2018 賽程表\n{}\n'.format('https://www.ptt.cc/bbs/WorldCup/M.1528816712.A.BB1.html')

def stock(keyword = ""):
    url = ""
    if len(keyword) == 0:
	    url = PTT_STOCK
    else:
        url = "{}/search?q={}".format(PTT_STOCK, keyword)
    print(url)
    return parse_web(url)
    #return url

def beauty(keyword = ""):
    url = ""
    if len(keyword) == 0:
        url = PTT_BEAUTY
    else:
        url = "{}/search?q={}".format(PTT_BEAUTY, keyword)
    return parse_web(url)
	
if __name__ == '__main__':
    # testing cases
    print("-----test fifa-----")
    print(fifa())
    
    print("-----test o2-----")
    print(o2())
    
    print("-----test stock-----")
    print(stock())
    
    print("-----test stock-----")
    print(stock('標的'))    
    
    print("-----test beauty-----")
    print(beauty())
    
    print("-----test beauty-----")
    print(beauty('高中'))
    
