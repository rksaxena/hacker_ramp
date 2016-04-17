import csv
import find_overlap
import scoring
import collections
import scrape
import json

mapping = dict()

def calculate_sum_searches(file):
    score_map = collections.OrderedDict()
    count = 0
    with open(file, 'rb') as f:
        output = csv.reader(f)
        headers1 = next(output)
        for row in output:
            if row[3] == '':
                row[3] = '1'
            count += int(row[3].replace('\'', ''))
            if int(row[3]) in score_map:
                score_map[int(row[3])] += 1
            else:
                score_map[int(row[3])] = 1
    print score_map
    newlist = list()
    vallist = score_map.values()
    for i in range(len(vallist)):
        newlist.append(sum(vallist[i+1:len(vallist)]))
    print newlist
    new_score_map = {}
    j = 0
    for k, v in score_map.iteritems():
        new_score_map[k] = float(((newlist[j] + (0.5 * v))/sum(newlist)))
        j += 1
    return count, new_score_map

# mapp = find_overlap.get_article_type("'denim dress'")
# print mapp


def calculate_final_score(map):
    print "article,finalscore,percentile,googlescore,itfscore,count"
    for key, values in map.iteritems():
        for k, v in values.iteritems():
            v['final_score'] = (0.5 * v['percentile'] * v['itf_score']) + (0.5 * (v['googlescore'] if 'googlescore' in v else 0))
            print k + "," + str(v['final_score']) + "," + str(v['percentile']) + "," + str(v['googlescore'] if 'googlescore' in v else 0) + "," + str(v['itf_score']) + "," + str(v['count'])
    return map

def final():
    total, google_score_map = calculate_sum_searches('mynew.csv')
    with open('mynew.csv', 'rb') as f, open('new.csv', 'w') as g:
        output = csv.reader(f)
        headers = next(output)
        data1 = scrape.create_vogue_response(True)
        data2 = scrape.create_zara_response(True)
        print json.dumps(data1)
        print json.dumps(data2)
        merged_map = find_overlap.merge_dicts(data1, data2)
        print merged_map
        mapping = scoring.calculate_percentiles(merged_map)
        for row in output:
            article_type = find_overlap.get_article_type(row[1].replace('\'', ''))
            print article_type
            if article_type in mapping:
                if row[3] == '':
                    row[3] = '1'
                if row[1].replace('\'', '') in mapping[article_type]:
                    mapping[article_type][row[1].replace('\'', '')]['googlescore'] = google_score_map[int(row[3])]
                row[-1] += '\n'
                g.write(','.join(row))
        # print mapping
    mapping = calculate_final_score(mapping)
    for key, value in mapping.iteritems():
        for k,v in value.iteritems():
            v['final_score'] *= 100
            v['itf_score'] *= 100
            v['percentile'] *= 100
            if "googlescore" not in v:
                v['googlescore'] = 0
            else:
                v['googlescore'] *= 100

    return mapping

