import sys
from flask import Flask, jsonify
import flask_cors
from scrapper import scrap_size_official
from buyer import buy_shoe

infos = {
    'product_name':'size?',
    'size' : '2.5-5',
    'mail' : 'chaoulammar1@gmail.com',
    'mdp' : 'Sneakersbot2019',
    'paypal_email' : 'avnerammar1@gmail.com',
    'paypal_mdp': 'lalala'
    #'paypal_mdp' : 'Avammar28!'
}
driver_path = './chromedriver'
scrap_url = 'https://www.sizeofficial.fr/femme/accessoires/'

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success'
    })

@app.route('/', methods=['GET'])
def api_root():
    launch_bot(driver_path, scrap_url, infos)
    return jsonify({
        'status': 'success'
    })

def launch_bot(driver_path, scrap_url, infos):
    scrap_size_official(driver_path, scrap_url, infos)
    buy_shoe(driver_path, infos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

flask_cors.CORS(app, expose_headers='Authorization')