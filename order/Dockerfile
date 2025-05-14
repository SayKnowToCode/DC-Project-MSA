# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if exists) to the working directory
COPY package*.json ./

# Install application dependencies
RUN npm install 

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port your Node.js application listens on (adjust if needed)
EXPOSE 5000

# Define the command to run your application 
CMD [ "node", "src/app.js" ]