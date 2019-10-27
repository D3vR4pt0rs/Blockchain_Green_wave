from web3 import Web3,HTTPProvider
from src import service_function
import json
import random
import uuid

network_config=open('network.json', 'r')
rpcUrl=str(json.load(network_config)['rpcUrl'])
web3 = Web3(HTTPProvider(rpcUrl))

f = open('network.json', 'r')
private_key = str(json.load(f)['privKey'])
private_key_for_senders_account = private_key
addressUser = Web3.toChecksumAddress(web3.eth.account.privateKeyToAccount('0x' + str(private_key_for_senders_account)).address)

def register_traffic_light(count_of_traffic_lights):
    uuids_of_traffic_lights=[]
    for i in range(count_of_traffic_lights):
        uuids_of_traffic_lights.append(str(uuid.uuid4()))
    traffic_lights_private_keys={}
    for i in range(len(uuids_of_traffic_lights)):

        uuid_of_tl=uuids_of_traffic_lights[i]
        uuid_of_tl=uuid_of_tl.replace('-','')
        code=random.randint(1000,9999)

        #Id светофора
        tl_id="tl"+str(i)

        #Генерация приватного ключа светофора
        private_key= service_function.generate_private_key(uuid=uuid_of_tl, pin_code=str(code))
        address= service_function.generate_address(private_key)

        traffic_lights_private_keys[tl_id]=private_key

    with open("private_keys.json", "w") as write_file:
        json.dump(traffic_lights_private_keys, write_file)

def give_award_for_good_driver(number_of_car):

    d = open('registrar.json', 'r')
    account_config = json.load(d)
    contract_address = str(account_config['carcoins']['address'])

    with open("carcoins.bin") as bin_file:
        content = json.loads(bin_file.read())
        bytecode = content['object']

    with open("carcoins.abi") as abi_file:
        abi = json.loads(abi_file.read())
    contract_reg = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi,
                                     bytecode=bytecode)

    f = open('network.json', 'r')

    tx=contract_reg.functions.GetUIFromNumber(number_of_car).buildTransaction({'gas': 3000000 ,'nonce': web3.eth.getTransactionCount(
                                                                                                        web3.eth.account.privateKeyToAccount(
                                                                                                            str(private_key_for_senders_account)).address)})

    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)


def give_award_for_good_team_of_traffic_lights(id1,id2):
    d = open('registrar.json', 'r')
    account_config = json.load(d)
    contract_address = str(account_config['trafficlights']['address'])

    with open("registrar.bin") as bin_file:
        content = json.loads(bin_file.read())
        bytecode = content['object']

    with open("registrar.abi") as abi_file:
        abi = json.loads(abi_file.read())

    contract_reg = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi,
                                     bytecode=bytecode)
    f = open('network.json', 'r')





register_traffic_light(10)