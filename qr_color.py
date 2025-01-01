import qrcode
from PIL import Image, ImageOps
from pyzbar.pyzbar import decode

def split_string(str_max):
    length = len(str_max)
    third_length = length//3
    part1 = str_max[:third_length]
    part2 = str_max[third_length:third_length*2]
    part3 = str_max[third_length*2:length]
    return part1, part2, part3

def generate_qr(string, fill):
    qr = qrcode.QRCode(
        #version=40,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        #box_size=10,
        #border=10,
    )

    #make QR code
    qr.add_data(string)

    img = qr.make_image(fill_color=fill, back_color="black")
    return img

def generate_color_qr(string, qr_file_path):
    p1,p2,p3 = split_string(string)
    qr_1 = generate_qr(p1, "#ff0000")
    qr_2 = generate_qr(p2, "#00ff00")
    qr_3 = generate_qr(p3, "#0000ff")
    try:
      color_qr_inv = Image.merge('RGB',(qr_1.split()[0],qr_2.split()[1],qr_3.split()[2]))
    except:
      raise Exception("The generated QR sizes do not match. Please try another size of text string") 
    color_qr = ImageOps.invert(color_qr_inv)
    #color_qr.show()
    color_qr.save(qr_file_path)

def decode_color_qr(file_name):
    color_qr_inv = Image.open(file_name).convert('RGB')
    rgb_qr = ImageOps.invert(color_qr_inv)
    r_rgb,g_rgb,b_rgb = rgb_qr.split()
    r_rgb_qr = Image.merge("RGB", (r_rgb, r_rgb, r_rgb))
    g_rgb_qr = Image.merge("RGB", (g_rgb, g_rgb, g_rgb))
    b_rgb_qr = Image.merge("RGB", (b_rgb, b_rgb, b_rgb))
    data_1 = decode(ImageOps.invert(r_rgb_qr))[0][0]
    data_2 = decode(ImageOps.invert(g_rgb_qr))[0][0]
    data_3 = decode(ImageOps.invert(b_rgb_qr))[0][0]
    print((data_1+data_2+data_3).decode('utf-8'))

if __name__ == '__main__':
    f = open("demo_content_small.txt", "r")
    #f = open("demo_content_large.txt", "r")
    text = f.read()
    generate_color_qr(text, 'color_qr.png')
    decode_color_qr("color_qr.png")
