API_KEY = '4a04781580'
BASE_URL = f'https://{API_KEY}.backend.sernes.cn'
# BASE_URL = "http://10.10.30.158:9000"
# 网络配置
NETWORK_NAME = 'satnet'

from tools import APIClient, WebSocketClient
import asyncio
import time

client = APIClient(BASE_URL)

# 创建网络的请求参数
network_params = {
  "network_name": "satnet",
  "network_description": "Satellite Network with OSPFv3",
  "constellation": {
    "name": "my_constellation",
    "type": "walker_delta",
    "orbit_altitude": 570,
    "orbit_inclination": 70,
    "orbit_num": 18,
    "sat_num_per_orbit": 10,
    "phase_shift": 1,
    "sat_isl_link_num": 4,
    "sat_gsl_link_num": 1,
    "sat_access_link_num": 0
  },
  "gs_set": [
    {
      "name": "gs_0",
      "latitude": 37.77,
      "longitude": -122.42,
      "elevation": 121.1,
      "gs_antenna_num": 1,
      "gs_antenna_angle": 25,
    }
  ],
}
# 发送创建网络的POST请求
print(network_params)
response = client.post('/api/network/create/', json_data=network_params)
if response:
    print("网络创建成功")
    network_id = response['network_id']
else:
    print("网络创建失败")

#client.post(f'/api/network/{network_id}/file/upload', files={'file': ('config.zip', open('/home/cnic/LEO_satellite_network_conf/divide_area_conf/6_area_conf.zip', 'rb'))})