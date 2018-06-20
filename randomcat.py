import requests, bs4

RANDOM_CAT = 'http://random.cat/'

class RandomCat():
    def query(self, url = RANDOM_CAT):   
        res = requests.get(url)
        try:
            res.raise_for_status()
        except:
            return RANDOM_CAT
            
        bs = bs4.BeautifulSoup(res.text, 'html.parser')
        links = bs.select('#cat')
        
        return links[0].get('src')
        

def test():
    cat = RandomCat()
    print(cat.query())
    
if __name__ == '__main__':
    test()