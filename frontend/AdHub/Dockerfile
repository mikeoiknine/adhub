# base image
FROM node:12-alpine

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# add app
COPY . /app

RUN npm install -g @angular/cli@8.3.14
RUN npm install

EXPOSE 4200

# start app
CMD ng serve --host 0.0.0.0 --disable-host-check