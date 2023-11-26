"""
This script is used to read emails from gmail.
"""

import os.path
import sys

from dotenv import load_dotenv

from gmail_api import convert_messages_to_dict
from gmail_api import fetch_email
from gmail_api import fetch_emails
from gmail_auth import build_api_service
from string_helpers import list_to_plain_text

load_dotenv()


FETCH_MAIL_COUNT = 1
OUTPUT_FILE = os.path.join("generated_output", "{}_messages.txt")


def save_messages(emails, file):
    """Save the provided list of emails to generated_output/messages.txt in JSON format."""
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "w", encoding="utf-8") as outfile:
        # convert to plain text and save
        text = list_to_plain_text(emails)
        outfile.write(text + "\n\n")


def main():
    """
    Main logic.
    """
    service = build_api_service()

    counter = 1
    for page_of_emails in fetch_emails(
        service, fetch_size=500, total_fetch=68500
    ):
        emails = convert_messages_to_dict(page_of_emails, service)
        save_messages(emails, OUTPUT_FILE.format(counter))
        counter += 1


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
