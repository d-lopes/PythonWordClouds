FROM python:3.7

# for local development
EXPOSE 8501

# defined so that heroku can provide its config from outside
ENV PORT=8501

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ ./src
COPY streamlit-config.toml /root/.streamlit/config.toml

CMD streamlit run ./src/generator.py