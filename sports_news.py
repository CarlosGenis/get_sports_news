# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#function that checks if a link can be scraped for data
def check_if_readable(link):
    url = link
    page = requests.get(url)
    return (page.text)

#check_if_readable("https://www.bbc.com/sport/football")

#make soups here
URL = "https://www.bbc.com/sport/football/gossip"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
#print(soup)

#basketball soup 
basketballURL = "https://www.nba.com/news/category/top-stories"
basketballpage = requests.get(basketballURL)
basketballsoup = BeautifulSoup(basketballpage.content, "html.parser")
#print basketball soup
#print(basketballsoup)

def get_title(soup, lookHere):
    title = soup.find(class_=lookHere).text
    return title

#print(get_title(soup))

#make links for football
football_gossip_class = 'gel-trafalgar-bold qa-story-headline gs-u-mv+'
football_gossip_body = "qa-story-body story-body gel-pica gel-10/12@m gel-7/8@l gs-u-ml0@l gs-u-pb++"
football_gossip_title = get_title(soup, football_gossip_class)
#print(football_gossip_title)

#make links for basketball
basketball_top_stories_class = "Columns_left__XkWXE"
basketball_class = "ArticleTile_tile__y70gI"

def get_text(soup, lookHere):
    
    body = soup.find(class_=lookHere)
    text = [p.text for p in body.find_all("p")] 
    return text

#print(get_text(soup, football_gossip_body))
football_headlines = get_text(soup, football_gossip_body)
#print(get_text(basketballsoup, basketball_top_stories_class))

#initialize the app
if not firebase_admin._apps:
    cred = credentials.Certificate("htr-sports-firebase-adminsdk-e7d0r-0a3a0b0e41.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://htr-sports-default-rtdb.firebaseio.com/'
        })
#Makes reference and retrieves dara
#ref = db.reference("/Posts")
#print(ref.get())

football_gossip_ref = db.reference("/FootballGossip")
#football_gossip_ref.push("testing2")

#def push_to_db(db_ref, contentsList)

#print(football_gossip_title)
football_gossip_ref.push(football_gossip_title)
football_gossip_ref.push(football_headlines)