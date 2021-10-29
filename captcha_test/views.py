from django.shortcuts import render, HttpResponse
import random
from django.contrib import messages
from collections import deque

# Import the following modules
from captcha.image import ImageCaptcha as ICaptcha

# Multicolor Captcha
from multicolorcaptcha import CaptchaGenerator
from PIL import Image, ImageOps, ImageFilter

# time
from datetime import datetime
import time

import os

# database
from captcha_test.models import TextCaptcha, ImageCaptcha

# 3D modeling
from random import uniform, shuffle, randint
from PIL import ImageFont, Image, ImageDraw
import numpy as np
import pylab
from mpl_toolkits.mplot3d import Axes3D

# cv2
import cv2

error_count = 0
word_list = [
    "50gaji",
    "sijakbub",
    "28 byul",
    "sangwane",
    "upneun",
    "imigiue",
    "nayul",
    "6809 byul",
    "sangwane",
    "upnun",
    "38soriue",
    "nayul",
    "1byunjuhagi",
    "apsungut",
    "160826 banbok",
    "55odokul",
    "yudohagi",
    "byul",
    "godjaneun",
    "sangkakel",
    "grulssahage",
    "byulil inyang",
    "daedanhan",
    "sangkakul",
    "godjaneun",
    "gutchurum",
    "ssgi",
    "gunnu dduigi",
    "319401 clishe",
    "muchim",
    "gmgie",
    "dojun",
    "banggui",
    "gguigi",
    "150967 soum",
    "naegi",
    "banghae",
    "hagi",
    "11ya!",
    "uzzurago!",
    "onul",
    "cheum",
    "bon",
    "saramerang",
    "death",
    "in wegas",
    "dudgi",
    "cufi",
    "masigo",
    "441283 sulegi",
    "yuneahagi",
    "5115 hoohiehaki",
    "ghaguro",
    "gusllu",
    "149028 kaki",
    "dasi",
    "dolaoziman",
    "71byulban",
    "darlazizi",
    "177640 aneum",
    "gnang",
    "18 salgi",
    "naiki",
    "80898 runklub",
    "99gaip",
    "25.3 giugagi",
    "25.3",
    "banggum",
    "ssutdun",
    "gut",
    "26da",
    "galaupgi",
    "ungdung",
    "27banga",
    "banggem",
    "na chutnya",
    "29aninde",
    "jinaganun",
    "pungkyung",
    "dagaonun",
    "pung kyung",
    "zzikgi",
    "31hldlin",
    "sajin",
    "110479 jiugi",
    "29475 jahae",
    "hokeun",
    "jaki hyumo",
    "ddaddthan",
    "ozum",
    "398nuki",
    "muhanhan",
    "geung jung",
    "jagiae",
    "jajongam",
    "6145mu",
]
queue = deque(word_list)
str_list = [
    "첫",
    "두",
    "세",
    "네",
    "다섯",
    "여섯",
    "일곱",
    "여덟",
    "아홉",
    "열",
    "열한",
    "열두",
    "열세",
    "열네",
    "열다섯",
    "열여섯",
    "열일곱",
    "열여덟",
    "열아홉",
    "스물",
]
str_list2 = ["첫", "두", "세", "네", "다섯", "여섯"]


def intro(request):
    return render(request, "intro.html")


