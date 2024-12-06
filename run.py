import os
from app import app
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
# 打印当前工作目录
print("Current working directory:", os.getcwd())

if __name__ == '__main__':
    app.run(debug=True)