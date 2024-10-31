# Event Manager Discord Bot

## Make Commands

This project uses `make` to streamline the development process. Below are the available `make` commands you can use:

## Commands
  
- **`make build`**
  - Builds the Docker image for the bot

- **`make run`**
  - Runs the Docker container for the bot

- **`make stop`**
  - Stops running the Docker container for the bot

- **`make logs`**
  - Displays the logs in real-time. Command to run the bot is in detached mode so logs not outputted automatically

- **`make clean`**
  - Removes any temporary files and stops the Docker container if it's running

- **`make restart`**
  - Calls to `stop`, `build` and `run` the bot

## Prerequisites

Before using these commands, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Make](https://www.gnu.org/software/make/)

## Usage

To use any of the commands, open a terminal in the project directory and type:

```bash
make <command>
