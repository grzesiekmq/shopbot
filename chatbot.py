from textblob.classifiers import NaiveBayesClassifier

with open('tags.json') as f:
    classifier = NaiveBayesClassifier(f, format="json")


def greet():
    print("hi")


def add():
    print("added " + product)


def count():
    print("total items")


def show():
    print("groceries status:")


def remove():
    print("removed")


def get_message(arg):
    switcher = {
        "greeting": greet,
        "add": add,
        "count": count,
        "show": show,
        "remove": remove
    }
    return switcher.get(arg, "sorry I don't understand")


prompt = "Hi available commands: add [product] (example: add chips), \n" \
         "items count, alias ic \n" \
         "groceries status, alias gs \n" \
         "show list, alias sl \n" \
         "remove list, alias rl, \n" \
         "$ "

input = input(prompt)
word = input.split()
product = word[1]

label = classifier.classify(input)

print('label: ', label)

get_message(label)()