def captcha(request):
    global now
    now = datetime.now()
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    global queue
    global str_word
    global logo
    global right_str
    global wrong_str
    right_str = "시의 {} 번째 줄 {} 번째 단어는 남아있습니다.".format(
        random.choice(str_list), random.choice(str_list2)
    )
    wrong_str = "시의 {} 번째 줄 {} 번째 단어는 사라졌습니다.".format(
        random.choice(str_list), random.choice(str_list2)
    )
    capt_page_list = [
        "captcha1.html",
        "captcha3.html",
        "captcha4.html",
        "captcha5.html",
        "captcha6.html",
        "captcha7.html",
        "captcha8.html",
        "captcha9.html",
        "captcha10.html",
        "captcha11.html",
        "captcha12.html",
    ]
    if request.method == "POST":
        global capt_page
        capt_page = random.choice(capt_page_list)
        if capt_page == "captcha8.html":
            logo_list = ["google"]
            logo = random.choice(logo_list)
            folder_lists = os.listdir("./static/images/img_captcha/")
            global folder
            folder = random.choice(folder_lists)
            img_path = "./static/images/img_captcha/{}".format(folder)

            img = select_rand_img(img_path)
            folder_path = "static/images/img_captcha_sliced/{}".format(folder)
            sliced_img_paths = slice_img(img_path, img, 4, 4, folder_path)

            return render(
                request,
                "captcha8.html",
                {
                    "capt": folder,
                    "logo": logo,
                    "sliced_img_paths": sliced_img_paths,
                },
            )
        else:
            if len(queue) == 0:
                queue = deque(word_list)
            else:
                pass
            str_word = queue.popleft()
            global capt_list
            capt_len = len(str_word)
            if len(str_word) > 7:
                capt_list = [
                    "ICaptcha",
                    "Gimpy",
                    "BWLDistImage",
                    "BWLSPImage",
                    "BWLLensImage",
                ]
            else:
                if len(str_word) > 6:
                    capt_list = [
                        "ICaptcha",
                        "Gimpy",
                        "BWLDistImage",
                        "BWLSPImage",
                        "BWLLensImage",
                        "OnecolorCaptcha",
                        "MulticolorCaptcha",
                        "GraycolorCaptcha",
                        "EdgedCaptcha",
                        "3dCaptcha",
                    ]
                else:
                    capt_list = [
                        "ICaptcha",
                        "Gimpy",
                        "BWLDistImage",
                        "BWLSPImage",
                        "BWLLensImage",
                        "OnecolorCaptcha",
                        "MulticolorCaptcha",
                        "GraycolorCaptcha",
                        "BluredCaptcha",
                        "ContouredCaptcha",
                        "EmbosedCaptcha",
                        "EdgedCaptcha",
                        "3dCaptcha",
                    ]
            capt = random.choice(capt_list)
            filepath = text_captcha(capt, str_word)
            logo_list = ["amazon", "naver", "google", "facebook"]

            if capt_page == "captcha1.html":
                logo = "yahoo"

                return render(
                    request,
                    "captcha1.html",
                    {
                        "str_word": str_word,
                        "capt": filepath,
                        "logo": logo,
                        "right_str": right_str,
                        "wrong_str": wrong_str,
                    },
                )
            elif capt_page == "captcha2.html":
                logo = "naver"

                return render(
                    request,
                    "captcha2.html",
                    {
                        "str_word": str_word,
                        "capt": filepath,
                        "logo": logo,
                        "right_str": right_str,
                        "wrong_str": wrong_str,
                    },
                )
            elif capt_page == "captcha3.html":

                return render(
                    request,
                    "captcha3.html",
                    {
                        "str_word": str_word,
                        "capt": filepath,
                        "right_str": right_str,
                        "wrong_str": wrong_str,
                    },
                )

            elif capt_page == "captcha4.html":

                return render(
                    request,
                    "captcha4.html",
                    {
                        "str_word": str_word,
                        "capt": filepath,
                        "right_str": right_str,
                        "wrong_str": wrong_str,
                    },
                )
            elif capt_page == "captcha5.html":
                logo = "amazon"

                return render(
                    request,
                    "captcha5.html",
                    {
                        "str_word": str_word,
                        "capt": filepath,
                        "logo": logo,
                        "right_str": right_str,
                        "wrong_str": wrong_str,
                    },
                )
            elif capt_page == "captcha6.html":
                logo = random.choice(logo_list)

                return render(
                    request,
                    "captcha6.html",
                    {
                        "str_word": str_word,
                        "capt": filepath,
                        "logo": logo,
                        "right_str": right_str,
                        "wrong_str": wrong_str,
                    },
                )
            elif capt_page == "captcha7.html":
                logo = "facebook"

                return render(
                    request,
                    "captcha7.html",
                    {
                        "str_word": str_word,
                        "capt": filepath,
                        "logo": logo,
                        "right_str": right_str,
                        "wrong_str": wrong_str,
                    },
                )
            elif capt_page == "captcha9.html":
                logo = "facebook"

                return render(
                    request,
                    "captcha9.html",
                    {
                        "str_word": str_word,
                        "capt": filepath,
                        "logo": logo,
                        "right_str": right_str,
                        "wrong_str": wrong_str,
                    },
                )

            elif capt_page == "captcha10.html":
                logo = "facebook"

                return render(
                    request,
                    "captcha10.html",
                    {
                        "str_word": str_word,
                        "capt": filepath,
                        "logo": logo,
                        "capt_len": capt_len,
                        "right_str": right_str,
                        "wrong_str": wrong_str,
                    },
                )
            elif capt_page == "captcha11.html":
                logo = "facebook"

                return render(
                    request,
                    "captcha11.html",
                    {
                        "str_word": str_word,
                        "capt": filepath,
                        "logo": logo,
                        "capt_len": capt_len,
                        "right_str": right_str,
                        "wrong_str": wrong_str,
                    },
                )
            elif capt_page == "captcha12.html":
                logo = "facebook"

                return render(
                    request,
                    "captcha12.html",
                    {
                        "str_word": str_word,
                        "capt": filepath,
                        "logo": logo,
                        "right_str": right_str,
                        "wrong_str": wrong_str,
                    },
                )
            else:
                return HttpResponse("<h4>No Return</h4>")
    else:
        return render(request, "intro.html")


