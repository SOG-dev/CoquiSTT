FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y sox ffmpeg git curl && \
    pip install stt==1.5.0 flask

# Download model
RUN mkdir -p /models && \
    curl -L -o /models/model.tflite https://coqui.gateway.scarf.sh/english/coqui/v1.0.0-huge-vocab/model.tflite && \
    curl -L -o /models/scorer.scorer https://coqui.gateway.scarf.sh/english/coqui/v1.0.0-huge-vocab/huge-vocabulary.scorer

# Copy app
COPY . .

EXPOSE 5000

CMD ["python", "server.py"]
