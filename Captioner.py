import tkinter as tk
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sqlite3 as sl
import PIL
import io
from PIL import ImageGrab
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

def checkEntry(w):
    url = w
    print(url)
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div', {'class': 'watch-main-col'})
    global title
    global vidid
    title = div.find("meta", itemprop="name")
    vidid = div.find("meta", itemprop="videoId")
    author = div.find("span", itemprop="author").find("link", itemprop="name")
    labelauthor.config(text=author['content'])
    labeltitle.config(text=title['content'])
    global writable
    if writable == 0:

        buttonsubmit = tk.Button(text="Snip and Caption", bg="white", fg="black", command=lambda: [submitEntry()], master=root)
        buttonsubmit.pack(side='top', fill="x", expand=1)
        writable = 1

def submitEntry():
    print(writable)
    if writable == 1:
        image = ImageGrab.grab(bbox=(0,126,1920,927))
        with Drawing() as draw:
            with Image(width = 1920, height = 256, background = Color('black')) as image2:
                draw.font = 'wandtests/assets/Courier New.otf'
                draw.font_size = 32
                draw.stroke_color = Color('yellow')
                draw.fill_color = Color('white')
                draw.text(64, 32 , title['content'] + " www.youtube.com/watch?v=" + vidid['content'])
                draw.font_size = 48
                draw.text(64, 96 , commentText.get("1.0",'end-1c'))
                draw(image2)
                image2.save(filename="text.png")
        pilcaption = PIL.Image.open("text.png")
        new_image = PIL.Image.new('RGB',(1920, 927-126+256), (250,250,250))
        new_image.paste(image,(0,0))
        new_image.paste(pilcaption,(0,927-126 ))
        imagename = vidid['content'] + ".jpg"
        new_image.save(imagename,"JPEG")
        new_image.show()
writable = 0
root = tk.Tk()
root.geometry("1920x384")
toolbar = tk.Frame(root, background="#d5e8d4")
titlebar = tk.Frame(root, background="#e3e3e3")
boolbar = tk.Frame(root, background="#e3e3e3")
main = tk.PanedWindow(root, background="#99fb99")
labelauthor = tk.Label(text="******", width=64, height=1, bg="white", fg="black", master=titlebar)
labeltitle = tk.Label(text="|||||||", width=64, height=1, bg="grey", fg="black", master=titlebar)
labeltitle.pack(side="top", fill="both", expand=1)
labelauthor.pack(side="top", fill="both", expand=1)

entry = tk.Entry(width=64, bg="white", fg="black", master=toolbar)
button = tk.Button(text="Get Url", width=8, bg="white", fg="black", command=lambda: [checkEntry(entry.get())], master=toolbar)
entry.pack(side="left", fill="x", expand=1)
button.pack(side="left")
toolbar.pack(side="top", fill="both", expand=1)
titlebar.pack(side='top', fill='x')
commentText = tk.Text( padx=64, height=3, bg="white", fg="black", font=("Courier New", 32), master=root)
commentText.pack(side='top', fill="x", expand=1)

main.pack(side="top", fill="both", expand=1)

root.mainloop()