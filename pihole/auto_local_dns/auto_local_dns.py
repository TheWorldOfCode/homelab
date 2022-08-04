#!/usr/bin/env python3
import logging
import docker
from time import sleep
from typing import List
import signal
import os

STOP = False

class Domain():

    """ Contains a domain and ip address """

    def __init__(self, name: str, ip: str):
        """ Create the object 

        @param name The domain name
        @param ip The ip address

        """
        self._name = name
        self._ip = ip

    def set_ip(self, new_ip: str):
        """ Set a new ip for domain """
        self._ip = new_ip

    def to_file(self) -> str:
        """ Return information according to pihole file format """
        return f"{self._ip} {self._name}"

    def __str__(self) -> str:
        return f"{self._ip} {self._name}"

    def __repr__(self) -> str:
        return repr((self._ip, self._name))

    def __eq__(self, b) -> bool:
        """ Compare two domains """
        if self._name != b._name:
            return False

        if self._ip != b._ip:
            return False

        return True


def stop(signum, frame):
    global STOP
    STOP = True
    print("Stopping")


def main():
    global STOP
    time = int(os.getenv("SCHEDULE_SECONDS", 5))
    label = os.getenv("LABEL_URL", "pihole.url")
    network = os.getenv("DOCKER_NETWORK", "frontend")
    pihole_list = os.getenv("PIHOLE_DNS_LIST_PATH", "/etc/pihole/custom.list")
    domain_ext = os.getenv("DOMAIN_EXTENSION", "home")
    overwrite_domain = os.getenv("OVERWRITE_DOMAIN_IP", "")
    pihole_container = os.getenv("PIHOLE_CONTAINER_NAME", "pihole")

    print(f"Schedule time: {time}")    
    print(f"Label url: {label}")    
    print(f"Network: {network}")    
    print(f"Pihole list: {pihole_list}")    
    print(f"Domain extension: {domain_ext}")    
    print(f"Overwrite domain ip: {overwrite_domain}")    
    print(f"Pihole container name: {pihole_container}")

    signal.signal(signal.SIGINT, stop)

    while not STOP:
        task(label, network, pihole_list, domain_ext, overwrite_domain,
             pihole_container)
        sleep(time)

def compare_domains(list_a: List[Domain], list_b: List[Domain]) -> bool:
    """
        Compare two list with domains

        @param list_a The first list
        @param list_b The second list
        @return True if the lists contains the same domains
    """

                                                       

    if len(list_a) != len(list_b):
        return False

    return sorted(reversed(list_a), key=lambda x: x._name) == sorted(list_b, key=lambda x: x._name)


def task(label, network, pihole_list, domain_ext, overwrite_domain,
         pihole_container_name):
    client = docker.from_env()

    containers = []
    for con in client.containers.list():
        try:
            domain = con.labels["pihole.url"]
            ip_addr = con.attrs['NetworkSettings']["Networks"][network]['IPAddress']

            if domain.split(".")[-1] == domain_ext:
                D = Domain(domain, ip_addr)
                if overwrite_domain != "":
                    D.set_ip(overwrite_domain)
                containers.append(D)
        except:
            pass

    if len(containers) != 0:
        print("Containers:",containers)
        
        pihole = []
        with open(pihole_list, "r") as f:
            for line in f.readlines():
                ip, domain = line.replace("\n", "").split(" ")
                pihole.append(Domain(domain, ip))

        print("Pihole list", pihole) 
        if not compare_domains(pihole, containers):
            with open(pihole_list, "w") as f:
                for d in containers:
                    f.write(f"{d.to_file()}\n")
            print("Update dns server")

            pihole_container = client.containers.get(pihole_container_name)
            pihole_container.exec_run("pihole restartdns")



if __name__ == "__main__":
    main()
