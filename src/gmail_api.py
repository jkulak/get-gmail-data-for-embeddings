"""
This module contains functions to fetch emails from Gmail using the Gmail API.
"""

import base64

from string_helpers import clean_up_content


def extract_body_data(part):
    """Recursively extract the body data from an email part."""

    if "data" in part.get("body", {}):
        content = base64.urlsafe_b64decode(part["body"]["data"]).decode(
            "utf-8"
        )

        # We do not trust the mime type, and always clean up the content
        return clean_up_content(content)

    if "parts" in part:
        for subpart in part["parts"]:
            body_data = extract_body_data(subpart)
            if body_data:
                return body_data
    return None


def convert_message_to_dict(message):
    """Convert a Gmail API message to a dictionary containing only the fields we care about."""
    result = {}
    payload = message["payload"]
    headers = payload["headers"]

    subject = next(
        (header["value"] for header in headers if header["name"] == "Subject"),
        None,
    )
    sender = next(
        (header["value"] for header in headers if header["name"] == "From"),
        None,
    )
    to = next(
        (header["value"] for header in headers if header["name"] == "To"),
        None,
    )
    cc = next(
        (header["value"] for header in headers if header["name"] == "Cc"),
        None,
    )
    bcc = next(
        (header["value"] for header in headers if header["name"] == "Bcc"),
        None,
    )
    sent_date = next(
        (header["value"] for header in headers if header["name"] == "Date"),
        None,
    )

    # Extracting email body
    content = extract_body_data(payload)

    # Extracting labels and other metadata
    labels = message.get("labelIds", [])
    other_metadata = {
        "threadId": message.get("threadId"),
        "mimeType": payload.get("mimeType"),  # Include MIME type here
    }

    result = {
        "title": subject,
        "sent_date": sent_date,
        "content": content,
        "from": sender,
        "to": to,
        "cc": cc,
        "bcc": bcc,
        "labels": labels,
        "other_metadata": other_metadata,
    }

    return result


def convert_messages_to_dict(messages, service):
    """
    Convert a list of Gmail API messages to a list of dictionaries containing
    only the fields we care about.
    """
    emails = []
    for message_info in messages:
        msg_id = message_info["id"]
        email_data = fetch_email(service, msg_id)
        email_dict = convert_message_to_dict(email_data)
        emails.append(email_dict)

    return emails


def fetch_email(service, msg_id):
    """Fetch a single email from Gmail API."""
    return service.users().messages().get(userId="me", id=msg_id).execute()


def fetch_emails(service, fetch_size=10, total_fetch=None):
    """Fetch the latest max_results emails and return them as a list of dictionaries."""
    page_token = None
    fetched_so_far = 0

    while True:
        # If we have a total fetch limit, determine the number of messages to fetch this iteration
        if total_fetch is not None:
            remaining_to_fetch = total_fetch - fetched_so_far
            current_fetch_size = min(fetch_size, remaining_to_fetch)
        else:
            current_fetch_size = fetch_size

        # Fetch messages
        if page_token:
            response = (
                service.users()
                .messages()
                .list(
                    userId="me",
                    maxResults=current_fetch_size,
                    pageToken=page_token,
                )
                .execute()
            )
        else:
            response = (
                service.users()
                .messages()
                .list(userId="me", maxResults=current_fetch_size)
                .execute()
            )

        messages = response.get("messages", [])

        if not messages:
            break

        yield messages

        fetched_so_far += len(messages)

        # Check if we've fetched enough messages according to total_fetch
        if total_fetch is not None and fetched_so_far >= total_fetch:
            break

        # Check if there's a next page to fetch from
        page_token = response.get("nextPageToken")
        if not page_token:
            break
