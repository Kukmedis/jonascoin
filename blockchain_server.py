from flask import Flask, jsonify, request
from json import JSONEncoder
from blockchain import Blockchain


class BlockEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__


app = Flask(__name__)
app.json_encoder = BlockEncoder
blockchain = Blockchain()


@app.route('/blocks', methods=['GET', 'POST'])
def work_with_blockchain():
    if request.method == 'GET':
        return jsonify(blockchain.blockchain)
    elif request.method == 'POST':
        blockchain.add_block(request.get_json()['data'], 0, 0)
        return jsonify(blockchain.blockchain[-1])
