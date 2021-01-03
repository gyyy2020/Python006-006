import pathlib
from time import sleep
import requests
from lxml import etree


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
s = requests.Session()


def get_url(url):
    # 打开链接
    r = s.get(url, headers=headers)
    print(r.status_code)
    return r


def get_position(resp, url):
    # 定位元素
    selector = etree.HTML(resp.text)
    titles = selector.xpath('//div[@id="center"]/div[@class="block_m"]/div[@class="ct_tittle"]/div[@class="bg_htit"]/h2/a/text()')
    links = selector.xpath('//div[@id="center"]/div[@class="block_m"]/div[@class="ct_tittle"]/div[@class="bg_htit"]/h2/a/@href')

    print(titles, len(titles))
    # print(links, len(links))
    for i in range(len(titles)):
        sleep(2)
        yield (titles[i], f'{url}/{links[i]}')


def crawling_content(title, url):
    # 查找文本
    r = get_url(url)
    selector = etree.HTML(r.text)
    main_news = selector.xpath('//div[@class="p_mainnew"]//text()')
    main_news = ''.join(main_news).strip()
    print(main_news)
    return title, main_news


def save2file(title, source, file_dst):
    # 保存到文件
    with open(file_dst, 'a', encoding='utf-8') as f:
        f.write(title+'\n')
        f.write(source+'\n'*2)


def storage_prepare():
    # 本地目录及文件准备
    p = pathlib.Path(__file__).resolve().parent
    p_stor = p.joinpath('FileStorage')
    if not p_stor.exists() or not p_stor.is_dir():
        p_stor.mkdir()
    
    filename = 'news_test.txt'
    file_dst = p_stor.joinpath(filename)
    if file_dst.exists() and file_dst.is_file():  # 备份旧文件
        p_backup = p_stor.joinpath(filename+'.bak')
        file_dst.replace(p_backup)
    
    return file_dst


if __name__ == '__main__':
    file_dst = storage_prepare()

    url = 'https://www.solidot.org/'
    r = get_url(url)
    news_content = (crawling_content(title, link) for title, link in get_position(r, url))
    for title, news in news_content:
        save2file(title, news, file_dst)
    print('下载完毕')
