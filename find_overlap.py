import tags
import difflib

vogue_data = {'foundation': ['Mousse Foundation'], 'chain': ['chain'], 'corset': ['closet'], 'tops': ['jersey top'], 'misc': ['everyday heavy duty makeup', 'minimum', 'gallery', 'place', 'heart-wrenching classic', 'blends', 'midway', 'high level', 'fashionista', 'heart-wrenching classic', 'skin types', 'skin types', 'faux fur bomber', 'everyday heavy duty makeup', 'everyday', 'off-shoulder blouses', 'style', 'acute aversion', 'gold accents', 'bell-bottoms', 'cabana', 'makes', 'faux fur bomber', 'long lasting', 'early 19th century', 'tones', 'Bollywood', 'erstwhile flower childs', 'bohemian sartorial sensibility', 'off-shoulder blouses', 'celebrity-inspired summer', 'cool evening winds', 'animal prints', 'perfect canvas', 'make-up free look', 'fashion accessory', 'no-make up', 'great coverage', 'collarbone steal', 'womens', 'thinking ahead', 'faux fur bomber', 'leather', 'light', 'popularity charts', 'Amazon India Fashion Week', 'larger-than-life persona', 'bohemian sartorial sensibility', 'pure style', 'animal prints', 'Rose Ivory', 'Rose Honey', 'round'], 'briefs': ['brief comebacks', 'brief comebacks'], 'source': 'vogue', 'trousers': ['trousers'], 'necklace': ['favourite statement necklace', 'favourite statement necklace'], 'earrings': ['stud earrings'], 'skirts': ['midi skirts', 'midi skirts', 'midi skirts']}
zara_data = {'coats': ['tribal linen coat', 'openwork coat'], 'sweaters': ['short sleeve sweater'], 'sunglasses': ['aviator sunglasses'], 'shorts': ['paisley print bermuda shorts', 'micro polka dot textured weave bermuda shorts', 'guipure lace bermuda shorts', 'bird print flowing bermuda shorts'], 'sweatshirts': ['sweatshirt', 'raglan sleeve sweatshirt', 'raglan sleeve sweatshirt'], 'tops': ['street top', 'frayed peplum top', 'guipure lace top'], 'dungarees': ['vintage fade denim dungarees', 'white dungarees with rips'], 'misc': ['tribal jacquard scarf', 'culottes', 'leather platform slides', 'blouse with lace trim', 'bandana print silk style scarf', 'blouse with open back', 'tie-dye jacquard culottes', 'tie-dye hand embroidered poncho', 'striped blouse'], 'source': 'zara', 't-shirt': ['striped back and pocket t-shirt', 'striped back and pocket t-shirt', 'striped fabric seamed t-shirt', 't-shirt with zip on sleeves', 'printed t-shirt', 'flower print t-shirt', 'textured t-shirt', 'creased texture t-shirt', 'textured t-shirt', 'short sleeve t-shirt with oversized pocket', 'short sleeve t-shirt with oversized pocket', 't-shirt with zip on sleeves', 'short sleeve t-shirt with oversized pocket', 'short sleeve t-shirt with oversized pocket', 'oversized linen t-shirt'], 'bag': ['studs and chain cross body bag'], 'blazers': ['textured weave suit blazer', 'paisley print blazer', 'micro polka dot textured weave blazer'], 'skirts': ['short tribal skirt', 'wrap skirt', 'tie-dye midi skirt', 'lace tube skirt'], 'shirts': ['plain twill shirt', 'striped indigo shirt', 'bull denim shirt', 'bull denim shirt', 'faded indigo striped shirt', 'poplin shirt', 'stretch shirt with mandarin collar', 'striped shirt', 'horizontal stripe shirt', 'stretch shirt with mandarin collar', 'poplin shirt with contrasting collar', 'short sleeve nautical print polo shirt', 'short sleeve nautical print polo shirt', 'poplin shirt', 'oversized studio shirt', 'denim shirt dress', 'asymmetric hem shirt'], 'jackets': ['bomber style jacket', 'patch bomber jacket', 'contrast blue jacket', 'long embroidered bomber jacket', 'roll-up sleeve jacket', 'bleach wash denim jacket', 'guipure lace bomber jacket', 'sequin patchwork jacket', 'jacket with asymmetric back'], 'trousers': ['textured weave suit trousers', 'bleach effect skinny trousers', 'darted trousers with cord', 'darted trousers with cord', 'darted trousers with cord', 'high waist skinny trousers', 'cropped trousers with front pleat', 'mid-rise biker trousers', 'straight leg flowing trousers', 'mid-rise power stretch trousers'], 'necklace': ['triple choker necklace'], 'sandals': ['crossover metallic sandals', 'leather strap sandals', 'casual roman sandals', 'flat metallic leather sandals', 'leather sandals with buckle'], 'hat': ['straw hat'], 'dresses': ['multicoloured striped dress', 'denim dress', 'lace midi dress', 'lace tube dress', 'guipure lace tube dress'], 'jumpsuit': ['faded denim jumpsuit', 'short jumpsuit', 'short jumpsuit', 'short jumpsuit']}


def count_duplicates_within_source(json):
    unique = set()
    new_map = dict()
    source = json['source']
    json.pop('source')
    for k, v in json.iteritems():
        new_map[k] = dict()
        for string in v:
            new_map[k].update({string:
                              {
                                  'source': source,
                                  'count': 1
                              }
            })
            if string not in unique:
                unique.add(string)
            else:
                new_map[k][string]['count'] += 1
    return new_map


def map_article_types(data, source):
    map = dict()
    map['misc'] = list()
    tag_map = tags.create_set_article_types()
    for k, v in data.iteritems():
        for line in v:
            flag = 0
            inner_flag = 0
            line1 = line.split()
            last_word = line1[-1]
            if last_word in tag_map:
                if last_word not in map:
                    map[last_word] = list()
                    map[last_word] = [line]
                else:
                    map[last_word].append(line)
                continue
            for xyz in tag_map:
                if difflib.SequenceMatcher(None, xyz, last_word).ratio() > 0.85:
                    if xyz in map:
                        map[xyz].append(line)
                    else:
                        map[xyz] = [line]
                    flag = 1
                    break
            if flag == 1:
                continue
            ratio = 0
            savetag = ''
            for string in line1:
                for tag in tag_map:
                    edit_distance = difflib.SequenceMatcher(None, tag, string).ratio()
                    if edit_distance > 0.8 and edit_distance > ratio:
                        savetag = tag
                        ratio = edit_distance
                        inner_flag = 1
            if inner_flag == 1:
                if savetag in map:
                    map[savetag].append(line)
                else:
                    map[savetag] = [line]
                continue
            map['misc'].append(line)
    map["source"] = source
    return map


def merge_dicts(dict1, dict2):
    cleaned_map1 = count_duplicates_within_source(dict1)
    cleaned_map2 = count_duplicates_within_source(dict2)
    merged_map = cleaned_map1.copy()
    for k, v in cleaned_map2.iteritems():
        if k in merged_map:
            merged_map[k].update(v)
        else:
            merged_map[k] = v
    print merged_map
    return merged_map


def match_ratio():
    print difflib.SequenceMatcher(None, 'tent', 'attention').ratio()


print merge_dicts(vogue_data, zara_data)