def submit(request):
    global error_count

    if request.method == "POST":
        if capt_page == "captcha8.html":
            global selected
            selected = request.POST.getlist("selected")
            ImageCaptcha(
                topic=folder, checked_lists=selected, create_date=now
            ).save()
            return render(request, "intro.html")

        else:
            response = request.POST.get("captcha").lower()
            TextCaptcha(
                answer=str_word, response=response, create_date=now
            ).save()

            if str_word == response:

                time.sleep(3)
                return render(
                    request,
                    "intro.html",
                    {
                        "right_str": right_str,
                    },
                )
            else:

                # if error_count < 2:
                #     error_count += 1

                #     capt = random.choice(capt_list)
                #     filepath = text_captcha(capt, str_word)
                #     time.sleep(2)
                #     return render(
                #         request,
                #         capt_page,
                #         {
                #             "str_word": str_word,
                #             "capt": filepath,
                #             "logo": logo,
                #             "wrong_str": wrong_str,
                #         },
                #     )
                # else:
                time.sleep(3)
                # error_count = 0
                return render(request, "intro.html", {"wrong_str": wrong_str})

    else:
        return render(request, "intro.html")


def select_rand_imgs(img_path):
    img_names = os.listdir(img_path)

    return img_names


def select_rand_img(img_path):
    img_names = os.listdir(img_path)
    img = random.choice(img_names)

    return img


def slice_img(img_path, input, xPieces, yPieces, save_dir):
    img_paths = []
    filename, file_extension = os.path.splitext(input)
    im = Image.open(os.path.join(img_path, input))
    imgwidth, imgheight = im.size
    height = imgheight // yPieces
    width = imgwidth // xPieces
    for i in range(0, yPieces):
        for j in range(0, xPieces):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            a = im.crop(box)
            try:
                img_path = os.path.join(
                    save_dir, f"{filename}_{i}_{j}{file_extension}"
                )
                img_paths.append(img_path)
                a.save(img_path)
            except:
                pass
    return img_paths


def makeGimpyImage(text):
    text = text.lower()
    text_splited = text.split(" ")

    gimpy_path = "./static/images/gimpy/"
    gimpy_lists = os.listdir(gimpy_path)
    gimpy = Image.open(os.path.join(gimpy_path, random.choice(gimpy_lists)))
    FONTS_PATH = "static/fonts"
    fonts_lists = []

    for root, directories, files in os.walk(FONTS_PATH, topdown=True):
        for file in files:
            f_name, f_ext = os.path.splitext(file)
            if f_ext == ".ttf":
                fonts_lists.append(os.path.join(root, file))

    draw = ImageDraw.Draw(gimpy)

    if len(text_splited) > 1:
        width1 = 0
        width2 = 40
        for i in range(len(text_splited)):
            width = randint(width1, width2)
            height = randint(0, 140)
            font = ImageFont.truetype(random.choice(fonts_lists), 42)
            draw.text(
                (width, height), text_splited[i], (255, 255, 255), font=font
            )
            width1 += 100
            width2 += 170
    else:
        width = randint(0, 80)
        height = randint(0, 140)
        font = ImageFont.truetype(random.choice(fonts_lists), 42)
        draw.text((width, height), text_splited[0], (255, 255, 255), font=font)

    filepath = "static/images/captcha/{}_{}.png".format(
        text, now.strftime("%H_%M_%S")
    )

    color_lists = [
        "#E0D7FF",
        "#FFCCE1",
        "#D7EEFF",
        "#FAFFC7",
        "#ffb3ba",
        "#ffdfba",
        "#ffffba",
        "#baffc9",
        "#bae1ff",
    ]
    line_color = random.choice(color_lists)
    create_noise_curve(gimpy, line_color)
    add_rand_line_to_image(gimpy, line_color=line_color)

    gimpy.save(filepath)

    return filepath


def makeBWImage(text):
    FONTS_PATH = "static/fonts"
    fonts_lists = []
    for root, directories, files in os.walk(FONTS_PATH, topdown=True):
        for file in files:
            f_name, f_ext = os.path.splitext(file)
            if f_ext == ".ttf":
                fonts_lists.append(os.path.join(root, file))

    text = text.lower()
    text_splited = text.split(" ")

    image = Image.new("RGBA", (512, 256), (255, 255, 255))
    font = ImageFont.truetype(random.choice(fonts_lists), 26)
    draw = ImageDraw.Draw(image)

    width = randint(0, 80)
    height = randint(0, 40)
    text = text.lower()
    if len(text_splited) > 1:
        width1 = 0
        width2 = 70
        for i in range(len(text_splited)):
            width = randint(width1, width2)
            height = randint(0, 180)
            font = ImageFont.truetype(random.choice(fonts_lists), 48)
            draw.text((width, height), text_splited[i], (0, 0, 0), font=font)
            width1 += 150
            width2 += 130
    else:
        width = randint(0, 150)
        height = randint(0, 180)
        font = ImageFont.truetype(random.choice(fonts_lists), 48)
        draw.text((width, height), text_splited[0], (0, 0, 0), font=font)

    filepath = "static/images/captcha/{}_{}.png".format(
        text, now.strftime("%H_%M_%S")
    )

    image.save(filepath)
    return filepath


