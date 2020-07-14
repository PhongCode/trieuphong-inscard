#copyright by nguyentrieuphong
#follow me on nguyentrieuphong.com

from PIL import Image, ImageDraw
from PIL import ImageFilter, ImageFont
from requests import get
import requests
import json

#JSON_process
image_instagram = "https://www.instagram.com/p/CCh4uKGJ_yb/?utm_source=ig_web_copy_link"
JSON_image_url = image_instagram.replace('utm_source=ig_web_copy_link', '__a=1', 1)
req_image = requests.get(JSON_image_url)
convert_1 = req_image.text
load_image = json.loads(convert_1)
main_link = load_image['graphql']['shortcode_media']['display_url']
avatar_link = load_image['graphql']['shortcode_media']['owner']['profile_pic_url']
user_name = load_image['graphql']['shortcode_media']['owner']['username']
posts = load_image['graphql']['shortcode_media']['owner']['edge_owner_to_timeline_media']['count']

# JSON GET follow
profile_instagram = "https://www.instagram.com/" + user_name + "/?__a=1"
req_profile = requests.get(profile_instagram)
convert_2 = req_profile.text
load_profile = json.loads(convert_2)
followers = load_profile['graphql']['user']['edge_followed_by']['count']
following = load_profile['graphql']['user']['edge_follow']['count']

#Download image module
def download(url, file_name):
    with open(file_name, "wb") as file:
        response = get(url)
        file.write(response.content)
download(main_link,"main_image.jpg")
download(avatar_link,"./materials/avatar.jpg")


#Input_module
image = Image.open('main_image.jpg')
h = image.size[0]
w = image.size[1]
if(h==w):
    image = image.resize((1080, 1080), Image.ANTIALIAS)
if(w<=h):
    image = image.crop((int(int(h - w) / 2), 0,int(int(h) - int(h - w) / 2),int(h) ))
if(w>h):
    if(h==1080):
        image = image
    else:
        image = image.crop((0, int(int(w - h) / 2), int(h), int(int(w) - int(w - h) / 2)))
        image = image.resize((1080, 1080), Image.ANTIALIAS)

#background module
background = image.crop((0, int(int(w-h)/2), int(h), int(int(w)-int(w-h)/2)))
#background.save('background.jpg', quality=95)

#card module
card = image.crop((270, 50, 860, 1050))

#shadow module
sh1 = background
sh2 = Image.open('./materials/shadow.jpg')
sh3 = Image.open('./materials/solid_shadow.jpg')
mask_sh = Image.new("L", sh2.size, 0)
draw_sh = ImageDraw.Draw(mask_sh)
mask_sh = sh3.resize(sh2.size).convert('L')
back_sh = sh1.copy()
back_sh.paste(sh2, (270, 100), mask_sh)
sh = back_sh.filter(ImageFilter.GaussianBlur(radius=10))

#insert card
background_shadow = sh
is1 = background_shadow.resize((1200, 1200), Image.ANTIALIAS)
is2 = card
is3 = Image.open('./materials/solid.jpg')
mask_is = Image.new("L", is2.size, 0)
draw_is = ImageDraw.Draw(mask_is)
mask_is = is3.resize(is2.size).convert('L')
back_is = is1.copy()
back_is.paste(is2, (298, 115), mask_is)
#back_is.save('card.jpg', quality=95)

#insert_avatar
av1 = back_is
av2_1 = Image.open('./materials/avatar.jpg')
av2 = av2_1.resize((100, 100), Image.ANTIALIAS)
av3 = Image.open('./materials/solid_avatar.jpg')
mask_av = Image.new("L", av2.size, 0)
draw_av = ImageDraw.Draw(mask_av)
mask_av = av3.resize(av2.size).convert('L')
av = av1.copy()
av.paste(av2, (345, 170), mask_av)

#text
text = av
draw_text = ImageDraw.Draw(text)
font_01 = ImageFont.truetype(r'.\fonts/TCCEB.ttf', 30)
font_02 = ImageFont.truetype(r'.\fonts/TCCEB.ttf', 40)
short = str(followers)
if(followers > 999999):
    followers = followers / 1000000
    short = str(int(followers)) + "M"
if(followers > 999):
    followers = followers / 1000
    short = str(int(followers)) + "K"
unl = len(str(following))
uw, uh = draw_text.textsize(user_name, font = font_01)
pw, ph = draw_text.textsize(str(posts), font = font_02)
fw, fh = draw_text.textsize(str(following), font = font_02)
draw_text.text((600-(uw/2), 160),user_name,(255,255,255),font=font_01)
draw_text.text((520 - (pw/2), 220),str(posts),(255,255,255),font=font_02)
draw_text.text((645 - (fw/2), 220),str(following),(255,255,255),font=font_02)
draw_text.text((680, 220),short.center(20),(255,255,255),font=font_02)

#insert theme
in1 = text
in2 = Image.open('./materials/white.jpg')
in3 = Image.open('./materials/info.jpg')
mask_info = Image.new("L", in2.size, 0)
draw_in = ImageDraw.Draw(mask_info)
mask_info = in3.resize(in2.size).convert('L')
info = in1.copy()
info.paste(in2, (298, 115), mask_info)
info.save('static/trieuphong_course03.jpg', quality=95)


