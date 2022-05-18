from random import randint
from typing import List


def generate_ips(size: int = 4) -> List[str]:
    cur_ip = '...'
    ips = [cur_ip, ]
    for _ in range(size):
        while cur_ip in ips:
            cur_ip = [str(randint(0, 255)) for _ in range(4)]
            cur_ip = '.'.join(cur_ip)

        ips.append(cur_ip)

    return ips[1:]
