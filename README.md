# 📡 P2P Messaging System with STUN Server

This project implements a **Peer-to-Peer (P2P) messaging system** that
allows users to communicate directly through TCP sockets while using a
centralized **STUN-like server** for peer discovery, friendship
management, and message persistence.

The system demonstrates hybrid networking architecture combining
**Client-Server** and **Peer-to-Peer** communication models.

------------------------------------------------------------------------

# 🎯 Project Objectives

The main goals of this project are:

-   Implement real-time P2P communication using TCP sockets
-   Design a centralized STUN-like server for peer discovery
-   Maintain chat history using database storage
-   Provide a CLI-based interactive messaging experience
-   Demonstrate containerized backend deployment using Docker

------------------------------------------------------------------------

# 🧱 System Architecture

    NET_Project/
    │
    ├── stun server/        → Django Backend (STUN Server)
    │
    └── peer/               → P2P Client Application

------------------------------------------------------------------------

## Communication Model

### 🔹 Peer ↔ Peer

-   Direct TCP socket communication
-   Used for real-time messaging
-   Reduces server load
-   Enables low-latency communication

### 🔹 Peer ↔ STUN Server

-   HTTP REST API communication
-   Used for:
    -   Peer discovery
    -   Friendship management
    -   Message storage and retrieval

------------------------------------------------------------------------

# 🟢 Phase 1 --- STUN Server (Django Backend)

The STUN server acts as a centralized directory service.\
It does **NOT relay messages** between peers.

------------------------------------------------------------------------

## 🔧 Technologies Used

-   Python
-   Django
-   SQLite Database
-   REST-style APIs

------------------------------------------------------------------------

## 📂 Backend Project Structure

    stun server/
    ├── conf/              → Django project configuration
    ├── server/            → Main application
    ├── db.sqlite3         → Database
    └── manage.py          → Django management tool

------------------------------------------------------------------------

# 🗄️ Database Design

## Peer Model

Stores network identity of each user.

``` python
class Peer(models.Model):
    username = models.CharField(max_length=50, unique=True)
    ip = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    last_seen = models.DateTimeField(auto_now=True)
```

### Purpose

-   Identifies each user in network
-   Stores connection information
-   Tracks last activity

------------------------------------------------------------------------

## Friendship Model

Stores social connections between peers.

``` python
class Friendship(models.Model):
    owner = models.ForeignKey(Peer)
    friend_username = models.CharField(max_length=50)
```

### Purpose

-   Maintains friend list
-   Enables chat relationship tracking

------------------------------------------------------------------------

## Message Model

Stores chat history between peers.

``` python
class Message(models.Model):
    sender = models.ForeignKey(Peer)
    receiver = models.ForeignKey(Peer)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
```

### Purpose

-   Maintains conversation history
-   Allows offline message retrieval

------------------------------------------------------------------------

# 🔌 STUN Server API Endpoints

## Peer Management

  Endpoint      Method   Description
  ------------- -------- -------------------------------
  `/register`   POST     Register or update peer
  `/peers`      GET      Retrieve all users
  `/peerinfo`   GET      Retrieve peer connection info

------------------------------------------------------------------------

## Friendship Management

  Endpoint           Method
  ------------------ ----------------------
  `/friend/start/`   Create friendship
  `/friend/get/`     Retrieve friend list

------------------------------------------------------------------------

## Message Management

  Endpoint             Method
  -------------------- -----------------------
  `/message/create/`   Save message
  `/message/get/`      Retrieve chat history

------------------------------------------------------------------------

# 💬 Phase 2 --- Peer Application (Client Side)

This is the main messaging application responsible for direct peer
communication.

------------------------------------------------------------------------

## 🔧 Technologies Used

-   Python
-   TCP Socket Programming
-   Multithreading
-   Requests Library
-   CLI Interface

------------------------------------------------------------------------

## 📂 Client Project Structure

    peer/
    ├── main.py          → Main CLI controller
    ├── com_server.py    → STUN Server communication
    └── utils.py         → Helper utilities

------------------------------------------------------------------------

# ⚙️ File Responsibilities

------------------------------------------------------------------------

## main.py

### Core Responsibilities

-   CLI command management
-   TCP server for receiving messages
-   TCP client for sending messages
-   Chat session management
-   Message box handling

------------------------------------------------------------------------

### Important Functions

#### start_server()

-   Opens local socket server
-   Accepts incoming peer connections
-   Starts message receiving threads

#### handle_peer()

-   Handles incoming messages
-   Updates message box
-   Detects disconnection events

#### start_client()

-   Connects to remote peer
-   Sends messages
-   Stores messages in database

------------------------------------------------------------------------

## com_server.py

Handles communication with STUN server using HTTP requests.

### Functions

-   register()
-   get_peers()
-   get_peer_info()
-   friendship()
-   save_message()
-   fetch_messages()

------------------------------------------------------------------------

## utils.py

Provides helper logic:

-   Message box creation
-   Chat history printing
-   UI formatting

------------------------------------------------------------------------

# 💬 Message Box System

Each user maintains:

-   Message history per friend
-   Notification flags for new messages
-   Active chat session tracking

------------------------------------------------------------------------

# 🖥️ CLI Usage Guide

After running the client:

    python main.py

------------------------------------------------------------------------

## Available Commands

### register

Registers a new peer in the STUN server.

User provides: - Username - Listening port

------------------------------------------------------------------------

### login

Authenticates peer and starts local socket server.

Loads: - Friend list - Message history

------------------------------------------------------------------------

### connect

Establishes TCP connection to a peer and starts messaging.

------------------------------------------------------------------------

### show chat

Displays conversation history and activates live chat mode.

------------------------------------------------------------------------

### end chat

Stops live chat session.

------------------------------------------------------------------------

### status

Displays friend list and indicates new message notifications.

------------------------------------------------------------------------

### logout

Stops server and logs user out.

------------------------------------------------------------------------

### exit

Completely exits application.

------------------------------------------------------------------------

# 🔄 Messaging Workflow

1.  User connects to peer via STUN discovery
2.  TCP connection established
3.  Messages sent directly
4.  Messages saved to database
5.  Chat history retrieved when needed

------------------------------------------------------------------------

# 🐳 Phase 3 --- Dockerized Backend

The STUN server can be containerized for deployment in local networks.

------------------------------------------------------------------------

## Dockerfile Overview

``` dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install django

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

------------------------------------------------------------------------

## Build Docker Image

    docker build -t stun-server .

------------------------------------------------------------------------

## Run Container

    docker run -p 8000:8000 stun-server

------------------------------------------------------------------------

# 🚀 Running the Full System

## Step 1 --- Start STUN Server

    cd stun server
    python manage.py runserver

OR using Docker

------------------------------------------------------------------------

## Step 2 --- Start Peer Client

    cd peer
    python main.py

------------------------------------------------------------------------

# 🧪 Error Handling Features

The client handles:

-   Peer disconnections
-   Offline peers
-   Network errors
-   Invalid inputs
-   Socket failures

All errors are displayed via CLI without crashing the application.

------------------------------------------------------------------------

# 📚 Educational Concepts Demonstrated

-   Socket Programming
-   Peer-to-Peer Networking
-   Client-Server Hybrid Architecture
-   REST API Design
-   Multithreading
-   Database Persistence
-   Containerized Deployment

------------------------------------------------------------------------

# 📌 Project Summary

This project demonstrates a scalable and modular P2P messaging
architecture combining real-time communication with centralized service
coordination.

------------------------------------------------------------------------

✍️ Developed as a Computer Networks Course Project
