# CScrub - Scraper for Vote-Record Database
Please note: This project is currently being refactored. All features are not yet operational in this build.

## Summary
Extracts council members, legistlation, meetings, and votes from the Chicago City Clerk's website. Saves to a PostgreSQL database to power the [CScrub API](https://github.com/willoughbylabs/cscrub-api). 

## What For
To convert that:
![City Clerk website](/img/chi_clerk.png)
Into this:
![PostgreSQL database with City Clerk data](/img/psql.png)

City Council vote data is publicly available on the [City Clerk's website](https://chicago.legistar.com/Calendar.aspx), but formulating an overview of a council member's voting record is difficult. Additionally, this information is not yet available on the [Open Data Portal](https://data.cityofchicago.org/).


## Installation
You could build this bot from source to build your own database, or access the information through [an upcoming API](https://github.com/willoughbylabs/cscrub-api).

To build from source, see install.md.

## Caveats
- Currently only fetches page 1 of meetings from City Clerk calendar.
- Currently only fetches first 200 legislation for each meeting.
- Table relationships are not yet defined.
- Potentially time intensive: 50 votes * 200+ legislation per meeting * 100 meetings = (~45K legislation, ~2.5M votes).

## Resources
A shoutout to these folks for the assists. [resources.md](/docs/resources.md)