def makeBWLDistImage(text):
    FONTS_PATH = "static/fonts"
    fonts_lists = []
    for root, directories, files in os.walk(FONTS_PATH, topdown=True):
        for file in files:
            f_name, f_ext = os.path.splitext(file)
            if f_ext == ".ttf":
                fonts_lists.append(os.path.join(root, file))

    text = text.lower()
    text_splited = text.split(" ")

    image = Image.new("RGBA", (512, 256), (255, 255, 255))
    font = ImageFont.truetype(random.choice(fonts_lists), 26)
    draw = ImageDraw.Draw(image)

    width = randint(0, 80)
    height = randint(0, 40)
    if len(text_splited) > 1:
        width1 = 0
        width2 = 70
        for i in range(len(text_splited)):
            width = randint(width1, width2)
            height = randint(0, 180)
            font = ImageFont.truetype(random.choice(fonts_lists), 48)
            draw.text((width, height), text_splited[i], (0, 0, 0), font=font)
            width1 += 150
            width2 += 130
    else:
        width = randint(0, 150)
        height = randint(0, 180)
        font = ImageFont.truetype(random.choice(fonts_lists), 48)
        draw.text((width, height), text_splited[0], (0, 0, 0), font=font)

    filepath = "static/images/captcha/{}_{}.png".format(
        text, now.strftime("%H_%M_%S")
    )
    color_lists = [
        "#E0D7FF",
        "#FFCCE1",
        "#D7EEFF",
        "#FAFFC7",
        "#ffb3ba",
        "#ffdfba",
        "#ffffba",
        "#baffc9",
        "#bae1ff",
    ]
    line_color = random.choice(color_lists)
    create_noise_curve(image, line_color)
    add_rand_line_to_image(image, line_color=line_color)
    create_noise_curve(image, line_color)
    add_rand_line_to_image(image, line_width=4, line_color=line_color)

    image.save(filepath)
    img = cv2.imread(filepath, 0)

    rows, cols = img.shape[:2]

    # ---① 설정 값 셋팅
    exp = round(
        random.uniform(0.5, 2), 1
    )  # 볼록, 오목 지수 (오목 : 0.1 ~ 1, 볼록 : 1.1~)
    scale = 1  # 변환 영역 크기 (0 ~ 1)

    # 매핑 배열 생성 ---②
    mapy, mapx = np.indices((rows, cols), dtype=np.float32)

    # 좌상단 기준좌표에서 -1~1로 정규화된 중심점 기준 좌표로 변경 ---③
    mapx = 2 * mapx / (cols - 1) - 1
    mapy = 2 * mapy / (rows - 1) - 1

    # 직교좌표를 극 좌표로 변환 ---④
    r, theta = cv2.cartToPolar(mapx, mapy)

    # 왜곡 영역만 중심확대/축소 지수 적용 ---⑤
    r[r < scale] = r[r < scale] ** exp

    # 극 좌표를 직교좌표로 변환 ---⑥
    mapx, mapy = cv2.polarToCart(r, theta)

    # 중심점 기준에서 좌상단 기준으로 변경 ---⑦
    mapx = ((mapx + 1) * cols - 1) / 2
    mapy = ((mapy + 1) * rows - 1) / 2
    # 재매핑 변환
    distorted = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # cv2.imwrite(filepath, img_sinx)
    # cv2.imwrite(filepath, img_cosy)
    cv2.imwrite(filepath, distorted)

    return filepath


