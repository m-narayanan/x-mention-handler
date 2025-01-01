# X Automated Mention Handler

## Overview
This project automates the process of detecting mentions on X (formerly Twitter), taking screenshots of the mentioned user's profile, and replying to the mention with this screenshot. 

## Workflow

1. **Login**: 
   - Logs into X using credentials stored in environment variables.

2. **Fetch Mentions**:
   - Navigates to the mentions page and collects all mentions not from the logged-in user.

3. **Screenshot**:
   - For each mention, navigates to the mentioned user's profile, captures a screenshot, and crops it to exclude sidebar elements.

4. **Reply**:
   - Opens the tweet where the mention occurred, clicks the reply button, selects to attach media, uploads the screenshot, and sends the reply. 

5. **Tracking**:
   - Keeps track of replied tweet IDs to avoid duplicate replies.

6. **Loop**:
   - The process runs in a loop, checking for new mentions every minute.

## Setup

### Prerequisites
- Python 3.x
- Selenium
- WebDriver Manager for Chrome
- Pillow for image processing
- `dotenv` for managing environment variables

### Installation

1. **Install Python packages**:
   pip install selenium webdriver_manager pillow python-dotenv

2. **Environment Variables**:
- Create a `.env` file in the project directory with the following:
  ```
  TWITTER_EMAIL=your_email@example.com
  TWITTER_USERNAME=your_username
  TWITTER_PASSWORD=your_password
  ```

### Running the Script
- Run the script from the command line:
  python main.py

## Notes
- The script uses Chrome in non-headless mode for easier debugging. Comment out `--window-size=1920,1080` for headless mode if needed.
- Be aware of X's automation policies and ensure your usage complies with their terms of service.
- X's interface might change, potentially breaking the XPaths used; thus, periodic updates might be necessary.
- Error handling is implemented, but additional checks might be needed for robustness.

## License
[it's for educational purposes only]

---
