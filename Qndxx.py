import requests
import re
import os
from config import configs

def getAllQndxxLinks():
    url = 'http://news.cyol.com/node_67071.htm'
    r = requests.get(url)
    res = r.content.decode('utf-8')
    # print(type(res))
    regex = re.compile(r'http://h5.cyol.com/special/daxuexi[^<]*<')
    regex_title = re.compile(r'>.*<')
    all_links = regex.findall(res)
    valid = []
    for link_title in all_links:
        link, title = link_title.split('" target="_blank"')
        title = regex_title.findall(title)[0][1:-1]
        if title:
            valid.append((title, link))

    return valid[::-1]


def getQndxxIdx():
    if not os.path.exists(configs['qndxx_idx_file']):
        with open(configs['qndxx_idx_file'], 'w') as f:
            f.write('0')
    with open(configs['qndxx_idx_file'], 'r') as f:
        try:
            idx = int(f.read())
        except:
            idx = 0
    with open(configs['qndxx_idx_file'], 'w') as f:
        f.write(str(idx+1))

    return idx

def getCurQndxxLink():
    all_links = getAllQndxxLinks()
    idx = getQndxxIdx()

    return all_links[idx%len(all_links)]


if __name__ == "__main__":

    print(getCurQndxxLink())

    # a = 'http://h5.cyol.com/special/daxuexi/9fahztvkm5/index.html" target="_blank"><><>'
    # regex = re.compile(r'http://h5.cyol.com/special/daxuexi[^<]*<')
    # print(regex.findall(a))
