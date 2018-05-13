# backend-TheatreShare

This repository contains the code for the backend of the TheatreShare webapp written with Django. 
Used in conjuction with [frontend-TheatreShare](https://github.com/enochtangg/frontend-TheatreShare), 
this web-application allows users to create "auditorium" rooms to watch videos and chat with friends in real time.

## How did I make this?
By utilizing `websockets`, we can establish a two way communication between the server and the client which
allows for real-time messages to be broadcasted across each theatre room. With the help of `django-channels`, the database
can push new information to a `redis queue` which allows the Vue instance to observe and broadcast new information 
to the user. The frontend was made using VueJS and styled with Vue Material. The library `vue-axious` came in handy when making http requests for authentication, creating theatres, and etc. In terms of sending and receive messages from the websocket, I decided to use `VueSocketio` rather than socket.io because it integrated nicely with Vue. One challenged I
faced was being able to dynamically alter vue components according to the socket responses. However, by finishing this project, I think I understand the archecture of VueJS and Django a lot more now. Try the webapp for yourself!

## Getting started

### Clone this project

```bash
git clone https://github.com/enochtangg/backend-TheatreShare.git
cd backend-TheatreShare;
```

### Install the dependencies

```bash
virtualenv venv;
cmd/install;
```

### Run the redis server

```bash
cmd/runredis;
```

### Run the server

```bash
cmd/runserver;
```

Configure frontend-TheatreShare as well and start watching videos/chatting with friends!
