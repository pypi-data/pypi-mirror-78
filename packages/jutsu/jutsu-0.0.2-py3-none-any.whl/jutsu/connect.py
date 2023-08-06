from PyInquirer import prompt
from oogway import Node

node_rpc = [
    {
        'type': 'input',
        'name': 'host',
        'message': 'Enter your node host'
    },
    {
        'type': 'input',
        'name': 'port',
        'default': '8332',
        'message': 'Enter your node port'
    },
    {
        'type': 'input',
        'name': 'username',
        'message': 'Enter your bitcoind RPC username'
    },
    {
        'type': 'password',
        'name': 'password',
        'message': 'Enter your bitcoind RPC password'
    },
]

def connect_node():
    answers = prompt(node_rpc)
    url = "http://%s:%s@%s:%s" % (answers['username'], answers['password'], answers['host'], answers['port'])
    n = Node(url, timeout=2000)
    return n