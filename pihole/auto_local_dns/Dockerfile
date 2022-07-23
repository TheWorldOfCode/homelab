FROM python:3.11-rc-alpine

RUN pip install docker 

COPY auto_local_dns.py /auto_local_dns.py

CMD ["-u", "auto_local_dns.py"]

ENTRYPOINT ["python3"]
