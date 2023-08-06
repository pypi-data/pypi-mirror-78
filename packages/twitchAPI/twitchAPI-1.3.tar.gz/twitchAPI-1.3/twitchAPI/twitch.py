#  Copyright (c) 2020. Lena "Teekeks" During <info@teawork.de>

import requests
from typing import Union, List, Optional
from .helper import build_url, TWITCH_API_BASE_URL, TWITCH_AUTH_BASE_URL, make_fields_datetime, build_scope, \
    fields_to_enum
from datetime import datetime
from .types import *


class Twitch:
    """
    Twitch API client
    """
    app_id: Optional[str] = None
    app_secret: Optional[str] = None
    __app_auth_token: Optional[str] = None
    __app_auth_scope: List[AuthScope] = []
    __has_app_auth: bool = False

    __user_auth_token: Optional[str] = None
    __user_auth_scope: List[AuthScope] = []
    __has_user_auth: bool = False

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret

    def __generate_header(self, auth_type: 'AuthType', required_scope: List[AuthScope]) -> dict:
        header = {"Client-ID": self.app_id}
        if auth_type == AuthType.APP:
            if not self.__has_app_auth:
                raise UnauthorizedException('Require app authentication!')
            for s in required_scope:
                if s not in self.__app_auth_scope:
                    raise MissingScopeException('Require app auth scope ' + s.name)
            header['Authorization'] = f'Bearer {self.__app_auth_token}'
        elif auth_type == AuthType.USER:
            if not self.__has_user_auth:
                raise UnauthorizedException('require user authentication!')
            for s in required_scope:
                if s not in self.__user_auth_scope:
                    raise MissingScopeException('Require user auth scope ' + s.name)
            header['Authorization'] = f'Bearer {self.__user_auth_token}'
        elif self.__has_user_auth or self.__has_app_auth:
            # if no required, set one anyway to get better rate limits if possible
            header['Authorization'] = \
                f'Bearer {self.__user_auth_token if self.__has_user_auth else self.__app_auth_token}'
        return header

    def __api_post_request(self,
                           url: str,
                           auth_type: 'AuthType',
                           required_scope: List[AuthScope],
                           data: Optional[dict] = None) -> requests.Response:
        """Make POST request with authorization"""
        headers = self.__generate_header(auth_type, required_scope)
        if data is None:
            return requests.post(url, headers=headers)
        else:
            return requests.post(url, headers=headers, json=data)

    def __api_put_request(self,
                          url: str,
                          auth_type: 'AuthType',
                          required_scope: List[AuthScope],
                          data: Optional[dict] = None) -> requests.Response:
        """Make PUT request with authorization"""
        headers = self.__generate_header(auth_type, required_scope)
        if data is None:
            return requests.put(url, headers=headers)
        else:
            return requests.put(url, headers=headers, json=data)

    def __api_patch_request(self,
                            url: str,
                            auth_type: 'AuthType',
                            required_scope: List[AuthScope],
                            data: Optional[dict] = None) -> requests.Response:
        """Make PUT request with authorization"""
        headers = self.__generate_header(auth_type, required_scope)
        if data is None:
            return requests.patch(url, headers=headers)
        else:
            return requests.patch(url, headers=headers, json=data)

    def __api_delete_request(self,
                             url: str,
                             auth_type: 'AuthType',
                             required_scope: List[AuthScope],
                             data: Optional[dict] = None) -> requests.Response:
        """Make PUT request with authorization"""
        headers = self.__generate_header(auth_type, required_scope)
        if data is None:
            return requests.delete(url, headers=headers)
        else:
            return requests.delete(url, headers=headers, json=data)

    def __api_get_request(self, url: str,
                          auth_type: 'AuthType',
                          required_scope: List[AuthScope]) -> requests.Response:
        """Make GET request with authorization"""
        headers = self.__generate_header(auth_type, required_scope)
        return requests.get(url, headers=headers)

    def __generate_app_token(self) -> None:
        params = {
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'grant_type': 'client_credentials',
            'scope': build_scope(self.__app_auth_scope)
        }
        url = build_url(TWITCH_AUTH_BASE_URL + 'oauth2/token', params)
        result = requests.post(url)
        if result.status_code != 200:
            raise Exception(f'Authentication failed with code {result.status_code} ({result.text})')
        try:
            data = result.json()
            self.__app_auth_token = data['access_token']
        except ValueError:
            raise Exception('Authentication response did not have a valid json body')
        except KeyError:
            raise Exception('Authentication response did not contain access_token')

    def authenticate_app(self, scope: List[AuthScope]) -> None:
        """Authenticate with a fresh generated app token

        :param scope: List of `twitchAPI.types.AuthScope` to use
        :return: None
        """
        self.__app_auth_scope = scope
        self.__generate_app_token()
        self.__has_app_auth = True

    def set_user_authentication(self, token: str, scope: List[AuthScope]) -> None:
        """Set a user token to be used.

        :param token: the generated user token
        :param scope: List of `AuthScope` that the given user token has
        :return: None
        """
        self.__user_auth_token = token
        self.__user_auth_scope = scope
        self.__has_user_auth = True

    def get_app_token(self) -> Union[str, None]:
        """Returns the app token that the api uses or None when not authenticated.

        :return: app token
        :rtype: Union[str, None]
        """
        return self.__app_auth_token

    # ======================================================================================================================
    # API calls
    # ======================================================================================================================

    def get_extension_analytics(self,
                                after: Optional[str] = None,
                                extension_id: Optional[str] = None,
                                first: int = 20,
                                ended_at: Optional[datetime] = None,
                                started_at: Optional[datetime] = None,
                                report_type: Optional[AnalyticsReportType] = None) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.ANALYTICS_READ_EXTENSION`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-extension-analytics

        :param after: optional str
        :param extension_id: optional str
        :param first: optional int range 1 to 100
        :param ended_at: optional :class:`datetime`
        :param started_at: optional :class:`datetime`
        :param report_type: optional :class:`~twitchAPI.types.AnalyticsReportType`
        :rtype: dict
        """
        if ended_at is not None or started_at is not None:
            # you have to put in both:
            if ended_at is None or started_at is None:
                raise Exception('you must specify both ended_at and started_at')
            if started_at > ended_at:
                raise Exception('started_at must be before ended_at')
        if first > 100 or first < 1:
            raise Exception('first must be between 1 and 100')
        url_params = {
            'after': after,
            'ended_at': ended_at.isoformat() if ended_at is not None else None,
            'extension_id': extension_id,
            'first': first,
            'started_at': started_at.isoformat() if started_at is not None else None,
            'type': report_type.value if report_type is not None else None
        }
        url = build_url(TWITCH_API_BASE_URL + 'analytics/extensions',
                        url_params,
                        remove_none=True)
        response = self.__api_get_request(url, AuthType.USER, required_scope=[AuthScope.ANALYTICS_READ_EXTENSION])
        data = response.json()
        return make_fields_datetime(data, ['started_at', 'ended_at'])

    def get_game_analytics(self,
                           after: Optional[str] = None,
                           first: int = 20,
                           game_id: Optional[str] = None,
                           ended_at: Optional[datetime] = None,
                           started_at: Optional[datetime] = None,
                           report_type: Optional[AnalyticsReportType] = None) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.ANALYTICS_READ_GAMES`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-game-analytics

        :param after: optional str
        :param first: optional int in range 1 to 100
        :param game_id: optional str
        :param ended_at: optional :class:`~datetime.datetime`
        :param started_at: optional :class:`~datetime.datetime`
        :param report_type: optional :class:`twitchAPI.types.AnalyticsReportType`
        :rtype: dict
        """
        if ended_at is not None or started_at is not None:
            if ended_at is None or started_at is None:
                raise Exception('you must specify both ended_at and started_at')
            if ended_at < started_at:
                raise Exception('ended_at must be after started_at')
        if first > 100 or first < 1:
            raise Exception('first must be between 1 and 100')
        url_params = {
            'after': after,
            'ended_at': ended_at.isoformat() if ended_at is not None else None,
            'first': first,
            'game_id': game_id,
            'started_at': started_at.isoformat() if started_at is not None else None,
            'type': report_type.value if report_type is not None else None
        }
        url = build_url(TWITCH_API_BASE_URL + 'analytics/games',
                        url_params,
                        remove_none=True)
        response = self.__api_get_request(url, AuthType.USER, [AuthScope.ANALYTICS_READ_GAMES])
        data = response.json()
        return make_fields_datetime(data, ['ended_at', 'started_at'])

    def get_bits_leaderboard(self,
                             count: int = 10,
                             period: TimePeriod = TimePeriod.ALL,
                             started_at: Optional[datetime] = None,
                             user_id: Optional[str] = None) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.BITS_READ`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-bits-leaderboard

        :param count: optional int in range 1 to 100
        :param period: optional :class:`~twitchAPI.types.TimePeriod`
        :param started_at: optional :class:`~datetime.datetime`
        :param user_id: optional str
        :rtype: dict
        """
        if count > 100 or count < 1:
            raise Exception('count must be between 1 and 100')
        url_params = {
            'count': count,
            'period': period.value,
            'started_at': started_at.isoformat() if started_at is not None else None,
            'user_id': user_id
        }
        url = build_url(TWITCH_API_BASE_URL + 'bits/leaderboard', url_params, remove_none=True)
        response = self.__api_get_request(url, AuthType.USER, [AuthScope.BITS_READ])
        data = response.json()
        return make_fields_datetime(data, ['ended_at', 'started_at'])

    def get_extension_transactions(self,
                                   extension_id: str,
                                   transaction_id: Optional[str] = None,
                                   after: Optional[str] = None,
                                   first: int = 20) -> dict:
        """Requires App authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-extension-transactions

        :param extension_id: str
        :param transaction_id: optional str
        :param after: optional str
        :param first: optional int in range 1 to 100
        :rtype: dict
        """
        if first > 100 or first < 1:
            raise Exception("first must be between 1 and 100")
        url_param = {
            'extension_id': extension_id,
            'id': transaction_id,
            'after': after,
            first: first
        }
        url = build_url(TWITCH_API_BASE_URL + 'extensions/transactions', url_param, remove_none=True)
        result = self.__api_get_request(url, AuthType.APP, [])
        data = result.json()
        return make_fields_datetime(data, ['timestamp'])

    def create_clip(self,
                    broadcaster_id: str,
                    has_delay: bool = False) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.CLIPS_EDIT`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#create-clip

        :param broadcaster_id: str
        :param has_delay: optional bool
        :rtype: dict
        """
        param = {
            'broadcaster_id': broadcaster_id,
            'has_delay': str(has_delay).lower()
        }
        url = build_url(TWITCH_API_BASE_URL + 'clips', param)
        result = self.__api_post_request(url, AuthType.USER, [AuthScope.CLIPS_EDIT])
        return result.json()

    def get_clips(self,
                  broadcaster_id: str,
                  game_id: str,
                  clip_id: List[str],
                  after: Optional[str] = None,
                  before: Optional[str] = None,
                  ended_at: Optional[datetime] = None,
                  started_at: Optional[datetime] = None) -> dict:
        """Requires no authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-clips

        :param broadcaster_id: str
        :param game_id: str
        :param clip_id: list of str
        :param after: optional str
        :param before: optional str
        :param ended_at: optional :class:`~datetime.datetime`
        :param started_at: optional :class:`~datetime.datetime`
        :rtype: dict
        """
        param = {
            'broadcaster_id': broadcaster_id,
            'game_id': game_id,
            'clip_id': clip_id,
            'after': after,
            'before': before,
            'ended_at': ended_at.isoformat() if ended_at is not None else None,
            'started_at': started_at.isoformat() if started_at is not None else None
        }
        url = build_url(TWITCH_API_BASE_URL + 'clips', param, split_lists=True, remove_none=True)
        result = self.__api_get_request(url, AuthType.NONE, [])
        data = result.json()
        return make_fields_datetime(data, ['created_at'])

    def create_entitlement_grants_upload_url(self,
                                             manifest_id: str) -> dict:
        """Requires App authentication\n
        For detailed documentation, see here:
        https://dev.twitch.tv/docs/api/reference#create-entitlement-grants-upload-url

        :param manifest_id: str
        :rtype: dict
        """
        if len(manifest_id) < 1 or len(manifest_id) > 64:
            raise Exception('manifest_id must be between 1 and 64 characters long!')
        param = {
            'manifest_id': manifest_id,
            'type': 'bulk_drops_grant'
        }
        url = build_url(TWITCH_API_BASE_URL + 'entitlements/upload', param)
        result = self.__api_post_request(url, AuthType.APP, [])
        return result.json()

    def get_code_status(self,
                        code: List[str],
                        user_id: int) -> dict:
        """Requires App authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-code-status

        :param code: list of str, maximum of 20 entries
        :param user_id: int
        :rtype: dict
        """
        if len(code) > 20 or len(code) < 1:
            raise Exception('only between 1 and 20 codes are allowed')
        param = {
            'code': code,
            'user_id': user_id
        }
        url = build_url(TWITCH_API_BASE_URL + 'entitlements/codes', param, split_lists=True)
        result = self.__api_get_request(url, AuthType.APP, [])
        data = result.json()
        return fields_to_enum(data, ['status'], CodeStatus, CodeStatus.UNKNOWN_VALUE)

    def redeem_code(self,
                    code: List[str],
                    user_id: int) -> dict:
        """Requires App authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#redeem-code

        :param code: list of str, maximum of 20 entries
        :param user_id: int
        :rtype: dict
        """
        if len(code) > 20 or len(code) < 1:
            raise Exception('only between 1 and 20 codes are allowed')
        param = {
            'code': code,
            'user_id': user_id
        }
        url = build_url(TWITCH_API_BASE_URL + 'entitlements/code', param, split_lists=True)
        result = self.__api_post_request(url, AuthType.APP, [])
        data = result.json()
        return fields_to_enum(data, ['status'], CodeStatus, CodeStatus.UNKNOWN_VALUE)

    def get_top_games(self,
                      after: Optional[str] = None,
                      before: Optional[str] = None,
                      first: int = 20) -> dict:
        """Requires no authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-top-games

        :param after: optional str
        :param before: optional str
        :param first: optional int in range 1 to 100
        :rtype: dict
        """
        if first < 1 or first > 100:
            raise Exception('first must be between 1 and 100')
        param = {
            'after': after,
            'before': before,
            'first': first
        }
        url = build_url(TWITCH_API_BASE_URL + 'games/top', param, remove_none=True)
        result = self.__api_get_request(url, AuthType.NONE, [])
        return result.json()

    def get_games(self,
                  game_ids: Optional[List[str]] = None,
                  names: Optional[List[str]] = None) -> dict:
        """Requires no authentication.
        In total, only 100 game ids and names can be fetched at once.

        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-games

        :param game_ids: optional list of str
        :param names: optional list of str
        :rtype: dict
        """
        if game_ids is None and names is None:
            raise Exception('at least one of either game_ids and names has to be set')
        if (len(game_ids) if game_ids is not None else 0) + (len(names) if names is not None else 0) > 100:
            raise Exception('in total, only 100 game_ids and names can be passed')
        param = {
            'id': game_ids,
            'name': names
        }
        url = build_url(TWITCH_API_BASE_URL + 'games', param, remove_none=True, split_lists=True)
        result = self.__api_get_request(url, AuthType.NONE, [])
        return result.json()

    def check_automod_status(self,
                             broadcaster_id: str,
                             msg_id: str,
                             msg_text: str,
                             user_id: str) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.MODERATION_READ`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#check-automod-status

        :param broadcaster_id: str
        :param msg_id: str
        :param msg_text: str
        :param user_id: str
        :rtype: dict
        """
        # TODO you can pass multiple sets in the body, account for that
        url_param = {
            'broadcaster_id': broadcaster_id
        }
        url = build_url(TWITCH_API_BASE_URL + 'moderation/enforcements/status', url_param)
        body = {
            'data': [{
                'msg_id': msg_id,
                'msg_text': msg_text,
                'user_id': user_id}
            ]
        }
        result = self.__api_post_request(url, AuthType.USER, [AuthScope.MODERATION_READ], data=body)
        return result.json()

    def get_banned_events(self,
                          broadcaster_id: str,
                          user_id: Optional[str] = None,
                          after: Optional[str] = None,
                          first: int = 20) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.MODERATION_READ`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-banned-events

        :param broadcaster_id: str
        :param user_id: optional str
        :param after: optional str
        :param first: optional int in range 1 to 100
        :rtype: dict
        """
        if first > 100 or first < 1:
            raise Exception('first must be between 1 and 100')
        param = {
            'broadcaster_id': broadcaster_id,
            'user_id': user_id,
            'after': after,
            'first': first
        }
        url = build_url(TWITCH_API_BASE_URL + 'moderation/banned/events', param, remove_none=True)
        result = self.__api_get_request(url, AuthType.USER, [AuthScope.MODERATION_READ])
        data = result.json()
        data = fields_to_enum(data, ['event_type'], ModerationEventType, ModerationEventType.UNKNOWN)
        data = make_fields_datetime(data, ['event_timestamp', 'expires_at'])
        return data

    def get_banned_users(self,
                         broadcaster_id: str,
                         user_id: Optional[str] = None,
                         after: Optional[str] = None,
                         before: Optional[str] = None) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.MODERATION_READ`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-banned-users

        :param broadcaster_id: str
        :param user_id: optional str
        :param after: optional str
        :param before: optional str
        :rtype: dict
        """
        param = {
            'broadcaster_id': broadcaster_id,
            'user_id': user_id,
            'after': after,
            'before': before
        }
        url = build_url(TWITCH_API_BASE_URL + 'moderation/banned', param, remove_none=True)
        result = self.__api_get_request(url, AuthType.USER, [AuthScope.MODERATION_READ])
        return make_fields_datetime(result.json(), ['expires_at'])

    def get_moderators(self,
                       broadcaster_id: str,
                       user_id: Optional[str] = None,
                       after: Optional[str] = None) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.MODERATION_READ`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-moderators

        :param broadcaster_id: str
        :param user_id: optional str
        :param after: optional str
        :rtype: dict
        """
        param = {
            'broadcaster_id': broadcaster_id,
            'user_id': user_id,
            'after': after
        }
        url = build_url(TWITCH_API_BASE_URL + 'moderation/moderators', param, remove_none=True)
        result = self.__api_get_request(url, AuthType.USER, [AuthScope.MODERATION_READ])
        return result.json()

    def get_moderator_events(self,
                             broadcaster_id: str,
                             user_id: Optional[str] = None) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.MODERATION_READ`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-moderator-events

        :param broadcaster_id: str
        :param user_id: optional str
        :rtype: dict
        """
        param = {
            'broadcaster_id': broadcaster_id,
            'user_id': user_id
        }
        url = build_url(TWITCH_API_BASE_URL + 'moderation/moderators/events', param, remove_none=True)
        result = self.__api_get_request(url, AuthType.USER, [AuthScope.MODERATION_READ])
        data = result.json()
        data = fields_to_enum(data, ['event_type'], ModerationEventType, ModerationEventType.UNKNOWN)
        data = make_fields_datetime(data, ['event_timestamp'])
        return data

    def create_stream_marker(self,
                             user_id: str,
                             description: Optional[str] = None) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.USER_EDIT_BROADCAST`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#create-stream-marker

        :param user_id: str
        :param description: optional str with max length of 140
        :rtype: dict
        """
        if description is not None and len(description) > 140:
            raise Exception('max length for description is 140')
        url = build_url(TWITCH_API_BASE_URL + 'streams/markers', {})
        body = {'user_id': user_id}
        if description is not None:
            body['description'] = description
        result = self.__api_post_request(url, AuthType.USER, [AuthScope.USER_EDIT_BROADCAST], data=body)
        data = result.json()
        return make_fields_datetime(data, ['created_at'])

    def get_streams(self,
                    after: Optional[str] = None,
                    before: Optional[str] = None,
                    first: int = 20,
                    game_id: Optional[str] = None,
                    language: Optional[List[str]] = None,
                    user_id: Optional[List[str]] = None,
                    user_login: Optional[List[str]] = None) -> dict:
        """Requires no authentication.\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-streams

        :param after: optional str
        :param before: optional str
        :param first: optional int in range 1 to 100
        :param game_id: optional str
        :param language: optional list of str with max length of 100
        :param user_id: optional list of str with max length of 100
        :param user_login: optional list of str with max length of 100
        :rtype: dict
        """
        if user_id is not None and len(user_id) > 100:
            raise Exception('a maximum of 100 user_ids are allowed')
        if user_login is not None and len(user_login) > 100:
            raise Exception('a maximum of 100 user_logins are allowed')
        if first > 100 or first < 1:
            raise Exception('first must be between 1 and 100')
        param = {
            'after': after,
            'before': before,
            'first': first,
            'game_id': game_id,
            'language': language,
            'user_id': user_id,
            'user_login': user_login
        }
        url = build_url(TWITCH_API_BASE_URL + 'streams', param, remove_none=True, split_lists=True)
        result = self.__api_get_request(url, AuthType.NONE, [])
        data = result.json()
        return make_fields_datetime(data, ['started_at'])

    def get_stream_markers(self,
                           user_id: str,
                           video_id: str,
                           after: Optional[str] = None,
                           before: Optional[str] = None,
                           first: int = 20) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.USER_READ_BROADCAST`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-stream-markers

        :param user_id: str
        :param video_id: str
        :param after: optional str
        :param before: optional str
        :param first: optional int in range 1 to 100
        :rtype: dict
        """
        if first > 100 or first < 1:
            raise Exception('first must be between 1 and 100')
        param = {
            'user_id': user_id,
            'video_id': video_id,
            'after': after,
            'before': before,
            'first': first
        }
        url = build_url(TWITCH_API_BASE_URL + 'streams/markers', param, remove_none=True)
        result = self.__api_get_request(url, AuthType.USER, [AuthScope.USER_READ_BROADCAST])
        return make_fields_datetime(result.json(), ['created_at'])

    def get_streams_metadata(self,
                             after: Optional[str] = None,
                             before: Optional[str] = None,
                             first: int = 20,
                             game_id: Optional[List[str]] = None,
                             language: Optional[List[str]] = None,
                             user_id: Optional[List[str]] = None,
                             user_login: Optional[List[str]] = None) -> dict:
        """Requires no authentication.\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-streams-metadata

        :param after: optional str
        :param before: optional str
        :param first: optional int in range between 1 and 100
        :param game_id: optional list of str with maximum 100 entries
        :param language: optional list of str with maximum 100 entries
        :param user_id: optional list of str with maximum 100 entries
        :param user_login: optional list str with maximum 100 entries
        :rtype: dict
        """
        if first < 1 or first > 100:
            raise Exception('first must be between 1 and 100')
        if game_id is not None and len(game_id) > 100:
            raise Exception('game_id can have a maximum of 100 entries')
        if language is not None and len(language) > 100:
            raise Exception('language can have a maximum of 100 entries')
        if user_id is not None and len(user_id) > 100:
            raise Exception('user_id can have a maximum of 100 entries')
        if user_login is not None and len(user_login) > 100:
            raise Exception('user_login can have a maximum of 100 entries')
        param = {
            'after': after,
            'before': before,
            'first': first,
            'game_id': game_id,
            'language': language,
            'user_id': user_id,
            'user_login': user_login
        }
        url = build_url(TWITCH_API_BASE_URL + 'streams/metadata', param, remove_none=True, split_lists=True)
        result = self.__api_get_request(url, AuthType.NONE, [])
        return result.json()

    def get_broadcaster_subscriptions(self,
                                      broadcaster_id: str,
                                      user_ids: Optional[List[str]] = None) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.CHANNEL_READ_SUBSCRIPTIONS`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-broadcaster-subscriptions

        :param broadcaster_id: str
        :param user_ids: optional list of str with maximum 100 entries
        :rtype: dict
        """
        if user_ids is not None and len(user_ids) > 100:
            raise Exception('user_ids can have a maximum of 100 entries')
        param = {
            'broadcaster_id': broadcaster_id,
            'user_id': user_ids
        }
        url = build_url(TWITCH_API_BASE_URL + 'subscriptions', param, remove_none=True, split_lists=True)
        result = self.__api_get_request(url, AuthType.USER, [AuthScope.CHANNEL_READ_SUBSCRIPTIONS])
        return result.json()

    def get_all_stream_tags(self,
                            after: Optional[str] = None,
                            first: int = 20,
                            tag_ids: Optional[List[str]] = None) -> dict:
        """Requires App authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-all-stream-tags

        :param after: optional str
        :param first: optional int in range 1 to 100
        :param tag_ids: optional list str with maximum 100 entries
        :rtype: dict
        """
        if first < 1 or first > 100:
            raise Exception('first must be between 1 and 100')
        if tag_ids is not None and len(tag_ids) > 100:
            raise Exception('tag_ids can not have more than 100 entries')
        param = {
            'after': after,
            'first': first,
            'tag_id': tag_ids
        }
        url = build_url(TWITCH_API_BASE_URL + 'tags/streams', param, remove_none=True, split_lists=True)
        result = self.__api_get_request(url, AuthType.APP, [])
        return result.json()

    def get_stream_tags(self,
                        broadcaster_id: str) -> dict:
        """Requires App authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-stream-tags

        :param broadcaster_id: str, id of streamer
        :rtype: dict
        """
        url = build_url(TWITCH_API_BASE_URL + 'streams/tags', {'broadcaster_id': broadcaster_id})
        result = self.__api_get_request(url, AuthType.APP, [])
        return result.json()

    def replace_stream_tags(self,
                            broadcaster_id: str,
                            tag_ids: List[str]) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.USER_EDIT_BROADCAST`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#replace-stream-tags

        :param broadcaster_id: str, id of streamer
        :param tag_ids: list of str, tag ids to be set
        :return: empty dict
        :rtype: dict
        """
        if len(tag_ids) > 100:
            raise Exception('tag_ids can not have more than 100 entries')
        url = build_url(TWITCH_API_BASE_URL + 'streams/tags', {'broadcaster_id': broadcaster_id})
        self.__api_put_request(url, AuthType.USER, [AuthScope.USER_EDIT_BROADCAST], data={'tag_ids': tag_ids})
        # this returns nothing
        return {}

    def get_users(self,
                  user_ids: Optional[List[str]] = None,
                  logins: Optional[List[str]] = None) -> dict:
        """Requires no authentication.\n
        You have to either provide user_ids or logins or both. The maximum combined entries should not exceed 100.

        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-users

        :param user_ids: optional list of str
        :param logins: optional list of str
        :rtype: dict
        """
        if user_ids is None and logins is None:
            raise Exception('please either specify user_ids or logins')
        if (len(user_ids) if user_ids is not None else 0) + (len(logins) if logins is not None else 0) > 100:
            raise Exception('the total number of entries in user_ids and logins can not be more than 100')
        url_params = {
            'id': user_ids,
            'login': logins
        }
        url = build_url(TWITCH_API_BASE_URL + 'users', url_params, remove_none=True, split_lists=True)
        response = self.__api_get_request(url, AuthType.NONE, [])
        return response.json()

    def get_users_follows(self,
                          after: Optional[str] = None,
                          first: int = 20,
                          from_id: Optional[str] = None,
                          to_id: Optional[str] = None) -> dict:
        """Requires no authentication.\n
        You have to use at least one of the following fields: from_id, to_id
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-users-follows

        :param after: optional str
        :param first: optional int between 1 and 100
        :param from_id: optional str
        :param to_id: optional str
        :rtype: dict
        """
        if first > 100 or first < 1:
            raise Exception('first must be between 1 and 100')
        if from_id is None and to_id is None:
            raise Exception('at least one of from_id and to_id needs to be set')
        param = {
            'after': after,
            'first': first,
            'from_id': from_id,
            'to_id': to_id
        }
        url = build_url(TWITCH_API_BASE_URL + 'users/follows', param, remove_none=True)
        result = self.__api_get_request(url, AuthType.NONE, [])
        return make_fields_datetime(result.json(), ['followed_at'])

    def update_user(self,
                    description: str) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.USER_EDIT`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#update-user

        :param description: str
        :rtype: dict
        """
        url = build_url(TWITCH_API_BASE_URL + 'users', {'description': description})
        result = self.__api_put_request(url, AuthType.USER, [AuthScope.USER_EDIT])
        return result.json()

    def get_user_extensions(self) -> dict:
        """Requires User authentication with scope :class:`~AuthScope.USER_READ_BROADCAST`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-user-extensions
        :rtype: dict
        """
        url = build_url(TWITCH_API_BASE_URL + 'users/extensions/list', {})
        result = self.__api_get_request(url, AuthType.USER, [AuthScope.USER_READ_BROADCAST])
        return result.json()

    def get_user_active_extensions(self,
                                   user_id: Optional[str] = None) -> dict:
        """Requires no authentication.\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-user-active-extensions

        :param user_id: optional str
        :rtype: dict
        """
        url = build_url(TWITCH_API_BASE_URL + 'users/extensions', {'user_id': user_id}, remove_none=True)
        result = self.__api_get_request(url, AuthType.NONE, [])
        return result.json()

    def update_user_extensions(self) -> dict:
        """"Requires User authentication with scope :class:`~AuthScope.USER_EDIT_BROADCAST`\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#update-user-extensions

        :rtype: dict
        """
        url = build_url(TWITCH_API_BASE_URL + 'users/extensions', {})
        result = self.__api_put_request(url, AuthType.USER, [AuthScope.USER_EDIT_BROADCAST])
        return result.json()

    def get_videos(self,
                   ids: Optional[List[str]] = None,
                   user_id: Optional[str] = None,
                   game_id: Optional[str] = None,
                   after: Optional[str] = None,
                   before: Optional[str] = None,
                   first: int = 20,
                   language: Optional[str] = None,
                   period: TimePeriod = TimePeriod.ALL,
                   sort: SortMethod = SortMethod.TIME,
                   video_type: VideoType = VideoType.ALL) -> dict:
        """Requires no authentication.\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-videos

        :param ids: optional list of str
        :param user_id: optional str
        :param game_id: optional str
        :param after: optional str
        :param before: optional str
        :param first: optional int in range 1 to 100
        :param language: optional str
        :param period: optional :class:`~twitchAPI.types.TimePeriod`
        :param sort: optional :class:`~twitchAPI.types.SortMethod`
        :param video_type: optional :class:`~twitchAPI.types.VideoType`
        :rtype: dict
        """
        if ids is None and user_id is None and game_id is None:
            raise Exception('you must use either ids, user_id or game_id')
        if first < 1 or first > 100:
            raise Exception('first must be between 1 and 100')
        param = {
            'id': ids,
            'user_id': user_id,
            'game_id': game_id,
            'after': after,
            'before': before,
            'first': first,
            'language': language,
            'period': period.value,
            'sort': sort.value,
            'type': video_type.value
        }
        url = build_url(TWITCH_API_BASE_URL + 'videos', param, remove_none=True, split_lists=True)
        result = self.__api_get_request(url, AuthType.NONE, [])
        data = result.json()
        data = make_fields_datetime(data, ['created_at', 'published_at'])
        data = fields_to_enum(data, ['type'], VideoType, VideoType.UNKNOWN)
        return data

    def get_webhook_subscriptions(self,
                                  first: Optional[str] = None,
                                  after: Optional[str] = None) -> dict:
        """Requires App authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-webhook-subscriptions

        :param first: optional str
        :param after: optional str
        :rtype: dict
        """
        url = build_url(TWITCH_API_BASE_URL + 'webhooks/subscriptions',
                        {'first': first, 'after': after},
                        remove_none=True)
        response = self.__api_get_request(url, AuthType.APP, [])
        return response.json()

    def get_channel_information(self,
                                broadcaster_id: str) -> dict:
        """Requires App or user authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-channel-information

        :param broadcaster_id: str
        :rtype dict
        """
        url = build_url(TWITCH_API_BASE_URL + 'channels', {'broadcaster_id': broadcaster_id})
        response = self.__api_get_request(url, AuthType.APP, [])
        return response.json()

    def modify_channel_information(self,
                                   broadcaster_id: str,
                                   game_id: Optional[str] = None,
                                   broadcaster_language: Optional[str] = None,
                                   title: Optional[str] = None) -> bool:
        """Requires User authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#modify-channel-information

        :param broadcaster_id: str
        :param game_id: optional str
        :param broadcaster_language: optional str
        :param title: optional str
        :rtype: bool
        """
        if game_id is None and broadcaster_language is None and title is None:
            raise Exception('You need to specify at least one of the optional parameter')
        url = build_url(TWITCH_API_BASE_URL + 'channels',
                        {'broadcaster_id': broadcaster_id,
                         'game_id': game_id,
                         'broadcaster_language': broadcaster_language,
                         'title': title}, remove_none=True)
        response = self.__api_patch_request(url, AuthType.USER, [AuthScope.USER_EDIT_BROADCAST])
        return response.status_code == 204

    def search_channels(self,
                        query: str,
                        first: Optional[int] = None,
                        after: Optional[str] = None,
                        live_only: Optional[bool] = False) -> dict:
        """Requires App or User authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#search-channels

        :param query: str, does NOT need to be URI encoded
        :param first: optional int
        :param after: optional str
        :param live_only: optional bool, default false
        :rtype: dict
        """
        if first < 1 or first > 100:
            raise Exception('first must be between 1 and 100')
        url = build_url(TWITCH_API_BASE_URL + 'search/channels',
                        {'query': query,
                         'first': first,
                         'after': after,
                         'live_only': live_only}, remove_none=True)
        response = self.__api_get_request(url, AuthType.APP, [])
        return make_fields_datetime(response.json(), ['started_at'])

    def search_categories(self,
                          query: str,
                          first: Optional[int] = None,
                          after: Optional[str] = None) -> dict:
        """Requires App or User authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#search-categories

        :param query: str, does NOT need to be URI encoded
        :param first: optional int
        :param after: optional str
        :rtype: dict
        """
        if first < 1 or first > 100:
            raise Exception('first must be between 1 and 100')
        url = build_url(TWITCH_API_BASE_URL + 'search/categories',
                        {'query': query,
                         'first': first,
                         'after': after}, remove_none=True)
        response = self.__api_get_request(url, AuthType.APP, [])
        return response.json()

    def get_stream_key(self,
                       broadcaster_id: str) -> dict:
        """Requires User authentication with AuthScope.CHANNEL_READ_STREAM_KEY\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-stream-key

        :param broadcaster_id: str
        :rtype: dict
        """
        url = build_url(TWITCH_API_BASE_URL + 'streams/key', {'broadcaster_id': broadcaster_id})
        response = self.__api_get_request(url, AuthType.USER, [AuthScope.CHANNEL_READ_STREAM_KEY])
        return response.json()

    def start_commercial(self,
                         broadcaster_id: str,
                         length: int) -> dict:
        """Requires User authentication with AuthScope.CHANNEL_EDIT_COMMERCIAL\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#start-commercial

        :param broadcaster_id: str
        :param length: int, one of these: [30, 60, 90, 120, 150, 180]
        :rtype: dict
        """
        if length not in [30, 60, 90, 120, 150, 180]:
            raise Exception('length needs to be one of these: [30, 60, 90, 120, 150, 180]')
        url = build_url(TWITCH_API_BASE_URL + 'channels/commercial',
                        {'broadcaster_id': broadcaster_id,
                         'length': length})
        response = self.__api_post_request(url, AuthType.USER, [AuthScope.CHANNEL_EDIT_COMMERCIAL])
        return response.json()

    def create_user_follows(self,
                            from_id: str,
                            to_id: str,
                            allow_notifications: Optional[bool] = False) -> bool:
        """Requires User authentication with AuthScope.USER_EDIT_FOLLOWS\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#create-user-follows

        :param from_id: str
        :param to_id: str
        :param allow_notifications: optional bool
        :rtype: bool
        """
        url = build_url(TWITCH_API_BASE_URL + 'users/follows',
                        {'from_id': from_id,
                         'to_id': to_id,
                         'allow_notifications': allow_notifications}, remove_none=True)
        response = self.__api_post_request(url, AuthType.USER, [AuthScope.USER_EDIT_FOLLOWS])
        return response.status_code == 204

    def delete_user_follows(self,
                            from_id: str,
                            to_id: str) -> bool:
        """Requires User authentication with AuthScope.USER_EDIT_FOLLOWS\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#delete-user-follows

        :param from_id: str
        :param to_id: str
        :rtype: bool
        """
        url = build_url(TWITCH_API_BASE_URL + 'users/follows',
                        {'from_id': from_id,
                         'to_id': to_id})
        response = self.__api_delete_request(url, AuthType.USER, [AuthScope.USER_EDIT_FOLLOWS])
        return response.status_code == 204

    def get_cheermotes(self,
                       broadcaster_id: str) -> dict:
        """Requires App or User authentication\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-cheermotes

        :param broadcaster_id: str
        :rtype: dict
        """
        url = build_url(TWITCH_API_BASE_URL + 'bits/cheermotes',
                        {'broadcaster_id': broadcaster_id})
        response = self.__api_get_request(url, AuthType.APP, [])
        return make_fields_datetime(response.json(), ['last_updated'])

    def get_hype_train_events(self,
                              broadcaster_id: str,
                              first: Optional[int] = 1,
                              id: Optional[str] = None,
                              cursor: Optional[str] = None) -> dict:
        """Requires App or User authentication with AuthScope.CHANNEL_READ_HYPE_TRAIN\n
        For detailed documentation, see here: https://dev.twitch.tv/docs/api/reference#get-hype-train-events

        :param broadcaster_id: str
        :param first: optional int, default 1, max 100
        :param id: optional str
        :param cursor: optional str
        :rtype: dict
        """
        if first < 1 or first > 100:
            raise Exception('first must be between 1 and 100')
        url = build_url(TWITCH_API_BASE_URL + 'hypetrain/events',
                        {'broadcaster_id': broadcaster_id,
                         'first': first,
                         'id': id,
                         'cursor': cursor}, remove_none=True)
        response = self.__api_get_request(url, AuthType.APP, [AuthScope.CHANNEL_READ_HYPE_TRAIN])
        data = make_fields_datetime(response.json(), ['event_timestamp',
                                                      'started_at',
                                                      'expires_at',
                                                      'cooldown_end_time'])
        data = fields_to_enum(data, ['type'], HypeTrainContributionMethod, HypeTrainContributionMethod.UNKNOWN)
        return data

