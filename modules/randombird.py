import requests, re, random

RANDOM_BIRD = 'https://www.pexels.com/search/bird/'

class RandomBird():
    def query(self, url = RANDOM_BIRD):
        image_url = RANDOM_BIRD
        res = requests.get(url)
        res.raise_for_status()
        
        regex = re.compile(r'https://images\S+.jpeg')
        pictures = regex.findall(res.text)
        
        print(len(pictures))
        
        count = len(pictures)
        
        index = random.randint(0, count-1)
        
        image_url = pictures[index] + '?auto=compress&cs=tinysrgb&h=350'
        
        return image_url

def test():
    bird = RandomBird()
    print(bird.query())
    
if __name__ == '__main__':
    for i in range(20):
        test()