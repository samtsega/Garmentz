# Use the official Flutter image
FROM cirrusci/flutter:latest

# Set the working directory
WORKDIR /app

# Copy your Flutter project
COPY . .

# Get dependencies
RUN flutter pub get

# Build the app
RUN flutter build web

# Serve the app using a simple HTTP server
CMD ["flutter", "run", "-d", "web-server", "--web-port", "8080", "--web-hostname", "0.0.0.0"]
