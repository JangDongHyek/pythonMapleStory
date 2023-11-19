import requests

def get_public_ip():
    try:
        # 외부 웹사이트에 GET 요청을 보내서 공인 IP 주소를 가져옵니다.
        response = requests.get("https://api64.ipify.org?format=json")

        if response.status_code == 200:
            public_ip = response.json()["ip"]
            return public_ip
        else:
            print(f"HTTP 요청 실패: 상태 코드 {response.status_code}")
            return None
    except Exception as e:
        print(f"에러 발생: {e}")
        return None

public_ip = get_public_ip()

print(public_ip)