from typing import Union

from PIL import Image, ImageDraw, ImageOps
import numpy as np
import matplotlib.pyplot as plt


# Module realizes cutting of line-organized formula by separate symbols
# version 0.13

# vertical borders between symbols detection
def straight_borders(pic):
    nb = []
    str_brds_set = [[[0, 0], [0, pic.shape[0] - 1]]]
    for j in range(pic.shape[1]):
        nb.append(len(pic[:, j][pic[:, j] > 0]))
        if (nb[len(nb) - 1] > 0) and (nb[len(nb) - 2] == 0):
            i = 2
            while nb[len(nb) - i] == 0:
                i += 1
            str_brds_set.append([[int(j - i / 2) + 1, 0], [int(j - i / 2) + 1, pic.shape[0] - 1]])

    str_brds_set.append([[pic.shape[1] - 1, 0], [pic.shape[1] - 1, pic.shape[0] - 1]])

    if pic[:, str_brds_set[0][0][0]:str_brds_set[1][0][0]].max() == 0:
        del str_brds_set[1]
    if pic[:, str_brds_set[-2][0][0]:str_brds_set[-1][0][0]].max() == 0:
        del str_brds_set[-2]

    return str_brds_set


# function for curve borders construction
def curve_border(pic, lb, rb):
    """
    :param pic:
    :param lb:
    :param rb:
    :return:
    """
    print(['lb/rb:', lb, rb])
    # Cut white area around symbols
    pp = np.sum(pic[:, lb:rb + 1], axis=0)
    sub_pp = np.sum(pic[:, lb:rb + 1], axis=1)
    left = lb + [i for i, x in enumerate(pp) if x][0]
    right = rb - [i for i, x in enumerate(pp[::-1]) if x][0]
    top = [i for i, x in enumerate(sub_pp) if x][0]
    bot = len(sub_pp) - [i for i, x in enumerate(sub_pp[::-1]) if x][0]

    print(['t/b/l/r =', top, bot, left, right])

    # determination of matrix with symbol external edges (has own index system)
    w, h = pic[top:bot, left:right].shape
    # print([w,h])
    padington = np.zeros((w + 1, h + 1))
    padington[0:w, 0:h] = pic[top:bot, left:right]
    v_edge = padington[0:w, :] - padington[1:w + 1, :]
    h_edge = padington[:, 0:h] - padington[:, 1:h + 1]
    for i in range(w):
        for j in range(h):
            if v_edge[i, j] == 255:
                v_edge[i, j] = 0
                if i < w - 1: v_edge[i + 1, j] = 1
            elif v_edge[i, j] == -255:
                v_edge[i, j] = 1
            if h_edge[i, j] == 255:
                h_edge[i, j] = 0
                if j < h - 1: h_edge[i, j + 1] = 1
            elif h_edge[i, j] == -255:
                h_edge[i, j] = 1
    edge = np.zeros((w, h))
    for i in range(w):
        for j in range(h):
            if 1 in [v_edge[i, j], h_edge[i, j]]:
                edge[i, j] = 1

    # find x-middle point and appropriate x-position
    x = int((left + right) / 2)
    delta_x = 1  # random.choice([1, -1])
    while (left < x < right) and ((pic[top, x] == 255) or (edge[0, x - left] == 1)):
        x = x + delta_x

    # go straight down as long as possible
    tr = [[x, 0], [x, top]]
    y = np.where(pic[:, x] == 255)[0][0] - 1
    if y < 0:
        y = 0
    tr.append([x, y])
    print(['start:', x, y])

    # following edge while it's impossible to fall down like a drop
    while len(pic[y:bot, x][pic[y:bot, x] > 0]) > 0:
        # print(x,y)
        if (x <= left) or (x >= right):
            print('Path has not been found!')
            tr.append([])
            break
        elif (y <= top) and (len(tr) > 3):
            print('Path has not been found!')
            tr.append([])
            break
        else:
            move = [[x, y + 1], [x - 1, y + 1], [x + 1, y + 1], [x - 1, y], [x + 1, y], [x - 1, y - 1], [x + 1, y - 1],
                    [x, y - 1]]
            previous_step = [x, y]
            for el in move:
                if (el[0] not in [left, right]) and (el[1] not in [top, bot]):
                    if (edge[el[1] - top, el[0] - left] == 1) and (el not in tr):
                        x, y = el
                        tr.append([x, y])
                        break
            if [x, y] == previous_step:
                print('snake bites its tale :-)')
                tr.append([])
                break

    if tr[-1]:
        tr.append([x, bot])
        tr.append([x, pic.shape[0] - 1])
        return tr
    else:
        return []