def makeBWLSPImage(text):
    FONTS_PATH = "static/fonts"
    fonts_lists = []
    for root, directories, files in os.walk(FONTS_PATH, topdown=True):
        for file in files:
            f_name, f_ext = os.path.splitext(file)
            if f_ext == ".ttf":
                fonts_lists.append(os.path.join(root, file))

    text = text.lower()
    text_splited = text.split(" ")

    image = Image.new("RGBA", (512, 256), (255, 255, 255))
    font = ImageFont.truetype(random.choice(fonts_lists), 26)
    draw = ImageDraw.Draw(image)

    width = randint(0, 80)
    height = randint(0, 40)
    text = text.lower()
    if len(text_splited) > 1:
        width1 = 0
        width2 = 70
        for i in range(len(text_splited)):
            width = randint(width1, width2)
            height = randint(0, 180)
            font = ImageFont.truetype(random.choice(fonts_lists), 48)
            draw.text((width, height), text_splited[i], (0, 0, 0), font=font)
            width1 += 150
            width2 += 130
    else:
        width = randint(0, 150)
        height = randint(0, 180)
        font = ImageFont.truetype(random.choice(fonts_lists), 48)
        draw.text((width, height), text_splited[0], (0, 0, 0), font=font)

    filepath = "static/images/captcha/{}_{}.png".format(
        text, now.strftime("%H_%M_%S")
    )
    color_lists = [
        "#bae1ff",
    ]
    line_color = random.choice(color_lists)
    create_noise_curve(image, line_color)
    add_rand_line_to_image(image, line_color=line_color)

    image.save(filepath)
    img = cv2.imread(filepath, 0)
    row, col = img.shape

    # Randomly pick some pixels in the
    # image for coloring them white
    # Pick a random number between 300 and 10000
    number_of_pixels = random.randint(3000, 10000)
    for i in range(number_of_pixels):

        # Pick a random y coordinate
        y_coord = random.randint(0, row - 1)

        # Pick a random x coordinate
        x_coord = random.randint(0, col - 1)

        # Color that pixel to white
        img[y_coord][x_coord] = 255

    # Randomly pick some pixels in
    # the image for coloring them black
    # Pick a random number between 300 and 10000
    number_of_pixels = random.randint(3000, 10000)
    for i in range(number_of_pixels):

        # Pick a random y coordinate
        y_coord = random.randint(0, row - 1)

        # Pick a random x coordinate
        x_coord = random.randint(0, col - 1)

        # Color that pixel to black
        img[y_coord][x_coord] = 0
    cv2.imwrite(filepath, img)

    return filepath


def makeBWLLensImage(text):
    FONTS_PATH = "static/fonts"
    fonts_lists = []
    for root, directories, files in os.walk(FONTS_PATH, topdown=True):
        for file in files:
            f_name, f_ext = os.path.splitext(file)
            if f_ext == ".ttf":
                fonts_lists.append(os.path.join(root, file))

    text = text.lower()
    text_splited = text.split(" ")

    image = Image.new("RGBA", (512, 256), (255, 255, 255))
    font = ImageFont.truetype(random.choice(fonts_lists), 26)
    draw = ImageDraw.Draw(image)

    width = randint(0, 80)
    height = randint(0, 40)
    text = text.lower()
    if len(text_splited) > 1:
        width1 = 0
        width2 = 70
        for i in range(len(text_splited)):
            width = randint(width1, width2)
            height = randint(0, 180)
            font = ImageFont.truetype(random.choice(fonts_lists), 48)
            draw.text((width, height), text_splited[i], (0, 0, 0), font=font)
            width1 += 150
            width2 += 130
    else:
        width = randint(0, 150)
        height = randint(0, 180)
        font = ImageFont.truetype(random.choice(fonts_lists), 48)
        draw.text((width, height), text_splited[0], (0, 0, 0), font=font)

    filepath = "static/images/captcha/{}_{}.png".format(
        text, now.strftime("%H_%M_%S")
    )
    color_lists = [
        "#bae1ff",
    ]
    line_color = random.choice(color_lists)
    create_noise_curve(image, line_color)
    create_noise_curve(image, line_color)
    add_rand_line_to_image(image, line_color=line_color)
    add_rand_line_to_image(image, line_width=4, line_color=line_color)

    image.save(filepath)
    img = cv2.imread(filepath, 0)

    l = randint(20, 25)  # 파장(wave length)
    amp = randint(5, 8)  # 진폭(amplitude)

    rows, cols = img.shape[:2]

    # 초기 매핑 배열 생성 ---①
    mapy, mapx = np.indices((rows, cols), dtype=np.float32)

    # sin, cos 함수를 적용한 변형 매핑 연산 ---②
    sinx = mapx + amp * np.sin(mapy / l)
    cosy = mapy + amp * np.cos(mapx / l)

    # 영상 매핑 ---③

    img_sinx = cv2.remap(img, sinx, mapy, cv2.INTER_LINEAR)  # x축만 sin 곡선 적용
    img_cosy = cv2.remap(img, mapx, cosy, cv2.INTER_LINEAR)  # y축만 cos 곡선 적용
    # x,y 축 모두 sin, cos 곡선 적용 및 외곽 영역 보정
    img_both = cv2.remap(
        img, sinx, cosy, cv2.INTER_LINEAR, None, cv2.BORDER_REPLICATE
    )

    # cv2.imwrite(filepath, img_sinx)
    # cv2.imwrite(filepath, img_cosy)
    cv2.imwrite(filepath, img_both)

    return filepath


