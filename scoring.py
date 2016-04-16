import find_overlap

scores = {
    'zara': 0.5,
    'vogue': 0.5,
    'google': 0.5
}


def find_keyword_occurences_in_source(map, source):
    freq = 0
    for key, value in map.iteritems():
        for k, v in value.iteritems():
            if v['source'] == source:
                freq += 1
    # print freq
    return freq
    # return update_internal_score(map, freq, source)


def count_matching_score_items(map, source):
    score_map = dict()
    for key, values in map.iteritems():
        for k, v in values.iteritems():
            if v['source'] == source:
                if v['count'] in score_map:
                    score_map[v['count']] += 1
                else:
                    score_map[v['count']] = 1
    return score_map


def calculate_rank(map, freq):
    keylist = map.values()
    new_list = list()
    for i in range(len(keylist)):
        new_list.append(sum(keylist[:i]))
    for k, v in map.iteritems():
        map[k] = float((new_list[k-1] + (0.5 * map[k]))/freq)
        # print float(new_list[k - 1] + (0.5 * map[k]) / freq)
    return map


def calculate_percentiles(map):
    vogue_freq = find_keyword_occurences_in_source(map, 'vogue')
    zara_freq = find_keyword_occurences_in_source(map, 'zara')
    zara_score_map = count_matching_score_items(map, 'zara')
    vogue_score_map = count_matching_score_items(map, 'vogue')
    zara_new_score_map = calculate_rank(zara_score_map, zara_freq)
    vogue_new_score_map = calculate_rank(vogue_score_map, vogue_freq)
    total_freq = zara_freq + vogue_freq
    print total_freq
    itf_vogue = float(zara_freq)/float(total_freq)
    itf_zara = float(vogue_freq)/float(total_freq)
    print itf_vogue, itf_zara
    # print zara_new_score_map, vogue_new_score_map
    for key, values in map.iteritems():
        for k, v in values.iteritems():
            if v['source'] == 'zara':
                v['percentile'] = zara_new_score_map[v['count']]
                v['itf_score'] = float(itf_zara * v['count'])
            if v['source'] == 'vogue':
                v['percentile'] = vogue_new_score_map[v['count']]
                v['itf_score'] = float(itf_vogue * v['count'])
    # print map
    return map


def update_internal_score(map, freq, source):
    for key, value in map.iteritems():
        for k, v in value.iteritems():
            if v['source'] == source:
                v['internal_ratio'] = float(v['count']/freq)
    return map

# data1 = find_overlap.vogue_data
# data2 = find_overlap.zara_data
# print

# print find_keyword_occurences_in_source(find_overlap.merge_dicts(data1, data2), 'vogue')
# merged_map = find_overlap.merge_dicts(data1, data2)
# calculate_percentiles(merged_map)
# count_matching_score_items(merged_map, 'zara')