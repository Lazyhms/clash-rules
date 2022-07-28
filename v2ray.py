import base64
import re
import urllib.request
import json


def verfity_base64(str):
    base64Pattern = "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$"

    match = re.match(base64Pattern, str)
    missing_padding = len(str) % 4

    if None != match and 0 == missing_padding:
        return True
    else:
        return False


def decode_file():
    raw = urllib.request.urlopen(
        url='https://raw.githubusercontent.com/freefq/free/master/v2').read().decode('utf-8')
    v2ray_raw = base64.b64decode(raw)
    v2ray_list = v2ray_raw.splitlines()

    file = open("freefq.yaml", "w", encoding="utf-8")
    file.writelines("proxies:\n")
    for item in v2ray_list:
        v2ray = item.decode('utf-8').split('://')
        if "vmess" == v2ray[0] or verfity_base64(v2ray[1]):
            v2ray_data = base64.b64decode(v2ray[1])
            jsonData = json.loads(v2ray_data)
            obj = {
                'type': v2ray[0],
                'name': jsonData.get('ps'),
                'server': jsonData.get('add'),
                'port': jsonData.get('port'),
                'uuid': jsonData.get('id'),
                'alterId': jsonData.get('aid'),
                'cipher': 'auto' if jsonData.get('type') == 'none' else False,
                'udp': True,
                'network': jsonData.get('net'),
                'ws-path': jsonData.get('path'),
                'ws-headers': {
                    'Host': jsonData.get('host')
                },
                'tls': True if jsonData.get('tls') == 'tls' else False,
            }
            json_str = json.dumps(obj, ensure_ascii=False)
            file.writelines("  - " + json_str + "\n")
        else:
            v2ray_data1 = re.split('@|:|#', v2ray[1])
            obj1 = {
                "type": v2ray[0],
                "name": urllib.parse.unquote(v2ray_data1[3]),
                "server": v2ray_data1[1],
                "port": v2ray_data1[2],
                "password": v2ray_data1[0],
                'cipher': 'auto',
                "udp": True,
                "skip-cert-verify": true
            }
            json_str1 = json.dumps(obj1, ensure_ascii=False)
            file.writelines("  - " + json_str1 + "\n")
    file.close()


decode_file()