# Vertical separation by straight horizontal line
def transverse_borders(pic):
    pxs = pic.sum(axis=1)
    hrz_brds_set = []
    lind = 0
    inds = np.where(pxs == 0)[0]
    for k in range(len(inds)):
        if inds[k] != lind:
            if inds[k] == inds[k - 1] + 1:
                if (k == len(inds) - 1) and (inds[k] != len(pxs) - 1):
                    hrz_brds_set.append(int((inds[k - 1] + lind) / 2))
                continue
            elif inds[k - 1] - lind >= 0:
                hrz_brds_set.append(int((inds[k - 1] + lind) / 2))
                lind = inds[k]

    if len(hrz_brds_set) > 0:
        hrz_brds_set[0] = 0
    else:
        hrz_brds_set.append(0)
    hrz_brds_set.append(pic.shape[0] - 1)

    # exclude situations like '='
    cens = np.zeros(len(hrz_brds_set))
    lens = np.zeros(len(hrz_brds_set))

    for j in range(1, len(hrz_brds_set)):
        cens[j], lens[j] = symb_points(pic[hrz_brds_set[j - 1]:hrz_brds_set[j], :])[0:2]

    ind_del = []
    for kk in range(1, len(np.where(lens <= 3)[0])):
        indxs = np.where(lens <= 3)[0]
        if (indxs[kk] == indxs[kk - 1] + 1) and (indxs[kk - 1] != 0):
            ind_del.append(indxs[kk - 1])
    if len(ind_del) > 0:
        for el in ind_del:
            del hrz_brds_set[el]
        cens = np.delete(cens, ind_del)
        lens = np.delete(lens, ind_del)

    return hrz_brds_set


# Black pixels length determination
def symb_points(pic):
    pxs = pic.sum(axis=1)
    ysum = 0
    for ind in np.where(pxs > 0)[0]:
        ysum = ysum + pxs[ind] * ind
    mass_center = int(ysum / pxs.sum())
    length = np.where(pxs > 0)[0][-1] - np.where(pxs > 0)[0][0]

    return mass_center, length, np.where(pxs > 0)[0][0], np.where(pxs > 0)[0][-1]


# subfunction for fraction, root and diacritical analysis
def strline_tracer(pic, x0, y0, dir):
    # define upper and lower deviation
    updev_x, updev_y = 1, 1
    dwdev_x, dwdev_y = 1, 1

    # define point displacement step
    if dir == 'left':
        x_step = -1
        y_step = 0
    elif dir == 'downleft':
        x_step = -1
        y_step = 1
    elif dir == 'upleft':
        x_step = -1
        y_step = -1

    # redefine deviations to stay in-situ
    if y0 - dwdev_y < 0:
        dwdev_y = dwdev_y - abs(y0 - dwdev_y)
    if x0 - dwdev_x < 0:
        dwdev_x = dwdev_x - abs(y0 - dwdev_x)
    if y0 + updev_y >= pic.shape[0] - 1:
        updev_y = updev_y - abs(y0 + updev_y - pic.shape[0] + 1)
    if x0 + updev_x >= pic.shape[1] - 1:
        updev_x = updev_x - abs(x0 + updev_x - pic.shape[1] + 1)

    x = x0  # + x_step
    y = y0  # + y_step

    if y_step == 0:
        # move to the left with a permissible deviation in y by 1
        while (0 < x + x_step < pic.shape[1]) and (255 in pic[y - dwdev_y: y + updev_y + 1, x + x_step]):
            x = x + x_step
            y_set = np.where(pic[y - dwdev_y:y + updev_y, x] == 255)[0]
            if len(y_set) > 0:
                dy = (y_set[0] + y_set[-1]) / 2
                y = y - dwdev_y + int(dy + (0.5 if dy > 0 else -0.5))
    else:
        # move vertically mainly with centering by x
        while (0 < y + y_step < pic.shape[0]) and (255 in pic[y + y_step, x - dwdev_x:x + updev_x + 1]):
            y = y + y_step
            cx = x - dwdev_x + np.where(pic[y, x - dwdev_x:x + updev_x + 1] == 255)[0][0]

            dx = cx
            while (dx > 0) and (pic[y, dx] == 255):
                dx = dx - 1
            ux = x  # cx
            # while (pic[y, ux] == 255) and (ux-dx < 6):
            # ux = ux + 1

            x = int((ux + dx) / 2 + (0.5 if (ux + dx) / 2 > 0 else -0.5))

    return x, y


