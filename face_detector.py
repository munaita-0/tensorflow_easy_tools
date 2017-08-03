# -*- coding:utf-8 -*-

import os
import cv2
import traceback
import random

CONF_FILE = 'haarcascade_frontalface_alt2.xml'

# trainとtestの割合
TRAIN_RATE = 0.8 
TEST_RATE = 0.2

# 元画像のディレクトリ
READ_PATH = '/path/to/dir'
# 出力先のディレクトリ
OUTPUT_PATH = '/path/to/dir'

def main():
  print('start.')

  # trainとtestのディレクトリ準備
  if not os.path.exists(OUTPUT_PATH + '/train'):
      os.mkdir(OUTPUT_PATH + '/train')
  if not os.path.exists(OUTPUT_PATH + '/test'):
      os.mkdir(OUTPUT_PATH + '/test')

  filelist = os.listdir(READ_PATH)
  for filename in filelist:
    if filename.startswith('.'):
      continue
    try:
      detect_faces(filename)
    except:
      traceback.print_exc()
      continue

def detect_faces(filename):
  cascade = cv2.CascadeClassifier(CONF_FILE)
  image = cv2.imread('{}/{}'.format(READ_PATH, filename))
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  faces = cascade.detectMultiScale(gray_image)

  if (len(faces) != 0):
    count = 0
    for face in faces:
      filepath = get_filepath(filename, count)
      print('writing... ' + filepath)
      (x, y, w, h) = face
      filtered_image = image[y:y+h, x:x+w]
      resized_image = cv2.resize(filtered_image, (100, 100))
      cv2.imwrite(filepath, resized_image)
      count += 1

def get_filepath(filename, count):
  v = random.uniform(0, 1)
  if v <= TRAIN_RATE/(TRAIN_RATE + TEST_RATE):
    return '{}/{}/{}.{}.jpg'.format(OUTPUT_PATH, 'train', filename, str(count), '.jpg')
  else:
    return '{}/{}/{}.{}.jpg'.format(OUTPUT_PATH, 'test', filename, str(count), '.jpg')

if __name__ == '__main__':
    main()
