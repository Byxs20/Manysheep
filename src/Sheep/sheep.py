import requests

def get_token(id):
    url = "https://cat-match.easygame2021.com/sheep/v1/game/user_info"

    params = {
        "uid": id,
        "t": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQzMjcyNDYsIm5iZiI6MTY2MzIyNTA0NiwiaWF0IjoxNjYzMjIzMjQ2LCJqdGkiOiJDTTpjYXRfbWF0Y2g6bHQxMjM0NTYiLCJvcGVuX2lkIjoiIiwidWlkIjo4MzU0MzAxNCwiZGVidWciOiIiLCJsYW5nIjoiIn0.5qpiRRjxwUmN1U8Qst8dFBMWMQyWi26DcfTgHIITZds",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.28(0x18001c26) NetType/WIFI Language/zh_CN"
    }

    response = requests.get(url, params=params)
    wx_id = response.json()["data"]["wx_open_id"]

    url = "https://cat-match.easygame2021.com/sheep/v1/user/login_oppo"

    js_data = {
        "uid": wx_id,
        "avatar": "1",
        "nick_name": "1",
        "sex": "1",
        "t": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQzMjcyNDYsIm5iZiI6MTY2MzIyNTA0NiwiaWF0IjoxNjYzMjIzMjQ2LCJqdGkiOiJDTTpjYXRfbWF0Y2g6bHQxMjM0NTYiLCJvcGVuX2lkIjoiIiwidWlkIjo4MzU0MzAxNCwiZGVidWciOiIiLCJsYW5nIjoiIn0.5qpiRRjxwUmN1U8Qst8dFBMWMQyWi26DcfTgHIITZds",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.28(0x18001c26) NetType/WIFI Language/zh_CN"
    }

    response = requests.post(url, data=js_data)
    return response.json()["data"]["token"]

def struct_params(game_time, token):
    url = f"http://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=1&rank_time={game_time}&rank_role=1&skin=1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; HD1900 Build/QKQ1.190716.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3263 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/146 MicroMessenger/8.0.16.2040(0x28001037) Process/appbrand2 WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "t": token,
        "referer": "https://servicewechat.com/wx141bfb9b73c970a9/20/page-frame.html",
    }
    return url, headers