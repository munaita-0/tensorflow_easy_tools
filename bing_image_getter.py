# -*- coding: utf-8 -*-
import requests
import urllib2
import httplib2

API_KEY = '<YOUR_API_KEY>'
END_POINT = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search'
headers = { 'Ocp-Apim-Subscription-Key': API_KEY }

# 一度にDLする数
OFFSET_COUNT = 150

# 出力先のディレクトリ
OUTPUT_PATH = '/path/to/dir'

# 検索ワード
SEARCH_ITEM = 'something'

# 取得数
TOTAL_NUM = 3000


def image_urls():
  img_list = []
  i = 0
  while i < TOTAL_NUM:
    params = {
      'imageContent': 'Portrait',
      'mkt': 'ja-JP',
      'count': OFFSET_COUNT,
      'offset': i,
      'q': SEARCH_ITEM,
    }
    res = requests.get(END_POINT, headers=headers, params=params)
    vals = res.json()['value']
    for j in range(len(vals)):
      img_list.append(vals[j]["contentUrl"])
    i=i+OFFSET_COUNT
  return img_list

def fetch_images(img_list):
  opener = urllib2.build_opener()
  http = httplib2.Http(".cache")
  for i in range(len(img_list)):
    try:
      print(img_list[i])
      response, content = http.request(img_list[i])
      with open('{}/image.{}.jpg'.format(OUTPUT_PATH, str(i)), 'wb') as f:
        f.write(content)
    except:
      traceback.print_exc()
      continue

if __name__ == "__main__":
  print('start.')
  fetch_images(image_urls())
