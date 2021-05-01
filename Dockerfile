FROM python:3.7

EXPOSE 8501

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ ./src
COPY streamlit-config.toml /root/.streamlit/config.toml

CMD streamlit run ./src/generator.py