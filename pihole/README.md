# Pi-hole

Pi-hole provides network-wide protection by functioning as a DNS server and
DHCP server. The main function of the DNS server is to check the domain names
of the queries. If the domain name is allowed, it would then contact an
external DNS server for requiring the ip address. 

Furthermore, Pi-hole contains also a local DNS server which allows for manually
adding domains to the server. This is useful of local domains. 

## Docker
Pi-hole can easily be deployed on a server using docker. One possible
configuration is showed in the file `docker-compose.yaml`. 

The compose file would launch to different containers. The Pi-hole and a small
container running a python script, which would automatically add local domains
to the DNS server, using the container labels.  Furthermore, the Pi-hole
container is setup with labels for traefix of accessing the web interface. The traefix should be on a network called `frontend`.

The compose file would look for the following environment variable for
configuration: 
- `PIHOLE_FRONTEND_NETWORK`: The name of the docker network for the traefix server
- `PIHOLE_ENTRYPOINT`: The Traefik entrypoint. Default web
- `PIHOLE_ENABLE_TLS`: Enable TLS. Default false
- `PIHOLE_CERTRESOLVER`: Which certresolver should be used. Default
  letsencrypt.
- `PIHOLE_AUTO_LOCAL_DNS_SCHEDULE`: How often the auto local dns script should run in seconds, default 5
- `PIHOLE_AUTO_LOCAL_DNS_DOMAIN_EXTENSION`: The domain externsion which represents a local domain, default home.
- `PIHOLE_AUTO_LOCAL_DNS_LABEL_DOMAIN`: The name of the docker label which contains the domain name, default pihole.url.
- `PIHOLE_OVERWRITE_DOMAIN`: Overwrite the IP address of the container with
  provided ip address.
