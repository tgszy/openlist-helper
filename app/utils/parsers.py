import re
import json

def parse_line(line, creds):
    try:
        line = line.strip()
        if not line or line.startswith('#'): 
            return None
            
        parts = line.split()
        if len(parts) < 2: 
            return None
            
        path = parts[0]

        if line.lstrip().startswith('token:'):
            token_part = line.split('token:', 1)[1].strip().split()[0]
            return {"mount_path": path, "driver": "AliyundriveOpen", "addition": json.dumps({"refresh_token": token_part, "root_folder_id": "root"})}

        url = ' '.join(parts[1:]).split()[0]

        if 'alipan.com' in url or 'aliyundrive.com' in url:
            match = re.search(r'/s/([a-zA-Z0-9]+)', url)
            share_id = match.group(1) if match else ""
            pwd = parts[-1] if len(parts) >= 3 and not parts[-1].startswith('http') else ""
            return {"mount_path": path, "driver": "AliyundriveShare", "addition": json.dumps({"share_id": share_id, "share_pwd": pwd, "refresh_token": creds.get('ali_token', '')})}

        if 'quark.cn' in url:
            match = re.search(r'/s/([a-z0-9]+)', url)
            share_id = match.group(1) if match else ""
            pwd = parts[-1] if len(parts) >= 3 else ""
            return {"mount_path": path, "driver": "Quark", "addition": json.dumps({"cookie": creds.get('quark_cookie', ''), "share_id": share_id, "share_pwd": pwd})}

        if len(parts) >= 4 and (parts[1].isdigit() or len(parts[1]) >= 20):
            return {"mount_path": path, "driver": "115 Cloud", "addition": json.dumps({"cookie": creds.get('115_cookie', ''), "share_code": parts[1] if parts[1].isdigit() else "", "root_folder_file_id": parts[2], "receive_code": parts[3]})}

        if 'cloud.189.cn' in url:
            match = re.search(r'/s/([a-z0-9]+)', url)
            share_id = match.group(1) if match else ""
            pwd = parts[-1] if len(parts) >= 3 else ""
            return {"mount_path": path, "driver": "189Cloud", "addition": json.dumps({"cookie": creds.get('ctyun_cookie', ''), "share_id": share_id, "share_pwd": pwd})}

        return None
    except Exception as e:
        # 记录错误日志
        print(f"解析行出错 '{line}': {str(e)}")
        return None
