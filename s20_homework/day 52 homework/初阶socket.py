import socket

# 创建一个socket对象
sk = socket.socket()
# 绑定一个端口
sk.bind(('127.0.0.1', 8000))
# 监听
sk.listen()

while 1:
    # 连接
    conn, addr = sk.accept()
    # 接收数据
    data = conn.recv(1024)
    # 获取路径
    url = data.decode('utf8').split()[1]    # 按空白切出列表，取第一个地址
    # 发送数据
    conn.send(b'HTTP://1.1 200 ok\r\n\r\n')
    conn.send(b'ok')
    # 断开连接
    conn.close()
