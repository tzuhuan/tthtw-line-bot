import requests, bs4

RANDOM_CAT = 'http://random.cat/'

class RandomCat():
    def query(self, url = RANDOM_CAT):
        image_url = RANDOM_CAT
        stop = False
        
        while not stop:
            res = requests.get(url)
            try:
                res.raise_for_status()
            except:
                break;
            
            bs = bs4.BeautifulSoup(res.text, 'html.parser')
            tags = bs.select('#cat')
            link = tags[0].get('src')
            
            if link.find('.gif') != -1 or link.find('.png') != -1:
                continue
            
            image_url = link
            stop = True
        
        return image_url     

def test():
    cat = RandomCat()
    print(cat.query())
    
if __name__ == '__main__':
    for i in range(20):
        test()