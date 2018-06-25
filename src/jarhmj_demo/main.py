import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}


def search_book(q='', tag='', start=0, count=20):
    '''
        搜索书籍
    :param q: 查询关键字，q和tag必传其一
    :param tag:查询的tag，q和tag必传其一
    :param start:取结果的offset，默认为0
    :param count:取结果的条数，默认为20，最大为100
    :return: 第一本书籍的id
    '''
    url = 'https://api.douban.com/v2/book/search'
    params = {'q': q,
              'tag': tag,
              'start': start,
              'count': count,
              }
    req = requests.get(url=url, params=params, headers=headers)
    result = req.json()
    # 根据返回状态码来处理结果
    if req.status_code == 200:
        books = result['books']
        if books:
            id = books[0]['id']
        return id
    else:
        print(result)
        req.raise_for_status()


def get_annotations(book_id, format='text', order='rank', page='', count=None):
    '''
        获得书籍的笔记
    :param book_id: 书籍的id
    :param format: 返回content字段格式，选填（编辑伪标签格式：text, HTML格式：html），默认为text
    :param order: 排序，选填（最新笔记：collect, 按有用程度：rank, 按页码先后：page），默认为rank
    :param page: 按页码过滤，选填
    :param count: 取结果的条数，默认为20，最大为100
    :return: 笔记的list
    '''
    url = 'https://api.douban.com/v2/book/{id}/annotations'.format(id=book_id)
    params = {'format': format,
              'order': order,
              'page': page,
              'count': count,
              }
    req = requests.get(url=url, params=params, headers=headers)
    result = req.json()
    # 根据返回状态码来处理结果
    if req.status_code == 200:
        annotations = result['annotations']
        annotation_content = [annotation['content'] for annotation in annotations]
        return annotation_content
    else:
        print(result)
        req.raise_for_status()


def check_str(content):
    '''
        检查字符串内容中中文字符是否大于50个
    :param content:字符串
    :return: 布尔值
    '''
    str = re.sub('[^\u4e00-\u9fa5]+', '', content)
    if len(str) > 50:
        return True
    else:
        return False


if __name__ == '__main__':
    # 搜索到《设计模式》这本书
    book_id = search_book(q='设计模式', count=1)
    # 获取该书最新的50条笔记
    annotation_content = get_annotations(book_id=book_id, order='collect', count=50)
    # 打印出超过50个中文字符的笔记
    for i, content in enumerate(annotation_content):
        if check_str(content):
            result = '第{i}条笔记:\n{content}'.format(i=i, content=content)
            print(result)
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
