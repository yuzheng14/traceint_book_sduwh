import time

def log(message):
    # with open('log.out','a',encoding='utf-8') as f:
        # f.write(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())+'\t'+f'{message}'+'\n')
    print((time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())+'\t'+f'{message}'+'\n'))