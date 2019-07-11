import socket

# 创建一个socket对象
sk = socket.socket()
# 绑定一个端口
sk.bind(('127.0.0.1', 8000))
# 监听
sk.listen()


def chaoge(url):
    ret = '{}--性感超哥，在线发牌'.format(url)
    return ret.encode('utf8')


def jinlaoban(url):
    ret = '{}--金老板怒绿西门庆，厉害了啊~~~'.format(url)
    return ret.encode('utf8')


def index(url):
    with open('index.html', 'rb')as f:
        return f.read()


list1 = [
    ('/chaoge/', chaoge),
    ('/jinlaoban/', jinlaoban),
    ('/index/', index),
]

while 1:
    # 连接
    conn, addr = sk.accept()
    # 接收数据
    data = conn.recv(1024)
    # 获取路径
    url = data.decode('utf8').split()[1]  # 按空白切出列表，取第一个地址
    # 发送数据
    conn.send(b'HTTP://1.1 200 ok\r\n\r\n')
    for i in list1:
        if i[0] == url:
            result = i[1](url)
            break
    else:
        result = b'404,no such html'
    conn.send(result)
    # 断开连接
    conn.close()
