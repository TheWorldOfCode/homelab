FROM python:3.11-rc-alpine

RUN pip install docker 

COPY auto_local_dns.py /auto_local_dns.py

ENTRYPOINT ["/auto_local_dns.py"]
