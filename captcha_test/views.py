from django.shortcuts import render, HttpResponse
import random
from django.contrib import messages

# Import the following modules
from captcha.image import ImageCaptcha as ICaptcha

# Multicolor Captcha
from multicolorcaptcha import CaptchaGenerator
from PIL import Image, ImageOps, ImageFilter

# time
from datetime import datetime

import os

# database
from captcha_test.models import TextCaptcha, ImageCaptcha


def intro(request):
    return render(request, "intro.html")


def captcha(request):
    print(request.method)
    global now
    now = datetime.now()
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ['50gaji', 'sijakbub', '28 byul', 'sangwane', 'upneun', 'imigiue', 'nayul', '6809 byul', 'sangwane', 'upnun', '38soriue', 'nayul', '1byunjuhagi', 'apsungut', '160826 banbok', '55odokul', 'yudohagi', 'byul', 'godjaneun', 'sangkakel', 'grulssahage', 'byulil inyang', 'daedanhan', 'sangkakul', 'godjaneun', 'gutchurum', 'ssgi', 'gunnu dduigi', '319401 clishe', 'muchim', 'gmgie', 'dojun', 'banggui', 'gguigi', '150967 soum', 'naegi', 'banghae', 'hagi', '11ya!', 'uzzurago!', 'onul', 'cheum', 'bon', 'saramerang', 'death', 'in wegas', 'dudgi', 'cufi', 'masigo',
                 '441283 sulegi', 'yuneahagi', '5115 hoohiehaki', 'ghaguro', 'gusllu', '149028 kaki', 'dasi', 'dolaoziman', '71byulban', 'darlazizi', '177640 aneum', 'gnang', '18 salgi', 'naiki', '80898 runklub', '99gaip', '25.3 giugagi', '25.3', 'banggum', 'ssutdun', 'gut', '26da', 'galaupgi', 'ungdung', '27banga', 'banggem', 'na chutnya', '29aninde', 'jinaganun', 'pungkyung', 'dagaonun', 'pung kyung', 'zzikgi', '31hldlin', 'sajin', '110479 jiugi', '29475 jahae', 'hokeun', 'jaki hyumo', 'ddaddthan', 'ozum', '398nuki', 'muhanhan', 'geung jung', 'jagiae', 'jajongam', '6145mu']
    global str_word
    str_word = random.choice(word_list)
    capt_page_list = ['captcha5.html', 'captcha6.html',
                      'captcha7.html', 'captcha8.html']
    global capt_page
    capt_page = random.choice(capt_page_list)

    if request.method == "POST":
        if len(str_word) > 7:
            capt_list = [
                "ICaptcha",
            ]
        else:
            capt_list = [
                "OnecolorCaptcha",
                "MulticolorCaptcha",
                "GraycolorCaptcha",
                "BluredCaptcha",
                "ContouredCaptcha",
                "EmbosedCaptcha",
                "EdgedCaptcha",
            ]
        # capt_list = ['ImageCaptcha']

        capt = random.choice(capt_list)
        filepath = text_captcha(capt)

        if capt_page == 'captcha5.html':
            logo_list = ["amazon"]
            logo = random.choice(logo_list)

            return render(request, "captcha5.html", {"capt": filepath, "logo": logo})

        elif capt_page == "captcha6.html":
            logo_list = ["google"]
            logo = random.choice(logo_list)

            return render(request, "captcha6.html", {"capt": filepath, "logo": logo})
        elif capt_page == 'captcha7.html':
            logo_list = ["facebook"]
            logo = random.choice(logo_list)

            return render(request, "captcha7.html", {"capt": filepath, "logo": logo})

        elif capt_page == "captcha8.html":
            logo_list = ["google"]
            logo = random.choice(logo_list)
            folder_lists = os.listdir("./static/images/img_captcha/")
            global folder
            folder = random.choice(folder_lists)
            img_path = "./static/images/img_captcha/{}".format(folder)

            img = select_rand_img(img_path)
            folder_path = "static/images/img_captcha_sliced/{}".format(
                folder)
            sliced_img_paths = slice_img(img_path, img, 4, 4, folder_path)

            return render(
                request,
                "captcha8.html",
                {"capt": folder, "logo": logo,
                    "sliced_img_paths": sliced_img_paths},
            )
        else:
            return HttpResponse("<h4>No Return</h4>")
    else:
        return render(request, "intro.html")


