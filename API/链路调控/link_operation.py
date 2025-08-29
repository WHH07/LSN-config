API_KEY = '4a04781580'
BASE_URL = f'https://{API_KEY}.backend.sernes.cn'
# BASE_URL = "http://10.10.30.158:9000"
# 网络配置
NETWORK_NAME = 'satnet'
use_https = True

import os
import sys
import requests
import asyncio
import time

# 确保可以从上级 API 目录导入 tools.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
API_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if API_DIR not in sys.path:
    sys.path.insert(0, API_DIR)

from tools import APIClient, WebSocketClient

def send_get_request(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def send_json_request(url, request_data, headers=None, use_https=True):
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=request_data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # 请求/api/satvis/scenario/status接口，获取当前运行中的网络ID和卫星仿真场景ID
    url = f"{BASE_URL}/api/satvis/scenario/status"
    response_data = send_get_request(url)
    if response_data is None:
        print(f"No network is running!")
        exit(1)
    elif response_data["emulation_status"] != 1 or "scenario_id" not in response_data:
        print(f"No scenario is running!")
        exit(1)
    scenario_id = response_data["scenario_id"]

    # 请求/api/satvis/{scenario_id}/init_edge_list接口，获取当前运行网络中的所有链路ID
    url = f"{BASE_URL}/api/satvis/{scenario_id}/init_edge_list"
    response_data = send_get_request(url)
    link_ids = [link["link_id"] for link in response_data["links"]]
    print(link_ids)

    # 请求/api/vlink/update/batch/接口，对链路进行批量操作
    url = f"{BASE_URL}/api/vlink/update/batch/"
    link=['24-121-25-125', '25-126-26-130', '15-78-25-127']
    request_data = {
        "op": "down",
        "link_ids": link
    }

    response_data = send_json_request(url, request_data, use_https=use_https)
    if response_data is None:
        print("Link set operation failed.")
    else:
        print("Link set operation succeeded.")

