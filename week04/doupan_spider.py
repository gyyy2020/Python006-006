import pathlib
from time import sleep
import csv
import requests
from lxml import etree
from fake_useragent import UserAgent


def get_url(url):
    r = s.get(url, headers=headers)
    print(r.status_code)

    selector = etree.HTML(r.text)
    film_star = selector.xpath('//span[@class="comment-info"]/span[2]/@class')
    film_comments = selector.xpath('//p[@class=" comment-content"]/span/text()')
    return film_star, film_comments


def save_file(content=''):
    p = pathlib.Path(__file__).resolve().parent
    csv_path = p.joinpath('csv_file')
    if not csv_path.exists() or not csv_path.is_dir():
        csv_path.mkdir()
    
    filename = 'douban.csv'
    file_dst = csv_path.joinpath(filename)
    if file_dst.exists() and file_dst.is_file():  # 备份旧文件
        file_backup = csv_path.joinpath(filename+'.bak')
        file_dst.replace(file_backup)
    
    with open(file_dst, 'a', encoding='utf-8-sig', newline="", errors='replace') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['星级', '评论内容'])
        # 有些评论没有星级，过滤掉，放这里可以同步过滤对应的评论内容，不需要活的index
        csv_writer.writerows((k[7], v) for k,v in content if k.startswith('allstar'))


if __name__ == '__main__':
    headers = {'User-Agent': UserAgent().random}
    s = requests.session()

    film_star = []
    film_comments = []
    urls = (f'https://movie.douban.com/subject/35172699/comments?start={20*i}&limit=20&status=P&sort=new_score' for i in range(5))
    for url in urls:
        tmp_a, tmp_b = get_url(url)
        film_star += tmp_a
        film_comments += tmp_b
        sleep(3)
    
    # 数据量不大，一次写入，减少io开销
    save_file(zip(film_star, film_comments))
    

