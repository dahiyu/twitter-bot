# coding:utf-8

import os
import requests
import feedparser
import key
from requests_oauthlib import OAuth1Session

TWEET_ENDPOINT = "https://api.twitter.com/1.1/statuses/update.json"
HATEBU_IT_RSS = "http://b.hatena.ne.jp/hotentry/it.rss"
TWEETED_URL_PATH = "./url.txt"

def main():
  text = scraping()
  if text != "":
    tweet(text)

def scraping():
  d = feedparser.parse(HATEBU_IT_RSS)

  text = ""
  if not os.path.exists(TWEETED_URL_PATH):
    with open(TWEETED_URL_PATH, 'w'):
      pass

  with open(TWEETED_URL_PATH, "r") as f:
    lines = f.readlines()
    for entry in d.entries:
      if not(existsEntry(entry, lines)):
        text = entry.link + "\n"
        break

  if text == "":
    return ""

  with open(TWEETED_URL_PATH, "a") as f:
    f.write(text)

  return text

def existsEntry(entry, lines):
  exists = False
  for line in lines:
    line = line.replace("\n","")
    if line == entry.link:
      exists = True
      break
  return exists

def tweet(text):
  twitter = OAuth1Session(key.CONSUMER_KEY,
                          key.CONSUMER_SECRET,
                          key.ACCESS_TOKEN,
                          key.ACCESS_TOKEN_SECRET)

  response = twitter.post(TWEET_ENDPOINT, params = {"status" : "" + text})

  if response.status_code == 200:
    print("Success.")
  else:
    print("Failed. : %d"% response.status_code)

if __name__ == '__main__':
  main()
