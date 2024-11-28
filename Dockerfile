FROM python:3.10.9

WORKDIR /usr/src

RUN pip install --upgrade pip && \
    pip install python-telegram-bot nest-asyncio spacy pymongo openai && \
    python -m spacy download en_core_web_md

COPY . .

CMD [ "python", "-u", "Telechat.py" ]