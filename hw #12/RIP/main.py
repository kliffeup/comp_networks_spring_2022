from network import Network


if __name__ == '__main__':
    net = Network('data.json')
    net.rip()
    net.print_report()
