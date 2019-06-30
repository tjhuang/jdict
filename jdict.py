#!/usr/bin/env python3

import requests
import json
import sys
import vlc
import time

oxford_api = "https://od-api.oxforddictionaries.com:443/api/v2/entries/en/"
app_id = ""
app_key = ""

pronun_audio = []

def parse_senses(senses_data):
    for s in senses_data:
        if "definitions" in s:
            print("  *  {}\n".format(s["definitions"][0]))

def parse_entries(entries):
    for e in entries:
        if "senses" in e:
            parse_senses(e["senses"])

def parse_pronun(pronun_data):
    for p in pronun_data:
            if "audioFile" in p:
                pronun_audio.append(p["audioFile"])
    
def parse_lexical_entries(lexical_entries):
    for l in lexical_entries:
        if "lexicalCategory" in l:
            print("[{}]".format(l["lexicalCategory"]["text"]))

        if "pronunciations" in l:
           parse_pronun(l["pronunciations"])

        if "entries" in l:
            parse_entries(l["entries"])

def parse_results(results_data):
    for r in results_data:
        if "lexicalEntries" in r:
            parse_lexical_entries(r["lexicalEntries"])

def lookup(action, word):
    r = requests.get(oxford_api + word.lower(), headers={"app_id": app_id, "app_key": app_key}) 

    if r.status_code != 200:
        print("Failed to query with status code {}".format(r.status_code))
        sys.exit()

    jdata = json.loads(r.text)

    parse_results(jdata["results"])

    if action == "speak" and pronun_audio[0]:
        player = vlc.MediaPlayer(pronun_audio[0])
        player.play()
        time.sleep(3)

if app_id == "" or app_key == "":
    print("Fill the Oxford Dictionary ID and Key")
    sys.exit()

try:
    action = sys.argv[1]
    word = sys.argv[2]
    lookup(action, word)
except IndexError:
    print("Usage: jdict <search|speak> <WORD>")