def makeImage(text, width=512, height=200, angle=None):
    angle = angle if angle != None else uniform(-50, 10)
    try:
        font = ImageFont.truetype(
            "static/fonts/GoogleFonts/ofl/graduate/Graduate-Regular.ttf",
            25,
        )
    except IOError:
        raise IOError(
            "Font file doesn't exist. Please set `fontPath` correctly."
        )
    txtW, txtH = font.getsize(text)
    img = Image.new("L", (txtW * 3, txtH * 3), 255)
    drw = ImageDraw.Draw(img)
    drw.text((txtW, txtH), text, font=font)

    fig = pylab.figure(figsize=(width / 120.0, height / 50.0))
    ax = Axes3D(fig)
    X, Y = np.meshgrid(range(img.size[0]), range(img.size[1]))
    Z = 1 - np.asarray(img) / 255
    ax.plot_wireframe(X, -Y, Z, rstride=1, cstride=1)
    ax.set_zlim((-3, 3))
    ax.set_xlim((txtW * 1.1, txtW * 1.9))
    ax.set_ylim((-txtH * 1.9, -txtH * 1.1))
    ax.set_axis_off()
    ax.view_init(elev=40, azim=-60 + angle)
    filepath = "static/images/captcha//{}_{}.png".format(
        text, now.strftime("%H_%M_%S")
    )
    fig.savefig(filepath)

    return filepath


def text_captcha(capt, str_word):
    now = datetime.now()

    if capt == "ICaptcha":
        # Create an image instance of the gicen size
        image = ICaptcha(width=280, height=90)
        capt_text = str_word
        # generate the image of the given text
        data = image.generate(capt_text)
        filepath = "static/images/captcha/{0}_{1}.png".format(
            str_word, now.strftime("%H_%M_%S")
        )

        # write the image on the given file and save it
        image.write(capt_text, filepath)

    elif capt == "Gimpy":
        filepath = makeGimpyImage(str_word)

    elif capt == "BWLDistImage":
        filepath = makeBWLDistImage(str_word)

    elif capt == "BWLSPImage":
        filepath = makeBWLSPImage(str_word)

    elif capt == "BWLLensImage":
        filepath = makeBWLLensImage(str_word)

    elif capt == "OnecolorCaptcha":
        # Captcha image size number (2 -> 640x360)
        CAPCTHA_SIZE_NUM = 2

        # Create Captcha Generator object of specified size
        generator = CaptchaGenerator(CAPCTHA_SIZE_NUM)

        # Generate a captcha image
        captcha = generator.gen_captcha_image(
            chars_mode="custom", input_text=str_word, difficult_level=1
        )

        # Get information of standard captcha
        image = captcha["image"]
        characters = captcha["characters"]
        # Save the images to files
        filepath = "static/images/captcha/{0}_{1}.png".format(
            str_word, now.strftime("%H_%M_%S")
        )
        image.save(filepath, "png")

    elif capt == "MulticolorCaptcha":
        # Captcha image size number (2 -> 640x360)
        CAPCTHA_SIZE_NUM = 2

        # Create Captcha Generator object of specified size
        generator = CaptchaGenerator(CAPCTHA_SIZE_NUM)

        # Generate a captcha image
        captcha = generator.gen_captcha_image(
            chars_mode="custom",
            input_text=str_word,
            difficult_level=1,
            multicolor=True,
        )

        # Get information of standard captcha
        image = captcha["image"]
        characters = captcha["characters"]
        # Save the images to files
        filepath = "static/images/captcha/{0}_{1}.png".format(
            str_word, now.strftime("%H_%M_%S")
        )
        image.save(filepath, "png")

    elif capt == "GraycolorCaptcha":
        # Captcha image size number (2 -> 640x360)
        CAPCTHA_SIZE_NUM = 2

        # Create Captcha Generator object of specified size
        generator = CaptchaGenerator(CAPCTHA_SIZE_NUM)

        true_false = [True, False]
        multicolor = random.choice(true_false)

        # Generate a captcha image
        captcha = generator.gen_captcha_image_gray(
            chars_mode="custom",
            input_text=str_word,
            difficult_level=1,
            multicolor=multicolor,
        )

        # Get information of standard captcha
        image = captcha["image"]
        characters = captcha["characters"]
        # Save the images to files
        filepath = "static/images/captcha/{0}_{1}.png".format(
            str_word, now.strftime("%H_%M_%S")
        )
        image.save(filepath, "png")

    elif capt == "BluredCaptcha":
        # Captcha image size number (2 -> 640x360)
        CAPCTHA_SIZE_NUM = 2

        # Create Captcha Generator object of specified size
        generator = CaptchaGenerator(CAPCTHA_SIZE_NUM)

        true_false = [True, False]
        multicolor = random.choice(true_false)

        # Generate a captcha image
        captcha = generator.gen_captcha_image(
            chars_mode="custom",
            input_text=str_word,
            difficult_level=1,
            multicolor=multicolor,
        )

        # Get information of standard captcha
        image = captcha["image"].filter(ImageFilter.BLUR)
        characters = captcha["characters"]
        # Save the images to files
        filepath = "static/images/captcha/{0}_{1}.png".format(
            str_word, now.strftime("%H_%M_%S")
        )
        image.save(filepath, "png")

    elif capt == "ContouredCaptcha":
        # Captcha image size number (2 -> 640x360)
        CAPCTHA_SIZE_NUM = 2

        # Create Captcha Generator object of specified size
        generator = CaptchaGenerator(CAPCTHA_SIZE_NUM)

        true_false = [True, False]
        multicolor = random.choice(true_false)

        # Generate a captcha image
        captcha = generator.gen_captcha_image(
            chars_mode="custom",
            input_text=str_word,
            difficult_level=1,
            multicolor=multicolor,
        )

        # Get information of standard captcha
        image = captcha["image"].filter(ImageFilter.CONTOUR)
        characters = captcha["characters"]
        # Save the images to files
        filepath = "static/images/captcha/{0}_{1}.png".format(
            str_word, now.strftime("%H_%M_%S")
        )
        image.save(filepath, "png")

    elif capt == "EmbosedCaptcha":
        # Captcha image size number (2 -> 640x360)
        CAPCTHA_SIZE_NUM = 2

        # Create Captcha Generator object of specified size
        generator = CaptchaGenerator(CAPCTHA_SIZE_NUM)

        true_false = [True, False]
        multicolor = random.choice(true_false)

        # Generate a captcha image
        captcha = generator.gen_captcha_image_gray(
            chars_mode="custom",
            input_text=str_word,
            difficult_level=1,
            multicolor=multicolor,
        )

        # Get information of standard captcha
        image = captcha["image"].filter(ImageFilter.EMBOSS)
        characters = captcha["characters"]
        # Save the images to files
        filepath = "static/images/captcha/{0}_{1}.png".format(
            str_word, now.strftime("%H_%M_%S")
        )
        image.save(filepath, "png")

    elif capt == "EdgedCaptcha":
        # Captcha image size number (2 -> 640x360)
        CAPCTHA_SIZE_NUM = 2

        # Create Captcha Generator object of specified size
        generator = CaptchaGenerator(CAPCTHA_SIZE_NUM)

        true_false = [True, False]
        multicolor = random.choice(true_false)

        # Generate a captcha image
        captcha = generator.gen_captcha_image_gray(
            chars_mode="custom",
            input_text=str_word,
            difficult_level=1,
            multicolor=multicolor,
        )

        # Get information of standard captcha
        image = captcha["image"].filter(ImageFilter.FIND_EDGES)
        characters = captcha["characters"]
        # Save the images to files
        filepath = "static/images/captcha/{0}_{1}.png".format(
            str_word, now.strftime("%H_%M_%S")
        )
        image.save(filepath, "png")

    elif capt == "3dCaptcha":
        filepath = makeImage(str_word)

    return filepath


