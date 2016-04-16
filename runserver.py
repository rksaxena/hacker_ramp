from flask import Flask
import scrape
import json
import myntra_selection_gap
app = Flask(__name__)


@app.route('/tags/all')
def get_tags_all():
    response = [scrape.start_with_file_vogue(), scrape.create_zara_response()]
    response = myntra_selection_gap.get_selection_gap(response)
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12313, threaded=True, debug=True )