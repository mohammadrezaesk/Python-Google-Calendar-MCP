# Google Calendar MCP

A Python-based Google Calendar integration that provides a simple interface to manage your Google Calendar events through a Modular Control Protocol (MCP) server.

## Features

- List all available calendars
- View upcoming events from any calendar
- Create new calendar events
- Delete existing events
- Interactive command-line interface

## Prerequisites

- Python 3.7 or higher
- Google Cloud Platform account with Calendar API enabled
- Google OAuth 2.0 credentials

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Python-Google-Calendar-MCP
```

2. Set up Google Calendar API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials
   - Download the credentials and save them as `credentials.json` in the project root

## Usage

1. Run the application:
```bash
uv run google_calendar.py
```

2. On first run, you'll be prompted to authenticate with your Google account through your web browser.

3. The application will create a `token.pickle` file to store your credentials for future use.

## Available Commands

The MCP server provides the following tools:

- `list_calendars()`: List all calendars you have access to
- `list_events(calendar_id, max_results)`: View upcoming events from a specific calendar
- `create_event(calendar_id, summary, description, start_time, end_time)`: Create a new event
- `delete_event(calendar_id, event_id)`: Delete an existing event

## Security

- Never share your `credentials.json` or `token.pickle` files
- Keep these files secure and out of version control
- The application uses OAuth 2.0 for secure authentication

## Dependencies

- google-auth-oauthlib>=1.0.0
- google-auth-httplib2>=0.1.0
- google-api-python-client>=2.0.0

