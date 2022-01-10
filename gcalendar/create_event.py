from datetime import datetime, timedelta
from gcalendar import cal_setup, assistant
import time

def take_event_title():
    assistant.talk("¿Cómo se llama el evento?")
    listen_title = assistant.listen()
    return listen_title


def take_event_desc():
    assistant.talk("¿Cuál es la descripción del evento?")
    listen_desc = assistant.listen()
    return listen_desc

def take_start_date():
    assistant.talk("¿En qué fecha y hora será el evento?")
    listen_date = assistant.listen().replace(' a las ', ' del ')
    listen_date = listen_date.split(' del ')
    new_date = listen_date[2] + '-' + listen_date[1] + '-' + listen_date[0]\
        + ' ' + listen_date[3]
    date_isoformat = datetime.fromisoformat(new_date).isoformat()
    return date_isoformat
  

def take_end_date():
    assistant.talk("¿En qué fecha y hora terminará el evento?")
    listen_date = assistant.listen().replace(' a las ', ' del ')
    listen_date = listen_date.split(' del ')
    new_date = listen_date[2] + '-' + listen_date[1] + '-' + listen_date[0]\
        + ' ' + listen_date[3]
    date_isoformat = datetime.fromisoformat(new_date).isoformat()
    return date_isoformat

def create_event():
   # creates one hour event tomorrow 10 AM IST
    event_title = take_event_title()
    time.sleep(0.5)
    event_desc = take_event_desc()
    time.sleep(0.5)
    start_date = take_start_date()
    end_date = take_end_date()  
    service = cal_setup.get_calendar_service()
    event_result = service.events().insert(calendarId='primary',
        body={
            "summary": event_title,
            "description": event_desc,
            "start": {"dateTime": start_date, "timeZone": 'America/Guayaquil'},
            "end": {"dateTime": end_date, "timeZone": 'America/Guayaquil'},
        }
    ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])

# if __name__ == '__main__':
#    create_event()