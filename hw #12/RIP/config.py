from json import dump, load
from random import randint, sample, seed
from typing import Dict, List


def load_config(file_name: str = 'data.json') -> Dict[int, List[int]]:
    with open(file_name, mode='r') as fp:
        config = load(fp)

    config = {int(router): subnets for router, subnets in config.items()}
    return config


def dump_config(
    config: Dict[int, List[int]],
    file_name: str = 'data.json',
) -> None:
    with open(file_name, mode='w') as fp:
        dump(config, fp)


def generate_random_config(
    router_num: int = 5,
    subnet_num: int = 6,
    seed_num: int = 42,
) -> Dict[int, List[int]]:
    if router_num < 1:
        raise ValueError(f'router_num must be at least 1, got {router_num}')

    if subnet_num < 1:
        raise ValueError(f'subnet_num must be at least 1, got {subnet_num}')

    seed(seed_num)

    routers = [i for i in range(1, router_num + 1)]
    subnets = [i for i in range(1, subnet_num + 1)]
    config = {}

    for router in routers:
        connected_subnet_num = randint(1, subnet_num)
        config[router] = sorted(sample(subnets, connected_subnet_num))

    return config
