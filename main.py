import pymysql
from modules.cardgen import CardGen
import modules.config as cfg

if __name__ == "__main__":
    cardgen = CardGen()
    cards = cardgen.get_cards(1)
    print(cards)
    
    # Connect to the database
    conn = pymysql.connect(host=cfg.host,
                           user=cfg.user,
                           password=cfg.password,
                           db=cfg.db,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit(True)
    query = 'INSERT INTO card (expansion, name, clk, pow, hp, effs, img) VALUES'
    for c in cards:
        query += '\n({0}, "{1}", {2}, {3}, {4}, "{5}", "{6}"),'.format(0, c['name'], c['clk'], c['pow'], c['hp'], c['eff'], c['img'])
    query = query[:-1] + ';'
    print("QUERY:\n\n\n" + query + "\n\n\n")
    conn.cursor().execute(query)
