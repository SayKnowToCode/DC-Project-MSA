# Use Node.js base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy rest of the source code
COPY . .

# Expose the app port
EXPOSE 3500

# Start the app
CMD ["node", "producer.js"]
