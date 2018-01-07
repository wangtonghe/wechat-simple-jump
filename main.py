import jump
from six.moves import input
import time
import os
import random
import sys
from PIL import Image


def main():
    flag = input('确定开始吗 Y/N')
    if not flag:
        return

    num = 0
    while True:
        if os.path.exists('autojump.png'):
            tmp = Image.open('autojump.png')
            tmp.save('error.png')
        os.system('adb shell screencap -p /sdcard/autojump.png')
        os.system('adb pull /sdcard/autojump.png autojump.png')
        image = Image.open('autojump.png')
        time_param = 2.44
        jump_time = jump.jump(image, time_param)
        image.close()
        if jump_time == 0:
            sys.exit(0)
        press_time = int(jump_time)
        print('跳跃时间：{}'.format(press_time))
        cmd = 'adb shell input swipe 220 1055 240 1100 {}'.format(press_time)
        os.system(cmd)
        num += 1
        time.sleep(random.uniform(1, 2))
        if num > random.uniform(6, 10):  # 每6-10次多休息一会
            print('{}连击，多休息一会'.format(num))
            time.sleep(3)
            num = 0


if __name__ == '__main__':
    main()
