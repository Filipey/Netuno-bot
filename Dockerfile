FROM python:3

WORKDIR /app

COPY . .

RUN python3 -m pip install -U discord.py python-dotenv youtube-dl PyNaCl

CMD python -u ./Netuno.py