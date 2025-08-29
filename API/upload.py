API_KEY = '4a04781580'
BASE_URL = f'https://{API_KEY}.backend.sernes.cn'
# BASE_URL = "http://10.10.30.158:9000"
# 网络配置
NETWORK_NAME = 'satnet'

from tools import APIClient, WebSocketClient
import asyncio
import time

client = APIClient(BASE_URL)

#network_id
client.post(f'/api/network/7/file/upload', files={'file': ('config.zip', open('/home/cnic/LEO_satellite_network_conf/divide_area_conf/3_prefix_conf.zip', 'rb'))})