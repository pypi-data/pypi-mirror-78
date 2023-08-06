# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2019-2020 Terbau

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import aiohttp
import asyncio
import logging
import json
import re
import time

from typing import TYPE_CHECKING, List, Optional, Any, Union, Tuple
from urllib.parse import quote
from .utils import MaybeLock

from .errors import HTTPException

if TYPE_CHECKING:
    from .client import Client

log = logging.getLogger(__name__)


class GraphQLRequest:
    def __init__(self, query: str, *,
                 operation_name: str = None,
                 variables: dict = None
                 ) -> None:
        self.query = query
        self.operation_name = operation_name
        self.variables = variables

    def _to_camel_case(self, text: str) -> str:
        components = text.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def __iter__(self) -> str:
        for key, value in self.__dict__.items():
            if value is None:
                continue

            yield (self._to_camel_case(key), value)

    def as_dict(self) -> dict:
        return dict(self)

    def as_multiple_payload(self) -> dict:
        return {
            'operationName': (self.operation_name
                              or self.get_operation_name_by_query()),
            'variables': self.variables,
            'query': self.query
        }

    def get_operation_name_by_query(self) -> str:
        return re.search(r'(?:mutation|query) (\w+)', self.query).group(1)


class Route:
    BASE = ''
    AUTH = None

    def __init__(self, path: str = '', *,
                 auth: str = None,
                 **params: Any) -> None:
        self.path = path
        self.params = {k: (quote(v) if isinstance(v, str) else v)
                       for k, v in params.items()}

        if self.BASE == '':
            raise ValueError('Route must have a base')

        url = self.BASE + self.path
        self.url = url.format(**self.params) if self.params else url

        if auth:
            self.AUTH = auth


class EpicGamesGraphQL(Route):
    BASE = 'https://graphql.epicgames.com/graphql'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class EpicGames(Route):
    BASE = 'https://www.epicgames.com'
    AUTH = None


class PaymentWebsite(Route):
    BASE = 'https://payment-website-pci.ol.epicgames.com'
    AUTH = None


class LightswitchPublicService(Route):
    BASE = 'https://lightswitch-public-service-prod06.ol.epicgames.com'
    AUTH = 'IOS_ACCESS_TOKEN'


class ProfileSearchService(Route):
    BASE = 'https://user-search-service-prod.ol.epicgames.com'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class AccountPublicService(Route):
    BASE = 'https://account-public-service-prod.ol.epicgames.com'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class EulatrackingPublicService(Route):
    BASE = 'https://eulatracking-public-service-prod-m.ol.epicgames.com'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class AffiliatePublicService(Route):
    BASE = 'https://affiliate-public-service-prod.ol.epicgames.com'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class EventsPublicService(Route):
    BASE = 'https://events-public-service-live.ol.epicgames.com'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class FortniteContentWebsite(Route):
    BASE = 'https://fortnitecontent-website-prod07.ol.epicgames.com'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class FortnitePublicService(Route):
    BASE = 'https://fortnite-public-service-prod11.ol.epicgames.com'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class FriendsPublicService(Route):
    BASE = 'https://friends-public-service-prod.ol.epicgames.com'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class PartyService(Route):
    BASE = 'https://party-service-prod.ol.epicgames.com'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class PresencePublicService(Route):
    BASE = 'https://presence-public-service-prod.ol.epicgames.com'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class StatsproxyPublicService(Route):
    BASE = 'https://statsproxy-public-service-live.ol.epicgames.com'
    AUTH = 'FORTNITE_ACCESS_TOKEN'


