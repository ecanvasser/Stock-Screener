import json
import requests
from textblob import TextBlob
from datetime import date

class Stock:
    # receives list of strings as argument
    def getScorePrice(tickers):
        args = tickers
        today = date.today().strftime('%m%d%Y')
        final_stats = []
        for arg in args:
            sentiment_response = requests.get('https://stocknewsapi.com/api/v1?tickers={}&items=15&date={}-{}&sortby=unique&token='.format(arg,today,today)).json()

            price_response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=1min&apikey='.format(arg)).json()
            prices_json = list(price_response['Time Series (1min)'].values())

            # Filters article text by length and ticker symbol(s), and adds [text, ticker] to list
            text_tick = []
            for i in range(len(sentiment_response['data'])):
                for item in sentiment_response['data']:
                    tick = sentiment_response['data'][i]['tickers']
                    text = sentiment_response['data'][i]['text']
                    text_split = text.split(' ')
                    if (len(tick) == 1) and (len(text_split) > 11):
                        ticker = tick
                        text_format = [text, ticker]
                        text_tick.append(text_format)
                    else:
                        pass
            
            # Cleans text_tick list by removing all repeated values. Only saves the unique values
            cleaned_text = []            
            for items in text_tick:
                if items not in cleaned_text:
                    cleaned_text.append(items)

            # Finds total number of articles per ticker            
            ticks_freq = {}
            for t in cleaned_text:
                ticks = t[1][0]
                if ticks in ticks_freq:
                    ticks_freq[ticks] += 1
                else:
                    ticks_freq[ticks] = 1

            # Checks if all arguments have sentiment score. If not, passes text response
            keys = list(ticks_freq.keys())
            for t in args:
                if t in keys:
                    pass
                else:
                    ticks_freq[t] = 'No news found'
            
            scores = {}
            raw_scores = []
            # # Sorts the raw scores into a list from each each list inside cleaned_text
            for i in range(len(cleaned_text)):
                t = cleaned_text[i][1][0]
                txt = cleaned_text[i][0]
                for a in args:
                    if t == a:
                        tblob = TextBlob(txt)
                        pol = round(tblob.sentiment.polarity, 2)
                        raw_scores.append([pol,a])
            # Calculates final score
            total_score = 0
            for b in raw_scores:
                score = b[0]
                ticker = b[1]
                total_score += score

            # Inputs final score into final_score dictionary
            final_stats.append({'ticker': arg, 'price': float(prices_json[0]['4. close']), 'sentiment': round(total_score, 2)})
            
        return final_stats
