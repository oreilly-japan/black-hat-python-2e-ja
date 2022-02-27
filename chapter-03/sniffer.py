import socket
import os

# リッスンするホストのIPアドレス
HOST = '192.168.1.203'

def main():
    # rawソケットを作成しパブリックなインタフェースにバインド
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))
    # キャプチャー結果にIPヘッダーを含めるように指定
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    # 単一パケットの読み込み
    print(sniffer.recvfrom(65565))

    #  Windowsの場合はプロミスキャスモードを無効化
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    

if __name__ == '__main__':
    main()