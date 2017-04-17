import json, requests, io, shutil
from pyquery import PyQuery as pq

import argparse

parser = argparse.ArgumentParser(description='Fetches crt/key-Pair from OPNsense web interface.')

parser.add_argument('--keyfile', help='export .key to', required=True)
parser.add_argument('--certfile', help='export .crt to', required=True)
parser.add_argument('--keyid',
                    help='which key number to export (get this from OPNsense web interface)',
                    required=True)
parser.add_argument('--url', help='url of OPNsense web interface', required=True)
parser.add_argument('--username', help='username for OPNsense web interface', required=True)
parser.add_argument('--password', help='password for OPNsense web interface', required=True)

args = parser.parse_args()

client = requests.session()
csrf_token = pq(client.get(args.url + '/index.php').text)('#__opnsense_csrf')[0].value

client.post(args.url + '/index.php', headers={'X-CSRFToken': csrf_token}, data={
    'usernamefld': args.username,
    'passwordfld': args.password,
    'login': 1,
})

def dl(url, destination):
    req = client.get(url, stream=True)
    if req.status_code == 200:
        with open(destination, 'wb') as output_file:
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, output_file)

dl(args.url + '/system_certmanager.php?act=exp&id=' + args.keyid, args.certfile)
dl(args.url + '/system_certmanager.php?act=key&id=' + args.keyid, args.keyfile)

