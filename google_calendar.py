from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
import datetime
from mcp.server.fastmcp import FastMCP

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Initialize the MCP server
mcp = FastMCP("Google Calendar MCP")

def get_calendar_service():
    """Get the Google Calendar service with proper authentication."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

@mcp.tool()
def list_calendars() -> list:
    """List all calendars the user has access to."""
    service = get_calendar_service()
    calendars = service.calendarList().list().execute()
    return calendars.get('items', [])

@mcp.tool()
def list_events(calendar_id: str = 'primary', max_results: int = 10) -> list:
    """List the next events from the specified calendar."""
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

@mcp.tool()
def create_event(
    calendar_id: str = 'primary',
    summary: str = '',
    description: str = '',
    start_time: str = None,
    end_time: str = None
) -> dict:
    """Create a new event in the specified calendar."""
    service = get_calendar_service()
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
    }
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return event

@mcp.tool()
def delete_event(calendar_id: str = 'primary', event_id: str = '') -> bool:
    """Delete an event from the specified calendar."""
    service = get_calendar_service()
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    return True

@mcp.prompt()
def calendar_prompt(message: str) -> str:
    """Create a prompt for calendar operations."""
    return f"Please help me with my calendar: {message}"

def main():
    print("Starting Google Calendar MCP Server...")
    mcp.run()

if __name__ == "__main__":
    main()
