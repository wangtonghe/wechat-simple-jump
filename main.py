import jump
from six.moves import input
import time
import os
import random
import sys
from PIL import Image
import json


def get_time_param():
    with open("config.json", 'r') as f:
        f_json = json.load(f)
        return f_json['time_param']


def main():
    flag = input('确定开始吗 Y/N')
    if not flag:
        return
    num = 0

    while True:
        # 0. 保存上一张图片，便于出错分析
        if os.path.exists('autojump.png'):
            tmp = Image.open('autojump.png')
            tmp.save('error.png')
        # 1. 使用adb将截图传过来
        os.system('adb shell screencap -p /sdcard/autojump.png')
        os.system('adb pull /sdcard/autojump.png autojump.png')

        # 2. 利用颜色区分棋子，使用色差分辨方块，找到两者距离
        image = Image.open('autojump.png')
        distance = jump.jump(image)
        if distance == 0:
            sys.exit(0)

        # 3. 获取时间参数,由此得到按压时间（此参数与具体机型有关，可多次测试找到合适的）
        time_param = get_time_param()
        press_time = int(distance * time_param)
        print('跳跃时间：{}'.format(press_time))

        # 4. 使用adb命令模拟触摸时间
        x1, y1, x2, y2 = 220, 1055, 240, 1100
        cmd = 'adb shell input swipe {} {} {} {} {}'.format(
            x1, y1, x2, y2, press_time)
        os.system(cmd)
        num += 1
        time.sleep(random.uniform(1, 2))
        if num > random.uniform(6, 10):  # 每6-10次多休息一会
            print('{}连击，多休息一会'.format(num))
            time.sleep(3)
            num = 0


if __name__ == '__main__':
    main()
