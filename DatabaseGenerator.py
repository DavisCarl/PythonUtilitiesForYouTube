import tkinter as tk
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sqlite3 as sl
import json

def initdict():
    dic = dict()
    dic['Sex'] = 0
    dic['Violence'] = 0
    dic['SexualViolence'] = 0
    dic['DomesticViolence'] = 0
    dic['Drugs'] = 0
    dic['SexWork'] = 0
    dic['Crime'] = 0
    return dic


def inittextdict():
    dic = dict()
    dic['ID'] = ""
    dic['Title'] = ""
    dic['Origin'] = "RU"
    dic['Author'] = ""
    dic['Comments'] = "None"
    return dic

def updatedict(e, b):
    print(e)
    print(b)
    if vals[e] == 1:
        vals[e] = 0
        b.config(bg="white")
    else:
        vals[e] = 1
        b.config(bg="red")


def checkEntry(w):
    url = w
    print(url)
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div', {'class': 'watch-main-col'})
    title = div.find("meta", itemprop="name")
    vidid = div.find("meta", itemprop="videoId")
    author = div.find("span", itemprop="author").find("link", itemprop="name")
    textvals['Title'] = title['content']
    textvals['ID'] = vidid['content']
    textvals['Author'] = author['content']
    labelauthor.config(text=textvals['Author'])
    labeltitle.config(text=textvals['Title'])


def initdb():
    query = "create table if not exists " + table_name + " (ID text primary key"
    for e in textvals.keys():
        if e != "ID":
            query += ", " + e.title() + " text"
    for e in vals.keys():
        query += ", " + e.title() + " integer"
    query += ')'
    print(query)
    connection.execute(query)


def submitform():
    textvals['Origin'] = locationentry.get()
    query = "INSERT or REPLACE INTO " + table_name + " values (\'" + textvals['ID'] + "\' "
    for e in textvals.keys():
        if e != "ID":
            query += ", \'" + textvals[e] + "\'"
    for e in vals.keys():
        query += ", " + str(vals[e]) + ""
    query += ')'
    print(query)
    connection.execute(query)
    connection.commit()

root = tk.Tk()
root.geometry("512x512")
textvals = inittextdict()
vals = initdict()
table_name = "Videos"
connection = sl.connect("music_videos.db")
initdb()
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
for k in vals:
    buttoni = tk.Button(master=boolbar)
    buttoni.config(text=k, bg="white", fg="black", command=lambda st=k, b=buttoni: [updatedict(st, b)])
    buttoni.pack(side="top", fill="both", expand=1)
locationentry = tk.Entry(titlebar, width=64)
locationentry.pack(side="top", fill="both", expand=1)
boolbar.pack(side="top", fill="both", expand=1)
buttonsubmit = tk.Button(text="Submit Form", bg="white", fg="black", command=lambda: [submitform()], master=root)
buttonsubmit.pack(side='top', fill="x", expand=1)
main.pack(side="top", fill="both", expand=1)

root.mainloop()