def add_rand_line_to_image(
    image, line_width=2, line_color="rgb(224, 187, 228)"
):
    """Draw a random line to a PIL image."""
    # Get line random start position
    line_x0 = randint(0, image.width)
    line_y0 = randint(0, image.height)
    # If line x0 is in center-to-right
    if line_x0 >= image.width / 2:
        # Line x1 from 0 to line_x0 position - 20% of image width
        line_x1 = randint(0, line_x0 - int(0.2 * image.width))
    else:
        # Line x1 from line_x0 position + 20% of image width to max image width
        line_x1 = randint(line_x0 + int(0.2 * image.width), image.width)
    # If line y0 is in center-to-bottom
    if line_y0 >= image.height / 2:
        # Line y1 from 0 to line_y0 position - 20% of image height
        line_y1 = randint(0, line_y0 - int(0.2 * image.height))
    else:
        # Line y1 from line_y0 position + 20% of image height to max image height
        line_y1 = randint(line_y0 + int(0.2 * image.height), image.height)
    # Generate a rand line color if not provided
    # if line_color == "notSet":
    #     line_color = "rgb({}, {}, {})".format(
    #         str(randint(0, 255)), str(randint(0, 255)), str(randint(0, 255))
    #     )
    # Get image draw interface and draw the line on it
    draw = ImageDraw.Draw(image)
    draw.line(
        (line_x0, line_y0, line_x1, line_y1),
        fill=line_color,
        width=line_width,
    )


def add_rand_horizontal_line_to_image(
    image, line_width=2, line_color="rgb(224, 187, 228)"
):
    """Draw a random line to a PIL image."""
    # Get line random start position (x between 0 and 20% image width; y with full height range)
    x0 = randint(0, int(0.2 * image.width))
    y0 = randint(0, image.height)
    # Get line end position (x1 symetric to x0; y random from y0 to image height)
    x1 = image.width - x0
    y1 = randint(y0, image.height)
    # Generate a rand line color if not provided
    # if line_color == "notSet":
    #     line_color = "rgb({}, {}, {})".format(
    #         str(randint(0, 255)), str(randint(0, 255)), str(randint(0, 255))
    #     )
    # Get image draw interface and draw the line on it
    draw = ImageDraw.Draw(image)
    draw.line((x0, y0, x1, y1), fill=line_color, width=5)


