# KMA Schedule Parser

**Language:** [🇺🇸 English](README.md) | [🇻🇳 Tiếng Việt](README_vi.md)

A Python tool to parse school schedules from KMA (Học viện Kỹ thuật Mật mã) HTML format and convert them to Google Calendar-compatible ICS format.

## Features

- Parses HTML schedule files from KMA student portal
- Converts complex Vietnamese schedule format to ICS calendar format
- Handles multiple time periods and date ranges
- Supports both lecture (LT) and practice (TH) sessions
- Includes course details, instructors, and locations
- Proper timezone handling for Vietnam (Asia/Ho_Chi_Minh)

## Requirements

- Python 3.9+
- beautifulsoup4
- icalendar

## Installation

Since the project includes a `pyproject.toml` file with all dependencies listed, installation is simple:

### Using pip (recommended)
```bash
pip install .
```

### Using uv (faster alternative)
If you have [uv](https://github.com/astral-sh/uv) installed:
```bash
uv pip install .
```

### Manual dependency installation
If you prefer to install dependencies manually:
```bash
pip install beautifulsoup4 icalendar
```

Or with uv:
```bash
uv pip install beautifulsoup4 icalendar
```

## Usage

### Step 1: Get your schedule HTML from KMA Portal

1. **Access the KMA student portal**:
   - Go to: http://qldt.actvn.edu.vn/CMCSoft.IU.Web.Info/Reports/Form/StudentTimeTable.aspx
   - Log in with your student credentials

2. **Navigate to your schedule**:
   - The page should show "Xem kết quả ĐKH" (View Registration Results)
   - Make sure your semester and term are selected correctly
   - Your schedule table should be visible on the page

3. **Get the HTML source code**:
   - Press `Ctrl + U` (or `Cmd + U` on Mac) to view the page source
   - This will open a new tab/window with the raw HTML code
   - Press `Ctrl + A` (or `Cmd + A` on Mac) to select all the HTML content
   - Press `Ctrl + C` (or `Cmd + C` on Mac) to copy the HTML

4. **Save to a file**:
   - Create a new text file (e.g., `my_schedule.html`)
   - Paste the copied HTML content into the file
   - Save the file with `.html` or `.txt` extension

> **📝 Important Notes:**
> - Make sure you're logged in and can see your actual schedule before getting the source code
> - The portal link: http://qldt.actvn.edu.vn/CMCSoft.IU.Web.Info/Reports/Form/StudentTimeTable.aspx
> - If you get a blank page or login page, make sure to log in first and navigate to your schedule
> - The HTML source should contain table data with your course information
> - If the page shows "no data" or empty schedule, check your semester/term selection

### Step 2: Run the parser
   ```bash
   python main.py -i <input_file> -o <output_file>
   ```
   
   Example:
   ```bash
   python main.py -i my_schedule.html -o my_calendar.ics
   ```

### Step 3: Import to Google Calendar
   - Open Google Calendar
   - Click the "+" next to "Other calendars"
   - Select "Import"
   - Upload the generated ICS file

## Command Line Options

- `-i, --input`: Input HTML file path containing the KMA schedule (required)
- `-o, --output`: Output ICS file path for the generated calendar (required)
- `-h, --help`: Show help message and exit

## Examples

```bash
# Basic usage
python main.py -i schedule.html -o calendar.ics

# Using full paths
python main.py -i /path/to/schedule.html -o /path/to/output/calendar.ics

# Show help
python main.py --help
```

## File Structure

- `main.py` - Main parser script
- `README.md` - English documentation (this file)
- `README_vi.md` - Vietnamese documentation (Tài liệu tiếng Việt)
- `kma_schedule.ics` - Generated calendar file
- `pyproject.toml` - Project dependencies

## How it Works

The parser:

1. **Extracts schedule data** from HTML tables using BeautifulSoup
2. **Parses complex time formats** like "Từ 27/10/2025 đến 16/11/2025: (1) Thứ 2 tiết 1,2,3 (LT)"
3. **Converts Vietnamese day names** (Thứ 2 = Monday, etc.) to standard weekdays
4. **Maps time periods** (tiết 1,2,3) to actual hours (07:00-09:25)
5. **Generates recurring events** for each week in the specified date ranges
6. **Creates ICS format** compatible with Google Calendar and other calendar applications

## Time Slot Mapping

The parser uses standard academic time slots:

- Tiết 1: 07:00-07:45
- Tiết 2: 07:50-08:35
- Tiết 3: 08:40-09:25
- Tiết 4: 09:35-10:20
- Tiết 5: 10:25-11:10
- Tiết 6: 11:15-12:00
- Tiết 7: 13:00-13:45
- Tiết 8: 13:50-14:35
- Tiết 9: 14:40-15:25
- Tiết 10: 15:35-16:20
- Tiết 11: 16:25-17:10
- Tiết 12: 17:15-18:00

## Example Output

The generated ICS file contains events like:

```
BEGIN:VEVENT
SUMMARY:Lập trình hướng đối tượng-1-25 (A21C908)
DTSTART;TZID=Asia/Ho_Chi_Minh:20250811T093500
DTEND;TZID=Asia/Ho_Chi_Minh:20250811T120000
DESCRIPTION:Course: CLC1ATCTKM5\nType: LT\nInstructor: Bùi Thị Như (GVM), Trịnh Anh Tuấn (GVM)\nPeriods: 4, 5, 6
LOCATION:201-TA1 TA1- 8T
UID:CLC1ATCTKM5-2025-08-11-09:35@kma.schedule
END:VEVENT
```

## Customization

To adapt for different schools or formats:

1. Update `day_mapping` for different day names
2. Modify `time_slots` for different time periods
3. Adjust the HTML parsing logic in `parse_html_file()` for different table structures
4. Update regex patterns in `parse_time_info()` for different date/time formats

## Troubleshooting

### Common Issues

1. **"Could not find schedule table in HTML file"**
   - Make sure you copied the HTML from the correct page (after logging in)
   - Verify that your schedule is visible on the web page before copying the source
   - Check that you selected the correct semester and term

2. **"No events generated" or empty calendar**
   - Ensure your HTML file contains the actual schedule data
   - Verify the semester dates are current and not from past terms
   - Check if the course registration is completed

3. **Portal access issues**
   - The KMA portal URL: http://qldt.actvn.edu.vn/CMCSoft.IU.Web.Info/Reports/Form/StudentTimeTable.aspx
   - Make sure you have valid KMA student credentials
   - Try accessing the portal from within the school network if external access is restricted

4. **Encoding issues**
   - Save your HTML file with UTF-8 encoding to preserve Vietnamese characters
   - If you see garbled text, try copying the source again

### Getting Help

If you encounter issues:
1. Check that your HTML file contains table data with course information
2. Verify the file size is reasonable (should be several KB, not just a few bytes)
3. Try the parser with the provided example file first to ensure it works

## License

[LICENSE](LICENSE)
