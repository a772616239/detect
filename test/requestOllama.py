import requests
import json

url = "http://192.168.100.98:11434/api/generate"
headers = {"Content-Type": "application/json"}

payload = {
    "model": "deepseek-r1:14b",
    "prompt": "文本里的角色改成 任意中世纪职业之一，同时，保持整个描述的结构和细节不变，比如颜色调色板、动画步骤等。完整生成100次，只输出英文：“A clean image set showcasing a sequence of attack frames, arranged in order. Eachanimation frame is displayed step by step, with the character in a pixel art style, resembling acommoner dressed in simple clothes. Each frame represents a different stage of the attackanimation, from the initial standing pose, charging, striking, to the finishing move. The colorpalette features soft tones, emphasizing the attack animation and energy. The frames areevenly spaced, and the background is white, providing a clean and orderly appearance. Thisis suitable for pixel art games 35mm film”",
    "stream": False  # 是否启用流式响应
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
if response.status_code == 200:
    result = response.json()
    print("模型回复:", result["response"])
else:
    print("请求失败，状态码：", response.status_code)