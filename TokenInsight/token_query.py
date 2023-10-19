import json
import requests

from django.conf import settings

class TokenQuery(object):
    def __init__(self):
        import configparser
        import os

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config = configparser.ConfigParser()
        config.read(os.path.join(BASE_DIR, 'config.ini'))

        self.rpc_bsc_https = f'https://{settings.RPC_URLS.get("RPC_BSC")}'
        self.rpc_bsc_wss = f'wss://{settings.RPC_URLS.get("RPC_BSC")}'

        self.headers = {
            'Content-Type': 'application/json',
        }

    # 获取最新区块号
    def getBlockNumber(self):
        payload = json.dumps({
            "method": "eth_blockNumber",
            "params": [],
            "id": 1,
            "jsonrpc": "2.0"
        })
        response = requests.post(self.rpc_bsc_https, headers=self.headers, data=payload)
        if response.status_code == 200:
            return response.json().get('result')
        else:
            raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
        
    # 获取指定钱包的指定代币余额
    def getTokenBalance(self, token_address, address):
        payload = json.dumps({
            "method": "eth_call",
            "params": [{
                "to": token_address,
                "data": "0x70a08231000000000000000000000000" + address[2:]
            }, "latest"],
            "id": 1,
            "jsonrpc": "2.0"
        })
        response = requests.post(self.rpc_bsc_https, headers=self.headers, data=payload)
        if response.status_code == 200:
            return response.json().get('result')
        else:
            raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
        
    def getLogs(self, token_address, event_signature, start_block, end_block):
        payload = json.dumps({
            "method": "eth_getLogs",
            "params": [{
                "fromBlock": start_block,
                "toBlock": end_block,
                "address": token_address,
                "topics": [event_signature]
            }],
            "id": 1,
            "jsonrpc": "2.0"
        })
        response = requests.post(self.rpc_bsc_https, headers=self.headers, data=payload)
        if response.status_code == 200:
            return response.json().get('result')
        else:
            raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
        
if __name__=='__main__':
    import channels
    token_address = '0xec1f55b5be7ee8c24ee26b6cc931ce4d7fd5955c'
    address = '0xc71F66aC702172203E2e07c7e202506CEBCddAE1'
    TQ = TokenQuery()
    TQ.getTokenBalance(token_address, address)