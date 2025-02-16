import os
import re
import base64
import paramiko

from urllib.parse import urlparse


class CmdError(Exception):
    pass


class URLFormatError(Exception):
    pass


class AddUserError(Exception):
    pass


class XRaySSHInterface(object):
    
    def __init__(self, host_ip, known_hosts=None, username=None, password=None, sudo_flg=True, sudo_password=None):
        
        self.host_ip = host_ip
        self.client = paramiko.SSHClient()
        self.sudo_flg = sudo_flg
        
        if known_hosts:
            self.client.load_system_host_keys(known_hosts)
            self.username = None
            self.password = None
            
        else:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.username = username
            self.password = password
            
        if self.sudo_flg:
            self.sudo_password = sudo_password
            
    def _get_xray_cmd(self, user_id, method, cwd='easy-xray-main'):
        
        sudo = 'sudo ' if self.sudo_flg else ''
        exec_path = os.path.join(cwd, 'ex.sh')
        config_path = f'conf/config_client_{user_id}.json'

        if method == 'add':
            cmd_str = f'cd {cwd}; {sudo}./ex.sh {method} {user_id}'
            
        elif method == 'link':
            cmd_str = f'cd {cwd}; {sudo}./ex.sh {method} {config_path}'
            
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
            print(f'Warning: wrong URL format: {url}')
        
        return all(checks)
    
    @staticmethod
    def _check_add_action(log, xray_ver='25.1.30', format_exception='raise'):
        
        log_txt = '\n'.join(log)
        xray_status = log[-1].split(': ')[-1]
        print(xray_status)
        check = xray_status == f'Xray {xray_ver} started'
        
        if not check and format_exception == 'raise':
            raise AddUserError(f'Something went wrong with user add: {log_txt}')
        elif not check and format_exception == 'warn':
            print(f'Warning: Something went wrong with user add: {log_txt}')
            
        return check
    
    # такая логика не работает с разными сессиями
    def _exec_command(self, cmd, timeout=30):
        
        try:
            self.client.connect(hostname=self.host_ip, 
                                username=self.username, 
                                password=self.password)
            if self.sudo_flg:
                stdin, stdout, stderr = self.client.exec_command(cmd, 
                                                                 timeout=timeout, 
                                                                 get_pty=True)
                stdin.write(self.sudo_password + "\n")
                stdin.flush()
            else:
                stdin, stdout, stderr = self.client.exec_command(cmd, 
                                                                 timeout=timeout)
            
            out = self._format_output(stdout.read().decode())
            err = self._format_output(stderr.read().decode())
            
            if err[0] != '':
                raise CmdError(err[0])
            
            return out
        
        except Exception as e:
            raise e
            
        finally:
            self.client.close()
            
    def add_xray_user(self, user_id, cwd, add_user_exception='warn'):
        
        cmd_xray_add = self._get_xray_cmd(user_id, 'add', cwd=cwd)
        
        try:
            self.client.connect(hostname=self.host_ip, 
                                username=self.username, 
                                password=self.password)
        
            stdin, stdout, stderr = self.client.exec_command(cmd_xray_add, 
                                                             timeout=30,
                                                             get_pty=True)
            stdin.write(self.sudo_password + "\n")
            stdin.write('Y\n')
            stdin.write('S\n')
            stdin.flush()

            log = self._format_output(stdout.read().decode())
            err = self._format_output(stderr.read().decode())
            
            if err[0] != '':
                raise CmdError(err[0])
            # непонятная ошибка на валидации stdout
            #check = self._check_add_action(log, add_user_exception)
            
            return True
        
        except Exception as e:
            raise e
            
        finally:
            self.client.close()
        
    def get_xray_url(self, user_id, cwd, url_format_exception='warn'):
        
        cmd_xray_link = self._get_xray_cmd(user_id, 'link', cwd=cwd)
        
        try:
            self.client.connect(hostname=self.host_ip, 
                                username=self.username, 
                                password=self.password)
        
            stdin, stdout, stderr = self.client.exec_command(cmd_xray_link, 
                                                             timeout=30,
                                                             get_pty=True)
            stdin.write(self.sudo_password + "\n")
            stdin.flush()

            out = self._format_output(stdout.read().decode())
            err = self._format_output(stderr.read().decode())
            
            if err[0] != '':
                raise CmdError(err[0])
                
            url = out[-1]
            _ = self._check_url_format(url, url_format_exception)
            
            return url
        
        except Exception as e:
            raise e
            
        finally:
            self.client.close()


def encode_urls(urls):
    
    url_str = '\n'.join(urls)
    encoded_url = base64.b64encode(url_str.encode()).decode()
    
    return encoded_url