# function to find fraction delimiter and root symbol
def root_frac_determiner(pic):
    # white margins cutting
    for i in range(pic.shape[0]):
        for j in range(pic.shape[1]):
            if pic[i, j] > 0:
                pic[i, j] = 255
    # remove white areas around formula
    l, r = np.where(pic.sum(axis=0) > 0)[0][0], np.where(pic.sum(axis=0) > 0)[0][-1] + 1
    u, d = np.where(pic.sum(axis=1) > 0)[0][0], np.where(pic.sum(axis=1) > 0)[0][-1] + 1
    pic = pic[u:d, l:r]

    # find possible right side of a line
    y_st = pic.sum(axis=1).argmax()
    x_st = np.where(pic.sum(axis=0) > 0)[0][-1]

    # trace horizontal straight left side
    x, y = strline_tracer(pic, x_st, y_st, 'left')

    # is it fraction delimiter, complex conjugation or part of root symbol?
    # is line?
    if ((x_st - x) / pic.shape[1] > 0.5):
        if (0 in pic[y:y + 10, :].sum(axis=1)):
            # !! not a root
            y_d = y + pic[y:y + 10, :].sum(axis=1).argmin()
            if len(np.where(pic[0:y, :].sum(axis=1) == 0)[0]) > 0:
                # fraction possibly
                y_u = np.where(pic[0:y, :].sum(axis=1) == 0)[0][-1]
                return ['\\frac{', pic[0:y_u, :], '}{', pic[y_d:, :], '}']
            else:
                # conjugation
                y_u = 0
                return ['\\overline{', pic[y_d:, :], '}']
        else:
            # root may be
            xx, yy = strline_tracer(pic, x, y, 'downleft')
            xxx, yyy = strline_tracer(pic, xx, yy, 'upleft')

            # primal zig-zag checker: control points should be different
            if (yy > y) and (x > xxx):
                # secondary zig-zag checker: it should be rather big
                if ((yy - y) / pic.shape[0] > 0.75):
                    # tertiary zig-zag checker: proportions of zigzag
                    if ((yy - yyy) / (yy - y) > 0.45) and ((xx - xxx) / (x - xxx) > 0.1):
                        # definitely root
                        # trying to find out root power
                        y_deg = yyy - 1
                        x_deg = int((yyy - 1) * ((x - xx) / (yy - y)) + xx - 1)
                        deg = pic[0:y_deg, 0:x_deg]

                        # detect expression
                        expr = pic[y + 4:, x + 4:]

                        if deg.sum().sum() > 0:
                            return ['\\sqrt[', deg, ']{', expr, '}']
                        else:
                            return ['\\sqrt{', expr, '}']


# ----------------------------------------------------------------------------------------------------------

# import image and convert to NumPy array
fpath = ''  # should be modified to take picture from memory
fpath = "/home/sfelshtyn/Pictures/formula.png"
im = Image.open(fpath)
im = ImageOps.invert(ImageOps.grayscale(im))
fig = np.array(im)

