from random import choices
from concurrent.futures import ThreadPoolExecutor
import redis


def counter(video_id):
    video_id = str(video_id)
    client.incr(video_id)
    return video_id, client.get(video_id).decode()


if __name__ == '__main__':
    client = redis.Redis(host='localhost', password='fakepassword')
    video_ids = tuple(range(1001, 1006))
    for id_ in video_ids:
        client.set(str(id_), 0)
        print(client.get(str(id_)))

    # client.set('1001', 0, nx=True)
    # client.set('1002', 0, nx=True)

    pool = ThreadPoolExecutor(100)
    results = pool.map(counter, choices(video_ids, weights=[1, 2, 1, 2, 3], k=100))
    for res in list(results):
        print(res)

