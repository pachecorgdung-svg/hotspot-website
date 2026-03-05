#!/usr/bin/env python
"""简单的Flask测试应用"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '跨境电商热点测试 - 应用正常运行！'

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'test'}

if __name__ == '__main__':
    print("启动简单的Flask测试应用...")
    print("访问地址: http://localhost:5000")
    print("按Ctrl+C停止")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)