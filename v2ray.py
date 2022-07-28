import base64
import re
import urllib.request
import json


def decode_file():
    raw = urllib.request.urlopen(
        url='https://raw.githubusercontent.com/freefq/free/master/v2').read().decode('utf-8')
    v2ray_raw = base64.b64decode(raw)
    v2ray_list = v2ray_raw.splitlines()

    file = open("freefq.yaml", "w", encoding="utf-8")
    file.writelines("proxies:\n")
    for item in v2ray_list:
        v2ray = item.decode('utf-8').split('://')
        if "vmess" == v2ray[0]:
            v2ray_data = base64.b64decode(v2ray[1])
            jsonData = json.loads(v2ray_data)
            obj = {
                'type': v2ray[0],
                'name': jsonData.get('ps'),
                'server': jsonData.get('add'),
                'port': jsonData.get('port'),
                'uuid': jsonData.get('id'),
                'alterId': jsonData.get('aid'),
                'cipher': 'auto',
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
            v2ray_data = re.split('@|:|#', v2ray[1])
            obj = {
                "type": v2ray[0],
                "name": urllib.parse.unquote(v2ray_data[3]),
                "server": v2ray_data[1],
                "port": v2ray_data[2],
                "password": v2ray_data[0],
                "udp": True,
                "skip-cert-verify": True
            }
            if("ss" == v2ray[0]):
                obj.update({"cipher": "aes-128-cfb"})
            json_str = json.dumps(obj, ensure_ascii=False)
            file.writelines("  - " + json_str + "\n")
    file.close()


decode_file()
