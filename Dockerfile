FROM python:3.10

ARG COMMIT_ID
ENV COMMIT_ID=${COMMIT_ID}

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install pyinstaller

RUN pyinstaller --onefile base_code/puffpad.py

CMD ["./dist/puffpad"]
