#!/usr/bin/env python3
"""
KMA Schedule Parser
Parses school schedule from HTML format and converts it to Google Calendar (ICS) format.
"""

from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import re
from zoneinfo import ZoneInfo
import argparse
import sys

class KMAScheduleParser:
    def __init__(self):
        self.vietnam_tz = ZoneInfo('Asia/Ho_Chi_Minh')
        
        # Vietnamese day mapping
        self.day_mapping = {
            'Thứ 2': 0,  # Monday
            'Thứ 3': 1,  # Tuesday
            'Thứ 4': 2,  # Wednesday
            'Thứ 5': 3,  # Thursday
            'Thứ 6': 4,  # Friday
            'Thứ 7': 5,  # Saturday
            'Chủ nhật': 6  # Sunday
        }
        
        # Time slot mapping (assuming standard academic periods)
        self.time_slots = {
            1: ('07:00', '07:45'),
            2: ('07:50', '08:35'),
            3: ('08:40', '09:25'),
            4: ('09:35', '10:20'),
            5: ('10:25', '11:10'),
            6: ('11:15', '12:00'),
            7: ('13:00', '13:45'),
            8: ('13:50', '14:35'),
            9: ('14:40', '15:25'),
            10: ('15:35', '16:20'),
            11: ('16:25', '17:10'),
            12: ('17:15', '18:00'),
        }

    def parse_html_file(self, file_path):
        """Parse the HTML file and extract schedule data."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the schedule table
        schedule_table = soup.find('table', {'id': 'gridRegistered'})
        if not schedule_table:
            raise ValueError("Could not find schedule table in HTML file")
        
        courses = []
        rows = schedule_table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 4:
                continue
                
            # Skip total row
            if 'Tổng' in cells[1].get_text():
                continue
            
            course_name = cells[1].get_text(strip=True)
            course_code = cells[2].get_text(strip=True)
            time_info = cells[3].decode_contents()  # Get HTML content to preserve formatting
            location = cells[4].get_text(strip=True)
            instructor = cells[5].get_text(strip=True)
            
            # Parse time information
            schedule_periods = self.parse_time_info(time_info)
            
            courses.append({
                'name': course_name,
                'code': course_code,
                'periods': schedule_periods,
                'location': location,
                'instructor': instructor
            })
        
        return courses

    def parse_time_info(self, time_info):
        """Parse the complex time information from the HTML."""
        periods = []
        
        # Clean up HTML and convert to text
        soup_time = BeautifulSoup(time_info, 'html.parser')
        clean_text = soup_time.get_text()
        
        # Replace non-breaking spaces with regular spaces
        clean_text = clean_text.replace('\xa0', ' ').replace('\n', ' ').replace('\t', ' ')
        
        # Split by date ranges
        date_pattern = r'Từ (\d{2}/\d{2}/\d{4}) đến (\d{2}/\d{2}/\d{4}): \((\d+)\)'
        date_matches = re.findall(date_pattern, clean_text)
        
        for start_date_str, end_date_str, period_num in date_matches:
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y').date()
            
            # Find time slots for this period
            period_section = self.extract_period_section(clean_text, period_num)
            time_slots = self.parse_time_slots(period_section)
            
            periods.append({
                'start_date': start_date,
                'end_date': end_date,
                'time_slots': time_slots
            })
        
        return periods

    def extract_period_section(self, clean_text, period_num):
        """Extract the time slots for a specific period."""
        # Find text between current period and next period or end
        pattern = rf'\({period_num}\)(.*?)(?=Từ|\Z)'
        match = re.search(pattern, clean_text, re.DOTALL)
        section = match.group(1) if match else ""
        
        return section

    def parse_time_slots(self, period_section):
        """Parse individual time slots from a period section."""
        time_slots = []
        
        # Pattern to match "Thứ X tiết Y,Z,W (LT/TH)"
        slot_pattern = r'(Thứ \d+) tiết ([\d,]+) \((LT|TH)\)'
        matches = re.findall(slot_pattern, period_section)
        
        for day, periods, class_type in matches:
            period_numbers = [int(p.strip()) for p in periods.split(',')]
            time_slots.append({
                'day': day,
                'periods': period_numbers,
                'type': class_type
            })
        
        return time_slots

    def create_calendar_events(self, courses):
        """Create calendar events from parsed course data."""
        calendar = Calendar()
        calendar.add('prodid', '-//KMA Schedule Parser//mxm.dk//')
        calendar.add('version', '2.0')
        calendar.add('calscale', 'GREGORIAN')
        calendar.add('method', 'PUBLISH')
        calendar['x-wr-caldesc'] = 'Schedule for KMA student'
        calendar['x-wr-calname'] = 'KMA Schedule'
        calendar['x-wr-timezone'] = 'Asia/Ho_Chi_Minh'
        
        for course in courses:
            for period in course['periods']:
                for time_slot in period['time_slots']:
                    events = self.create_events_for_time_slot(
                        course, period, time_slot
                    )
                    for event in events:
                        calendar.add_component(event)
        
        return calendar

    def create_events_for_time_slot(self, course, period, time_slot):
        """Create individual events for a time slot."""
        events = []
        
        # Get day of week
        day_name = time_slot['day']
        if day_name not in self.day_mapping:
            return events
        
        weekday = self.day_mapping[day_name]
        
        # Calculate start and end times for the time slot
        periods = time_slot['periods']
        start_period = min(periods)
        end_period = max(periods)
        
        start_time_str, _ = self.time_slots[start_period]
        _, end_time_str = self.time_slots[end_period]
        
        # Generate events for each occurrence
        current_date = period['start_date']
        end_date = period['end_date']
        
        # Find the first occurrence of the weekday
        days_ahead = weekday - current_date.weekday()
        if days_ahead < 0:  # Target day already happened this week
            days_ahead += 7
        
        first_occurrence = current_date + timedelta(days=days_ahead)
        
        # Create events for each week
        event_date = first_occurrence
        while event_date <= end_date:
            event = self.create_single_event(
                course, time_slot, event_date, start_time_str, end_time_str
            )
            events.append(event)
            event_date += timedelta(days=7)  # Next week
        
        return events

    def create_single_event(self, course, time_slot, event_date, start_time_str, end_time_str):
        """Create a single calendar event."""
        event = Event()
        
        # Parse times
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()
        
        # Create datetime objects
        start_dt = datetime.combine(event_date, start_time)
        end_dt = datetime.combine(event_date, end_time)
        
        # Localize to Vietnam timezone
        start_dt = start_dt.replace(tzinfo=self.vietnam_tz)
        end_dt = end_dt.replace(tzinfo=self.vietnam_tz)
        
        # Set event properties
        event.add('summary', course['name'])
        event.add('dtstart', start_dt)
        event.add('dtend', end_dt)
        event.add('location', course['location'])
        
        # Create description
        description = f"Course: {course['code']}\n"
        description += f"Type: {time_slot['type']}\n"
        description += f"Instructor: {course['instructor']}\n"
        description += f"Periods: {', '.join(map(str, time_slot['periods']))}"
        
        event.add('description', description)
        event.add('uid', f"{course['code']}-{event_date}-{start_time_str}@kma.schedule")
        
        return event

    def convert_to_ics(self, html_file_path, output_file_path):
        """Main method to convert HTML schedule to ICS format."""
        print("Parsing HTML schedule...")
        courses = self.parse_html_file(html_file_path)
        print(f"Found {len(courses)} courses")
        
        print("Creating calendar events...")
        calendar = self.create_calendar_events(courses)
        
        print(f"Writing ICS file to {output_file_path}...")
        with open(output_file_path, 'wb') as f:
            f.write(calendar.to_ical())
        
        print("Conversion completed successfully!")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description='Parse KMA school schedule from HTML format and convert to Google Calendar (ICS) format.'
    )
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input HTML file path containing the KMA schedule'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output ICS file path for the generated calendar'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            pass  # Just check if file can be opened
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Cannot read input file '{args.input}': {e}")
        sys.exit(1)
    
    schedule_parser = KMAScheduleParser()
    
    try:
        schedule_parser.convert_to_ics(args.input, args.output)
        print(f"\nSchedule successfully converted from '{args.input}' to '{args.output}'")
        print("You can now import this file into Google Calendar or any other calendar application.")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()