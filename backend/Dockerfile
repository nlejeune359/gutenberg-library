FROM pypy:3.9-bullseye
WORKDIR /gutenbergAPI
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY ./app .
