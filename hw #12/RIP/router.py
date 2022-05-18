from typing import List, Dict, TypeVar


class Router:
    Router_ = TypeVar('Router', bound='Router')

    def __init__(self, ip: str, distance_table: Dict[int, str]) -> None:
        self._ip = ip
        self.distance_table = distance_table
        self.messages = []
        self._update_neighbor_subnets()

    def _update_neighbor_subnets(self) -> None:
        self.neighbor_subnets = {
            subnet for subnet, (distance, _) in self.distance_table.items() \
            if distance == 1
        }

    def _is_neighbor(self, router: Router_) -> bool:
        return self.neighbor_subnets & router.neighbor_subnets

    def send_distance_table(self, router_list: List[Router_] = None) -> None:
        for router in router_list:
            if self._is_neighbor(router):
                router.messages.append(self.distance_table)

    def update_distance_table(self) -> bool:
        is_updated = False

        for message in self.messages:
            for subnet, (distance, router) in message.items():
                cur_distance = distance + 1
                if cur_distance < 16:
                    if subnet not in self.distance_table or \
                        self.distance_table[subnet][0] > cur_distance:
                        self.distance_table[subnet] = [cur_distance, router]
                        is_updated = True

        self.messages = []
        self._update_neighbor_subnets()
        return is_updated

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip):
        self._ip = ip

    def __str__(self):
        s = f''
        for subnet, (distance, router) in self.distance_table.items():
            s += f'{self.ip:20}{subnet:20}{router:20}{distance:<20}\n'

        return s
