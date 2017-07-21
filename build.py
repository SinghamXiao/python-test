#!/usr/bin/env python
# coding=utf-8

import pexpect
import sys

host = ""
loginPassword = ""


def scp_command(src, dest, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    # 为 ssh 命令生成一个 spawn 类的子程序对象.
    child = pexpect.spawn('scp -r %s %s' % (src, dest))
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
    child.sendline(password)
    return child


if __name__ == "__main__":
    print('This is main of module "build.py"')
    child = scp_command(sys.argv[1], host, loginPassword)
    child.expect(pexpect.EOF)
    # 输出命令结果.
    print(child.before)
