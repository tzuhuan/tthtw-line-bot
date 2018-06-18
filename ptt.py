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
	
    results = ['bot:\n']

    for link in links:
        print(str(link))
        print(link.get('href'))

    try:	
        results.append("{}\n{}{}\n".format(links[0].getText(), PTT, links[0].get('href')))
        results.append("{}\n{}{}\n".format(links[1].getText(), PTT, links[1].get('href')))
        results.append("{}\n{}{}\n".format(links[2].getText(), PTT, links[2].get('href')))
    except:
        return 'Not found.'

    print('\n')

    for i in results:
        print(i)
    #return url
    return results
    

def o2():
    url = "{}/search?q={}".format(PTT_O2, '徵男')
    print(url)
    return parse_web(url)  

def fifa():
    return 'FIFA2018 賽程表\n{}'.format('https://www.ptt.cc/bbs/WorldCup/M.1528816712.A.BB1.html')

def stock(keyword):
    url = ""
    if len(keyword) == 0:
	    url = PTT_STOCK
    else:
        url = "{}/search?q={}".format(PTT_STOCK, keyword)
    print(url)
    return parse_web(url)
    #return url

def beauty():
    url = PTT_BEAUTY
    return parse_web(url)
	
if __name__ == '__main__':
    print(sys.argv)
    commands = sys.argv[1].split()
    print(commands)
    if commands[0] == 'o2':
        print(o2())
    elif commands[0] == 'stock':
        if len(commands) > 1:
            print(stock(commands[1]))
        else:
            print(stock(""))
    elif commands[0] == 'fifa':
        print(fifa())
    elif commands[0] == 'beauty':
        print(beauty())
    else:
        print('command error')
    
