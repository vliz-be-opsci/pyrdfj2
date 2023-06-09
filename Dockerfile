FROM python:3.8-buster

COPY ./ /pyrdfj2
WORKDIR /pyrdfj2

RUN python -m pip install --upgrade pip && \
    pip install poetry && \
    make init

ENTRYPOINT ["pyrdfj2"]
