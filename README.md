# WhatsByAPI

WhatsByAPI is a Python wrapper for the WhatsApp Cloud API with Webhook support.

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


---
Developed with ❤️ by Abdelhak Zaaim

[![Follow on GitHub](https://img.shields.io/github/followers/aabdelhak-zaaim?label=Follow&style=social)](https://github.com/abdelhak-zaaim)
