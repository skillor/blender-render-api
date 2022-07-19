FROM nytimes/blender:latest

WORKDIR /code

COPY . /code

RUN $BLENDERPIP install --no-cache-dir --upgrade -r /code/requirements_api.txt

ENV TMP_DIRECTORY "/tmp/blender-render-api"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]