class HTTPClient:
    def __init__(self, client: 'Client', *,
                 connector: aiohttp.BaseConnector = None) -> None:
        self.client = client
        self.connector = connector
        self._jar = aiohttp.CookieJar()
        self.headers = {}
        self.device_id = self.client.auth.device_id

        self.create_connection()

    @staticmethod
    async def json_or_text(response: aiohttp.ClientResponse) -> Union[str,
                                                                      dict]:
        text = await response.text(encoding='utf-8')
        if 'application/json' in response.headers.get('content-type', ''):
            return json.loads(text)
        return text

    @property
    def user_agent(self) -> str:
        return 'Fortnite/{0.client.build} {0.client.os}'.format(self)

    @property
    def session(self) -> aiohttp.ClientSession:
        return self.__session

    def get_auth(self, auth: str) -> str:
        u_auth = auth.upper()

        if u_auth == 'IOS_BASIC_TOKEN':
            return 'basic {0}'.format(self.client.auth.ios_token)
        elif u_auth == 'FORTNITE_BASIC_TOKEN':
            return 'basic {0}'.format(self.client.auth.fortnite_token)
        elif u_auth == 'IOS_ACCESS_TOKEN':
            return self.client.auth.ios_authorization
        elif u_auth == 'FORTNITE_ACCESS_TOKEN':
            return self.client.auth.authorization
        return auth

    def add_header(self, key: str, val: Any) -> None:
        self.headers[key] = val

    def remove_header(self, key: str) -> Any:
        return self.headers.pop(key)

    async def close(self) -> None:
        self._jar.clear()
        if self.__session:
            await self.__session.close()

    def create_connection(self) -> None:
        self.__session = aiohttp.ClientSession(
            connector=self.connector,
            connector_owner=self.connector is None,
            loop=self.client.loop,
            cookie_jar=self._jar
        )

    async def request(self, method: str, url: str,
                      **kwargs: Any
                      ) -> Tuple[aiohttp.ClientResponse, Union[str, dict]]:
        try:
            params = kwargs['params']
            if isinstance(params, dict):
                kwargs['params'] = {k: (str(v).lower() if isinstance(v, bool)
                                        else v) for k, v in params.items()}
            else:
                kwargs['params'] = [(k, (str(v).lower() if isinstance(v, bool)
                                         else v)) for k, v in params]
        except KeyError:
            pass

        pre_time = time.time()
        async with self.__session.request(method, url, **kwargs) as r:
            log.debug('{0} {1} has returned {2.status} in {3:.2f}s'.format(
                method,
                url,
                r,
                time.time() - pre_time
            ))

            data = await self.json_or_text(r)
            return r, data

    async def _fn_request(self, method: str,
                          route: Union[Route, str],
                          auth: Optional[str] = None,
                          graphql: Optional[Union[Route, List[Route]]] = None,
                          **kwargs: Any) -> Any:
        url = route.url if not isinstance(route, str) else route

        headers = {**kwargs.get('headers', {}), **self.headers}
        headers['User-Agent'] = self.user_agent

        auth = auth or route.AUTH
        if auth is not None:
            headers['Authorization'] = self.get_auth(auth)

        device_id = kwargs.pop('device_id', None)
        if device_id is not None:
            headers['X-Epic-Device-ID'] = (self.device_id if device_id is True
                                           else device_id)

        if graphql is not None:
            is_multiple = isinstance(graphql, (list, tuple))

            if not is_multiple:
                graphql = (graphql,)
            kwargs['json'] = [gql_query.as_multiple_payload()
                              for gql_query in graphql]

        kwargs['headers'] = headers

        raw = kwargs.pop('raw', False)
        r, data = await self.request(method, url, **kwargs)

        if raw:
            return r

        if 'errorCode' in data:
            raise HTTPException(r, data)

        if graphql is not None:

            error_data = None
            for child_data in data:
                if 'errors' in child_data:
                    error_data = child_data['errors']

            if error_data is not None:
                selected = error_data[0]

                obj = {'errorMessage': selected['message']}
                service_response = selected['serviceResponse']
                if service_response == '':
                    error_payload = {}
                else:
                    error_payload = json.loads(service_response)

                raise HTTPException(r, {**obj, **error_payload})

            def get_payload(d):
                return next(iter(d['data'].values()))

            if len(data) == 1:
                return get_payload(data[0])
            return [get_payload(d) for d in data]
        return data

    async def fn_request(self, method: str,
                         route: Union[Route, List[Route]],
                         auth: Optional[str] = None,
                         graphql: Union[Route, List[Route]] = None,
                         **kwargs: Any) -> Any:
        try:
            return await self._fn_request(method, route, auth, graphql,
                                          **kwargs)
        except HTTPException as exc:
            catch = (
                'errors.com.epicgames.common.oauth.invalid_token',
                ('errors.com.epicgames.common.authentication.'
                 'token_verification_failed')
            )
            if exc.message_code in catch and not self.client._closing:
                force_attempts = 3

                async with MaybeLock(self.client._reauth_lock):
                    retry = True

                    def should_force():
                        ts = self.client._refresh_times
                        if len(ts) > force_attempts:
                            self.client._refresh_times = ts[-force_attempts:]
                        try:
                            old = self.client._refresh_times[-force_attempts]
                        except IndexError:
                            return True
                        else:
                            return time.time() - old > 20

                    if should_force():
                        try:
                            await self.client.auth.do_refresh()
                        except Exception:
                            if self.client.can_restart():
                                await self.client.restart()
                    else:
                        retry = False

                    if retry:
                        return await self.fn_request(
                            method,
                            route,
                            auth,
                            graphql,
                            **kwargs
                        )
                    else:
                        raise exc from None

            elif exc.message_code in ('errors.com.epicgames.common.'
                                      'server_error',):
                await asyncio.sleep(0.5)
                return await self._fn_request(method, route, auth, graphql,
                                              **kwargs)

            elif exc.message_code in ('errors.com.epicgames.common.'
                                      'concurrent_modification_error',):
                return await self.fn_request(method, route, auth, graphql,
                                             **kwargs)

            raise

    async def get(self, route: Union[Route, str],
                  auth: Optional[str] = None,
                  **kwargs: Any) -> Any:
        return await self.fn_request('GET', route, auth, **kwargs)

    async def post(self, route: Union[Route, str],
                   auth: Optional[str] = None,
                   **kwargs: Any) -> Any:
        return await self.fn_request('POST', route, auth, **kwargs)

    async def delete(self, route: Union[Route, str],
                     auth: Optional[str] = None,
                     **kwargs: Any) -> Any:
        return await self.fn_request('DELETE', route, auth, **kwargs)

    async def patch(self, route: Union[Route, str],
                    auth: Optional[str] = None,
                    **kwargs: Any) -> Any:
        return await self.fn_request('PATCH', route, auth, **kwargs)

    async def put(self, route: Union[Route, str],
                  auth: Optional[str] = None,
                  **kwargs: Any) -> Any:
        return await self.fn_request('PUT', route, auth, **kwargs)

    async def graphql_request(self, graphql: Union[GraphQLRequest,
                                                   List[GraphQLRequest]],
                              auth: Optional[str] = None,
                              **kwargs: Any) -> Any:
        return await self.fn_request('POST', EpicGamesGraphQL(), auth, graphql,
                                     **kwargs)

    ###################################
    #        Epicgames GraphQL        #
    ###################################

    async def graphql_friends_set_alias(self) -> Any:
        variables = {
            "friendId": "65db72079052463cb345d23ee27ae6a1",
            "alias": "Hallo1233"
        }

        query = """
        mutation FriendsMutation($friendId: String!, $alias: String!) {
            Friends {
                setAlias(friendId: $friendId, alias: $alias) {
                    success
                }
            }
        }"""

        return await self.graphql_request(
            GraphQLRequest(query, variables=variables))

    async def graphql_initialize_friends_request(self) -> List[dict]:
        queries = (
            GraphQLRequest(
                query="""
                query FriendsQuery($displayNames: Boolean!) {
                    Friends {
                        summary(displayNames: $displayNames) {
                            friends {
                                alias
                                note
                                favorite
                                ...friendFields
                            }
                            incoming {
                                ...friendFields
                            }
                            outgoing {
                                ...friendFields
                            }
                            blocklist {
                                ...friendFields
                            }
                        }
                    }
                }

                fragment friendFields on Friend {
                    accountId
                    displayName
                    account {
                        externalAuths {
                            type
                            accountId
                            externalAuthId
                            externalDisplayName
                        }
                    }
                }
                """,
                variables={
                    'displayNames': True
                }
            ),
            GraphQLRequest(
                query="""
                query PresenceV2Query($namespace: String!, $circle: String!) {
                    PresenceV2 {
                        getLastOnlineSummary(namespace: $namespace, circle: $circle) {
                            summary { #Type: [LastOnline]
                                friendId #Type: String
                                last_online #Type: String
                            }
                        }
                    }
                }
                """,  # noqa
                variables={
                    'namespace': 'Fortnite',
                    'circle': 'friends'
                }
            )
        )

        return await self.graphql_request(queries)

    ###################################
    #            Epicgames            #
    ###################################

    async def epicgames_get_csrf(self) -> aiohttp.ClientResponse:
        return await self.get(EpicGames('/id/api/csrf'), raw=True)

    async def epicgames_reputation(self, xsrf_token: str) -> Any:
        headers = {
            'x-xsrf-token': xsrf_token
        }

        return await self.get(EpicGames('/id/api/reputation'), headers=headers)

    async def epicgames_login(self, email: str,
                              password: str,
                              xsrf_token: str) -> Any:
        headers = {
            'x-xsrf-token': xsrf_token
        }

        payload = {
            'email': email,
            'password': password,
            'rememberMe': False,
            'captcha': ''
        }

        return await self.post(EpicGames('/id/api/login'),
                               headers=headers,
                               data=payload)

    async def epicgames_mfa_login(self, method: str,
                                  code: str,
                                  xsrf_token: str) -> Any:
        headers = {
            'x-xsrf-token': xsrf_token
        }

        payload = {
            'code': code,
            'method': method,
            'rememberDevice': False
        }

        return await self.post(EpicGames('/id/api/login/mfa'),
                               headers=headers,
                               data=payload)

    async def epicgames_redirect(self, xsrf_token: str) -> Any:
        headers = {
            'x-xsrf-token': xsrf_token
        }

        return await self.get(EpicGames('/id/api/redirect'), headers=headers)

    async def epicgames_get_exchange_data(self, xsrf_token: str) -> dict:
        headers = {
            'x-xsrf-token': xsrf_token
        }

        r = EpicGames('/id/api/exchange/generate')
        return await self.post(r, headers=headers)

    ###################################
    #        Payment Website          #
    ###################################

    async def payment_website_search_sac_by_slug(self, slug: str) -> Any:
        params = {
            'slug': slug
        }

        r = PaymentWebsite('/affiliate/search-by-slug', auth=None)
        return await self.get(r, params=params)

    ###################################
    #           Lightswitch           #
    ###################################

    async def lightswitch_get_status(self, *,
                                     service_id: Optional[str] = None) -> list:
        params = {'serviceId': service_id} if service_id else None

        r = LightswitchPublicService('/lightswitch/api/service/bulk/status')
        return await self.get(r, params=params)

    ###################################
    #           User Search           #
    ###################################

    async def user_search_by_prefix(self, prefix: str, platform: str) -> list:
        params = {
            'prefix': prefix,
            'platform': platform
        }

        r = ProfileSearchService('/api/v1/search')
        return await self.get(r, params=params)

    ###################################
    #            Account              #
    ###################################

    async def account_get_exchange_data(self, auth: str) -> dict:
        r = AccountPublicService('/account/api/oauth/exchange')
        return await self.get(r, auth=auth)

    async def account_oauth_grant(self, **kwargs: Any) -> dict:
        r = AccountPublicService('/account/api/oauth/token')
        return await self.post(r, **kwargs)

    async def account_generate_device_auth(self, client_id: str) -> dict:
        r = AccountPublicService(
            '/account/api/public/account/{client_id}/deviceAuth',
            client_id=client_id
        )
        return await self.post(r, auth="IOS_ACCESS_TOKEN", json={})

    async def account_get_device_auths(self, client_id: str) -> list:
        r = AccountPublicService(
            '/account/api/public/account/{client_id}/deviceAuth',
            client_id=client_id,
            auth="IOS_ACCESS_TOKEN"
        )
        return await self.get(r)

    async def account_lookup_device_auth(self, client_id: str,
                                         device_id: str) -> dict:
        r = AccountPublicService(
            '/account/api/public/account/{client_id}/deviceAuth/{device_id}',
            client_id=client_id,
            device_id=device_id,
            auth="IOS_ACCESS_TOKEN"
        )
        return await self.get(r)

    async def account_delete_device_auth(self, client_id: str,
                                         device_id: str) -> None:
        r = AccountPublicService(
            '/account/api/public/account/{client_id}/deviceAuth/{device_id}',
            client_id=client_id,
            device_id=device_id,
            auth="IOS_ACCESS_TOKEN"
        )
        return await self.delete(r)

    async def account_sessions_kill_token(self, token: str, auth=None) -> Any:
        r = AccountPublicService(
            '/account/api/oauth/sessions/kill/{token}',
            token=token
        )
        return await self.delete(r, auth='bearer {0}'.format(token))

    async def account_sessions_kill(self, kill_type: str,
                                    auth='IOS_ACCESS_TOKEN') -> Any:
        params = {
            'killType': kill_type
        }

        r = AccountPublicService('/account/api/oauth/sessions/kill')
        return await self.delete(r, params=params, auth=auth)

    async def account_get_by_display_name(self, display_name: str) -> dict:
        r = AccountPublicService(
            '/account/api/public/account/displayName/{display_name}',
            display_name=display_name
        )
        return await self.get(r)

    async def account_get_by_user_id(self, user_id: str, *,
                                     auth: Optional[str] = None) -> dict:
        r = AccountPublicService(
            '/account/api/public/account/{user_id}',
            user_id=user_id
        )
        return await self.get(r, auth=auth)

    async def account_get_by_email(self, email: str) -> dict:
        r = AccountPublicService(
            '/account/api/public/account/email/{email}',
            email=email
        )
        return await self.get(r, auth='IOS_ACCESS_TOKEN')

    async def account_get_external_auths_by_id(self, user_id: str) -> list:
        r = AccountPublicService(
            '/account/api/public/account/{user_id}/externalAuths',
            user_id=user_id
        )
        return await self.get(r)

    async def account_get_multiple_by_user_id(self,
                                              user_ids: List[str]) -> list:
        params = [('accountId', user_id) for user_id in user_ids]
        r = AccountPublicService('/account/api/public/account')
        return await self.get(r, params=params)

    async def account_graphql_get_multiple_by_user_id(self,
                                                      user_ids: List[str]
                                                      ) -> dict:
        return await self.graphql_request(GraphQLRequest(
            query="""
            query AccountQuery($accountIds: [String]!) {
                Account {
                    # Get details about an account given an account ID
                    accounts(accountIds: $accountIds) { #Type: [Account]
                        # The AccountID for this account
                        id #Type: String
                        # The epic display name for this account
                        displayName #Type: String
                        # External auths associated with this account
                        externalAuths { #Type: [ExternalAuth]
                            type #Type: String
                            accountId #Type: String
                            externalAuthId #Type: String
                            externalDisplayName #Type: String
                        }
                    }
                }
            }
            """,
            variables={
                'accountIds': user_ids
            }
        ))

    async def account_graphql_get_by_display_name(self,
                                                  display_name: str) -> dict:
        return await self.graphql_request(GraphQLRequest(
            query="""
            query AccountQuery($displayName: String!) {
                Account {
                    account(displayName: $displayName) {
                        id
                        displayName
                        externalAuths {
                            type
                            accountId
                            externalAuthId
                            externalDisplayName
                        }
                    }
                }
            }
            """,
            variables={
                'displayName': display_name
            }
        ))

    async def account_graphql_get_clients_external_auths(self) -> dict:
        return await self.graphql_request(GraphQLRequest(
            query="""
            query AccountQuery {
                Account {
                    myAccount {
                        externalAuths {
                            type
                            accountId
                            externalAuthId
                            externalDisplayName
                        }
                    }
                }
            }
            """
        ))

    ###################################
    #          Eula Tracking          #
    ###################################

    async def eulatracking_get_data(self) -> dict:
        r = EulatrackingPublicService(
            '/eulatracking/api/public/agreements/fn/account/{client_id}',
            client_id=self.client.user.id
        )
        return await self.get(r)

    async def eulatracking_accept(self, version: int, *,
                                  locale: str = 'en') -> Any:
        params = {
            'locale': locale
        }

        r = EulatrackingPublicService(
            ('/eulatracking/api/public/agreements/fn/version/{version}'
             '/account/{client_id}/accept'),
            version=version,
            client_id=self.client.user.id
        )
        return await self.post(r, params=params)

    ###################################
    #         Fortnite Public         #
    ###################################

    async def fortnite_grant_access(self) -> Any:
        r = FortnitePublicService(
            '/fortnite/api/game/v2/grant_access/{client_id}',
            client_id=self.client.user.id
        )
        return await self.post(r, json={})

    async def fortnite_get_store_catalog(self) -> dict:
        r = FortnitePublicService('/fortnite/api/storefront/v2/catalog')
        return await self.get(r)

    async def fortnite_get_timeline(self) -> dict:
        r = FortnitePublicService('/fortnite/api/calendar/v1/timeline')
        return await self.get(r)

    ###################################
    #        Fortnite Content         #
    ###################################

    async def fortnitecontent_get(self) -> dict:
        r = FortniteContentWebsite('/content/api/pages/fortnite-game')
        return await self.get(r)

    ###################################
    #            Friends              #
    ###################################

    async def friends_get_all(self, *,
                              include_pending: bool = False) -> list:
        params = {
            'includePending': include_pending
        }

        r = FriendsPublicService('/friends/api/public/friends/{client_id}',
                                 client_id=self.client.user.id)
        return await self.get(r, params=params)

    async def friends_add_or_accept(self, user_id: str) -> Any:
        r = FriendsPublicService(
            '/friends/api/v1/{client_id}/friends/{user_id}',
            client_id=self.client.user.id,
            user_id=user_id
        )
        return await self.post(r)

    async def friends_remove_or_decline(self, user_id: str) -> Any:
        r = FriendsPublicService(
            '/friends/api/v1/{client_id}/friends/{user_id}',
            client_id=self.client.user.id,
            user_id=user_id
        )
        return await self.delete(r)

    async def friends_remove_all(self) -> Any:
        r = FriendsPublicService('/friends/api/v1/{client_id}/friends',
                                 client_id=self.client.user.id)
        return await self.delete(r)

    async def friends_get_blocklist(self) -> list:
        r = FriendsPublicService('/friends/api/v1/{client_id}/blocklist',
                                 client_id=self.client.user.id)
        return await self.get(r)

    async def friends_set_nickname(self, user_id: str, nickname: str) -> Any:
        r = FriendsPublicService(
            '/friends/api/v1/{client_id}/friends/{user_id}/alias',
            client_id=self.client.user.id,
            user_id=user_id
        )
        return await self.put(r, data=nickname)

    async def friends_remove_nickname(self, user_id: str) -> Any:
        r = FriendsPublicService(
            '/friends/api/v1/{client_id}/friends/{user_id}/alias',
            client_id=self.client.user.id,
            user_id=user_id
        )
        return await self.delete(r)

    async def friends_set_note(self, user_id: str, note: str) -> Any:
        r = FriendsPublicService(
            '/friends/api/v1/{client_id}/friends/{user_id}/note',
            client_id=self.client.user.id,
            user_id=user_id
        )
        return await self.put(r, data=note)

    async def friends_remove_note(self, user_id: str) -> Any:
        r = FriendsPublicService(
            '/friends/api/v1/{client_id}/friends/{user_id}/note',
            client_id=self.client.user.id,
            user_id=user_id
        )
        return await self.delete(r)

    async def friends_get_summary(self) -> dict:
        r = FriendsPublicService('/friends/api/v1/{client_id}/summary',
                                 client_id=self.client.user.id)
        return await self.get(r)

    async def friends_block(self, user_id: str) -> Any:
        r = FriendsPublicService(
            '/friends/api/v1/{client_id}/blocklist/{user_id}',
            client_id=self.client.user.id,
            user_id=user_id
        )
        return await self.post(r)

    async def friends_unblock(self, user_id: str) -> Any:
        r = FriendsPublicService(
            '/friends/api/v1/{client_id}/blocklist/{user_id}',
            client_id=self.client.user.id,
            user_id=user_id
        )
        return await self.delete(r)

    async def friends_get_mutual(self, user_id: str) -> Any:
        r = FriendsPublicService(
            '/friends/api/v1/{client_id}/friends/{user_id}/mutual',
            client_id=self.client.user.id,
            user_id=user_id
        )
        return await self.get(r)

    ###################################
    #            Presence             #
    ###################################

    async def presence_get_last_online(self) -> dict:
        r = PresencePublicService('/presence/api/v1/_/{client_id}/last-online',
                                  client_id=self.client.user.id)
        return await self.get(r)

    ###################################
    #              Stats              #
    ###################################

    async def stats_get_v2(self, user_id: str, *,
                           start_time: Optional[int] = None,
                           end_time: Optional[int] = None) -> dict:
        params = {}
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time

        r = StatsproxyPublicService(
            '/statsproxy/api/statsv2/account/{user_id}',
            user_id=user_id
        )
        return await self.get(r, params=params)

    async def stats_get_mutliple_v2(self, ids: List[str], stats: List[str], *,
                                    start_time: Optional[int] = None,
                                    end_time: Optional[int] = None) -> list:
        payload = {
            'appId': 'fortnite',
            'owners': ids,
            'stats': stats
        }
        if start_time:
            payload['startDate'] = start_time
        if end_time:
            payload['endDate'] = end_time

        r = StatsproxyPublicService('/statsproxy/api/statsv2/query')
        return await self.post(r, json=payload)

    async def stats_get_leaderboard_v2(self, stat: str) -> dict:
        r = StatsproxyPublicService(
            '/statsproxy/api/statsv2/leaderboards/{stat}',
            stat=stat
        )
        return await self.get(r)

    ###################################
    #             Party               #
    ###################################

    async def party_send_invite(self, party_id: str,
                                user_id: str,
                                send_ping: bool = True) -> Any:
        conn_type = self.client.default_party_member_config.cls.CONN_TYPE
        payload = {
            'urn:epic:cfg:build-id_s': self.client.party_build_id,
            'urn:epic:conn:platform_s': self.client.platform.value,
            'urn:epic:conn:type_s': conn_type,
            'urn:epic:invite:platformdata_s': '',
            'urn:epic:member:dn_s': self.client.user.display_name,
        }

        params = {
            'sendPing': send_ping
        }

        r = PartyService(
            '/party/api/v1/Fortnite/parties/{party_id}/invites/{user_id}',
            party_id=party_id,
            user_id=user_id
        )
        return await self.post(r, json=payload, params=params)

    async def party_delete_invite(self, party_id: str, user_id: str) -> Any:
        r = PartyService(
            '/party/api/v1/Fortnite/parties/{party_id}/invites/{user_id}',
            party_id=party_id,
            user_id=user_id
        )
        return await self.delete(r)

    # NOTE: Depracated since fortnite v11.30. Use param sendPing=True with
    #       send_invite
    # NOTE: Now used for sending invites from private parties
    async def party_send_ping(self, user_id: str) -> Any:
        r = PartyService(
            '/party/api/v1/Fortnite/user/{user_id}/pings/{client_id}',
            user_id=user_id,
            client_id=self.client.user.id
        )
        return await self.post(r, json={})

    async def party_delete_ping(self, user_id: str) -> Any:
        r = PartyService(
            '/party/api/v1/Fortnite/user/{client_id}/pings/{user_id}',
            client_id=self.client.user.id,
            user_id=user_id
        )
        return await self.delete(r)

    async def party_decline_invite(self, party_id: str) -> Any:
        r = PartyService(
            ('/party/api/v1/Fortnite/parties/{party_id}/invites/'
             '{client_id}/decline'),
            party_id=party_id,
            client_id=self.client.user.id
        )
        return await self.post(r, json={})

    async def party_member_confirm(self, party_id: str, user_id: str) -> Any:
        r = PartyService(
            ('/party/api/v1/Fortnite/parties/{party_id}/members/'
             '{user_id}/confirm'),
            party_id=party_id,
            user_id=user_id
        )
        return await self.post(r, json={})

    async def party_member_reject(self, party_id: str, user_id: str) -> Any:
        r = PartyService(
            ('/party/api/v1/Fortnite/parties/{party_id}/members/'
             '{user_id}/reject'),
            party_id=party_id,
            user_id=user_id
        )
        return await self.post(r, json={})

    async def party_promote_member(self, party_id: str, user_id: str) -> Any:
        r = PartyService(
            ('/party/api/v1/Fortnite/parties/{party_id}/members/'
             '{user_id}/promote'),
            party_id=party_id,
            user_id=user_id
        )
        return await self.post(r, json={})

    async def party_kick_member(self, party_id: str, user_id: str) -> Any:
        r = PartyService(
            '/party/api/v1/Fortnite/parties/{party_id}/members/{user_id}',
            party_id=party_id,
            user_id=user_id
        )
        return await self.delete(r)

    async def party_leave(self, party_id: str) -> Any:
        conn_type = self.client.default_party_member_config.cls.CONN_TYPE
        payload = {
            'connection': {
                'id': self.client.user.jid,
                'meta': {
                    'urn:epic:conn:platform_s': self.client.platform.value,
                    'urn:epic:conn:type_s': conn_type,
                },
            },
            'meta': {
                'urn:epic:member:dn_s': self.client.user.display_name,
                'urn:epic:member:type_s': conn_type,
                'urn:epic:member:platform_s': self.client.platform.value,
                'urn:epic:member:joinrequest_j': json.dumps({
                    'CrossplayPreference_i': '1'
                }),
            }
        }

        r = PartyService(
            '/party/api/v1/Fortnite/parties/{party_id}/members/{client_id}',
            party_id=party_id,
            client_id=self.client.user.id
        )
        return await self.delete(r, json=payload)

    async def party_join_request(self, party_id: str) -> Any:
        conf = self.client.default_party_member_config
        conn_type = conf.cls.CONN_TYPE
        yield_leadership = conf.yield_leadership
        payload = {
            'connection': {
                'id': str(self.client.xmpp.xmpp_client.local_jid),
                'meta': {
                    'urn:epic:conn:platform_s': self.client.platform.value,
                    'urn:epic:conn:type_s': conn_type,
                },
                'yield_leadership': yield_leadership,
            },
            'meta': {
                'urn:epic:member:dn_s': self.client.user.display_name,
                'urn:epic:member:joinrequestusers_j': json.dumps({
                    'users': [
                        {
                            'id': self.client.user.id,
                            'dn': self.client.user.display_name,
                            'plat': self.client.platform.value,
                            'data': json.dumps({
                                'CrossplayPreference': '1',
                                'SubGame_u': '1',
                            })
                        }
                    ]
                }),
            },
        }

        r = PartyService(
            ('/party/api/v1/Fortnite/parties/{party_id}/members/'
             '{client_id}/join'),
            party_id=party_id,
            client_id=self.client.user.id
        )
        return await self.post(r, json=payload)

    async def party_lookup(self, party_id: str) -> dict:
        r = PartyService('/party/api/v1/Fortnite/parties/{party_id}',
                         party_id=party_id)
        return await self.get(r)

    async def party_lookup_user(self, user_id: str) -> dict:
        r = PartyService('/party/api/v1/Fortnite/user/{user_id}',
                         user_id=user_id)
        return await self.get(r)

    async def party_lookup_ping(self, user_id: str) -> list:
        r = PartyService(
            ('/party/api/v1/Fortnite/user/{client_id}/pings/'
             '{user_id}/parties'),
            client_id=self.client.user.id,
            user_id=user_id
        )
        return await self.get(r)

    async def party_create(self, config: dict) -> dict:
        conf = self.client.default_party_member_config
        conn_type = conf.cls.CONN_TYPE
        yield_leadership = conf.yield_leadership

        _chat_enabled = str(config['chat_enabled']).lower()
        payload = {
            'config': {
                'join_confirmation': config['join_confirmation'],
                'joinability': config['joinability'],
                'max_size': config['max_size']
            },
            'join_info': {
                'connection': {
                    'id': str(self.client.xmpp.xmpp_client.local_jid),
                    'meta': {
                        'urn:epic:conn:platform_s': self.client.platform.value,
                        'urn:epic:conn:type_s': conn_type
                    },
                    'yield_leadership': yield_leadership,
                },
            },
            'meta': {
                'urn:epic:cfg:accepting-members_b': False,
                'urn:epic:cfg:build-id_s': str(self.client.party_build_id),
                'urn:epic:cfg:can-join_b': True,
                'urn:epic:cfg:chat-enabled_b': _chat_enabled,
                'urn:epic:cfg:invite-perm_s': 'Noone',
                'urn:epic:cfg:join-request-action_s': 'Manual',
                'urn:epic:cfg:not-accepting-members-reason_i': 0,
                'urn:epic:cfg:party-type-id_s': 'default',
                'urn:epic:cfg:presence-perm_s': 'Noone',
            }
        }

        r = PartyService('/party/api/v1/Fortnite/parties')
        return await self.post(r, json=payload)

    async def party_update_member_meta(self, party_id: str,
                                       user_id: str,
                                       updated_meta: dict,
                                       deleted_meta: list,
                                       overridden_meta: dict,
                                       revision: int,
                                       override={}) -> Any:
        payload = {
            'delete': deleted_meta,
            'update': updated_meta,
            'override': overridden_meta,
            'revision': revision,
        }

        r = PartyService(
            ('/party/api/v1/Fortnite/parties/{party_id}/members/'
             '{user_id}/meta'),
            party_id=party_id,
            user_id=user_id
        )
        return await self.patch(r, json=payload)

    async def party_update_meta(self, party_id: str,
                                updated_meta: dict,
                                deleted_meta: list,
                                overridden_meta: dict,
                                config: dict,
                                revision: int) -> Any:
        payload = {
            'config': {
                'join_confirmation': config['join_confirmation'],
                'joinability': config['joinability'],
                'max_size': config['max_size']
            },
            'meta': {
                'delete': deleted_meta,
                'update': updated_meta,
                'override': overridden_meta
            },
            'party_state_overridden': {},
            'party_privacy_type': config['joinability'],
            'party_type': config['type'],
            'party_sub_type': config['sub_type'],
            'max_number_of_members': config['max_size'],
            'invite_ttl_seconds': config['invite_ttl_seconds'],
            'revision': revision
        }

        r = PartyService('/party/api/v1/Fortnite/parties/{party_id}',
                         party_id=party_id)
        return await self.patch(r, json=payload)
