# WhatsByAPI

> ⚠️ This project is based on [pywa](https://github.com/david-lev/pywa), created by David Lev.  
> The original project is licensed under the MIT License.  
> All rights and credits for the base work go to the original author.

## Features

- Easy to use Pythonic interface.
- Supports all major features of the WhatsApp Cloud API.
- Includes support for webhooks.
- Optional dependencies for Flask and FastAPI integration.

## Installation

You can install WhatsByAPI from PyPI:

```bash
pip install whatsbyapi
```

## Usage

```python
from whatsbyapi import WhatsApp

# Initialize the client
wa = WhatsApp(api_key='your-api-key')

# Send a message
wa.send_message(phone_number='1234567890', message='Hello, World!')
```

