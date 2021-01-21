FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /src

ENV LD_LIBRARY_PATH=:/lib64/
COPY libnsm.so /lib64/.
