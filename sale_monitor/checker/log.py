import datetime


def log(message: str):

    dt = datetime.datetime.now()
    with open('./log.txt', 'a') as log_file:
        log_file.write(str(dt) + '\n')
        log_file.write(message + '\n')
        log_file.write('\n')