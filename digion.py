import requests
import paramiko
import os
import psycopg2
import time


class digion:
    def __init__(self):
        self.api_key = "Your-Token"

    def images(self):
        headers = {"Authorization": "Bearer {}".format(self.api_key)}
        response = requests.get('https://api.digitalocean.com/v2/images', headers=headers)
        return response.json()

    def ip_address(self, id):
        time.sleep(25)
        headers = {"Authorization": "Bearer {}".format(self.api_key)}
        for _ in range(15):
            try:
                response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)
                drop = response.json()['droplets']
                for key in drop:
                    if key['id'] == f'{id}':
                        print(key)
                for pub in key['networks']['v4']:
                    if pub['type'] == 'public':
                        jj = pub['ip_address']
                return jj
            except:
                time.sleep(8)
        return False

    def status(self, id_):
        headers = {"Authorization": "Bearer {}".format(self.api_key)}
        response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)
        status = response.json()['droplets']
        for droplets in status:
            if droplets['droplets'] == f'{id_}':
                print(droplets)
        for status in droplets['status']:
            if status['status'] == 'active':
                print('active')
                return status
        return status

    def snapshot(self, id_, namesht):
        DIGITALOCEAN = ('Your-Token')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {DIGITALOCEAN}",
        }
        data = f'{"type":"snapshot","name":"{namesht}"}'
        response = requests.post(f'https://api.digitalocean.com/v2/droplets/{id_}/actions', headers=headers, data=data)
        return response

    def create_date(self):
        headers = {"Authorization": "Bearer {}".format(self.api_key)}
        response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)
        create_date = response.json()['droplets'][0]['created_at']
        return create_date

    def delete(self, name):
        headers = {"Authorization": "Bearer {}".format(self.api_key)}
        params = (
            ('tag_name', f'{name}'),
        )
        response = requests.delete('https://api.digitalocean.com/v2/droplets', headers=headers, params=params)
        return response

    def delete_query(self, tag):
        conn = psycopg2.connect(
            user='postgres',
            password='Your-pass',
            host='127.0.0.1',
            port='5432',
            database='postgres',
            # sslmode = 'require',
        )
        cur = conn.cursor()
        cur.execute(f"""DELETE FROM public.digion
	                        WHERE tag='{tag}';""")
        conn.commit()
        cur.close()
        conn.close()

    def reset_password(self, id_):
        headers = {"Authorization": "Bearer {}".format(self.api_key)}
        data = '{"type":"password_reset"}'
        response = requests.post(f'https://api.digitalocean.com/v2/droplets/{id_}/actions', headers=headers, data=data)
        return response

    def poweron(self, id_):
        DIGITALOCEAN = ('Your-Token')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {DIGITALOCEAN}",
        }
        data = '{"type":"power_on"}'
        response = requests.post(f'https://api.digitalocean.com/v2/droplets/{id_}/actions', headers=headers, data=data)
        return response

    def poweroff(self, id_):
        DIGITALOCEAN = ('Your-Token')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {DIGITALOCEAN}",
        }
        data = '{"type":"power_off"}'
        response = requests.post(f'https://api.digitalocean.com/v2/droplets/{id_}/actions', headers=headers, data=data)
        return response

    def req_region(self):
        DIGITALOCEAN = ('Your-Token')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {DIGITALOCEAN}",
        }
        params = {
            'page': '1',
            'per_page': '1',
        }
        response = requests.get('https://api.digitalocean.com/v2/droplets', params=params, headers=headers)
        status = response.json()['droplets'][0]['size']['regions']
        return status

    def req_sizes(self):
        DIGITALOCEAN = ('Your-Token')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {DIGITALOCEAN}",
        }
        params = {
            'page': '1',
            'per_page': '1',
        }
        response = requests.get('https://api.digitalocean.com/v2/droplets', params=params, headers=headers)
        a = response.json()['droplets'][0]['region']['sizes']
        return a

    def reboot(self, id_):
        DIGITALOCEAN = ('Your-Token')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {DIGITALOCEAN}",
        }
        data = '{"type":"reboot"}'
        response = requests.post(f'https://api.digitalocean.com/v2/droplets/{id_}/actions', headers=headers, data=data)
        return response

    def insert(self, id_vm, tag, ip_address, user, project_name, size, workers, date_at):
        conn = psycopg2.connect(
            user='postgres',
            password='Your-pass',
            host='127.0.0.1',
            port='5432',
            database='postgres',
            # sslmode = 'require',
        )
        cur = conn.cursor()
        cur.execute(f"""INSERT INTO public.digion(
	        id_vm, tag, ip_address, username, project_name, size_, worker, date_at)
	        VALUES ({id_vm}, '{tag}','{ip_address}','{user}','{project_name}',  '{size}', '{workers}', '{date_at}');""")
        conn.commit()
        cur.close()
        conn.close()

    def resize(self):
        DIGITALOCEAN_TOKEN = os.getenv('Your-Token')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {DIGITALOCEAN_TOKEN}",
        }
        response = requests.get('https://api.digitalocean.com/v2/sizes', headers=headers)
        return response

    def select(self, tag):
        conn = psycopg2.connect(
            user='postgres',
            password='Your-pass',
            host='127.0.0.1',
            port='5432',
            database='postgres',
            # sslmode = 'require',
        )
        cur = conn.cursor()
        cur.execute(f"""SELECT  id_vm
            FROM public.digion WHERE tag = '{tag}' ;""")
        a = cur.fetchone()[0]
        cur.close()
        conn.close()
        return a

    def select_username(self, user):
        conn = psycopg2.connect(
            user='postgres',
            password='Your-pass',
            host='127.0.0.1',
            port='5432',
            database='postgres',
            # sslmode = 'require',
        )
        cur = conn.cursor()
        cur.execute(f"""SELECT  id_vm, ip_address ,tag ,project_name ,  size_, worker, date_at
            FROM public.digion WHERE username = '{user}' ;""")
        a = cur.fetchall()
        cur.close()
        conn.close()
        return a

    def createvm(self, project_name, tag, size ,loc):
        url = "https://api.digitalocean.com/v2/droplets"
        headers = {"Authorization": "Bearer {}".format(self.api_key)}
        data = {
            "name": f"{project_name}",
            "region": loc,
            "size": f"{size}",
            "image": "centos-7-x64",
            "ssh_keys": ['your-fingerprint'],
            "backups": 'false',
            "ipv6": 'false',
            "monitoring": 'false',
            "tags": f"{tag}",
        }
        response = requests.post(url, data=data, headers=headers)
        print(response.status)
        print(response.text)
        id_cloud = response.json()['droplet']['id']
        date = response.json()['droplet']['created_at']
        jj = {
            'id_cloud': id_cloud,
            'date': date,
        }
        return jj

    def ssh_doc(self, host):
        private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa', '')
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username='root', port=22, pkey=private_key, passphrase='')
            command1 = [
                'yum update -y'
                'yum install -y yum-utils',
                'yum install -y firewalld wget tmux',
                'systemctl start firewalld',
                'firewall-cmd --add-port=port/tcp --permanent',
                'firewall-cmd --reload',
                'yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo',
                'yum install -y docker-ce docker-ce-cli containerd.io',
                'systemctl start docker',
                'wget http://your-ip-address:port/get_files --user your-user --password your-password',
                f"mv get_files myapp.tar",
                f'docker load < ./myapp.tar',
                "tmux new-session -d -s 'api' 'docker run -p port:port -it myapp'"
            ]
            for command in command1:
                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.read()
                print(lines.decode(), '\n')
                lines = stderr.read()
                print(lines.decode(), '\n')
            ssh.close()

    def ssh_test(self, host):
        private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa', '')
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username='root', port=22, pkey=private_key, passphrase='')
            command1 = [
                "yum  -y update",
                "yum install python3 -y",
                "yum install -y zip unzip wget",
                "yum install -y tmux",
                'wget --continue http://your-ip-address:your-port/get_files?file=your-zipfile --user your-user --password your-pass',
                'mv get_files?file=your-file file-test.zip',
                "pip3 install --upgrade pip",
                "yum install firewalld -y",
                "systemctl start firewalld",
                "systemctl enable firewalld",
                "firewall-cmd --add-port=your-port/tcp --permanent",
                "firewall-cmd --reload",
                "pip3 install requests\
                        uvicorn==0.15.0\
                        fastapi\
                        flask==1.0.2\
                            "
            ]
            for command in command1:
                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.read()
                print(lines.decode(), '\n')
                lines = stderr.read()
                print(lines.decode(), '\n')
            ssh.close()

    def uvicorn(self, host, workers):
        private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa', '')
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username='root', port=22, pkey=private_key, passphrase='')
            command1 = (
                f"tmux new-session -d -s 'api' 'uvicorn main:app --host 0.0.0.0 --port your-port  --workers {workers}'")
            stdin, stdout, stderr = ssh.exec_command(command1)
            lines = stdout.read()
            print(lines.decode(), '\n')
            lines = stderr.read()
            print(lines.decode(), '\n')
            ssh.close()

