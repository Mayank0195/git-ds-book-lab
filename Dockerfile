FROM python:3.13-slim
RUN useradd --create-home --uid 10001 app
WORKDIR /app
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt
COPY src/ src/
COPY models/model.joblib models/model.joblib
ENV PYTHONPATH=/app/src
USER app
EXPOSE 8000
CMD ["uvicorn", "churn.api:app", "--host", "0.0.0.0", "--port", "8000"]
