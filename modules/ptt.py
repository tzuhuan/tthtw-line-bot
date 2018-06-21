import requests, bs4, sys

PTT = 'https://www.ptt.cc'
PTT_BBS = 'https://www.ptt.cc/bbs/'
PTT_WORLDCUP = 'https://www.ptt.cc/bbs/WorldCup'

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

def fifa():
    return 'WorldCup 2018 賽程表\n{}\n'.format('https://www.ptt.cc/bbs/WorldCup/M.1528816712.A.BB1.html')
	
def query(commands):
    commands = commands.split()
    length = len(commands)
    if length < 2: # ptt
        return ""
    
    if length == 2: # ptt Stock
        if commands[1] == 'AllTogether':
            url = '{}{}/search?q={}'.format(PTT_BBS, commands[1], '徵男')
        else:
            url = '{}{}'.format(PTT_BBS, commands[1])
    else: # ptt Stock 0050
        url = '{}{}/search?q={}'.format(PTT_BBS, commands[1], commands[2])
    
    return parse_web(url)
    
def test():
    print("-----test fifa-----")
    print(fifa())
    
    print("-----test AllTogether-----")
    print(query('ptt AllTogether'))

    print("-----test allTogether 台北-----")
    print(query('ptt allTogether 台北'))
    
    print("-----test Stock-----")
    print(query('ptt Stock'))
    
    print("-----test stock 0050-----")
    print(query('ptt stock 0050'))
    
    print("-----test Beauty-----")
    print(query('ptt Beauty'))
    
    print("-----test beauty 高中-----")
    print(query('ptt beauty 高中'))  
    
if __name__ == '__main__':
    test()
    
