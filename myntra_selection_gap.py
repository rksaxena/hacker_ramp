import requests
import json

MYNTRA_DEV = 'http://developer.myntra.com/search/data'

def get_selection_gap(trends):

    '''

    :param {
                data :[{
                        'source': 'Zara',
                        'article_type1': ['trend1', 'trend2', ... ],
                         'article_type2': ..
                    ]]
            }
    :return: {
                data:[ {
                        'source' : 'Zara',
                        'article_type1' :{
                                        'total_count' :100,
                                        'gap_count' :20,
                                        absent_trends:['trend1', 'trend2', ....]
                                        },
                        'article_type2':{
                                            ...
                                        }
                        }]
            }
    '''
    gap ={
        'data':[]
    }
    sources = trends
    for source in sources:
        gap_obj ={}
        gap_obj['source'] = source['source']
        # for each article type
        print 'Doing ', gap_obj['source']
        print "Input "
        print source['source']
        for article_type in source :
            if article_type == 'source':
                continue
            gap_obj[article_type] = {
                'total_count': 0,
                'gap_count': 0,
                'absent_trends': []
            }
            #for each trend in this article type
            for trend in source[article_type] :
                if trend in gap_obj[article_type]['absent_trends']:
                    continue
                r = requests.get(MYNTRA_DEV + '/' + trend)
                if r.status_code != 200:
                    r = requests.get(MYNTRA_DEV + '/' + trend)
                    if r.status_code !=200:
                        print 'Problem connecting for ', gap_obj['source'], 'for trend', trend
                        continue
                response = json.loads(r.text)
                if response['data']['totalProductsCount'] == 0:
                    gap_obj[article_type]['absent_trends'].append(trend)
                    gap_obj[article_type]['total_count'] += 1
                    gap_obj[article_type]['gap_count'] += 1
                else:
                    gap_obj[article_type]['total_count'] += 1

        print gap_obj['source'] + ' Done'
        print gap_obj
        gap['data'].append(gap_obj)

    return gap
if __name__ == '__main__':
    print get_selection_gap(
        [{

                        'source': 'Zara',
                        'skirts': ['midi skirts', 'short skirts' ],
                        'jackets': ['biker jackets', 'leather jackets'],
                        'jeans' :['bell bottoms']

        }]
    )