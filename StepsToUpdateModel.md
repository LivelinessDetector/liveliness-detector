# If you update the model

# Build the Docker Container:
docker build -t liveliness-detector .

# Run the Docker Container:
docker run -p 8000:8000 liveliness-detector

# Distribute the Docker image:
docker push livelinessdetector/liveliness-detector:latest

