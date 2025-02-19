# src/__init__.py

from .notion_client import fetch_notion_data
from .mattermost_client import send_mattermost_message
from .scheduler import check_and_notify