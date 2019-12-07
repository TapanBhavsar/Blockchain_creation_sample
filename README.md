# Blockchain_creation_sample

### Required software
1. Postman

## version 0.1
sample blockchain creation program to understand basics of blockchain piece by piece in python.
*blockchain.py* is single handed script working on blockchain concept such as:
* mine block
* create a chain and add genesis block,  
* proof of work concept
* block hashing

To run the blockchain, the following steps are required:
1. run *blockchain.py* with all required python libraries.
2. install Postman for the system and do the login/signup.
3. do get request as *http://0.0.0.0:5000/get_chain* (which is required at first time to generate genesis block)
4. do another get request as *http://0.0.0.0:5000/mine_block* (which create a block in chain on local node, here block can be mined as many as want)
5. do last get request as *http://0.0.0.0:5000/is_blockchain_valid* (validate blockchain is corrent of corrupt)

## version 0.2
This version requires 5 files (tapcoin.py, tapcoin_5002.py, tapcoin_5003.py, nodes.json, transaction.json)
Both json files are the format to post requests for create local nodes of blockchain and transaction data into the recent local block.

To run the cryptocurrency, the following steps are required:
1. run 3 scripts on different terminals/command lines/console.
2. create 3 tabs on Postman
3. do get request as *http://127.0.0.1:PORT/get_chain* in all 3 tabs. (change PORT with it's port value (e.g 5001))
4. To add peer node into chain: change all status from get to post, go to body> raw > json , paste nodes.json except current node address
5. do get request as *http://127.0.0.1:PORT/mine_block* to mine a block on any node.
6. do get request for *http://127.0.0.1:PORT/replace_chain* on all nodes
7. do post request to *http://127.0.0.1:PORT/add_transactions* as transaction.json format
8. do get request *http://127.0.0.1:PORT/mine_block*
9. get request *http://127.0.0.1:PORT/replace_chain* on all nodes