def submit(request):
    if request.method == "POST":
        if capt_page == "captcha8.html":
            selected = request.POST.getlist('selected')
            ImageCaptcha(topic=folder, checked_lists=selected,
                         create_date=now).save()
            print(folder, selected)

        else:
            response = request.POST.get('captcha')
            TextCaptcha(answer=str_word, response=response,
                        create_date=now).save()
            print("Answer: {0}, Response: {1}".format(str_word, response))
        return render(request, "intro.html")
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
            box = (j * width, i * height, (j + 1)
                   * width, (i + 1) * height)
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


def captcha5(request):
    now = datetime.now()
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["amazon"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)

    capt_list = [
        "ICaptcha",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt)

    return render(request, "captcha5.html", {"capt": filepath, "logo": logo})


def captcha6(request):
    now = datetime.now()
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["google"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)

    capt_list = [
        "ICaptcha",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt)

    return render(request, "captcha6.html", {"capt": filepath, "logo": logo})


def captcha7(request):
    now = datetime.now()
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["facebook"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)
    capt_list = [
        "ICaptcha",
        "OnecolorCaptcha",
        "MulticolorCaptcha",
        "GraycolorCaptcha",
        "BluredCaptcha",
        "ContouredCaptcha",
        "EmbosedCaptcha",
        "EdgedCaptcha",
    ]
    # capt_list = ['ImageCaptcha']

    capt = random.choice(capt_list)
    filepath = text_captcha(capt)

    return render(request, "captcha7.html", {"capt": filepath, "logo": logo})


def captcha8(request):
    now = datetime.now()
    # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    word_list = ["chicken"]
    logo_list = ["google"]
    global str_word
    str_word = random.choice(word_list)
    logo = random.choice(logo_list)
    folder_lists = os.listdir("./static/images/img_captcha/")
    folder = random.choice(folder_lists)
    img_path = "./static/images/img_captcha/{}".format(folder)

    img = select_rand_img(img_path)
    folder_path = "static/images/img_captcha_sliced/{}".format(str_word)
    sliced_img_paths = slice_img(img_path, img, 4, 4, folder_path)

    return render(
        request,
        "captcha8.html",
        {"capt": folder, "logo": logo, "sliced_img_paths": sliced_img_paths},
    )


def text_captcha(capt):
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

    return filepath

    # def captcha1(request):
    #     num = random.randrange(1021, 9899)
    #     global str_word
    #     str_word = str(num)
    #     return render(request, "captcha1.html", {"capt": str_word})

    # def captcha2(request):
    #     word_list = ["test", "tjdwo", "chicken", "potato", "hamburger"]
    #     global str_word
    #     str_word = random.choice(word_list)
    #     return render(request, "captcha2.html", {"capt": str_word})

    # def captcha3(request):
    #     word_list = ["test", "tjdwo", "chicken", "potato", "hamburger"]
    #     global str_word
    #     str_word = random.choice(word_list)
    #     return render(request, "captcha3.html", {"capt": str_word})

    # def captcha4(request):
    #     now = datetime.now()
    #     # word_list = ['test', 'tjdwo', 'chicken', 'potato', 'hamburger']
    #     word_list = ["chicken"]
    #     logo_list = ["naver", "amazon", "google"]
    #     global str_word
    #     str_word = random.choice(word_list)
    #     logo = random.choice(logo_list)

    #     capt_list = [
    #         "ImageCaptcha",
    #         "OnecolorCaptcha",
    #         "MulticolorCaptcha",
    #         "GraycolorCaptcha",
    #         "BluredCaptcha",
    #         "ContouredCaptcha",
    #         "EmbosedCaptcha",
    #         "EdgedCaptcha",
    #     ]
    #     # capt_list = ['ImageCaptcha']

    #     capt = random.choice(capt_list)
    #     filepath = text_captcha(capt)

    #     print(capt)
    #     print(str_word)

    #     return render(request, "captcha4.html", {"capt": filepath, "logo": logo})