def create_noise_curve(image, color):
    w, h = image.size
    x1 = random.randint(0, int(w / 5))
    x2 = random.randint(w - int(w / 5), w)
    y1 = random.randint(int(h / 5), h - int(h / 5))
    y2 = random.randint(y1, h - int(h / 5))
    points = [x1, y1, x2, y2]
    end = random.randint(160, 200)
    start = random.randint(0, 20)
    ImageDraw.Draw(image).arc(points, start, end, fill=color)
    return image


def captcha1(request):
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["amazon"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)

    capt_list = [
        "ICaptcha",
        "Gimpy",
        "BWLDistImage",
        "BWLSPImage",
        "BWLLensImage",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
        "3dCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt, str_word)

    return render(request, "captcha1.html", {"capt": filepath, "logo": logo})


def captcha2(request):
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["naver"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)

    capt_list = [
        "ICaptcha",
        "Gimpy",
        "BWLDistImage",
        "BWLSPImage",
        "BWLLensImage",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
        "3dCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt, str_word)

    return render(request, "captcha2.html", {"capt": filepath, "logo": logo})


def captcha3(request):
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["naver"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)

    capt_list = [
        "ICaptcha",
        "Gimpy",
        "BWLDistImage",
        "BWLSPImage",
        "BWLLensImage",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
        "3dCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt, str_word)

    return render(request, "captcha3.html", {"capt": filepath, "logo": logo})


def captcha4(request):
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["naver"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)

    capt_list = [
        "ICaptcha",
        "Gimpy",
        "BWLDistImage",
        "BWLSPImage",
        "BWLLensImage",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
        "3dCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt, str_word)

    return render(request, "captcha4.html", {"capt": filepath, "logo": logo})


def captcha5(request):
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["amazon"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)

    capt_list = [
        "ICaptcha",
        "Gimpy",
        "BWLDistImage",
        "BWLSPImage",
        "BWLLensImage",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
        "3dCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt, str_word)

    return render(request, "captcha5.html", {"capt": filepath, "logo": logo})


def captcha6(request):
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["google"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)

    capt_list = [
        "ICaptcha",
        "Gimpy",
        "BWLDistImage",
        "BWLSPImage",
        "BWLLensImage",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
        "3dCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt, str_word)

    return render(request, "captcha6.html", {"capt": filepath, "logo": logo})


def captcha7(request):
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["facebook"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)
    capt_list = [
        "ICaptcha",
        "Gimpy",
        "BWLDistImage",
        "BWLSPImage",
        "BWLLensImage",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
        "3dCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt, str_word)

    return render(request, "captcha7.html", {"capt": filepath, "logo": logo})


def captcha9(request):
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["facebook"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)
    capt_list = [
        "ICaptcha",
        "Gimpy",
        "BWLDistImage",
        "BWLSPImage",
        "BWLLensImage",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
        "3dCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt, str_word)

    return render(request, "captcha9.html", {"capt": filepath, "logo": logo})


def captcha10(request):
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["facebook"]
    global str_word
    str_word = random.choice(word_list)
    capt_len = len(str_word)
    logo = random.choice(logo_list)
    capt_list = [
        "ICaptcha",
        "Gimpy",
        "BWLDistImage",
        "BWLSPImage",
        "BWLLensImage",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
        "3dCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt, str_word)

    return render(
        request,
        "captcha10.html",
        {"capt": filepath, "capt_len": capt_len, "logo": logo},
    )


def captcha11(request):
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["facebook"]
    global str_word
    capt_len = len(str_word)
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)
    capt_list = [
        "ICaptcha",
        "Gimpy",
        "BWLDistImage",
        "BWLSPImage",
        "BWLLensImage",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
        "3dCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt, str_word)

    return render(
        request,
        "captcha11.html",
        {"capt": filepath, "capt_len": capt_len, "logo": logo},
    )


def captcha12(request):
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["facebook"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)
    capt_list = [
        "ICaptcha",
        "Gimpy",
        "BWLDistImage",
        "BWLSPImage",
        "BWLLensImage",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
        "3dCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt, str_word)

    return render(request, "captcha12.html", {"capt": filepath, "logo": logo})


def captcha8(request):
    logo_list = ["google"]
    logo = random.choice(logo_list)
    folder_lists = os.listdir("./static/images/img_captcha/")
    folder = random.choice(folder_lists)
    img_path = "./static/images/img_captcha/{}".format(folder)

    img = select_rand_img(img_path)
    folder_path = "static/images/img_captcha_sliced/{}".format(folder)
    sliced_img_paths = slice_img(img_path, img, 4, 4, folder_path)

    return render(
        request,
        "captcha8.html",
        {"capt": folder, "logo": logo, "sliced_img_paths": sliced_img_paths},
    )
