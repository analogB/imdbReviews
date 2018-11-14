#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 13:34:20 2018

@author: brad
"""
#pip install -e git+https://github.com/analogB/imdbpy#egg=rogers
import imdb  # to access imdb API

import pandas # for data array handling
from numpy import nan
from bs4 import BeautifulSoup
import requests
import re
import time

#the input to this program is a url to a public IMDB movie list
listpath = 'https://www.imdb.com/list/ls045539551/'
listsoup = BeautifulSoup(requests.get(listpath).text,'lxml')
movie_list = [[re.sub('(^.*?tt)','',header.find('a')['href'])[0:7],header.find('a').contents[0]] for header in listsoup.find_all(class_="lister-item-header")]

ia = imdb.IMDb()     

df = pandas.DataFrame(columns=[
    'movie_title',
    'imdb_movie_id',
    'movie_rating',
    'review_title',
    'review_date',
    'review_author',
    'review_rating',
    'review_helpful',
    'review_not_helpful',
    'review_source',
    'review_content']) # initialise data frame

index=0
print('Loading IMDB reviews for:')
x=6
for i in range(x,len(movie_list)-1): # for each movie
    print(movie_list[i][1])
    mo_rating = ia.get_movie_vote_details(movie_list[i][0])['data']['arithmetic mean']
    
    #get_movie_reviews has to push the load more button in the website until it disappears, this seems to conflict with an animated popup ad that sometimes appears ugh
    mo_reviews = ia.get_movie_reviews(movie_list[i][0])['data']['reviews']  # Meta critic
    
    for k in range(len(mo_reviews)-1):
        index+=1
        if (type(mo_reviews[k]['rating'])==int):
            rev_rating = mo_reviews[k]['rating']                
        else:
            rev_rating = nan
            
        df=df.append(pandas.DataFrame(index=[index],data={
            'movie_title':      movie_list[i][1],
            'imdb_movie_id':    movie_list[i][0],
            'movie_rating':     mo_rating,
            'review_title':     mo_reviews[k]['title'],
            'review_date':      mo_reviews[k]['date'],
            'review_author':    mo_reviews[k]['author'],
            'review_rating':    float(rev_rating),
            'review_helpful':   mo_reviews[k]['helpful'],
            'review_not_helpful':mo_reviews[k]['not_helpful'],
            'review_source':    'IMDb',
            'review_content':   mo_reviews[k]['content'],
            
            }))