import requests, bs4
import random

class RandomWife():
    def query(self):
        wife_list = ['https://imgur.com/AOV9FRn',
                     'https://imgur.com/dNczf84',
                     'https://imgur.com/DpkLjzH']
                     
        url = wife_list[random.randint(0, 2)]
        res = requests.get(url)
        try:
            res.raise_for_status()
        except:
            return "";
            
        bs = bs4.BeautifulSoup(res.text, 'html.parser')
        tags = bs.select('meta[name="twitter:image"]')
        return tags[0].get('content')
        #print(tags[0].get('content'))
        
        
def test():
    wife = RandomWife()
    return wife.query()
    
if __name__ == '__main__':
    for i in range(3):
        print(test())