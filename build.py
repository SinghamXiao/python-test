#!/usr/bin/env python
# coding=utf-8

import pexpect
import sys

host = ""
loginUser = ""
loginPassword = ""
COMMANDS = """ls -l && cd /usr/local/ && ls -l"""


def ssh_command(commands):
    ssh_newkey = 'Are you sure you want to continue connecting'
    # 为 ssh 命令生成一个 spawn 类的子程序对象.
    child = pexpect.spawn(commands[0])
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
    # 如果登录超时，打印出错信息，并退出.
    if i == 0:  # Timeout
        print('ERROR!')
        print('SSH could not login. Here is what SSH said:')
        print(child.before, child.after)
        return None
    # 如果 ssh 没有 public key，接受它.
    if i == 1:  # SSH does not have the public key. Just accept it.
        child.sendline('yes')
        child.expect('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0:  # Timeout
            print('ERROR!')
            print('SSH could not login. Here is what SSH said:')
            print(child.before, child.after)
        return None
    # 输入密码.
    child.sendline(commands[1])
    return child


if __name__ == "__main__":
    print("Start ...")
    command = 'scp -r %s %s' % (sys.argv[1], loginUser + "@" + host + ":~/")
    child = ssh_command([command, loginPassword])
    child.expect(pexpect.EOF)
    # 输出命令结果.
    print(child.before)

    command = 'ssh -l %s %s %s' % (loginUser, host, COMMANDS)
    child = ssh_command([command, loginPassword])
    child.expect(pexpect.EOF)
    # 输出命令结果.
    print(child.before)
