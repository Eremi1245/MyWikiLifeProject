FROM python:3.11

# Это папка которая будет корневой, когда вы будете входить в контейнер, и в которой будет запускаться скрипт
# ВАЖНО!!! ЛУЧШЕ НЕ НАЗЫВАТЬ ЕГО ТАКЖЕ КАК ВАШУ НЕПОСРЕДСТВЕННУЮ ПАПКУ С КОДОМ!!!
WORKDIR /mywikilifeproject

# первый путь, это путь относительно папки из которой запускается docker-compose 
# или папка из которой запускается dockerfile
# второй путь это путь в папке которую вы указали в WORKDIR , если оставите точку, то скопируется ровно в папку mywikilifeproject
COPY ./backend/requirements.txt .
# команда будет исполняться в папке mywikilifeproject
RUN pip install -r requirements.txt

# копироваться будут файлы относительно папки из которой запускаетет docker-compose или dockerfile
# вторая точка, это куда скопировать в папке mywikilifeproject
COPY ./backend .

CMD ["sh", "-c", "python wait_for_it.py && python -m unittest discover -s tests && uvicorn app:app --host 0.0.0.0 --port 8000 --reload"]

