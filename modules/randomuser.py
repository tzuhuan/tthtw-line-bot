import requests, json

RANDOM_USER_API = 'https://randomuser.me/api/?'
random_user_params = {'results' : '1',
                     'gender' : 'female',
                     'nat' : 'us',
                     'inc' : 'picture'}

class RandomUser():
    def __init__(self):
        self.url = RANDOM_USER_API
        for i in random_user_params:
            self.url = self.url + i + '=' + random_user_params[i] + '&'
        self.url = self.url[:-1] # remove the latest &    
        #print(self.url)
        
    def query(self):
        res = requests.get(self.url)
        try:
            res.raise_for_status()
        except:
            return url
            
        data = json.loads(res.text)
        #print(data['results'][0]['picture']['thumbnail'])
        return data['results'][0]['picture']['thumbnail']
        
def test():
    user = RandomUser()
    return user.query()

if __name__ == '__main__':
    print(test())