"""
日志分析器：读取日志文件
"""
from pathlib import Path

def read_log_file(filename):
    """
    读取日志文件，返回日志内容列表
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    return lines

def analyze_log_file(lines):
    """
    分析日志文件，统计错误日志数量
    """
    error_count = 0
    for line in lines:
        if "ERROR" in line:
            error_count += 1
    return error_count

def main():
    # 【Python】__file__ = 当前脚本的路径  【C++】argv[0]
    script_dir = Path(__file__).parent              # 脚本所在目录
    filename = script_dir / "log.txt"               # / 拼接路径（pathlib 语法）
    lines = read_log_file(filename)
    error_count = analyze_log_file(lines)
    print(f"日志文件 {filename} 中有 {error_count} 条错误日志")

if __name__ == "__main__":
    main()