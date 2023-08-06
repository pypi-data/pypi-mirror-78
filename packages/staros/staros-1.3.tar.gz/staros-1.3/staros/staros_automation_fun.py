import paramiko
import time
import json

import threading
from multiprocessing.dummy import Pool as ThreadPool


class StarosAutoFun:

    def __init__(self, username, password, port_staros, print_answer):
        self.username = username
        self.password = password
        self.port_staros = port_staros
        self.resultfinal_star = []
        # print_answer: 0 - not print answer command, 1 - print all data
        self.print_answer = print_answer

    def command_send(self, ip_address, hostname, command_list):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ip_address, port=self.port_staros, username=self.username, password=self.password)
            chan = ssh.invoke_shell()
            for line in command_list:
                chan.send(line + '\n')
                time.sleep(5)
            output = chan.recv(100000).decode("utf-8")
            answ = '\n'.join(output.split('\n')[3:]) + '\n' + '*' * 80
            self.resultfinal_star.append({hostname: answ})
            if self.print_answer == 1:
                print('#Info from: ' + hostname + ':\n')
                print(answ)
            ssh.close()
        except:
            answ = {hostname: "ERROR"}
            self.resultfinal_star.append(answ)
            if self.print_answer == 1:
                print('#ERROR: ' + hostname + ':\n')

    def massive_command_send(self, ip_list, command_list):
        threads = []
        for one_host in ip_list:
            thread1 = threading.Thread(target=self.command_send,
                                       args=(ip_list[one_host], one_host, command_list))
            # thread1.setDaemon(True)
            thread1.start()
            threads.append(thread1)
        for thread in threads:
            thread.join()
        # json.dumps(self.resultfinal_star, indent=4, sort_keys=True)
        return self.resultfinal_star



