from flask import request, render_template_string, session
import requests, json, time
from app import app, DISK_CONFIGS, SUPPORTED_DRIVERS
from app.utils.parsers import parse_line

# HTML模板
HTML = '''
<!DOCTYPE html>
<html class="bg-gray-900 text-gray-100 min-h-screen">
<head>
    <meta charset="utf-8">
    <title>OpenList 快速导入神器</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <style>
        .gradient-title { background: linear-gradient(to right, #a855f7, #3b82f6); -webkit-background-clip: text; color: transparent; }
        details summary { list-style: none; }
        details[open] > summary > span:last-child { transform: rotate(90deg); }
    </style>
</head>
<body class="p-6 max-w-5xl mx-auto font-sans">
    <div class="text-center mb-12">
        <h1 class="text-5xl font-bold gradient-title">OpenList 快速导入神器</h1>
        <p class="text-gray-400 mt-3 text-lg">便捷地批量添加网盘资源到 OpenList</p>
    </div>

    <form method="post" class="space-y-8">
        <!-- OpenList 连接 -->
        <div class="grid md:grid-cols-2 gap-6 bg-gray-800/50 p-6 rounded-2xl border border-gray-700">
            <div>
                <label class="block text-purple-400 mb-2">OpenList 地址</label>
                <input name="url" value="{{url}}" required placeholder="http://192.168.1.100:5244" class="w-full px-4 py-3 bg-gray-900 rounded-lg border border-gray-700 focus:ring-2 focus:ring-purple-500">
            </div>
            <div>
                <label class="block text-purple-400 mb-2">Admin Token</label>
                <input name="token" value="{{token}}" required placeholder="粘贴 Admin Token" class="w-full px-4 py-3 bg-gray-900 rounded-lg border border-gray-700 focus:ring-2 focus:ring-purple-500">
            </div>
        </div>

        <!-- 配置网盘账号（默认收缩） -->
        <details class="bg-gray-800/50 rounded-2xl border border-gray-700">
            <summary class="flex justify-between items-center px-6 py-4 cursor-pointer hover:bg-gray-700/50">
                <span class="text-xl font-semibold text-purple-400">配置网盘账号（点击展开）</span>
                <span class="text-2xl transition">→</span>
            </summary>
            <div class="p-6 border-t border-gray-700 space-y-6">
                <div class="flex flex-wrap gap-3">
                    <button type="button" hx-get="/refresh" hx-target="#disk-list" hx-swap="innerHTML" class="px-5 py-2.5 bg-blue-600 rounded-lg hover:bg-blue-700">刷新现有网盘</button>
                    <button type="button" hx-get="/add-form" hx-target="#add-form" hx-swap="innerHTML" class="px-5 py-2.5 bg-green-600 rounded-lg hover:bg-green-700">新增网盘</button>
                    <button type="button" hx-get="/detect" hx-target="#disk-list" hx-swap="innerHTML" class="px-5 py-2.5 bg-yellow-600 rounded-lg hover:bg-yellow-700">检测状态</button>
                </div>
                <div id="disk-list" class="bg-gray-900/50 rounded-lg p-4 text-sm">
                    <p class="text-gray-500">点击“刷新现有网盘”加载列表</p>
                </div>
                <div id="add-form"></div>
                <p class="text-sm text-gray-400">
                    提示：您可以在 <a href="https://api.oplist.org" target="_blank" class="text-blue-400 hover:underline">OpenList 官方 Token 网站</a> 获取网盘 Cookie 和 Token
                </p>
            </div>
        </details>

        <!-- 资源批量添加区 -->
        <div class="space-y-4">
            <label class="block text-xl font-semibold text-purple-400">资源批量添加区（支持直接粘贴）</label>
            <textarea name="resources" rows="12" required placeholder="/阿里/电影 https://www.alipan.com/s/xxxx 1234&#10;/夸克/资源 https://pan.quark.cn/s/xxxx&#10;/115/资料 114514 1234567890ABCDEF 8888&#10;/天翼/备份 https://cloud.189.cn/s/xxxx pwd" class="w-full px-5 py-4 bg-gray-800 border border-gray-700 rounded-xl font-mono text-sm"></textarea>
            <div class="text-right">
                <button type="submit" class="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-xl font-bold rounded-xl">开始导入</button>
            </div>
        </div>
    </form>

    {% if result %}
    <div class="mt-8 bg-gray-800/50 rounded-2xl p-8 border border-gray-700">
        <h3 class="text-2xl font-bold mb-6">导入完成（用时 {{ "%.1f"|format(result.time) }} 秒）</h3>
        <div class="grid grid-cols-3 gap-6 text-center">
            <div class="bg-green-900/40 py-6 rounded-xl"><div class="text-4xl font-bold">{{result.success}}</div><div class="text-green-400">成功</div></div>
            <div class="bg-red-900/40 py-6 rounded-xl"><div class="text-4xl font-bold">{{result.failed}}</div><div class="text-red-400">失败</div></div>
            <div class="bg-blue-900/40 py-6 rounded-xl"><div class="text-4xl font-bold">{{result.total}}</div><div class="text-blue-400">总数</div></div>
        </div>
        {% if result.failed > 0 %}
        <details class="mt-6">
            <summary class="cursor-pointer text-red-400">查看失败记录</summary>
            <textarea class="w-full mt-3 bg-black/30 p-4 rounded text-sm" rows="8" readonly>{{result.failed_text}}</textarea>
        </details>
        {% endif %}
    </div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start = time.time()
        url = request.form['url'].rstrip('/')
        token = request.form['token']
        session['url'] = url
        session['token'] = token
        session.update({k: request.form.get(k, '') for k in ['ali_token','quark_cookie','115_cookie','ctyun_cookie']})

        lines = [l for l in request.form['resources'].split('\n') if l.strip()]
        success = failed = 0
        failed_lines = []
        
        # 定义带超时和错误处理的API请求函数
        def api_request(method, endpoint='', **kwargs):
            try:
                response = requests.request(
                    method,
                    f"{url}{endpoint}",
                    headers={"Authorization": token},
                    timeout=10,  # 添加超时设置
                    **kwargs
                )
                response.raise_for_status()  # 检查 HTTP 错误
                return response
            except requests.exceptions.Timeout:
                raise Exception("请求超时")
            except requests.exceptions.RequestException as e:
                raise Exception(f"网络错误: {str(e)}")

        for line in lines:
            data = parse_line(line, session)
            if not data:
                failed += 1
                failed_lines.append(f"{line} → 格式错误")
                continue
            
            try:
                # 解析 addition 字符串为 JSON 对象
                if isinstance(data['addition'], str):
                    data['addition'] = json.loads(data['addition'])
                
                r = api_request(
                    'POST',
                    endpoint='/api/admin/storage/create',
                    json={**data, "cache_expiration": 30, "web_proxy": False, "webdav_policy": "native_proxy"}
                )
                
                response_data = r.json()
                if response_data.get('success', True):
                    success += 1
                else:
                    failed += 1
                    failed_lines.append(f"{line} → {response_data.get('message','未知错误')}")
            except json.JSONDecodeError:
                failed += 1
                failed_lines.append(f"{line} → JSON 解析错误")
            except Exception as e:
                failed += 1
                failed_lines.append(f"{line} → {str(e)}")

        result = {"success": success, "failed": failed, "total": len(lines), "time": time.time()-start, "failed_text": "\n".join(failed_lines)}
        return render_template_string(HTML, url=url, token=token, result=result)

    return render_template_string(HTML, url=session.get('url','http://'), token=session.get('token',''))

@app.route('/refresh')
def refresh():
    url, token = session.get('url'), session.get('token')
    if not url or not token:
        return '<p class="text-red-400">请先填写 OpenList 地址和 Token</p>'
    
    try:
        r = requests.get(
            f"{url}/api/admin/storage/list",
            headers={"Authorization": token},
            timeout=10  # 添加超时设置
        )
        r.raise_for_status()  # 检查 HTTP 错误
        
        data = r.json()
        storages = [s for s in data.get('data', []) if s['driver'] in SUPPORTED_DRIVERS]
        session['existing'] = storages
        
        return render_template_string('''
        <table class="w-full text-sm">
            <thead class="bg-gray-800"><tr><th>类型</th><th>路径</th><th>状态</th><th>操作</th></tr></thead>
            <tbody>
            {% for s in existing %}
            <tr class="border-t border-gray-700"><td>{{ DISKS[s.driver].name }}</td><td>{{ s.mount_path }}</td><td>{% if s.status != "error" %}有效{% else %}失效{% endif %}</td><td><button hx-delete="/delete/{{ s.id }}" hx-target="#disk-list" hx-swap="innerHTML" class="text-red-400 text-xs">删除</button></td></tr>
            {% endfor %}
            </tbody>
        </table>
        ''', existing=storages, DISKS=DISK_CONFIGS)
        
    except requests.exceptions.Timeout:
        return '<p class="text-red-400">请求超时，请检查网络连接</p>'
    except requests.exceptions.RequestException as e:
        return f'<p class="text-red-400">获取失败: {str(e)}</p>'
    except json.JSONDecodeError:
        return '<p class="text-red-400">无效的响应格式</p>'
    except Exception as e:
        return f'<p class="text-red-400">获取失败: {str(e)}</p>'

@app.route('/add-form')
def add_form():
    return '''
    <div class="bg-gray-800/50 p-4 rounded mt-4">
        <select name="driver" class="w-full p-2 bg-gray-900 rounded mb-2">
            <option value="AliyundriveOpen">阿里云盘（账号）</option>
            <option value="Quark">夸克网盘</option>
            <option value="115 Cloud">115网盘</option>
            <option value="189Cloud">天翼云盘</option>
        </select>
        <input name="mount_path" placeholder="挂载路径 如 /阿里/新盘" class="w-full p-2 bg-gray-900 rounded mb-2">
        <textarea name="addition" placeholder='{"refresh_token":"..."} 或 {"cookie":"..."}' rows="4" class="w-full p-2 bg-gray-900 rounded mb-2"></textarea>
        <button hx-post="/add" hx-target="#disk-list" hx-swap="innerHTML" class="w-full p-2 bg-green-600 rounded">添加</button>
    </div>
    '''

@app.route('/add', methods=['POST'])
def add_storage():
    url, token = session.get('url'), session.get('token')
    if not url or not token:
        return '<p class="text-red-400">请先填写 OpenList 地址和 Token</p>'
    
    try:
        driver = request.form.get('driver')
        mount_path = request.form.get('mount_path')
        addition = request.form.get('addition')
        
        if not driver or not mount_path or not addition:
            return '<p class="text-red-400">请填写完整的信息</p>'
        
        # 解析 addition 为 JSON
        addition_json = json.loads(addition)
        
        # 构建请求数据
        data = {
            'driver': driver,
            'mount_path': mount_path,
            'addition': addition_json,
            'cache_expiration': 30,
            'web_proxy': False,
            'webdav_policy': 'native_proxy'
        }
        
        # 发送请求
        r = requests.post(
            f"{url}/api/admin/storage/create",
            headers={"Authorization": token},
            json=data
        )
        
        if r.status_code == 200 and r.json().get('success', True):
            # 添加成功，刷新列表
            return refresh()
        else:
            return f'<p class="text-red-400">添加失败: {r.json().get("message", "未知错误")}</p>'
            
    except json.JSONDecodeError:
        return '<p class="text-red-400">配置格式错误，请检查 JSON 格式</p>'
    except Exception as e:
        return f'<p class="text-red-400">添加失败: {str(e)}</p>'

@app.route('/delete/<int:sid>', methods=['DELETE'])
def delete_storage(sid):
    url, token = session.get('url'), session.get('token')
    if not url or not token:
        return '<p class="text-red-400">请先填写 OpenList 地址和 Token</p>'
    
    try:
        r = requests.delete(
            f"{url}/api/admin/storage/delete/{sid}",
            headers={"Authorization": token}
        )
        
        if r.status_code == 200 and r.json().get('success', True):
            # 删除成功，刷新列表
            return refresh()
        else:
            return f'<p class="text-red-400">删除失败: {r.json().get("message", "未知错误")}</p>'
            
    except Exception as e:
        return f'<p class="text-red-400">删除失败: {str(e)}</p>'

@app.route('/detect')
def detect_storage():
    url, token = session.get('url'), session.get('token')
    if not url or not token:
        return '<p class="text-red-400">请先填写 OpenList 地址和 Token</p>'
    
    try:
        # 获取存储列表
        r = requests.get(f"{url}/api/admin/storage/list", headers={"Authorization": token})
        if r.status_code != 200:
            return '<p class="text-red-400">获取存储列表失败</p>'
        
        storages = [s for s in r.json().get('data', []) if s['driver'] in SUPPORTED_DRIVERS]
        
        # 检测每个存储的状态
        for storage in storages:
            try:
                status_r = requests.get(
                    f"{url}/api/admin/storage/status/{storage['id']}",
                    headers={"Authorization": token}
                )
                if status_r.status_code == 200:
                    storage['status'] = status_r.json().get('data', {}).get('status', 'unknown')
            except Exception:
                storage['status'] = 'error'
        
        session['existing'] = storages
        
        return render_template_string('''
        <table class="w-full text-sm">
            <thead class="bg-gray-800"><tr><th>类型</th><th>路径</th><th>状态</th><th>操作</th></tr></thead>
            <tbody>
            {% for s in existing %}
            <tr class="border-t border-gray-700"><td>{{ DISKS[s.driver].name }}</td><td>{{ s.mount_path }}</td><td>{% if s.status != "error" %}有效{% else %}失效{% endif %}</td><td><button hx-delete="/delete/{{ s.id }}" hx-target="#disk-list" hx-swap="innerHTML" class="text-red-400 text-xs">删除</button></td></tr>
            {% endfor %}
            </tbody>
        </table>
        ''', existing=storages, DISKS=DISK_CONFIGS)
        
    except Exception as e:
        return f'<p class="text-red-400">检测失败: {str(e)}</p>'
