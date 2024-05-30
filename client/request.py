import requests
import json

# 全局变量队列
failed_requests = []


# 从配置文件读取URL
def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config['url']


def send_post_request(time, device, content):
    global failed_requests

    url = load_config()
    data = {
        "time": time,
        "device": device,
        "content": content
    }
    headers = {
        "Content-Type": "application/json"
    }

    # 尝试发送当前请求
    try:
        response = requests.post(url, json=data, headers=headers)

        # 检查响应内容类型是否为JSON
        if response.headers.get('Content-Type') == 'application/json':
            try:
                response_data = response.json()
            except json.JSONDecodeError as json_err:
                print(f"JSON decode error: {json_err}")
                failed_requests.append(data)
                return False
        else:
            print(f"Unexpected content type: {response.headers.get('Content-Type')}")
            failed_requests.append(data)
            return False

        if 'status' in response_data and response_data['status'] == True:
            # 如果当前请求成功，检查并发送队列中的请求
            temp_queue = failed_requests.copy()
            failed_requests.clear()

            for failed_data in temp_queue:
                try:
                    retry_response = requests.post(url, json=failed_data, headers=headers)
                    if retry_response.headers.get('Content-Type') == 'application/json':
                        try:
                            retry_response_data = retry_response.json()
                        except json.JSONDecodeError as json_err:
                            print(f"JSON decode error on retry: {json_err}")
                            failed_requests.append(failed_data)
                            continue
                    else:
                        print(f"Unexpected content type on retry: {retry_response.headers.get('Content-Type')}")
                        failed_requests.append(failed_data)
                        continue

                    if 'status' not in retry_response_data or retry_response_data['status'] != True:
                        failed_requests.append(failed_data)
                except Exception as e:
                    print(f"Failed to send queued request: {failed_data}, Error: {e}")
                    failed_requests.append(failed_data)

            return True
        else:
            print(response_data)
            failed_requests.append(data)
            return False

    except Exception as e:
        print(f"Failed to send request: {data}, Error: {e}")
        failed_requests.append(data)
        return False

#
# # 示例调用
# response = send_post_request("2024-05-30 10:00:00", "Device1", "Sample content")
# print(response)
