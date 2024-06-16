import click
import socket
import psutil
import pythonping

LOWEST_MTU = 68
HEADERS = 28

def is_working(host, size, verbose):
    ret: pythonping.Res = pythonping.ping(host, size=size, df=True, count=1, timeout=5)._responses[0]
    if verbose:
        if ret.success:
            print(f'{size} is OK!')
        else:
            print(f'{size} exceeded MTU...')
    return ret.success

@click.command()
@click.argument('dest', type=str, required=True)
@click.option("-v", "--verbose", is_flag=True, show_default=True, default=False)
def mtu_discovering(dest, verbose):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect((dest, 0))
    except socket.error as e:
        sock.close()
        print("Error:", e)
        exit(1)

    laddr = sock.getsockname()[0]
    interface_mtu = -1
    for addrs, stats in zip(psutil.net_if_addrs().values(), psutil.net_if_stats().values()):
        if addrs[0][1] == laddr:
            interface_mtu = int(stats[3])
            break

    sock.close()

    if interface_mtu == -1:
        print("Couldn't find interface assosiated with connection")
        exit(1)

    if not is_working(dest, LOWEST_MTU, verbose=False):
        print("Error: host is unreachable or ICMP isn't working")
        exit(1)

    l = LOWEST_MTU
    h = interface_mtu + 1 - HEADERS
    while h - l > 1:
        mid = (h + l) // 2
        if is_working(dest, mid, verbose):
            l = mid
        else:
            h = mid

    print(f'lowest MTU is {l + HEADERS}')
    sock.close()

if __name__ == '__main__':
    mtu_discovering()
