from flask import Flask
import scrape
import json
import myntra_selection_gap
app = Flask(__name__)


@app.route('/tags/all')
def get_tags_all():
    demo = True
    if demo:
        with open("FinalResponse.txt", 'r') as f:
            response = f.readline()
        print response
        return response
    demo = True
    response = [scrape.create_vogue_response(demo), scrape.create_zara_response(demo), scrape.create_elle_response(demo)]
    response = myntra_selection_gap.get_selection_gap(response)
    print response
    if response:
        with open("FinalResponse.txt", 'w') as f:
            f.write(json.dumps(response))
    return json.dumps(response)


@app.route('/brands/all')
def get_brands_all():
    response = [scrape.create_elle_response()]
    response = myntra_selection_gap.get_selection_gap(response)
    return json.dumps(response)


@app.route('/tags/vogue')
def get_tags_vogue():
    response = [scrape.start_with_file_vogue()]
    response = myntra_selection_gap.get_selection_gap(response)
    return json.dumps(response)


@app.route('/tags/zara')
def get_tags_zara():
    response = [scrape.create_zara_response()]
    response = myntra_selection_gap.get_selection_gap(response)
    return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12313, threaded=True, debug=True )