from functools import partial, wraps
import redis


def sendsms(telephone_number, content, key=None):
    telephone_number = str(telephone_number)
    if len(content) <= 70:
        if int(client.hget('sended_sms', telephone_number).decode()) >= 5:
            print('1 分钟内发送次数超过 5 次, 请等待 1 分钟')
            return False
        print(content, end='\t')
        print('sms send successful')
        client.hincrby('sended_sms', telephone_number, 1)
        return True
    else:
        sendsms(telephone_number, content[:70], key=key)
        sendsms(telephone_number, content[70:], key=key)


if __name__ == '__main__':
    client = redis.Redis(host='localhost', password='fakepassword')
    telephone_numbers = (12345654321, 18899966651, 18899966653)
    client.hmset('sended_sms', {str(t_num): 0 for t_num in telephone_numbers})
    
    sendsms(12345654321, content='hello')
    sendsms(12345654321, content='hi')
    sendsms(12345654321, content='idiot')
    sendsms(12345654321, content='Are you Trump Donald')
    sendsms(12345654321, content='I am Biden, thank you brother')
    sendsms(12345654321, content='今天天气很好，万里无云，蓝蓝的天空上飘着洁白的云彩')
    sendsms(18899966651, content='How are you?')
    sendsms(18899966651, content=''.join([str(i) for i in range(203)]))
    sendsms(18899966653, content='1'*140)
    sendsms(18899966653, content='1'*139)

