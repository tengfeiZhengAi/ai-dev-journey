# -*- coding: utf-8 -*-
"""
    API调用
"""

import os
import sys
import requests

API_KEY = os.environ.get("DASHSCOPE_API_KEY")
if not API_KEY:
    sys.exit(1)

MODEL = "qwen-turbo"
URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

def chat(user_input: str) -> str:
    """发送单轮对话并返回模型回复内容"""
    payload = {
        "model":MODEL,
        "messages":[
            {"role": "user", "content": user_input}
        ]
    }
    resp = requests.post(URL, headers=HEADERS, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]

def main():
    while True:
        try:
            user_input = input("阿飞: ").strip()
            response = chat(user_input)
            print(f"Qwen: {response}")
        except KeyboardInterrupt:
            print("\n程序退出")
            break

if __name__ == "__main__":
    main()