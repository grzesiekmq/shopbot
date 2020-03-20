from tkinter import *

from textblob.classifiers import NaiveBayesClassifier

with open('tags.json') as f:
    classifier = NaiveBayesClassifier(f, format="json")

products = []

bot_name = "Shoppy"


def greet():
    return "hi"


def add():
    products.append(product)
    added_product = "added " + product
    return added_product


def count():
    total = str(len(products))
    total_items = "total items: " + total
    return total_items


def show():
    if (product != None):
        status = "groceries status: \n"
        for p in products:
            status += "> " + p + '\n'
        return status


def remove():
    products.clear()
    return "removed list"


def get_message(arg):
    switcher = {
        "greeting": greet,
        "add": add,
        "count": count,
        "show": show,
        "remove": remove
    }
    return switcher.get(arg, "sorry I don't understand")


start_text = "Hi available commands: \n add [product] (example: add chips), \n" \
             "items count, alias total \n" \
             "groceries status, alias gs \n" \
             "show list, alias sl \n" \
             "remove list, alias rl, \n"

## GUI ##
tk = Tk()
tk.title("Shop bot")
tk.geometry("400x500")
tk.resizable(width=FALSE, height=FALSE)
# box to enter message
EntryBox = Text(tk, bd=0, bg="#123456", width="29", height="5", font="Arial")

product = ""


def send():
    input_text = EntryBox.get("1.0", "end-1c")
    chatlog_builder(input_text)

    EntryBox.delete("0.0", END)

    global product

    contains_add = input_text.__contains__("add")
    word = input_text.split()
    # when product consists of many words

    if (contains_add and len(word) > 2):
        product = input_text[4:]
    elif (contains_add):
        product = word[1]

    label = classifier.classify(input_text)

    user_msg = get_message(label)

    ChatLog.insert(END, bot_name + ': ' + user_msg())


ChatLog = Text(tk, bd=0, bg="white", height="8", width="50", font="Arial", )

ChatLog.config(foreground="#fff", font=("Verdana", 12), bg="#123456")

# bot
ChatLog.insert(END, bot_name + ': ' + start_text + '\n\n')
ChatLog.config(state=NORMAL)

scrollbar = Scrollbar(tk, command=ChatLog.yview, cursor="heart")


def chatlog_builder(arg):
    if (arg != ""):
        # user
        ChatLog.insert(END, "\n User: " + arg + '\n\n')
        ChatLog.yview(END)


def bind_scrollbar():
    ChatLog['yscrollcommand'] = scrollbar.set


bind_scrollbar()

SendBtn = Button(tk,
                 font=("Verdana", 12, 'bold'),
                 text="Send",
                 width="10",
                 height=5,
                 bd=1,
                 bg="#fff",
                 activebackground="#3c9d9b",
                 fg='#123456',
                 command=send)


def place_component():
    scrollbar.place(x=376, y=6, height=386)
    ChatLog.place(x=6, y=6, height=386, width=370)
    EntryBox.place(x=128, y=401, height=90, width=265)
    SendBtn.place(x=6, y=401, height=90)


place_component()

tk.mainloop()
