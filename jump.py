from PIL import Image
import math

DEFAULT_GAP = 10

DEFAULT_DISTANCE = 100

DEFAULT_ERROR_TIME = 0  # 默认最小时间


def compare_px(pre, cur, select_cl, like_num, x):
    if pre is None:  # 第一次查找
        return False, like_num
    else:
        pr, py, pb, pa = pre
        r, y, b, a = cur
        if select_cl is None:
            if (abs(pr - r) + abs(py - y) + abs(pb - b) > DEFAULT_GAP) \
                    and not is_spot(cur):  # 若与上一个点色差过大且不是棋子
                return True, like_num + 1  # 目标色点还未赋值，表明第一次发现色点
            return False, like_num  # 色差过大，未找到
        else:  # 则与目标色点比较，若相似且距离合适则表明又发现了一个色点
            sr, sy, sb, sx = select_cl
            if abs(sr - r) < DEFAULT_GAP \
                    and abs(sy - y) < DEFAULT_GAP \
                    and abs(sb - b) < DEFAULT_GAP \
                    and abs(sx - x) < DEFAULT_DISTANCE:
                like_num += 1
                return True, like_num
            return False, like_num  # 相差过大，不是上次选中的色点


# 判断是否是棋子
def is_spot(px):
    r, y, b, a = px
    flag = False
    if r == y == b == 0x5A:  # 奶茶杯特殊处理
        flag = False
    elif (0x30 < r < 0x70) \
            and (0x30 < y < 0x60) \
            and (0x40 < b < 0x9f):
        flag = True
    return flag


def jump(image, time_param):
    width, height = image.size
    num = 0
    sum_x = 0
    sum_y = 0

    for i in range(0, width, 10):
        for j in range(0, height, 20):
            pixel = image.getpixel((i, j))
            # print(pixel)
            if (0x20 < pixel[0] < 0x40) \
                    and (0x20 < pixel[1] < 0x40) \
                    and (0x45 < pixel[2] < 0x80):
                r, g, b, a = pixel
                # print('颜色是{}，{}，{}'.format(r, g, b))
                # print('坐标：{},{}'.format(i, j))
                num = num + 1
                sum_x = sum_x + i
                sum_y = sum_y + j
    if num == 0:  # 出错，停止
        return DEFAULT_ERROR_TIME
    avg_x = int(sum_x / num)
    avg_y = int(sum_y / num)

    print('小人坐标为：{},{}'.format(avg_x, avg_y))

    e_h = int(height * 2 / 3)
    s_h = int(height / 4)

    pre_px = None
    h_num = 0
    h_sum_x = 0
    h_sum_y = 0
    select_color = None
    l_num = 0

    flag = False

    for j in range(s_h, e_h, 30):
        for i in range(0, width, 30):
            px = image.getpixel((i, j))
            # print('坐标：{},{}'.format(i, j))
            r, g, b, a = px
            cap, l_num = compare_px(pre_px, px, select_color, l_num, i)
            if not is_spot(px):
                pre_px = px
            if cap:  # 若色差够大
                h_num = h_num + 1
                h_sum_x = h_sum_x + i
                h_sum_y = h_sum_y + j
                # print('颜色是{}，{}，{}'.format(r, g, b))
                print('寻找的坐标：{},{}'.format(i, j))
                if h_num == 1:
                    select_color = r, g, b, i
            if l_num == 12:  # 找到足够多的点，跳出循环
                flag = True
        if flag:
            break
    if h_num == 0:  # 未找到，重新开始

        return DEFAULT_ERROR_TIME

    h_avg_x = int(h_sum_x / h_num)
    h_avg_y = int(h_sum_y / h_num)

    print('棋盘坐标为：{},{}'.format(h_avg_x, h_avg_y))

    distance = math.sqrt(math.pow(abs(h_avg_x - avg_x), 2) +
                         math.pow(abs(h_avg_y - avg_y), 2))

    print('距离是{}'.format(distance))

    jump_time = distance * time_param
    return jump_time


if __name__ == '__main__':
    im = Image.open('error.png')
    jump(im, 2.45)
