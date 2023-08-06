# pyquestionit

Simple [QuestionIt.space](https://questionit.space) API client for Python 3.6+.

See [docs](https://docs.questionit.space) for more details.

> This documencation is a WIP. It should be completed later.

## Installing the package

Install the package using pip.

```bash
pip install pyquestionit
```

You're ready to import it in your project.

```py
import pyquestionit
```

## Getting started

### Make unlogged requests

You can easily make requests to the QuestionIt.space API with the generic HTTP methods `.get`, `.post`, `.put`, `.patch` and `.delete`.
Find documentation about every endpoint in the [documentation](https://docs.questionit.space).

```py
# Instanciate the client
client = pyquestionit.QuestionIt()

# Make unlogged requests to allowed endpoints
users = client.get('users/find', params={'q': 'questionit'})
# users == [{'id': '1', 'slug': 'questionitspace', ...}]
```

For every method, you can find the following parameters:

- `endpoint` (`str`): Specify the endpoint (mandatory)
- `params` (`dict`): Specify query or body parameters of your request. It will be automatically formatted.
- `headers` (`dict`): If you want to set custom headers.
- `auth` (`bool` or `str`): If `True` (default), request will use registred token. If `str`, use the string as token. If `False` , disable auth.
- `with_rq` (`boolean`): If `True`, return the response object instead of the direct result. You can use `response.json()` to get result.

**Endpoint** parameter is the remaining part after `https://api.questionit.space/` URL.
For example, for endpoint `https://api.questionit.space/users/find`, parameter should be `users/find`.


### Make an authentificated request

This kind of request requires an **access token**. If you don't have it yet, jump to ***Authentification*** part.

You can specify your token inside `QuestionIt` constructor

```py
client = pyquestionit.QuestionIt('some-token-here');
```

or just use `set_access_token()` method.

```py
client.set_access_token('some-token-here');
```

Token will be automatically added to request headers.

```py
relationship = client.get('relationships/with/2');

print(f"You {'follow' if relationship.following else 'do not follow'} user #2")
```


### Errors

This library uses `requests` package and raise exceptions when HTTP status code is not a success.
You can catch exceptions with `requests.exceptions.HTTPError` type:

```py
import requests

try:
  users = client.get('users/find', params={'q': 'questionit'})
except requests.exceptions.HTTPError as e:
  request = e.request
  response = e.response
  result = response.json() # Usually, result is an APIError result

  # Do something with response or result...
  print('Error code: ', result['code'])
```

## Authentification

You can generate login tokens and get access token through this library.

### Get a request token

A request token is used to ask user to connect to your app.

```py
import urllib.parse

token = client.get_request_token(
  'app-key-here', 
  'redirect-url-after-confirm-or-deny' # or 'oob' for no redirection
)

token_encoded = urllib.parse.quote(token)
url = 'https://questionit.space/appflow?token=' + token_encoded

# Send user to {url} !
```

### Get access token

Once user has approved the app, he will be redirected to your redirect URL (or will have an access PIN displayed).

For redirect URLs, there's formed like: 
`https://yoursite.com/callback?validator={validator}`.

You can extract `validator` from query string, they're needed to generate access token.

```py
result = client.get_access_token(
  'app-key-here',
  # You need to have original token, it should be stored somewhere on your side. 
  # You can give an unique key into callback URL (like in query),
  # it will be keeped.
  'token-here', 
  'validator-or-PIN-here'
)

print(f"Access token is {result['token']}.")
```

You can now use this token with the instance.

```py
client.set_access_token(result['token'])
```

## Endpoint-based methods

This Python library binds most of the endpoints of the API to specific methods, so you don't need to handle boring things by yourself.
Their usage is pretty straight-forward and don't need to be explained (the method parameters are usually whats API is taking), except for a few methods (see below).

The following methods exists:
- `.verify_token` -> `GET auth/token/verify`
- `.revoke_token` -> `DELETE auth/token`
- `.find_users` -> `GET users/find`
- `.get_user` -> `GET users/id/:id` and `GET users/slug/:slug`
- `.get_logged` -> `GET users/logged`
- `.set_pinned` -> `PATCH questions/pin`
- `.remove_pinned` -> `DELETE questions/pin`
- `.set_muted_words` -> `POST users/blocked_words`
- `.get_muted_words` -> `GET users/blocked_words`
- `.ask` -> `POST questions`, `POST questions/anonymous` and `POST polls`
- `.waiting_questions` -> `GET questions/waiting`
- `.reply` -> `POST questions/answer`
- `.remove_question` -> `DELETE questions`
- `.remove_muted_questions` -> `DELETE questions/masked`
- `.like` -> `POST likes`
- `.unlike` -> `DELETE likes`
- `.likers_of` -> `GET likes/list/:id`
- `.likers_ids_of` -> `GET likes/ids/:id`
- `.questions_of` -> `GET questions`
- `.asked_questions_of` -> `GET questions/sent`
- `.home_timeline` -> `GET questions/timeline`
- `.ancestors_of` -> `GET questions/tree/:root`
- `.replies_of` -> `GET questions/replies/:id`
- `.relationship_with` -> `GET relationships/with/:id`
- `.relationship_between` -> `GET relationships/between`
- `.follow` -> `POST relationships/:id`
- `.unfollow` -> `DELETE relationships/:id`
- `.followers` -> `GET relationships/followers`
- `.followings` -> `GET relationships/followings`
- `.block` -> `POST blocks/:id`
- `.unblock` -> `DELETE blocks/:id`
- `.get_notifications` -> `GET notifications`
- `.remove_notification` -> `DELETE notifications/:id`
- `.get_notification_count` -> `GET notifications/count`
- `.notifications_all_mark_as_seen` -> `POST notifications/bulk_seen`

### .get_user

This method can fetch an user by user ID or by slug.

It automatically choose between ID and slug regarding the given string ; if it's numeric, ID endpoint will be used.

```py
client.get_user('2')  # calls users/id/2
client.get_user('questionitspace')  # calls users/slug/questionitspace
```

### .ask

You can attach multiple choices "polls" directly with this method.
Just give a simple list of strings in the `poll` parameter.

```py
client.ask('Cat or dog?', user_id='2', in_reply_to='36', poll=['Cats!!', 'Dogs :('])
```

### .reply

When you reply to a question, you can attach medias (JPEG, PNG and GIF images).

You must attach the picture in the `picture` parameter of `.reply` by following this example:

```py
import mimetypes

path = 'path-to-file.ext'

client.reply(
  answer='Yes, cats are the best.', 
  question_id='32',
  picture=(
    'picture',  # Name, required for multipart/form-data send 
    open(path, 'rb'),  # Open as 'rb' !
    mimetypes.guess_type(path)[0]  # MIME type
  ),
)
```
