# -*- coding: utf-8 -*-
"""
    API调用
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# 自动加载项目根目录的 .env 文件（向上找两层：API_CALL -> 项目根目录）
load_dotenv(Path(__file__).parent.parent / ".env")

API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not API_KEY:
    print("[错误] 未检测到 API Key，请检查项目根目录的 .env 文件")
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