# Python program to create Blockchain
 
# For timestamp
from asyncio.windows_events import NULL
import datetime
 
# Calculating the hash
# in order to add digital
# fingerprints to the blocks
import hashlib
 

 
# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, jsonify, request

# To store data
# in our blockchain
import json

from Encryption import Encryption

# from requests import request
 
 
class Blockchain:
   
    # This function is created
    # to create the very first
    # block and set its hash to "0"
    def __init__(self):
        self.encryptor = NULL
        self.chain = []
        self.create_block(proof=1, previous_hash='0')
        self.encryptor = self.create_encryptor()
 
    def create_encryptor(self):
        if(self.encryptor == NULL):
            self.encryptor = Encryption()
        return self.encryptor
    # This function is created
    # to add further blocks
    # into the chain
    def create_block(self, proof, previous_hash):
        self.encryptor = self.create_encryptor()
        first_name = self.encryptor.encrypt_message(b"Tilanie")
        last_name = self.encryptor.encrypt_message(b"Bresler")
        email = self.encryptor.encrypt_message(b"tilanietest@gmail.com")
        address = self.encryptor.encrypt_message(b"Street, Country, Zip")
        age = self.encryptor.encrypt_message(b"22")
        gender = self.encryptor.encrypt_message(b"F")
        phone_number = self.encryptor.encrypt_message(b"0122223344")
        dob = self.encryptor.encrypt_message(b"01/01/2000")
        games_owned_asset = self.encryptor.encrypt_message(b"my cool gun")


        block = {'index': len(self.chain) + 1,
                 'first_name': first_name,
                 'last_name': last_name,
                 'email': email,
                 'address': address,
                 'age': age,
                 'gender': gender,
                 'phone_number': phone_number,
                 'dob': dob,
                 'games_owned': {
                     "Counter Strike": [
                        {
                            "id": 1,
                            "description": games_owned_asset
                        }
                    ]
                 },
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
       
    # This function is created
    # to display the previous block
    def print_previous_block(self):
        return self.chain[-1]
       
    # This is the function for proof of work
    # and used to successfully mine the block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
         
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
                 
        return new_proof
 
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
 
    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
         
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
               
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
             
            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1
         
        return True

    def decrypt_information(self, incoming_message_object):
        message_object = incoming_message_object['chain'][0]

        new_message = {'index': len(self.chain) + 1,
                 "first_name": self.encryptor.decrypt_message(message_object['first_name']),
                 "last_name": self.encryptor.decrypt_message(message_object['last_name']),
                 "email": self.encryptor.decrypt_message(message_object['email']),
                 "address": self.encryptor.decrypt_message(message_object['address']),
                 "age": self.encryptor.decrypt_message(message_object['age']),
                 "gender": self.encryptor.decrypt_message(message_object['gender']),
                 "phone_number": self.encryptor.decrypt_message(message_object['phone_number']),
                 "dob": self.encryptor.decrypt_message(message_object['dob']),
                 "games_owned": {
                     "Counter Strike": [
                        {
                            "id": 1,
                            "description": self.encryptor.decrypt_message(message_object['games_owned']['Counter Strike'][0]['description']),
                        }
                    ]
                 },
                 "timestamp": str(datetime.datetime.now()),
                 "proof": message_object['proof'],
                 "previous_hash": message_object['previous_hash']}
        return new_message
    
    def format_chain(self):
        message_object = blockchain.chain[0]
      
        new_message = {'index': len(self.chain) + 1,
                 "first_name": str(message_object['first_name']),
                 "last_name": str(message_object['last_name']),
                 "email": str(message_object['email']),
                 "address": str(message_object['address']),
                 "age": str(message_object['age']),
                 "gender": str(message_object['gender']),
                 "phone_number": str(message_object['phone_number']),
                 "dob": str(message_object['dob']),
                 "games_owned": {
                     "Counter Strike": [
                        {
                            "id": 1,
                            "description": str(message_object['games_owned']['Counter Strike'][0]['description']),
                        }
                    ]
                 },
                 "timestamp": str(datetime.datetime.now()),
                 "proof": str(message_object['proof']),
                 "previous_hash": str(message_object['previous_hash'])}
        return new_message
# Creating the Web
# App using flask
app = Flask(__name__)
 
# Create the object
# of the class blockchain
blockchain = Blockchain()
 
# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
 
    previous_proof = previous_block['proof']

    proof = blockchain.proof_of_work(previous_proof)

    previous_hash = blockchain.hash(previous_block)

    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'A block is MINED',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}

    return jsonify(response), 200
 
# Display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
    blockchain.chain[0] = blockchain.format_chain()
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200
 
 # Request user credentials
@app.route('/get_credentials', methods=['POST'])
def get_credentials():
   
    print("The application " + request.json['application_name'] + " is requesting your information. Do you want to grant access?" )
    print("Enter 'yes' to approve or 'no' to reject: ")
    c = input()
   
    if(c == 'yes'):
        response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
        return jsonify(blockchain.decrypt_information(response)), 200
    else:
        return "Request not authorized", 401

# Check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)
     
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200
 
 
# Run the flask server locally
app.run(host='127.0.0.1', port=5000)