#!/usr/bin/env python3
import logging
import docker
from time import sleep
import signal
import os

STOP = False

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
    domain_ext = os.get("DOMAIN_EXTENSION", "home")

    print(f"Schedule time: {time}")    
    print(f"Label url: {label}")    
    print(f"Network: {network}")    
    print(f"Pihole list: {pihole_list}")    
    print(f"Domain extension: {domain_ext}")    

    signal.signal(signal.SIGINT, stop)

    while not STOP:
        task(label, network, pihole_list, domain_ext)
        sleep(time)


def task(label, network, pihole_list, domain_ext):
    client = docker.from_env()

    containers = []
    for con in client.containers.list():
        try:
            domain = con.labels["pihole.url"]
            ip_addr = con.attrs['NetworkSettings']["Networks"][network]['IPAddress']

            if domain.split(".")[-1] == domain_ext:
                containers.append(f"{ip_addr} {domain}")
        except:
            pass

    if len(containers) != 0:

        with open(pihole_list, "w") as f:
            f.writelines(containers)








if __name__ == "__main__":
    main()
