"""
Slack utilities
"""
import json
from typing import Optional

from pydantic import BaseModel

from backend.config import SETTINGS
from backend.utils.http import BaseApiError, gen_make_request


class SlackApiError(BaseApiError):
    """
    Error when accessing the Slack API
    """


MAKE_REQUEST = gen_make_request("Slack", SlackApiError)
USERS_PROFILE_SET_URI = "https://slack.com/api/users.profile.set"
USERS_PROFILE_GET_URI = "https://slack.com/api/users.profile.get"
TOKEN_EXCHANGE_URI = "https://slack.com/api/oauth.access"


class TokenExchangeData(BaseModel):
    """
    Data returned by Slack after exchanging tokens
    """

    ok: bool
    access_token: str
    scope: str
    user_id: str
    team_id: str
    team_name: str


async def get_new_access_token(code: str) -> TokenExchangeData:
    """
    Exchange a code for a new access token
    """
    exchange_args = {
        "client_id": SETTINGS.slack_client_id,
        "client_secret": SETTINGS.slack_client_secret,
        "code": code,
        "redirect_uri": SETTINGS.slack_redirect_uri,
    }
    return await MAKE_REQUEST(
        "POST", TOKEN_EXCHANGE_URI, TokenExchangeData, data=exchange_args,
    )


class UserProfileArgs(BaseModel):
    """
    Options when updating a Slack user profile
    """

    status_text: str
    status_emoji: str
    status_expiration: Optional[int] = 0


class UserProfileData(BaseModel):
    """
    Data returned by Slack after updating a profile
    """

    ok: bool
    error: Optional[str]

async def get_status(access_token: str) -> UserProfileData:
    """
    Get the user's status
    """
    return await MAKE_REQUEST(
        "GET",
        UserProfileData,
        USERS_PROFILE_GET_URI,
        access_token=access_token
    )



async def set_status(
    user_profile_args: UserProfileArgs, access_token: str
) -> UserProfileData:
    """
    Set the user's status
    """
    return await MAKE_REQUEST(
        "POST",
        USERS_PROFILE_SET_URI,
        UserProfileData,
        access_token=access_token,
        data={
            "profile": json.dumps(user_profile_args.dict()).encode("UTF-8"),
        },
    )
