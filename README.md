# Offline Voting System

<!-- Code created by https://linktr.ee/saran709 -->

A simple, secure offline voting system built with Python and SQLite.

## Features

- **Offline Operation**: No internet connection required
- **SQLite Database**: Reliable local data storage
- **User Authentication**: Secure voter identification
- **Admin Panel**: Manage candidates and view results
- **Vote Validation**: Prevents duplicate voting
- **GUI Interface**: User-friendly tkinter interface

## System Requirements

- Python 3.7 or higher
- All required libraries are built into Python (sqlite3, tkinter, datetime, hashlib)

## Installation

1. Clone or download this project
2. Run the main application:
   ```
   python main.py
   ```

## Usage

### For Voters
1. Launch the application
2. Enter your voter ID
3. Select your preferred candidate
4. Submit your vote

### For Administrators
1. Use the admin panel to:
   - Add/remove candidates
   - View real-time results
   - Manage voter registration
   - Generate reports

## Database Structure

- **voters**: Stores voter information and authentication
- **candidates**: Stores candidate details
- **votes**: Records all cast votes with timestamps

## Security Features

- Voter ID validation
- One vote per voter enforcement
- Vote anonymity (votes not linked to voter identity in results)
- Secure hash-based authentication

## File Structure

```
voting_system/
├── main.py              # Main application entry point
├── database_manager.py  # Database operations
├── voting_system.py     # Core voting logic
├── gui.py              # User interface
├── admin_panel.py      # Administration interface
├── voting_database.db  # SQLite database (created automatically)
└── README.md           # This file
```