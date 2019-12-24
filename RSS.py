from tkinter import *
import sqlite3
import pyperclip
import feedparser

# базы данных

links = sqlite3.connect("links.db")
cursor = links.cursor()
bigdata = dict()
resource = [row[1] for row in cursor.execute("SELECT rowid, * FROM links ORDER BY adress")]


# функции

def copy_link():
    select = list(listbox.curselection())
    select = [listbox.get(i) for i in select]
    select = ' '.join(select)
    pyperclip.copy(select)


def find():
    key = entry1.get()
    for i in bigdata:
        for j in range(len(bigdata[i])):
            for k in range(3):
                if key in bigdata[i][j][k]:
                    listbox.insert(END, bigdata[i][j][k])


def delete():
    select = list(listbox.curselection())
    select.reverse()
    for i in select:
        listbox.delete(i)
        string = resource.pop(i)
        sql = "DELETE FROM links WHERE adress = '%s'" % string
        cursor.execute(sql)
        links.commit()


def add_new():
    new_task = """INSERT INTO links VALUES ('%s')""" % entry2.get()
    cursor.execute(new_task)
    links.commit()
    listbox.insert(END, entry2.get())
    resource.append(entry2.get())


def see_all():
    global right, listbox, scroll, button7, bigdata, resource
    right.destroy()
    right = Frame(window, bg='paleturquoise')
    right.grid(column=1, row=1, rowspan=3)
    top = Frame(right)
    top.pack()
    listbox = Listbox(top, selectmode=EXTENDED, width=120, height=27)
    scroll = Scrollbar(top, command=listbox.yview)
    listbox.pack(side=LEFT, fill=Y)
    scroll.pack(fill=Y)
    listbox.config(yscrollcommand=scroll.set)
    button7 = Button(right, text='Скопировать', command=copy_link, bg='lightcyan', font=('Arial', 16),
                     fg='midnightblue')
    button7.pack(side=BOTTOM)
    for source in resource:
        feeds = feedparser.parse(source)
        bigdata[feeds['feed']['title']] = []
        for article in feeds['entries']:
            bigdata[feeds['feed']['title']].append([article['title'], article['description'], article['link']])
            listbox.insert(END, article['title'])
            listbox.insert(END, article['description'])
            listbox.insert(END, article['link'])


def find_in():
    global right, entry1, label2, label3, listbox, scroll1, button6, button8
    right.destroy()
    right = Frame(window, bg='paleturquoise')
    right.grid(column=1, row=1, rowspan=3, sticky=N + S + W + E)
    top = Frame(right)
    label2 = Label(right, text='Искать в новостях: ', bg='paleturquoise', fg='midnightblue', font=('Arial', 16))
    label3 = Label(right, text='Результаты: ', bg='paleturquoise', fg='midnightblue', font=('Arial', 16), height=2)
    entry1 = Entry(right, font=('Arial', 16), width=40)
    button6 = Button(right, text='Искать', command=find, bg='lightcyan', font=('Arial', 16), fg='midnightblue')
    listbox = Listbox(top, selectmode=EXTENDED, width=120, height=18)
    scroll1 = Scrollbar(top, command=listbox.yview)
    button8 = Button(right, text='Скопировать', command=copy_link, bg='lightcyan', font=('Arial', 16),
                     fg='midnightblue')
    label2.pack()
    entry1.pack()
    button6.pack()
    label3.pack()
    top.pack()
    listbox.pack(side=LEFT, fill=Y)
    scroll1.pack(side=LEFT, fill=Y)
    listbox.config(yscrollcommand=scroll1.set)
    button8.pack()


def add_feed():
    global right, entry2, label4, label5, listbox, scroll2, button4, button9
    right.destroy()
    right = Frame(window, bg='paleturquoise')
    right.grid(column=1, row=1, rowspan=3, sticky=N + S + W + E)
    label4 = Label(right, text='Ваши источники: ', bg='paleturquoise', fg='midnightblue', font=('Arial', 16))
    label4.pack()
    top = Frame(right)
    top.pack()
    listbox = Listbox(top, selectmode=EXTENDED, width=120, height=18)
    scroll2 = Scrollbar(top, command=listbox.yview)
    listbox.pack(side=LEFT, fill=Y)
    scroll2.pack(side=LEFT, fill=Y)
    listbox.config(yscrollcommand=scroll2.set)
    bottom = Frame(right)
    bottom.pack()
    button4 = Button(bottom, text='Удалить выбранные', command=delete, bg='lightcyan', font=('Arial', 16),
                     fg='midnightblue')
    label5 = Label(right, text='Добавить источник: ', bg='paleturquoise', fg='midnightblue', font=('Arial', 16),
                   height=2)
    entry2 = Entry(right, font=('Arial', 16), width=40)
    button5 = Button(right, text='Добавить', command=add_new, bg='lightcyan', font=('Arial', 16), fg='midnightblue')
    button9 = Button(bottom, text='Скопировать', command=copy_link, bg='lightcyan', font=('Arial', 16),
                     fg='midnightblue')
    button5.pack(side=BOTTOM)
    button9.pack(side=LEFT)
    entry2.pack(side=BOTTOM)
    label5.pack(side=BOTTOM)
    button4.pack(side=LEFT)
    for source in resource:
        listbox.insert(END, source)


# главное окно

window = Tk()
window.title('RSS Reader')
window.geometry('887x508')
window['bg'] = 'paleturquoise'
window.iconbitmap(default='newspaper.ico')
window.minsize(887, 508)
window.maxsize(887, 508)

label1 = Label(window, text='Breaking news:', font=('Arial', 16), bg='paleturquoise', fg='black', anchor='w',
               relief=RAISED)
label1.grid(column=0, row=0, columnspan=2, sticky=W + E)

button1 = Button(window, text='Просмотреть\nвсё', command=see_all, bg='lightcyan', font=('Arial', 16), fg='gray')
button2 = Button(window, text='Искать\nв списке', command=find_in, bg='lightcyan', font=('Arial', 16), fg='gray')
button3 = Button(window, text='Управление\nисточниками', command=add_feed, bg='lightcyan', font=('Arial', 16),
                 fg='gray')
button1.grid(column=0, row=1, sticky=N + S + W + E)
button2.grid(column=0, row=2, sticky=N + S + W + E)
button3.grid(column=0, row=3, sticky=N + S + W + E)

right = Frame()
see_all()

window.mainloop()