from functools import partial, wraps
import redis


def send_times(func=None, times=10):
    if func is None:
        return partial(send_times, times=times)
    @wraps(func)
    def wrapper(*args, **kwargs):
        telephone_number = str(args[0])
        content = kwargs['content']
        if int(client.hget('sended_sms', telephone_number).decode()) >= 5:
            print('1 分钟内发送次数超过 5 次, 请等待 1 分钟')
        else:
            if len(content) <= 70:
                client.hincrby('sended_sms', telephone_number, 1)
            return func(*args, **kwargs)
    return wrapper


@send_times(times=5)
def sendsms(telephone_number, content='', key=None):
    if len(content) <= 70:
        print(content, end='\t')
        print('sms send successful')
    else:
        sendsms(telephone_number, content=content[:70], key=key)
        sendsms(telephone_number, content=content[70:], key=key)


if __name__ == '__main__':
    client = redis.Redis(host='localhost', password='fakepassword')
    telephone_numbers = (12345654321, 18899966651)
    [client.hset('sended_sms', t_num, 0) for t_num in telephone_numbers]
    
    sendsms(12345654321, content='hello')
    sendsms(12345654321, content='hi')
    sendsms(12345654321, content='idiot')
    sendsms(12345654321, content='Are you Trump Donald')
    sendsms(12345654321, content='I am Biden, thank you brother')
    sendsms(12345654321, content='今天天气很好，万里无云，蓝蓝的天空上飘着洁白的云彩')
    sendsms(18899966651, content='How are you?')
    sendsms(18899966651, content=''.join([str(i) for i in range(203)]))
    sendsms(18899966651, content='1'*140)
    sendsms(18899966651, content='1'*139)

