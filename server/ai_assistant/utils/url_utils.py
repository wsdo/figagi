### 判断 link 是否是完整 url，如果不是，则添加基础路径
def url_join(base: str, link: str) -> str:
    lower_link = link.lower()
    if (lower_link.startswith('http') or lower_link.startswith('https')):
        return link

    sep = '/'
    if (lower_link.startswith('/')):
        sep = ''

    data = f'{base}{sep}{link}'
    
    return data
    