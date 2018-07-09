import twstock

PRICE_LENGTH = 7
VOLUME_LEHGTH = 7

class Stock():    
    def query(self, stock_number = '2330'):
        data = twstock.realtime.get(stock_number)
        stock = twstock.Stock(stock_number)
        return self.parse_data(data, stock)
        
    def parse_data(self, data, stock):
        try:
            if not data['success']:
                return 'error'
            
            company_name = data['info']['name']
            company_code = data['info']['code']
            latest_trade_price = data['realtime']['latest_trade_price']
            open_price = data['realtime']['open']
            best_bid_price = data['realtime']['best_bid_price']
            best_bid_volume = data['realtime']['best_bid_volume']
            best_ask_price = data['realtime']['best_ask_price']
            best_ask_volume = data['realtime']['best_ask_volume']
        
            result = company_name + ' (' + company_code + ')\n'

            result = result + '即時價格: ' + latest_trade_price + '\n開盤價: ' + open_price + '\n'
            
            bfp = twstock.BestFourPoint(stock)
            strategy = bfp.best_four_point()
            
            if strategy != None:
                if strategy[0] == True:
                    result = result + '買,'
                else:
                    result = result + '賣, '
                
                result = result + strategy[1] + '\n'
            
            #result = result + '買'.center(PRICE_LENGTH + VOLUME_LEHGTH - 1, '-') + '\n'
            #for i in range(5):
            #    result = result + \
            #             best_bid_volume[i].ljust(PRICE_LENGTH, ' ') + \
            #             best_bid_price[i].rjust(VOLUME_LEHGTH, ' ') + \
            #             '\n'
            
            #result = result + '賣'.center(PRICE_LENGTH + VOLUME_LEHGTH - 1, '-') + '\n'
            #for i in range(5):
            #    result = result + \
            #             best_ask_volume[i].ljust(PRICE_LENGTH, ' ') + \
            #             best_ask_price[i].rjust(VOLUME_LEHGTH, ' ') + \
            #             '\n'            
            
            return result
            
            #print(company_name + ' (' + company_code + ')')
            #print('即時價格: ' + latest_trade_price + ', 開盤價: ' + open_price)
            
            #print('買'.center(PRICE_LENGTH + VOLUME_LEHGTH, '-') + '|' + '賣'.center(PRICE_LENGTH + VOLUME_LEHGTH, '-'))
            #for i in range(5):
            #    print(best_bid_price[i].ljust(PRICE_LENGTH, ' ') + \
            #          best_bid_volume[i].rjust(VOLUME_LEHGTH) + \
            #          '  ' + \
            #          best_ask_price[i].ljust(PRICE_LENGTH, ' ') + \
            #          best_ask_volume[i].rjust(VOLUME_LEHGTH, ' '))
            
        except:
            return 'data error'
        
if __name__ == '__main__':
    stock = Stock()
    
    print('-----5203-----')
    result = stock.query('5203')
    print(result)
    
    s = twstock.Stock('5203')
    bfp = twstock.BestFourPoint(s)
    print(bfp.best_four_point())
    
    #print('-----2330-----')
    #result = stock.query()
    #print(result)
    
    #print('-----3008-----')
    #result = stock.query('3008')
    #print(result)    
    
    #print('-----0000-----')
    #result = stock.query('0000')
    #print(result)