# Google Keep - Alexa Synchronizer

## Motivation

When shopping, we find it more convenient to use Google Keep. However, during our daily routine, we tell Alexa to add items to the shopping list, which means we had to manually review and synchronize each list. This project automates that synchronization to save time and avoid mistakes.

## Features

- Synchronizes items between Google Keep and Alexa's shopping list.
- Supports both synchronous and asynchronous synchronization.
- Asynchronous synchronization uses webhooks to notify the result.
- Lightweight and optimized for ARM-based devices.
- Runs as a Python-based server.

## Installation

### Prerequisites

1. **Hardware**: RK3228 TV box running Armbian (could work also on a Raspberry Pi).
2. **Software**: Ensure Python 3.12 is installed or Docker.
3. **Home Assistant**: Home Assistant with the [madmachinations server add-on](https://github.com/madmachinations/home-assistant-alexa-shopping-list) installed.
4. **Google Keep Master Token**: A master token to access Google Keep (instructions to obtain it can be found [here](https://github.com/simon-weber/gpsoauth#alternative-flow)).
5. **Google Keep Note ID**: The ID of the Google Keep note to be used as the shopping list.
6. **"Alexa" Item in Keep**: An item in the Google Keep list named "Alexa," under which new items synchronized from Alexa will be added.

### Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/gkeep-alexa-synchronizer.git
   cd gkeep-alexa-synchronizer
   ```

2. Run the container:
   ```bash
   make up
   ```

3. Access the service at `http://<device-ip>:5000`.

## Usage

This service acts as a client for the server implementation from [madmachinations/home-assistant-alexa-shopping-list](https://github.com/madmachinations/home-assistant-alexa-shopping-list) to handle Alexa's shopping list API.

### Configuration

- Ensure your Google Keep credentials are properly configured in the environment variables or configuration file.


## Notes

- This project is specifically designed for ARM-based devices like the RK3228 TV box.

