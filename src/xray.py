import os
import re
import base64
import paramiko

from urllib.parse import urlparse


class CmdError(Exception):
    pass


class URLFormatError(Exception):
    pass


class XRaySSHInterface(object):
    
    def __init__(self, host_ip, known_hosts=None, username=None, password=None):
        
        self.host_ip = host_ip
        self.client = paramiko.SSHClient()
        
        if known_hosts:
            self.client.load_system_host_keys(known_hosts)
            self.username = None
            self.password = None
            
        else:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.username = username
            self.password = password
            
    @staticmethod
    def _get_xray_cmd(user_id, method, sudo_flg=True, script='ex.sh', cwd='/opt/easy-xray-main'):
        
        sudo = 'sudo ' if sudo_flg else ''
        exec_path = os.path.join(cwd, script)
        config_path = os.path.join(cwd, f'conf/config_client_{user_id}.json')

        if method == 'add':
            cmd_str = f'{sudo}{exec_path} {method} {user_id}'
            
        elif method == 'link':
            cmd_str = f'{sudo}{exec_path} {method} {config_path}'
            
        else:
            raise NotImplementedError

        return cmd_str
    
    @staticmethod
    def _format_output(output_raw):
        
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        output = ansi_escape.sub('', output_raw.strip()).split('\n')
        
        return output
    
    @staticmethod
    def _check_url_format(url, format_exception='raise'):
        
        url_components = urlparse(url)
        checks = [
            url_components.scheme == 'vless',
            all([
                url_components.scheme, 
                url_components.netloc, 
                url_components.query, 
                url_components.fragment
            ])
        ]
        
        if not all(checks) and format_exception == 'raise':
            raise URLFormatError(f'Wrong URL format: {url}')
        elif not all(checks) and format_exception == 'warn':
            print('Warning: wrong URL format: {url}')
        
        return all(checks)
            
    def _exec_command(self, cmd, timeout=30):
        
        try:
            self.client.connect(hostname=self.host_ip, 
                                username=self.username, 
                                password=self.password)
            stdin, stdout, stderr = self.client.exec_command(cmd, 
                                                             timeout=timeout)
            
            out = self._format_output(stdout.read().decode())
            err = self._format_output(stderr.read().decode())
            
            if err[0] != '':
                raise CmdError(err[0])
            
            return out
        
        except Exception as e:
            print(f"Ошибка: {e}")
            
        finally:
            self.client.close()
            
    def add_xray_user(self, user_id, sudo_flg=True):
        
        cmd_xray_add = self._get_xray_cmd(user_id, 'add', sudo_flg=sudo_flg)
        output = self._exec_command(cmd_xray_add)
        
        return output
        
    def get_xray_url(self, user_id, sudo_flg=True, url_format_exception='warn'):
        
        cmd_xray_link = self._get_xray_cmd(user_id, 'link', sudo_flg=sudo_flg)
        out = self._exec_command(cmd_xray_link)
        url = out[-1]
        _ = self._check_url_format(url, url_format_exception)

        return url


def encode_urls(urls):
    
    url_str = '\n'.join(urls)
    encoded_url = base64.b64encode(url_str.encode()).decode()
    
    return encoded_url


