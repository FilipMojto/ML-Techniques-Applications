# Base image with Node.js
FROM node:lts-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project to the working directory
COPY . .

# Build the project
RUN npm run build

# Expose the port your app will run on (for example, Next.js uses 3000 by default)
EXPOSE 3000

# Start the app every time the container is restarted
CMD ["sh", "-c", "npm run start"]