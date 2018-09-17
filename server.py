from flask import Flask
from flask import abort
from flask_cors import CORS
import modules.cardgen as cardgen
import json
import csv
import threading
import queue

DEV_MODE = False

app = Flask(__name__)
CORS(app)

QUEUE_SIZE = 30
card_queue = queue.Queue(QUEUE_SIZE)
generating_cards = True

class GenerationThread(threading.Thread):
    def run(self):
        global generating_cards
        while not card_queue.full():
            card_queue.put(cardgen.generate_card())
            print("Card generated! Now " + str(card_queue.qsize()) + " in queue")
        print("Queue filled!")
        generating_cards = False

@app.route("/cards/generate/<qty>")
def generate(qty):
    global generating_cards
    print("Request received at /cards/generate/" + str(qty))
    try:
        qty = int(qty)
    except ValueError:
        abort(400)
    if(qty > QUEUE_SIZE):
        abort(400)

    cards = []
    for x in range(0, qty):
        while card_queue.empty():
            pass
        cards.append(card_queue.get())
    response = { 'cards': cards }
    if(not generating_cards):
        GenerationThread().start()
        generating_cards = True
    print("Response sent")
    return "" + json.dumps(response) + ""

if __name__ == "__main__":
    if DEV_MODE:
        uinput = ""
        while(uinput != "exit"):
            response = cardgen.generate_cards(3)
            uinput = input("Do you pick card #0, 1, or 2?\n")
            if(uinput.isdigit()):
                if(int(uinput) >= 0 and int(uinput) <= 2):
                    response = json.loads(response)
                    card = response['cards'][int(uinput)]
                    with open('data/cards.csv', 'a') as csvfile:
                        f = csv.writer(csvfile)
                        f.writerow([None, card['POW'], card['HP'], card['CLK'], card['EFF']])
                    continue
            print("Invalid input")
    GenerationThread().start()
    app.run()