# binarization
for i in range(fig.shape[0]):
    for j in range(fig.shape[1]):
        if fig[i, j] > 0:
            fig[i, j] = 255

# remove white areas around formula
l, r = np.where(fig.sum(axis=0) > 0)[0][0], np.where(fig.sum(axis=0) > 0)[0][-1] + 1
u, d = np.where(fig.sum(axis=1) > 0)[0][0], np.where(fig.sum(axis=1) > 0)[0][-1] + 1
fig = fig[u:d, l:r]

# make vertical straight borders
borders = straight_borders(fig)
print(borders)

# plt.imshow(fig, cmap='binary')
# for el in borders:
#    el = np.array(el)
#    plt.plot(el[:,0], el[:,1], 'r')
# plt.show()

# regularize set of linear and curve borders from left to right
new_borders = []
for i in range(len(borders) - 1):
    # print(i)
    new_borders.append(borders[i])
    cb = curve_border(fig, borders[i][0][0], borders[i + 1][0][0])
    if len(cb) == 0:
        cb = curve_border(fig[::-1, :], borders[i][0][0], borders[i + 1][0][0])
        if len(cb) != 0:
            cb = cb[::-1]
            for j in range(len(cb)):
                cb[j][1] = (fig.shape[0] - 1) - cb[j][1]
            new_borders.append(cb)
    else:
        new_borders.append(cb)
new_borders.append(borders[-1])
borders = new_borders
# print(['!!', len(borders)])
# print(borders)


# plt.figure()
# plt.imshow(fig, cmap='binary')
# for el in borders:
#    el = np.array(el)
#    plt.plot(el[:,0], el[:,1], 'r')
# plt.show()

# make set of images with separated symbols
symb_list = []
for i in range(len(borders) - 1):
    left = np.array(borders[i])[:, 0].min()
    right = np.array(borders[i + 1])[:, 0].max()
    # print((left, right))
    pl = []
    for el in borders[i] + borders[i + 1][::-1]:
        pl.append((el[0], el[1]))
    # print(pl)
    mask = Image.new('L', (fig.shape[1], fig.shape[0]), color=0)
    ImageDraw.Draw(mask).polygon(pl, fill=1, outline=1)
    mask = np.array(mask)
    symbol = np.array(fig * mask)[:, left:right + 1]

    symb_list.append(symbol)

# for im in symb_list:
#    plt.figure()
#    plt.imshow(im, cmap='binary')

# determine mass center for all symbols
cl = []
for el in symb_list:
    cl.append(symb_points(el)[0])
cl = np.array(cl)
cl = np.argmax(np.bincount(cl)) + 1

# plt.figure()
# plt.imshow(fig, cmap='binary')
# for el in borders:
#    el = np.array(el)
#    plt.plot(el[:,0], el[:,1], 'r')
# plt.plot([0, fig.shape[1]], [cl, cl], 'g')
# plt.show()

# fraction and root detection
exchange = []
for i in range(len(symb_list)):
    if type(symb_list[i]) != str:
        sub_list = root_frac_determiner(symb_list[i])
        if sub_list != None:
            exchange.append([i, sub_list])
for ex in exchange[::-1]:
    symb_list.pop(ex[0])
    for j in range(len(ex[1])):
        symb_list.insert(ex[0] + j, ex[1][j])

# line, i = '', 0
# for p in symb_list:
#    if type(p) != str:
#        i += 1
#        plt.figure()
#        plt.imshow(p, cmap='binary')
#        plt.title(str(i))
#        line = line + '[' + str(i) + ']'
#    else:
#        line = line + p
# print(line)


# up/down index processing and diacritical symbol analyses
symb_list = symb_list  # symbol_composer(symb_list, cl, fig.shape[0])

# complex math expressions composer
symb_list = symb_list  # c_math_expr(symb_list)

# symbol recognition
symb_list = symb_list  #

# redactiong
symb_list = symb_list.sum()
symb_list = symb_list  # final_redaction(symb_list, flag)

print(symb_list)
