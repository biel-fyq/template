FROM bieldatalab/py-db-drivers:python3.11

WORKDIR /app

COPY . /app

RUN --mount=type=cache,target=/root/.cache/pip,from=pip_cache pip install -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]