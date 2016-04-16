import csv
import find_overlap
import scoring
import collections


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
    for key, values in map.iteritems():
        for k, v in values.iteritems():


total, google_score_map = calculate_sum_searches('mynew.csv')
with open('mynew.csv', 'rb') as f, open('new.csv', 'w') as g:
    output = csv.reader(f)
    headers = next(output)
    data1 = find_overlap.vogue_data
    data2 = find_overlap.zara_data
    merged_map = find_overlap.merge_dicts(data1, data2)
    mapping = scoring.calculate_percentiles(merged_map)
    for row in output:
        article_type = find_overlap.get_article_type(row[1].replace('\'', ''))
        if row[1].replace('\'', '') in mapping[article_type]:
            if row[3] == '':
                row[3] = '1'
            mapping[article_type][row[1].replace('\'', '')]['googlescore'] = google_score_map[int(row[3])]
            row[-1] += '\n'
            g.write(','.join(row))
    print mapping
