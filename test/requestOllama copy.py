import requests
import time

class ChatSession:
    def __init__(self, model="deepseek-r1:14b"):
        self.model = model
        self.messages = []
        self.system_prompt = {"role": "system", "content": "你是一个专业助理"}
        self.max_context_length = 5  # 保留最近5轮对话
        self.timeout = 60  # 单位：秒

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def clean_response(self, text):
        return text.replace('<think>', '').replace('</think>', '').strip()

    def get_response(self):
        try:
            # 构建有效上下文
            effective_messages = [self.system_prompt] + self.messages[-self.max_context_length*2:]
            
            # 发送请求
            start_time = time.time()
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": self.model,
                    "messages": effective_messages,
                    "stream": False,
                    "options": {"temperature": 0.5}
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            json_data = response.json()
            print(f"DEBUG [耗时 {time.time()-start_time:.1f}s]:", json_data)

            # 解析响应
            if "message" in json_data:
                return self.clean_response(json_data["message"].get("content", ""))
            elif "response" in json_data:
                return self.clean_response(json_data["response"])
            return "Error: 无法识别的响应格式"

        except requests.exceptions.Timeout:
            return "错误：响应超时，请尝试以下方法：\n1. 简化问题\n2. 减少对话轮次\n3. 检查模型是否正常加载"
        except requests.exceptions.RequestException as e:
            return f"网络错误: {str(e)}"
        except Exception as e:
            return f"系统错误: {str(e)}"

if __name__ == "__main__":
    session = ChatSession()
    print("输入 'exit' 结束对话")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        session.add_message("user", user_input)
        response = session.get_response()
        print("\nAI:", response)
        session.add_message("assistant", response)