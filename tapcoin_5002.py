# module 1: create a blockchain

import json
import datetime
import hashlib
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Create blockchain
class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash="0")
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
            "transactions": self.transactions,
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                proof += 1
        return proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self):
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False

            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False

            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({"sender": sender, "receiver": receiver, "amount": amount})
        previous_block = self.get_previous_block()
        return previous_block["index"] + 1

    def add_node(self, address):  # address = 'http://127.0.0.1:5000'
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f"http://{node}/get_chain")
            if response.status_code is 200:
                length = response.json()["length"]
                chain = response.json()["chain"]
                if length > max_length and self.is_chain_valid():
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


# Mining blockchain
app = Flask(__name__)

node_address = str(uuid4()).replace("_", "")

blockchain = BlockChain()


@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver="tapan1", amount=1)
    block = blockchain.create_block(proof=proof, previous_hash=previous_hash)
    response = {
        "message": "Block is mined",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
        "transactions": block["transactions"],
    }
    return jsonify(response), 200


@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    return jsonify(response), 200


@app.route("/is_blockchain_valid", methods=["GET"])
def is_blockchain_valid():
    validation_status = blockchain.is_chain_valid()
    response = {
        "message": "Blockchain validation status",
        "status": validation_status,
    }
    return jsonify(response), 200


@app.route("/add_transactions", methods=["POST"])
def add_transaction():
    json_data = request.get_json()
    transaction_keys = ["sender", "receiver", "amount"]
    if not all(key in json_data for key in transaction_keys):
        return "some elements of the transaction are missing", 400
    index = blockchain.add_transaction(
        sender=json_data["sender"], receiver=json_data["receiver"], amount=json_data["amount"]
    )
    response = {"message": f"This transaction will be addded to block {index}"}
    return jsonify(response), 201


@app.route("/connect_node", methods=["POST"])
def connect_node():
    json_data = request.get_json()
    nodes = json_data.get("nodes")
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        "message": "All the nodes are connected. The tapcoin blockchain now contains the following total nodes",
        "total_nodes": list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route("/replace_chain", methods=["GET"])
def replace_chain():
    chain_replace_status = blockchain.replace_chain()
    if chain_replace_status:
        response = {
            "message": "The nodes had different chains so the chain was replaced by the longest one",
            "new_chain": blockchain.chain,
        }
    else:
        response = {"message": "All good. The chain is the largest one"}
    return jsonify(response), 200


# decentralize our blockchain
app.run(host="127.0.0.1", port=5002)
