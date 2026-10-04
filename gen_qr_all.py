# -*- coding: utf-8 -*-
"""
重新生成全部溯源二维码：内容改为公网URL（微信扫码可直接打开溯源页）
用法：python gen_qr_all.py [公网地址]
默认地址：https://466e522f.r1.cpolar.top
"""
import os
import sqlite3
import sys

# 公网地址（cpolar 免费版随机域名，地址变更后重新运行本脚本即可）
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else 'https://466e522f.r1.cpolar.top'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, 'data.db')
QR_DIR = os.path.join(BASE_DIR, 'static', 'qr')
os.makedirs(QR_DIR, exist_ok=True)

import qrcode

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
rows = conn.execute(
    "SELECT id, trace_code FROM products WHERE trace_code != '' ORDER BY id"
).fetchall()
conn.close()

print(f'公网地址: {BASE_URL}')
print(f'待生成二维码产品数: {len(rows)}')
for r in rows:
    pid = r['id']
    code = r['trace_code']
    url = f'{BASE_URL}/trace?code={code}'
    path = os.path.join(QR_DIR, f'qr_{pid}.png')
    img = qrcode.make(url)
    img.save(path)
    print(f'  qr_{pid}.png <- {url}')
print('全部生成完成')
