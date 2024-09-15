import praw
from random import randint
from loggerino import log, log_post_id
from chatgpt import get_ai_response

username = ''
client_id = ''
client_secret = ''
password = ''

replied_to = []

#creates reddit instance for given user
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent='windows:testingproject:v0.01'
)
## checks login. if successfull it should print the logged in user
def check_login():
    try:
        log(f'logged in successfully to: {reddit.user.me()}')
    except Exception as e:
        log('Authentication Failed' + e)


    ## posts to a subreddit, while taking post content into account. best with small text content (eg r/jokes)
def post_comment(modifier, subreddit_list):
    try:

        subreddit = reddit.subreddit(subreddit_list[randint(0, (len(subreddit_list)-1))])

        log(f'Subreddit selected: {subreddit}')
        #selects a random post from the 10 newest posts in tha subreddit. checks if the post has already been posted to by bot
        latest_posts = []
        for submission in subreddit.new(limit=10):
            latest_posts.append(submission.id)
        post_found = False
         #checks that the post hasn't been found yet
        while post_found == False:
            target_post_id = latest_posts[randint(0,9)]
            post_log_read = open("post_id.txt", "r")
            if target_post_id not in post_log_read.read():
                post_found = True
            log('Already posted in selected post. selecting new post')
        ## gets both the title and the content of the post
        target_post = f'{reddit.submission(target_post_id).title} \n {reddit.submission(target_post_id).selftext}'
        #logs post id into the log so it can check on the next iteration
        log_post_id(target_post_id)
        #returns id and title of selected post
        log(f'post selected: {target_post}')
    except Exception as e:
        log(f'failed to receive posts from reddit {e}')
    # gets a comment to post from chatgpt
    try:
        comment = get_ai_response(target_post, modifier)
    except Exception as e:
        log(f'failed to get ai response: ' + e)
    # posts the reply
    reply_to_post(target_post_id, comment)

def reply_to_comments(modifier, subreddit_list):
    try:
        ## selects subreddit to post in
        subreddit = reddit.subreddit(subreddit_list[randint(0, (len(subreddit_list) - 1))])
        hot_posts = []
        log(f'Subreddit selected: {subreddit}')
        ## selects post to reply to
        for submission in subreddit.hot(limit=10):
            hot_posts.append(submission.id)
        target_post_id = hot_posts[randint(0, 9)]
        target_post = reddit.submission(target_post_id).title
        post = reddit.submission(target_post_id)
        log(f'post selected: {target_post}')
        ## selects comment to reply to
        comment_list = []
        for comment in post.comments:
            comment_list.append(comment.id)
        target_comment_id = comment_list[randint(0, (len(comment_list) - 1))]
        target_comment_body = reddit.comment(id=target_comment_id).body
        log(f'Comment Selected: {target_comment_body}')
        ##asks for AI reply
        reply = get_ai_response(target_comment_body, modifier, post=f'comment on this post: {target_post}')
        ## posts the reply to reddit
        reddit.comment(id=target_comment_id).reply(reply)
        log(f'reply posted successfully.')

    except Exception as e:
        log('Failed to reply to comment:' + e)








def reply_to_post(post_id, response):
    try:
        replied_to.append(post_id)
        reddit.submission(post_id).reply(response)
        log('reply posted successfully')
    except Exception as e:
        log(f'failed to post to reddit: {e}')

def get_karma():
    redditor_name = username
    redditor = reddit.redditor(redditor_name)
    log(f"The current comment karma of {redditor_name} is: {str(redditor.comment_karma)}")