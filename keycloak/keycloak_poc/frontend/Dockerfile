# Use Node.js as base image
FROM node:20

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install dependencies
RUN npm install

# Build the app
RUN npm run build

# Expose the port
EXPOSE 3000

# Serve the app
CMD ["npm", "run", "preview"]
