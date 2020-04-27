import json
import requests
from textblob import TextBlob

def getScore(tickers):
    response = requests.get('https://stocknewsapi.com/api/v1?tickers={}&items=15&date=04242020-04242020&sortby=unique&token=q4ozzmxwlsgzgp8ht8jucd8iqthrnpj44htf5i4b'.format(tickers)).json()
    # print(response)

    # Filters article text by length and ticker symbol(s), and adds [text, ticker] to list
    text_tick = []
    for i in range(len(response['data'])):
        for item in response['data']:
            tick = response['data'][i]['tickers']
            text = response['data'][i]['text']
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
    args = tickers
    for t in args:
        if t in keys:
            pass
        else:
            ticks_freq[t] = 'No news found'
    
    scores = {}
    raw_scores = []
    # Sorts the raw scores into a list from each each tuple inside cleaned_text
    for i in range(len(cleaned_text)):
        t = cleaned_text[i][1][0]
        txt = cleaned_text[i][0]
        for a in args:
            if t == a:
                tblob = TextBlob(txt)
                pol = round(tblob.sentiment.polarity, 2)
                raw_scores.append([pol,a])
    # Calculates score for each ticker inside raw_scores
    for b in raw_scores:
        score = b[0]
        ticker = b[1]
        if ticker in scores:
            scores[ticker] += score 
        else:
            scores[ticker] = score
    
    print(scores)
    print(ticks_freq)

getScore(['FB','TSLA','AAPL'])
