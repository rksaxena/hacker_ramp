# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

import requests
import string
import json


def create_set_string_care_about():
    tags = set()
    file_name = "Article_type.txt"
    # file_name = "Strings_I_Care_About.txt"
    f = open(file_name, 'r')
    for line in f:
        values = line.split(',')
        if values[0].lower()[:-1] in tags:
            continue
        tags.add(values[0].lower()[:-1])
    return tags

def create_set_article_types():
    ats = set()
    file_name = "Article_type.txt"
    f = open(file_name, 'r')
    for line in f:
        values = line.split(',')
        if values[0].lower()[:-1] in ats:
            continue
        ats.add(values[0].lower()[:-1])
    return ats

tags = {}
article_types = {}

def get_tags():
    global tags
    if len(tags) == 0 or len(tags) == 1:
        tags = create_set_string_care_about()
    return tags


def get_article_types():
    global article_types
    if len(article_types) == 0 or len(article_types) == 1:
        article_types = create_set_article_types()
    return article_types

def call_text_enricher(text):
    printable = string.printable
    text = filter(lambda x: x in printable, text)
    url = "http://text-enricher.myntra.com/AttrTags"
    payload = {
        "id": "123",
        "payload":
            {
                "text_to_enrich": text,
                "entity_id": "234"
            }
    }
    res = requests.post(url=url, data=json.dumps(payload), headers={'Content-type': 'application/json'})
    return res


def filter_data(res):
    input_tags = get_tags()
    json_response = res.json()
    return_tags = {}
    for item in input_tags:
        return_tags[item] = set()
        new_list = [s for s in json_response["response"]["data"]["tags"] if item in s]
        if len(new_list):
            [return_tags[item].add(s) for s in new_list]
        if not len(return_tags[item]):
            return_tags.pop(item)
    return return_tags


def create_response(tags):
    res = {}
    article_types = get_article_types()
    for tag in tags:
        if tag in article_types:
            res[tag] = []
            for t in tags[tag]:
                res[tag].append(t)
        else:
            if "Misc" not in res:
                res["Misc"] = []
            for t in tags[tag]:
                res["Misc"].append(t)
    print json.dumps(res)


def main(text):
    response = call_text_enricher(text)
    output_tags = filter_data(response)
    return output_tags
