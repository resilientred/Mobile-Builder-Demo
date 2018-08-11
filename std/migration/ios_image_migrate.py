# Create Content.json for LOGO-SET
import json
import os
import shutil

from std.std import merge


SCALE_LIST = ["@2", "@3"]
RES_PATH = "Client/Assets.xcassets"
imageset = '.imageset'
appiconset = '.appiconset'
res_type = 'ios'
png = ".png"


def create_logo_content(temp_path: str, path_to_type: str) -> None:
    logo: str = "appicon"
    menulogo: str = "menulogo"
    logo_splash: str = "logo_splash"
    itunnes = "itunesartwork@2x"

    idiom_ipad: str = "ipad"
    idiom_iphone: str = "iphone"

    scale_one: str = "@1"
    scale_two: str = "@2"
    scale_three: str = "@3"

    path_to_image: str = merge(temp_path, "/appicon")
    path_splash: str = merge(temp_path, "/splash")
    path_menulogo: str = merge(temp_path, menulogo)

    dest: str = merge(path_to_type, logo)
    dest_splash: str = merge(path_to_type, logo_splash)
    dest_menulogo: str = merge(path_to_type, menulogo)

    if not os.path.exists(dest):
        os.makedirs(dest)

    if not os.path.exists(dest_splash):
        os.makedirs(dest_splash)

    if not os.path.exists(dest_menulogo):
        os.makedirs(dest_menulogo)

    # 20 IMAGE SIZE
    shutil.copy(
        src=merge(path_to_image, 'icon-20.png'),
        dst=merge(dest, logo + "-" + idiom_ipad + "20x20" + scale_one + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-small-40.png'),
        dst=merge(dest, logo + "-" + idiom_ipad + "20x20" + scale_two + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-small-40.png'),
        dst=merge(dest, logo + "-" + idiom_iphone + "20x20" + scale_two + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-60.png'),
        dst=merge(dest, logo + "-" + idiom_iphone + "20x20" + scale_three + png))

    # 60 IMAGE SIZE
    shutil.copy(
        src=merge(path_to_image, 'icon-60@2x.png'),
        dst=merge(dest, logo + "-" + idiom_iphone + "60x60" + scale_two + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-60@3x.png'),
        dst=merge(dest, logo + "-" + idiom_iphone + "60x60" + scale_three + png))

    # 40 IMAGE SIZE
    shutil.copy(
        src=merge(path_to_image, 'icon-small-40.png'),
        dst=merge(dest, logo + "-" + idiom_ipad + "40x40" + scale_one + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-small-40@2x.png'),
        dst=merge(dest, logo + "-" + idiom_ipad + "40x40" + scale_two + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-small-40@2x.png'),
        dst=merge(dest, logo + "-" + idiom_iphone + "40x40" + scale_two + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-small-40@3x.png'),
        dst=merge(dest, logo + "-" + idiom_iphone + "40x40" + scale_three + png))

    # 29 IMAGE SIZE
    shutil.copy(
        src=merge(path_to_image, 'icon-small.png'),
        dst=merge(dest, logo + "-" + idiom_ipad + "29x29" + scale_one + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-small@2x.png'),
        dst=merge(dest, logo + "-" + idiom_ipad + "29x29" + scale_two + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-small@2x.png'),
        dst=merge(dest, logo + "-" + idiom_iphone + "29x29" + scale_two + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-small@3x.png'),
        dst=merge(dest, logo + "-" + idiom_iphone + "29x29" + scale_three + png))

    # 76 IMAGE SIZE
    shutil.copy(
        src=merge(path_to_image, 'icon-76.png'),
        dst=merge(dest, logo + "-" + idiom_ipad + "76x76" + scale_one + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-76@2x.png'),
        dst=merge(dest, logo + "-" + idiom_ipad + "76x76" + scale_two + png))

    # 83.5 IMAGE SIZE
    shutil.copy(
        src=merge(path_to_image, 'icon-167.png'),
        dst=merge(dest, logo + "-" + idiom_ipad + "83.5x83.5" + scale_one + png))
    shutil.copy(
        src=merge(path_to_image, 'icon-167.png'),
        dst=merge(dest, logo + "-" + idiom_ipad + "83.5x83.5" + scale_two + png))


    #  MENULOGO
    shutil.copy(
        src=merge(path_menulogo, 'menulogo@2x.png'),
        dst=merge(dest_menulogo, menulogo + scale_two + png))
    shutil.copy(
        src=merge(path_menulogo, 'menulogo@3x.png'),
        dst=merge(dest_menulogo, menulogo + scale_three + png))
    shutil.copy(
        src=merge(path_to_image, itunnes + '.png'),
        dst=merge(dest, itunnes + png))

    # FULL SCREEN SPLASH


    shutil.copy(
        src=merge(path_splash, '640x960.png'),
        dst=merge(dest_splash, "640x960" + png))

    shutil.copy(
        src=merge(path_splash, '640x1024.png'),
        dst=merge(dest_splash, "640x1024" + png))

    shutil.copy(
        src=merge(path_splash, '640x1136.png'),
        dst=merge(dest_splash, "640x1136" + png))

    shutil.copy(
        src=merge(path_splash, '750x1334.png'),
        dst=merge(dest_splash, "750x1334" + png))

    shutil.copy(
        src=merge(path_splash, '768x1024.png'),
        dst=merge(dest_splash, "1024x768" + png))

    shutil.copy(
        src=merge(path_splash, '1125x2436.png'),
        dst=merge(dest_splash, "1125x2436" + png))

    shutil.copy(
        src=merge(path_splash, '1242x2208.png'),
        dst=merge(dest_splash, "1242x2208" + png))

    shutil.copy(
        src=merge(path_splash, '1431x2000.png'),
        dst=merge(dest_splash, "1431x2000" + png))

    shutil.copy(
        src=merge(path_splash, '1536x2048.png'),
        dst=merge(dest_splash, "2048x1536" + png))

    shutil.copy(
        src=merge(path_splash, '2048x2732.png'),
        dst=merge(dest_splash, "2048x2732" + png))
