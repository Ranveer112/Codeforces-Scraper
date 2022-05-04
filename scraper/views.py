from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import os
import argparse
import re
import time


def index(request):
    return render(request, 'index.html')

def fetch(request):
    handle = request.GET['handle']
    pattern =request.GET['pattern']
    target_lang = request.GET['lang']
    FROM = 1
    TILL = 10000
    COUNT = 1
    URL = "https://codeforces.com/api/user.status?handle=" + handle + "&from=" + str(FROM) + "&count=" + str(TILL)
    print(target_lang)
    response = requests.get(URL)
    submissions = response.json()["result"]
    normalizedSubmissions = []
    OK = "OK"
    for i in range(0, len(submissions)):
        if submissions[i]['verdict'] == OK and submissions[i]['programmingLanguage'] == target_lang:
            normalizedSubmissions.append({'sId': submissions[i]['id'], 'contestId': submissions[i]['contestId'],
                                          'name': submissions[i]['problem']['name'],
                                          'lang': submissions[i]['programmingLanguage']})
    #FILE_EXTENSIONS = {'GNU C++17': 'cpp', 'GNU C++14':'cpp', 'GNU C++20(64)':'cpp',  'Java 5': 'java', 'Java 8': 'java'}
    for i in range(0, len(normalizedSubmissions)):
        time.sleep(2)
        URL = "https://codeforces.com/contest/" + str(normalizedSubmissions[i]['contestId']) + "/submission/" + str(
            normalizedSubmissions[i]['sId'])
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find(id="program-source-text"):
            code = soup.find(id="program-source-text").get_text()
            if re.search(pattern, code):
                context={'code':code}
                return render(request, 'index.html', context)
    return render(request, 'index.html')
