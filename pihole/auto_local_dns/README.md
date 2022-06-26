# Auto Local DNS
The script `auto_local_dns.py` is a small script, which purpose is to update
the local dns server of a pi-hole server. This is done by periodly checking the
running containers of a specific docker label and if their are on a specific
network. Note that the local DNS would be overwritten.

Beware that the script requires access to the docker socket, which could pose a
security risk. 

## Configuration
The behaviour of the script is determined by a number of environment variables. 

- `SCHEDULE_SECONDS`: How often the script should check the labels in seconds, default: 5.
- `LABEL_URL`: The name of the docker label containing the domain names
- `DOCKER_NETWORK`: Which network the containers should be on
- `PIHOLE_DNS_LIST_PATH` The path to pi-hole file containing the local DNS records, default: /etc/pihole/custom.list
- `DOMAIN_EXTENSION`: The extension of the domains which is concided local.
