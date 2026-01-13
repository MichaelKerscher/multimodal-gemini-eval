from lib.clients import gemini_client
from lib.clients import companygpt_client

CLIENTS = {
    "gemini": gemini_client,
    "506": companygpt_client,
    "companygpt": companygpt_client
}