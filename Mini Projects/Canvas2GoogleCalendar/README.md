# Canvas Calendar to Google Calendar
## Why Canvas Calendar to Google Calendar?
- We are lazy people!! We don't want to manually type in all schedules and due dates by hand!!
- Google Calendar is FREE!!!
## Usage
- Copy & paste your ics url into `cal_address.txt` or just replace line 17 with your string url
- Run `main.py`
- import `optimized_calendar.ics` to a calendar of your choice (only tested on Google Calendar)
## Features
### Remove all redundant canvas events:
- We don't like Office Hours bunch up in our Calendar!

### Optimized event names:
Note: Examples below are real courses.
- #### Before (Very unorganized):
  - CL3 [COGS18_SP20_B00]
  - AWP 4B - 000 - Analytical Writing B - Lastname [SP20] [AWP4B_SP20_000
 ]
  - Conference Attendance (Week of Jan 0-Jan 32) [AWP4B_SP20_000]
  - MAE 3 - Lab Section A00\\, Firstname Lastname (Tue 00:00 am) [MAE3_SP20_
 A00]
  - Discussion Section B00 [MATH20D_SP20_B00]
- #### After (Organized):
  - COGS 18 (A) CL3    ` // (A) stands for Assignment`
  - AWP 4B Lecture
  - AWP 4B (A) Conference Attendance 
  - MAE 3 Lab
  - MATH 20D Discussion

#### Assignments will be notified 1 day before due date, lectures, labs, and discussions will be notified 5 mins before starting.
#### All events before today will get trimmed off.
