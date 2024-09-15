import time
from reddit_api import check_login, get_karma, post_comment, reply_to_comments

from loggerino import log
import datetime
from random import randint
 # these get inserted into the prompt for the AI to generate responses with a diffent attitude
joking_modifier = 'realistic but unexpected'
serious_modifier ='realistic and empathetic'
joking_subs = ['AskReddit', 'dadjokes', 'Jokes', ]



while True:
    check_login()
    what_do = randint(1, 10)
    if what_do >= 3:
        post_comment(joking_modifier, joking_subs)
    else:
        reply_to_comments(joking_modifier, joking_subs)
    get_karma()
    hour = datetime.datetime.now().hour
    if 6 <  hour < 7:
        log('Going to sleep for 8 hours :)')
        time.sleep(28800)
    sleep_time = randint(900,1800)
    log(f'waiting {datetime.timedelta(seconds=sleep_time)} minutes to post again')
    time.sleep(sleep_time)




