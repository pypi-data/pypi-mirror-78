from client import QuestionIt
import requests
from config import APP_KEY, TOKEN, DEV_MODE

if __name__ == '__main__':
  token = TOKEN

  questionit = QuestionIt(token)

  # If dev mode, use local server
  if DEV_MODE:
    questionit.set_prefix('http://localhost:2999/')

  try:
    res = ''

    ### Test auth
    # res_token = questionit.get_request_token(APP_KEY, 'oob')
    # print(res_token)
    # # Pause in order to validate with res_token
    # res = questionit.get_access_token(APP_KEY, res_token, '280187')

    ### Test endpoints
    # res = questionit.verify_token()
    # res = questionit.find_users('alki')
    # res = questionit.get_user('2')
    res = questionit.get_user('alkihis')
    # res = questionit.remove_pinned()
    # res = questionit.set_pinned('11')
    # res1 = questionit.get_muted_words()
    # print(res1)
    # res = questionit.set_muted_words(['hello'])
    # print(res)
    # res = questionit.set_muted_words(res1)
    # res = questionit.ask('Hello, how are you?', user_id='2', in_reply_to='84', anonymous=False, poll=['Fine', 'Badly :c'])
    # res = questionit.ask('With a picture please?', user_id='2')
    # res = questionit.waiting_questions(muted=False, since='102')
    # res = questionit.waiting_questions(muted=True)
    # res = questionit.reply('now, i\'m ok i guess.', '103', post_on_twitter=False)
    # res = questionit.reply(
    #   '', 
    #   '105', 
    #  picture=('auvergne-rhonealpes', open('/Users/alki/Downloads/auvergne-rhonealpes_1487329573.jpg', 'rb'), 'image/jpeg')
    # )
    # res = questionit.remove_question('66')
    # res = questionit.remove_muted_questions()
    # res = questionit.like('106')
    # res = questionit.unlike('106')
    # res = questionit.likers_of('106')
    # res = questionit.likers_ids_of('106')
    # res = questionit.questions_of('1')
    # res = questionit.asked_questions_of('1')
    # res = questionit.home_timeline(since='80')
    # res = list(map(lambda x: x['id'], questionit.ancestors_of('19')['ancestors']))
    # res = questionit.replies_of('17')
    # res = questionit.relationship_with('2')
    # res = questionit.relationship_between('1', '2')
    # print(questionit.rate_limits['relationships/between'])
    # res = questionit.unfollow('2')
    # res = questionit.followers()
    # res = questionit.followings()
    # res = questionit.block('2')
    # res = questionit.unblock('2')
    # res = questionit.follow('2')
    # res = questionit.get_notifications()
    # res = questionit.get_notification_count()
    # res = questionit.notifications_all_mark_as_seen()

    print(res)
  except requests.exceptions.HTTPError as e:
    data = e.request
    print(e, data.body, e.response.json())

