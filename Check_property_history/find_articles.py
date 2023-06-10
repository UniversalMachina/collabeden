import nltk
from bs4 import BeautifulSoup
from selenium import webdriver

#this code checks if there any relevant articles about the property
property="147 hope ave"
query = f'{property} news'
#get news links
def getlinks(query):
    driver = webdriver.Chrome("chromedriver.exe")
    # Query to obtain links
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    links = [] # Initiate empty list to capture final results
    #gets the first 10 results
    url = "http://www.google.com/search?q=" + query + "&start=" +  str((1 - 1) * 10)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    search = soup.find_all('div', class_="yuRUbf")
    for h in search:
        links.append(h.a.get('href'))
    return links
links=getlinks(query)
print(links)


import requests
from bs4 import BeautifulSoup
titles=[]
for link in links:
    try:
        response = requests.get(link, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.title:  # Check if title tag exists
            title = soup.title.string
            print(title)
            titles.append(title)
        else:
            print(f"No title tag found for {link}")
            titles.append(f"Not An Article")
    except requests.exceptions.RequestException as err:
        print ("Error occurred: ",err)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)


for title in titles:
    import openai
    openai.api_key = "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"

    def generate_text(prompt):
        import time
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt},
                    ]
                )
                message = completion["choices"][0]["message"]["content"]
                return message
            except Exception as e:
                print(f"Error occurred: {e}. Retrying...")
                time.sleep(1)  # Optional: add a time delay between attempts
        else:
            print(f"Failed after {max_attempts} attempts.")
    ans=generate_text(f"is {title} a news article, return yes or no only")
    print(ans)

# driver.close()
#
# import spacy
# from spacy.lang.en.stop_words import STOP_WORDS
# from string import punctuation
# from heapq import nlargest
#
# #read articles
# import trafilatura
# #test links
# #downloaded = trafilatura.fetch_url('https://www.britannica.com/topic/the-Beatles')
# downloaded = trafilatura.fetch_url('https://www.bbc.com/news/uk-61585886')
# articletext=trafilatura.extract(downloaded)
#
#
# #countOfWords = len(sentence.split())
# articlesentences=articletext.split("\n")
# countOfWords=[]
# newsentece=""
# #removes paragraphs with less than 12 words (to filter out ads and authurs)
# for i in range(len(articlesentences)-1):
#     holder=len(articlesentences[i].split())
#     countOfWords.insert(i,holder)
#     if countOfWords[i] > 12:
#         newsentece+=articlesentences[i]+"\n"
#
# #summerizes article
# def summarize(text, per):
#     nlp = spacy.load('en_core_web_sm')
#     doc= nlp(text)
#     tokens=[token.text for token in doc]
#     word_frequencies={}
#     for word in doc:
#         if word.text.lower() not in list(STOP_WORDS):
#             if word.text.lower() not in punctuation:
#                 if word.text not in word_frequencies.keys():
#                     word_frequencies[word.text] = 1
#                 else:
#                     word_frequencies[word.text] += 1
#     max_frequency=max(word_frequencies.values())
#     for word in word_frequencies.keys():
#         word_frequencies[word]=word_frequencies[word]/max_frequency
#     sentence_tokens= [sent for sent in doc.sents]
#     sentence_scores = {}
#     for sent in sentence_tokens:
#         for word in sent:
#             if word.text.lower() in word_frequencies.keys():
#                 if sent not in sentence_scores.keys():
#                     sentence_scores[sent]=word_frequencies[word.text.lower()]
#                 else:
#                     sentence_scores[sent]+=word_frequencies[word.text.lower()]
#     select_length=int(len(sentence_tokens)*per)
#     summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
#     final_summary=[word.text for word in summary]
#     summary=''.join(final_summary)
#     return summary
#
#
# #print(len(sentence.split()))
# #get word count of article
# x=len(articletext.split())
# #the amount of text you want to take from the article
# y=round(x/400, 2)
# #puts each new sentence into a list
# newnewsetences=(summarize(newsentece, round(1/y, 2))).split("\n")
#
#
# tokencount=int()
# finishedtext=""





