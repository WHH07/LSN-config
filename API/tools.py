import requests
import json
import websockets

class APIClient:
    """API客户端类,用于发送HTTP请求"""
    
    def __init__(self, base_url):
        """
        初始化API客户端
        :param base_url: API的基础URL
        """
        self.base_url = base_url.rstrip('/')
        
    def get(self, endpoint, params=None, download=False, file_path=None):
        """
        发送GET请求
        :param endpoint: API端点
        :param params: URL参数(可选)
        :param download: 是否下载响应内容(可选)
        :param file_path: 下载文件保存路径(可选)
        :return: 响应数据
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            if download:
                if response.headers.get('Content-Type') == 'application/zip':
                    with open(file_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    print(f"ZIP file saved as '{file_path}'")
                return file_path
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GET请求失败: {str(e)}")
            print(f"请求URL: {url}")
            print(f"请求参数: {params}")
            if hasattr(e.response, 'text'):
                print(f"错误响应: {e.response.text}")
            raise

    def post(self, endpoint, data=None, json_data=None, files=None, download=False, file_path=None):
        """
        发送POST请求
        :param endpoint: API端点
        :param data: 表单数据(可选)
        :param json_data: JSON数据(可选) 
        :param files: 要上传的文件(可选),格式为{'file': ('filename', open('file','rb'))}
        :param download: 是否下载响应内容(可选)
        :param file_path: 下载文件保存路径(可选)
        :return: 响应数据
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.post(url, data=data, json=json_data, files=files)
            response.raise_for_status()
            if download:
                if response.headers.get('Content-Type') == 'application/zip':
                    with open(file_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    print(f"ZIP file saved as '{file_path}'")
                return file_path
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"POST请求失败: {str(e)}")
            print(f"请求URL: {url}")
            print(f"表单数据: {data}")
            print(f"JSON数据: {json_data}")
            print(f"上传文件: {files}")
            if hasattr(e.response, 'text'):
                print(f"错误响应: {e.response.text}")
            raise


class WebSocketClient:
    """WebSocket客户端类"""
    
    def __init__(self, base_url):
        """
        初始化WebSocket客户端
        :param base_url: WebSocket的基础URL
        """
        self.base_url = base_url.rstrip('/')
        self.websocket = None
        
    def get_ws_url(self):
        """
        获取WebSocket URL
        :return: WebSocket URL
        """
        ws_url = self.base_url
        if ws_url.startswith('http://'):
            ws_url = 'ws://' + ws_url[7:]
        elif ws_url.startswith('https://'):
            ws_url = 'wss://' + ws_url[8:]
        return ws_url

    async def connect(self, endpoint):
        """
        创建WebSocket连接
        :param endpoint: WebSocket端点
        :return: None
        """
        ws_url = f"{self.get_ws_url()}/{endpoint.lstrip('/')}"
        try:
            self.websocket = await websockets.connect(ws_url)
            print(f"WebSocket连接成功: {ws_url}")
        except Exception as e:
            print(f"WebSocket连接失败: {str(e)}")
            print(f"WebSocket URL: {ws_url}")
            raise

    async def receive(self):
        """
        接收WebSocket消息
        :return: 接收到的消息
        """
        if not self.websocket:
            raise Exception("WebSocket未连接")
        try:
            message = await self.websocket.recv()
            return message
        except Exception as e:
            print(f"接收消息失败: {str(e)}")
            raise

    async def send(self, message):
        """
        发送WebSocket消息
        :param message: 要发送的消息
        :return: None
        """
        if not self.websocket:
            raise Exception("WebSocket未连接")
        try:
            await self.websocket.send(message)
        except Exception as e:
            print(f"发送消息失败: {str(e)}")
            raise

    async def disconnect(self):
        """
        断开WebSocket连接
        :return: None
        """
        if self.websocket:
            try:
                await self.websocket.close()
                self.websocket = None
                print("WebSocket连接已断开")
            except Exception as e:
                print(f"断开连接失败: {str(e)}")
                raise

