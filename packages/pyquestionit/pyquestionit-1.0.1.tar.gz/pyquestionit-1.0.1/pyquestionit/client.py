import requests
from typing import Dict, Optional, Union, Any, List
from requests_toolbelt.multipart.encoder import MultipartEncoder

QuestionItParams = Union[Dict[str, Any], List[any]]
QuestionItAuth = Optional[Union[str, bool]]
NumberString = Union[str, int]

class QuestionIt:
  """
    QuestionIt official client. Instantiate with or without token.
    
    *get*, *post*, *patch*, *put* and *delete* methods take the following *options*:

    params
      Query or body parameter, as a dictionnary
    headers
      Custom HTTP headers as a dictionnary
    auth
      `True` (default) if current token is used, `False` for no auth,
      a `str` for custom authentification token
    with_rq
      `True` if response should be returned instead of the direct result
  """

  __PREFIX = 'https://api.questionit.space/'
  __FORM_DATA = {'questions/answer', 'users/profile'}
  __QUERY_METHODS = {'GET', 'HEAD', 'DELETE'}

  def __init__(self, token: Optional[str] = None):
    self.token = token
    self.rate_limits = {}


  ### UTILITY FUNCTIONS

  def set_access_token(self, token: str):
    self.token = token

  def remove_access_token(self):
    self.token = None

  def set_prefix(self, prefix: str):
    self.__PREFIX = prefix


  ### SPECIFIC BASED FUNCTIONS

  ## Token based

  def get_request_token(self, app_key: str, url: str = 'oob') -> str:
    """Get request token to ask user for access to the QuestionIt.space API."""
    resp = self.post('apps/token', params={'key': app_key, 'url': url}, auth=False)
    return resp['token']

  def get_access_token(self, app_key: str, token: str, validator: str):
    """Get access token to access the QuestionIt.space API."""
    return self.post('auth/token/create', params={'key': app_key, 'token': token, 'validator': validator}, auth=False)

  def verify_token(self):
    """Check token validity, get logged user and verify token permissions."""
    return self.get('auth/token/verify')

  def revoke_token(self):
    """Cancel a token existence."""
    return self.delete('auth/token')

  
  ## User based

  def find_users(self, query: str, until: Optional[str] = None):
    """Find users using a query. Query can concern user slug or user name."""
    return self.get('users/find', params={'q': query, 'until': until})

  def get_user(self, user: NumberString):
    """Get a single user. If you give a numberstring, ID will be supported. Otherwise, it will search by slug."""
    user = str(user)

    if user.isnumeric():
      return self.get('users/id/' + user)

    return self.get('users/slug/' + user)

  def get_logged(self):
    """Get logged user."""
    return self.get('users/logged')

  def set_pinned(self, question_id: NumberString):
    """Set pinned question of user profile."""
    return self.patch('questions/pin', params={'id': str(question_id)})

  def remove_pinned(self):
    """Remove pinned question of user profile."""
    return self.delete('questions/pin')

  def set_muted_words(self, words: List[str]):
    """Overwrite muted words for logged user."""
    return self.post('users/blocked_words', params={'words': words})

  def get_muted_words(self):
    return self.get('users/blocked_words')

  
  ## Post / manage questions

  def ask(self, content: str, user_id: str, anonymous: bool = True, in_reply_to: Optional[str] = None, poll: Optional[List[str]] = None):
    """Ask {user_id} as {anonymous}/logged with {content}."""
    params = {'content': content, 'to': user_id}
    self.__set_args(params, in_reply_to=in_reply_to)

    if poll:
      if len(poll) < 2 or len(poll) > 4:
        raise ValueError('Multiple choices are only allowed from 2 to 4 choices')

      poll_data = self.post('polls', params={'options': poll})
      params['poll_id'] = poll_data['poll_id']

    if anonymous:
      return self.post('questions/anonymous', params=params)
    return self.post('questions', params=params)

  def waiting_questions(self, since: Optional[str] = None, until: Optional[str] = None, size: Optional[str] = None, sort_by: Optional[str] = None, muted: bool = False):
    """Get waiting questions. Cursor the result using {since} and {until}. Use {muted} to get muted waiting questions."""

    params = {'muted': 'true' if muted else 'false'}
    self.__set_args(params, since=since, until=until, size=size, sort_by=sort_by)

    return self.get('questions/waiting', params=params)

  def reply(self, answer: str, question_id: str, post_on_twitter: bool = False, picture = None):
    """Post a reply {answer} for {question_id}. If you want to attach a picture, give a valid file pointer/bytes/str in {picture} (do not give a filename!)."""
    params = {
      'answer': answer, 
      'question': question_id, 
      'post_on_twitter': 'true' if post_on_twitter else 'false'
    }

    if picture is not None:
      params['picture'] = picture

    return self.post('questions/answer', params=params)

  def remove_question(self, question_id: str):
    """Remove question {question_id}"""
    return self.delete('questions', params={'question': question_id})

  def remove_muted_questions(self):
    """Remove every muted question."""
    return self.delete('questions/masked')


  ## Like questions

  def like(self, question_id: str):
    """Like {question_id}."""
    return self.post('likes/' + question_id)

  def unlike(self, question_id: str):
    """Unlike {question_id}."""
    return self.delete('likes/' + question_id)

  def likers_of(self, question_id: str, since: Optional[str] = None, until: Optional[str] = None, size: Optional[str] = None):
    """Get user objects of likers of question {question_id}. Cursor the result with {since} and {until}."""

    params = {}
    self.__set_args(params, since=since, until=until, size=size)

    return self.get('likes/list/' + question_id , params=params)

  def likers_ids_of(self, question_id: str, since: Optional[str] = None, until: Optional[str] = None, size: Optional[str] = None):
    """Get user IDs of likers of question {question_id}. Cursor the result with {since} and {until}."""

    params = {}
    self.__set_args(params, since=since, until=until, size=size)

    return self.get('likes/ids/' + question_id , params=params)
    

  ## Get question timelines

  def questions_of(self, user_id: Optional[str] = None, since: Optional[str] = None, until: Optional[str] = None, size: Optional[str] = None, sort_by: Optional[str] = None):
    """Get replied questions of user {user_id}. Cursor the result using {since} and {until}."""

    params = {}
    self.__set_args(params, user_id=user_id, since=since, until=until, size=size, sort_by=sort_by)

    return self.get('questions', params=params)

  def asked_questions_of(self, user_id: Optional[str] = None, since: Optional[str] = None, until: Optional[str] = None, size: Optional[str] = None, sort_by: Optional[str] = None):
    """Get asked questions of user {user_id}. Cursor the result using {since} and {until}."""

    params = {}
    self.__set_args(params, user_id=user_id, since=since, until=until, size=size, sort_by=sort_by)

    return self.get('questions/sent', params=params)

  def home_timeline(self, since: Optional[str] = None, until: Optional[str] = None, size: Optional[str] = None, sort_by: Optional[str] = None):
    """Get timeline of logged user. Cursor the result using {since} and {until}."""

    params = {}
    self.__set_args(params, since=since, until=until, size=size, sort_by=sort_by)

    return self.get('questions/timeline', params=params)

  def ancestors_of(self, question_id: str, size: Optional[str] = None):
    """Get ancestors of questions {question_id}."""

    params = {}
    self.__set_args(params, size=size)

    return self.get('questions/tree/' + question_id, params=params)

  def replies_of(self, question_id: str, since: Optional[str] = None, until: Optional[str] = None, size: Optional[str] = None, sort_by: Optional[str] = None):
    """Get replies of question {question_id}. Cursor the result using {since} and {until}."""

    params = {}
    self.__set_args(params, since=since, until=until, size=size, sort_by=sort_by)

    return self.get('questions/replies/' + question_id, params=params)


  ## Relationships

  def relationship_with(self, user_id: str):
    """Get the relationship object between logged user and another user {user_id}"""
    return self.get('relationships/with/' + user_id)

  def relationship_between(self, source_user_id: str, target_user_id: str):
    """Get the relationship object between source user {source_user_id} and target user {target_user_id}"""
    return self.get('relationships/between', params={'source': source_user_id, 'target': target_user_id})

  def follow(self, user_id: str):
    """Follow {user_id} from logged user."""
    return self.post('relationships/' + user_id)

  def unfollow(self, user_id: str):
    """Unfollow {user_id} from logged user."""
    return self.delete('relationships/' + user_id)

  def followers(self, since: Optional[str] = None, until: Optional[str] = None, size: Optional[str] = None):
    """Get followers of logged user. Cursor the result using {since} and {until}."""

    params = {}
    self.__set_args(params, since=since, until=until, size=size)

    return self.get('relationships/followers', params=params)

  def followings(self, since: Optional[str] = None, until: Optional[str] = None, size: Optional[str] = None):
    """Get followings of logged user. Cursor the result using {since} and {until}."""

    params = {}
    self.__set_args(params, since=since, until=until, size=size)

    return self.get('relationships/followings', params=params)

  def block(self, user_id: str):
    """Block {user_id} from logged user."""
    return self.post('blocks/' + user_id)

  def unblock(self, user_id: str):
    """Unblock {user_id} from logged user."""
    return self.delete('blocks/' + user_id)


  ## Notifications

  def get_notifications(self, mark_as_seen: bool = True, since: Optional[str] = None, until: Optional[str] = None, size: Optional[str] = None, sort_by: Optional[str] = None):
    """Get notifications of logged user. Cursor the result using {since} and {until}."""

    params = {'mark_as_seen': 'true' if mark_as_seen else 'false'}
    self.__set_args(params, since=since, until=until, size=size, sort_by=sort_by)

    return self.get('notifications', params=params)

  def remove_notification(self, notification_id: str):
    """Remove {notification_id}. (You can specify "all" to delete every notification)."""
    return self.delete('notifications/' + notification_id)

  def get_notification_count(self):
    """Get waiting questions and unseen notification counts."""
    return self.get('notifications/count')

  def notifications_all_mark_as_seen(self):
    """Mark all notifications as seen."""
    return self.post('notifications/bulk_seen')


  ### GENERIC REQUEST FUNCTIONS

  def get(self, endpoint: str, params: QuestionItParams = {}, headers = {}, auth: QuestionItAuth = None, with_rq: bool = False):
    """Make a request with GET method."""
    return self.__make(endpoint, 'GET', params=params, headers=headers, auth=auth, with_rq=with_rq)

  def post(self, endpoint: str, params: QuestionItParams = {}, headers = {}, auth: QuestionItAuth = None, with_rq: bool = False):
    """Make a request with POST method."""
    return self.__make(endpoint, 'POST', params=params, headers=headers, auth=auth, with_rq=with_rq)

  def patch(self, endpoint: str, params: QuestionItParams = {}, headers = {}, auth: QuestionItAuth = None, with_rq: bool = False):
    """Make a request with PATCH method."""
    return self.__make(endpoint, 'PATCH', params=params, headers=headers, auth=auth, with_rq=with_rq)

  def put(self, endpoint: str, params: QuestionItParams = {}, headers = {}, auth: QuestionItAuth = None, with_rq: bool = False):
    """Make a request with PUT method."""
    return self.__make(endpoint, 'PUT', params=params, headers=headers, auth=auth, with_rq=with_rq)

  def delete(self, endpoint: str, params: QuestionItParams = {}, headers = {}, auth: QuestionItAuth = None, with_rq: bool = False):
    """Make a request with DELETE method."""
    return self.__make(endpoint, 'DELETE', params=params, headers=headers, auth=auth, with_rq=with_rq)

  def __make(
    self, 
    endpoint: str,
    method: str, 
    params: QuestionItParams = {},
    headers = {}, 
    auth: QuestionItAuth = None,
    with_rq: bool = False
  ):
    options = {
      'headers': headers,
    }

    if type(auth) is str:
      headers['Authorization'] = 'Bearer ' + auth
    elif (auth == True or auth is None) and self.token:
      headers['Authorization'] = 'Bearer ' + self.token

    method = method.upper()

    if len(params):
      if method in self.__QUERY_METHODS:
        options['params'] = params
      else:
        if endpoint in self.__FORM_DATA:
          fd = MultipartEncoder(fields=params)
          options['data'] = fd
          headers['Content-Type'] = fd.content_type
        else:
          headers['Content-Type'] = 'application/json'
          options['json'] = params

    resp: requests.Response
    url = self.__PREFIX + endpoint

    if method == 'GET':
      resp = requests.get(url, **options)
    elif method == 'POST':
      resp = requests.post(url, **options)
    elif method == 'PATCH':
      resp = requests.patch(url, **options)
    elif method == 'PUT':
      resp = requests.put(url, **options)
    elif method == 'DELETE':
      resp = requests.delete(url, **options)
    else:
      raise ValueError('Unknown used HTTP method')

    # Register the rate limit
    if 'X-RateLimit-Limit' in resp.headers:
      self.rate_limits[endpoint] = {
        'limit': int(resp.headers['X-RateLimit-Limit']),
        'remaining': int(resp.headers['X-RateLimit-Remaining']),
        'reset': int(resp.headers['X-RateLimit-Reset'])
      }

    resp.raise_for_status()

    if with_rq:
      return resp

    return resp.json() if len(resp.text) else None

  ### PRIVATE UTILITIES
  def __set_args(self, options: dict, **kwargs):
    for key, item in kwargs.items():
      if item is not None:
        options[key] = item

