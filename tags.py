# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

import requests
import string
import json
import re
import HTMLParser
import editdistance


def create_set_string_care_about():
    tags = set()
    # file_name = "Article_type.txt"
    file_name = "Strings_I_Care_About.txt"
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
    mappings = create_article_type_map_zara(json_response["response"]["data"]["tags"])
    res = {
        'source': 'vogue',
        'misc': []
    }
    for value in json_response["response"]["data"]["tags"]:
        if value in mappings['direct_map']:
            print "Skipped value - " + str(value)
            continue
        if value in mappings['dist_map']:
            at = mappings['dist_map'][value]
            if at not in res:
                res[at] = []
            if value not in res[at]:
                res[at].append(value)
            continue
        if value in mappings['partial_map']:
            at = mappings['partial_map'][value]
            if at not in res:
                res[at] = []
            if value not in res[at]:
                res[at].append(value)
            continue
        res['misc'].append(value)
    return res

    '''
    print "\n\n\n"
    return_tags = {}
    for item in input_tags:
        return_tags[item] = set()
        new_list = [s for s in json_response["response"]["data"]["tags"] if item in s]
        if len(new_list):
            [return_tags[item].add(s) for s in new_list]
        if not len(return_tags[item]):
            return_tags.pop(item)
    return return_tags
    '''


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
    return json.dumps(res)


def main(text):
    response = call_text_enricher(text)
    output_tags = filter_data(response)
    return output_tags


def create_article_type_map_zara(tags):
    c = get_article_types()
    ref_list = {}
    for k in c:
        ref_list[(k.rstrip()).lower()] = True

    not_found = {}
    found_in_color_list = {}
    count = 0
    h = HTMLParser.HTMLParser()

    # 1. Check if the key name already exists
    for k in tags:
        k = h.unescape(k)
        kl = re.split(",|/|&|;|:", k)
        for kvl in kl:
            kvl = kvl.encode("ascii", "ignore")
            kvl = kvl.replace("-", "")
            kv = re.sub('[^A-Za-z]+', '', kvl)
            if kv.strip() in ref_list:
                count += 1
                found_in_color_list[kv.strip()] = kv.strip()
            else:
                kv = kv.replace(" ", "")
                if kv.strip() in ref_list:
                    count += 1
                else:
                    if kvl.strip() not in not_found:
                        not_found[kvl.strip()] = 0
                    not_found[kvl.strip()] += 1

    # 3. Try partial mapping
    # print "Starting step 3..."
    partial_map_ct = 0
    no_partial_map = {}
    partial_map = {}
    for key in not_found:
        ks = key.split(" ")
        f = False
        for k in ks:
            for r in ref_list:
                if r in k:
                    partial_map_ct += 1
                    ks = " ".join(ks)
                    partial_map[ks] = r
                    f = True
                    break
            if f:
                break

        if not f:
            ks = " ".join(ks)
            if ks not in no_partial_map:
                no_partial_map[ks] = 0
            no_partial_map[ks] += 1

    known_keys = ref_list.keys()
    # print "Starting step 4..."
    ct_dist = 0
    no_dist_map = {}
    dist_map = {}
    for key in no_partial_map:
        key_arr = key.split(" ")
        found = False
        for k in key_arr:
            # last_word = key.split(' ')[-1]
            for kk in known_keys:
                # ed = editdistance.eval(last_word, kk)
                ed = editdistance.eval(k, kk)
                # if ed <= 2 or (ed <= 3 and sorted(kk) == sorted(last_word)):
                if ed <= 1 or (ed <= 2 and sorted(kk) == sorted(k)):
                    dist_map[key] = kk
                    ct_dist += 1
                    found = True
                    break
        if not found:
            no_dist_map[key] = True

    full_color_map = {}
    full_color_map["direct_map"] = found_in_color_list
    full_color_map["partial_map"] = partial_map
    full_color_map["dist_map"] = dist_map
    full_color_map["no_dist_map"] = no_dist_map
    return full_color_map


if __name__ == "__main__":
    tags = ['culottes', 'oversized studio shirt', 'studs and chain cross body bag', 'long embroidered bomber jacket', 'multicoloured striped dress', 'frayed peplum top', 'leather platform slides', 'white dungarees with rips', 'blouse with lace trim', 'denim dress', 'high waist skinny trousers', 'denim shirt dress', 'bandana print silk style scarf', 'asymmetric hem shirt', 'cropped trousers with front pleat', 'roll-up sleeve jacket', 'tribal linen coat', 'short tribal skirt', 'crossover metallic sandals', 'bleach wash denim jacket', 'guipure lace bermuda shorts', 'guipure lace bomber jacket', 'wrap skirt', 'oversized linen t-shirt', 'sequin patchwork jacket', 'leather strap sandals', 'tie-dye midi skirt', 'blouse with open back', 'tie-dye jacquard culottes', 'tie-dye hand embroidered poncho', 'mid-rise biker trousers', 'short jumpsuit', 'lace midi dress', 'triple choker necklace', 'straight leg flowing trousers', 'jacket with asymmetric back', 'short jumpsuit', 'striped blouse', 'lace tube skirt', 'guipure lace top', 'bird print flowing bermuda shorts', 'casual roman sandals', 'short jumpsuit', 'mid-rise power stretch trousers', 'short sleeve sweater', 'flat metallic leather sandals', 'lace tube dress', 'openwork coat', 'guipure lace tube dress', 'leather sandals with buckle', 'bomber style jacket', 'plain twill shirt', 'striped back and pocket t-shirt', 'striped indigo shirt', 'striped back and pocket t-shirt', 'striped fabric seamed t-shirt', 'bull denim shirt', 'textured weave suit blazer', 'textured weave suit trousers', 'aviator sunglasses', 'faded denim jumpsuit', 't-shirt with zip on sleeves', 'sweatshirt', 'printed t-shirt', 'flower print t-shirt', 'bleach effect skinny trousers', 'bull denim shirt', 'vintage fade denim dungarees', 'faded indigo striped shirt', 'patch bomber jacket', 'raglan sleeve sweatshirt', 'raglan sleeve sweatshirt', 'textured t-shirt', 'creased texture t-shirt', 'darted trousers with cord', 'textured t-shirt', 'paisley print blazer', 'poplin shirt', 'stretch shirt with mandarin collar', 'paisley print bermuda shorts', 'striped shirt', 'horizontal stripe shirt', 'contrast blue jacket', 'tribal jacquard scarf', 'micro polka dot textured weave bermuda shorts', 'stretch shirt with mandarin collar', 'micro polka dot textured weave blazer', 'poplin shirt with contrasting collar', 'short sleeve nautical print polo shirt', 'short sleeve nautical print polo shirt', 'darted trousers with cord', 'darted trousers with cord', 'short sleeve t-shirt with oversized pocket', 'straw hat', 'short sleeve t-shirt with oversized pocket', 't-shirt with zip on sleeves', 'poplin shirt', 'short sleeve t-shirt with oversized pocket', 'short sleeve t-shirt with oversized pocket', 'street top']
    create_article_type_map_zara(tags)