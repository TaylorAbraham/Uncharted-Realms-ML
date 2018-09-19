from flask import Flask
from flask import abort
from flask_cors import CORS
from modules.cardgen import CardGen
from modules.cardgen import QUEUE_SIZE
import json
import csv
from multiprocessing import Process
DEV_MODE = False

cardgen = CardGen()
app = Flask(__name__)
CORS(app)

@app.route("/cards/generate/<qty>")
def generate(qty):
    print("Request received at /cards/generate/" + str(qty))
    try:
        qty = int(qty)
    except ValueError:
        abort(400)
    if(qty > QUEUE_SIZE):
        abort(400)
    response = { 'cards': cardgen.get_cards(qty) }
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
    cardgen.start_card_generation()
    app.run()
