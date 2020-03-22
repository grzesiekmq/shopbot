from textblob.classifiers import NaiveBayesClassifier

import asyncio

import websockets

product = ""
bonus_product = ""
mba = ""

products = []

pairs = [["chips", "beer"],
         ["eggs", "bacon"],
         ["bread", "butter"],
         ["buns", "butter"],
         ["corn flakes", "milk"],
         ["coffee", "milk"],
         ["ketchup", "sausage"],
         ["garlic sauce", "sausage"],
         ["mustard", "sausage"]
         ]


def get_bonus_product():
    for pair in pairs:
        contains_product = pair.__contains__(product)
        product_index = pair.index(product)

        # lhs (product left-hand side)
        # bonus product right-hand side - see on google association rules
        if (contains_product and product_index == 0):
            bonus_product_index = product_index + 1
            bonus_product_rhs = pair[bonus_product_index]
            return bonus_product_rhs
        # rhs (product right-hand side)
        # bonus product left-hand side
        elif (contains_product and product_index == 1):
            bonus_product_index = product_index - 1
            bonus_product_lhs = pair[bonus_product_index]
            return bonus_product_lhs


with open('tags.json') as f:
    classifier = NaiveBayesClassifier(f, format="json")


def greet():
    return "hi"


def add():
    products.append(product)


def count():
    total = str(len(products))
    total_items = "total items: " + total
    return total_items


def show():
    if (product != None):
        status = "<ol><b>groceries status</b> <br>"
        for p in products:
            status += "<li>" + p + '</li>'
        status += '</ol>'
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


def process_text(input_text):
    global product, mba
    contains_add = input_text.__contains__("add")

    word = input_text.split()
    # when product consists of many words
    if (contains_add and len(word) > 2):
        product = input_text[4:]
    elif (contains_add):
        product = word[1]

    label = classifier.classify(input_text)

    print('label ' + label)

    user_msg = get_message(label)
    return user_msg


async def time(websocket, path):
    while True:
        global bonus_product
        input_text = await websocket.recv()
        print('msg' + input_text)

        user_msg = process_text(input_text)

        if (input_text.__contains__("add")):
            bonus_product = get_bonus_product()
            mba = "Do you want to also add " + bonus_product + '?'
            await websocket.send(mba)
        else:
            await websocket.send(user_msg())


start_server = websockets.serve(time, "127.0.0.1", 5678)
print('connected')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
