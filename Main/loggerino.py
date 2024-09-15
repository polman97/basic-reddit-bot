from datetime import datetime

log_file = open("log.txt","a")

post_log_read = open("post_id.txt", "r")

#overwrites the old log file, logs all the prints to new log file every time the program gets opened
def log(text):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f'[{current_time}]: {text}')
    log_file.write(f'[{current_time}]: {text.encode("utf-8")}\n')

def log_post_id(post_id):
    post_log_write = open("post_id.txt", "a")
    post_log_write.write(f'{post_id}, ')




