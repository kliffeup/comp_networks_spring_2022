from config import *
from router import Router
from utils import generate_ips


class Network:
    def __init__(
        self,
        file_name: str = None,
        dump: bool = True,
        seed_num: int = 42,
    ) -> None:
        if file_name:
            self.config = load_config(file_name)
        else:
            self.config = generate_random_config(seed_num=seed_num)

            if dump:
                dump_config(self.config)

        self._init_subnets()
        self._init_routers()

    def _init_subnets(self) -> None:
        subnets = {subnet for l in self.config.values() for subnet in l}
        subnet_ips = generate_ips(len(subnets))
        subnets = {
            subnet: subnet_ip for subnet, subnet_ip in zip(subnets, subnet_ips)
        }

        self.subnets = subnets

    def _init_routers(self) -> None:
        router_ips = generate_ips(len(self.config.keys()))
        self.routers = []

        for router_id, subnets in self.config.items():
            router_ip = router_ips[router_id - 1]
            router = Router(
                ip=router_ip,
                distance_table={
                    self.subnets[subnet]: [1, router_ip] for subnet in subnets
                },
            )

            self.routers.append(router)

    def rip(self) -> None:
        is_changed = True
        while is_changed:
            is_changed = False
            for router in self.routers:
                router.send_distance_table(self.routers)

            for router in self.routers:
                is_changed = is_changed or router.update_distance_table()

    def print_report(self):
        for router in self.routers:
            print(f'Final state of router {router.ip}')
            print(f'{"Source IP":20}{"Destination IP":20}'
                  f'{"Next Hop":20}{"Metric":20}')
            print(router)
