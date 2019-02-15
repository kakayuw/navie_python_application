import matplotlib.pyplot as plt
show_heigth = 200
show_width = 300

# Generate an ASCII char list
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
# ascii_char = list("1-")

char_len = len(ascii_char)

pic = plt.imread("./img/cty/7.png")
# Utilize .imread to read pictures, return size = heigth*width*3 for color graph
# (R G B) in matplotlib 

pic_heigth, pic_width, _ = pic.shape
# get height and width

gray = 0.2126 * pic[:,:,0] + 0.7152 * pic[:,:,1] + 0.0722 * pic[:,:,2]
# RGB to grayscale      gray = 0.2126 * r + 0.7152 * g + 0.0722 * b

# map gray to ascii_char
alltext = ""
for i in range(show_heigth):
    y = int(i * pic_heigth / show_heigth)
    text = ""
    for j in range(show_width):
        x = int(j * pic_width / show_width)
        # text += ascii_char[int(gray[y][x] / 256 * char_len)]
        text += ascii_char[int(( gray[y][x]) * (char_len + 1)) % char_len]
        # text += ascii_char[int(gray[y][x])]
    alltext += text + '\n'

print(alltext)
wt = open('./mapdata/charpic.txt', 'w', encoding="utf-8")
wt.write(alltext)
wt.close()
