# Multi-Agent LLM System

This project implements a multi-agent LLM system where several specialized agents collaborate sequentially to solve problems by analyzing system logs.

## Overview

The system consists of two main components:
1. A log server that provides access to host system logs via SSE (Server-Sent Events)
2. A multi-agent application that chains together different specialized AI agents

## Prerequisites

- Docker and Docker Compose
- Ollama running locally on macOS with the Mistral model
- The system connects to Ollama at `http://host.docker.internal:11434/api/generate` 
(Note that ollama can run on a remote server as well and target it from my machine)


## How It Works

1. The log server container mounts the host's `/var/log/` directory in read-only mode and serves log data over HTTP SSE
2. The agents container runs multiple LLM agents in sequence:
   - Project Manager
   - Solutions Architect
   - Developer
   - DevOps Engineer
3. Each agent receives the output from the previous agent in the chain, along with system log data

## Getting Started

1. Make sure Ollama is running locally with the Mistral model installed
2. Build and run the containers:
`docker-compose up`

3. When prompted, enter your idea or request in the terminal
4. The system will: 
    - Fetch the relevant system logs
    - Process your request through the chain of agents
    - Output each agent's response

Commands step by step:
```
brew services start ollama
docker compose up -d --build
docker compose attach agents
```