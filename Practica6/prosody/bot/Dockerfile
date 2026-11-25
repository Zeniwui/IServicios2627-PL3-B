FROM python:3.7
RUN pip install wheel slixmpp==1.8.6

RUN mkdir /bot
COPY bot.py ingserv3b.crt /bot/
WORKDIR /bot

ENV SERVIDOR_XMPP=prosody
ENV CERT_FILE=/bot/ingserv3b.crt

CMD ["python", "-u", "bot.py"]