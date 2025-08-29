import argparse
import requests
import random
base_url = "backend.sernes.cn"
use_https = True

parser = argparse.ArgumentParser(description='A script set a batch of ISL links up or down')
parser.add_argument('operation', type=str,
                    help='Operation to be executed on links [up|down]')
parser.add_argument('-r', '--ratio', type=float, required=False,
                    help='Proportion of randomly down\'ed links [up|down]')
parser.add_argument('--api-key', type=str, required=True, help='API密钥')
args = parser.parse_args()


def validate_args():
    if args.api_key is None:
        print(f"Please assign the API key! (e.g.: --api-key <api_key>)")
        exit(1)
    if args.operation not in ["up", "down"]:
        print(f"Invalid operation \"{args.operation}\"! (Supposed to be \"up\" or \"down\")")
        exit(1)
    if args.operation == "down":
        if args.ratio is None:
            print(f"Please assign the ratio of links to be set down! (e.g.: -r 0.1)")
            exit(1)
        if args.ratio <= 0 or args.ratio >= 1:
            print(f"Invalid link-down ratio: {args.ratio}! (Supposed to be among (0, 1))")
            exit(1)


def send_get_request(url, params=None, headers=None, use_https=True):
    scheme = "https" if use_https else "http"
    full_url = f"{scheme}://{url}"
    try:
        response = requests.get(full_url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def send_json_request(url, request_data, headers=None, use_https=True):
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    scheme = "https" if use_https else "http"
    full_url = f"{scheme}://{url}"
    try:
        response = requests.post(full_url, json=request_data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    validate_args()
    base_url = f"{args.api_key}.{base_url}"
    # 请求/api/satvis/scenario/status接口，获取当前运行中的网络ID和卫星仿真场景ID
    url = f"{base_url}/api/satvis/scenario/status"
    response_data = send_get_request(url, use_https=use_https)
    if response_data is None:
        print(f"No network is running!")
        exit(1)
    elif response_data["emulation_status"] != 1 or "scenario_id" not in response_data:
        print(f"No scenario is running!")
        exit(1)
    scenario_id = response_data["scenario_id"]

    # 请求/api/satvis/{scenario_id}/init_edge_list接口，获取当前运行网络中的所有链路ID
    url = f"{base_url}/api/satvis/{scenario_id}/init_edge_list"
    response_data = send_get_request(url, use_https=use_https)
    link_ids = [link["link_id"] for link in response_data["links"]]

    # 请求/api/vlink/update/batch/接口，对链路进行批量操作
    url = f"{base_url}/api/vlink/update/batch/"
    if args.operation == "up":
        # 若操作为up，将所有链路设置为up
        request_data = {
            "op": "up",
            "link_ids": link_ids
        }
    if args.operation == "down":
        # 若操作为down，将一定比例（args.ratio）的链路设置为down
        sample_size = max(1, int(len(link_ids) * args.ratio))
        selected_link_ids = random.sample(link_ids, sample_size)
        request_data = {
            "op": "down",
            "link_ids": selected_link_ids
        }
    response_data = send_json_request(url, request_data, use_https=use_https)
    if response_data is None:
        print("Link set operation failed.")
    else:
        print("Link set operation succeeded.")