# Set the base image to use Node.js 16 LTS (Long-Term Support) version
FROM node:16-alpine

# Set the working directory for all following commands
WORKDIR /app

# Copy the package.json and yarn.lock files into the working directory
COPY package.json yarn.lock ./

RUN yarn

# Copy the rest of the application source code into the working directory
COPY . .

# Build the Next.js application
RUN yarn build

# Expose the port that the Next.js application will run on
EXPOSE 3000

# Set the command to start the Next.js application
CMD ["yarn", "start"]
