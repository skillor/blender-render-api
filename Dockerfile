FROM nytimes/blender:latest

RUN apt update && apt install python3 python3-pip -y

WORKDIR /code

COPY . /code

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements_api.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
