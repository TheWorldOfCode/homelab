# Traefik

DESCRIPTION OF TRAEFIK 



## Launching 

Environment variable:
    - `TRAEFIK_ETC`: The path to folder containing the configuration for traefik (default: the current folder)
    - `TRAEFIK_SIMPLY_ACCOUNT_NAME`: The account for the simply.com
    - `TRAEFIK_SIMPLY_API_KEY`: The api key for simply.com
    - `TRAEFIK_DOMAIN`: The domain of the Traefik dashboard, default: `traefik.home`.
    - `TRAEFIK_ENABLE`: Allow traefik to handle the container, default: `true`.
    - `TRAEFIK_ENTRYPOINT`: The traefik entrypoint, default: `web`.
    - `TRAEFIK_ENABLE_TLS`: Enable TLS, default: `false`.
    - `TRAEFIK_CERTRESOLVER`: The certresolver, default: `letsencrypt`.
