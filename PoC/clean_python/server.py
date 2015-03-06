from flask import Flask, request
from datetime import datetime
from time import strftime
import sqlite3

#CREATE TABLE "stat" (
#    "id" INTEGER PRIMARY KEY NOT NULL,
#    "date" DATE,
#    "user" VARCHAR(100),
#    "money" REAL,
#    "comment" TEXT
#);

app = Flask(__name__)

def show_table():
    htmlc = """<HTML>
<HEAD><TITLE>KORMUSHKA</TITLE></HEAD>
<BODY>
<table border="1" width="90%">
<tr>
 <td>Дата</td>
 <td>Фио</td>
 <td>Сумма</td>
 <td>Продукт</td>
</tr>
"""

    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM stat')
    for row in cur:
        htmlc += "<tr> <td>" + row[1] + "</td> <td>" + row[2] + "</td> <td>" + str(row[3]) + "</td> <td>" + row[4] + "</td></tr>"
    con.close()

    htmlc += """<tr><td colspan="4">
<form method="post">
 <label class="control-label" for="user">Имя</label>
 <input id="user" name="user" type="text">

 <label class="control-label" for="money">Сумма</label>
 <input id="money" name="money" type="text">

 <label class="control-label" for="comment">Что куплено?</label>
 <input id="comment" name="comment" type="text">
 <input type="submit">
</form>
</tr></tr>
</table>
</BODY>
</HTML>"""
    return htmlc

def add_record(user, money, comment):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute('''INSERT INTO stat (date, user, money, comment) VALUES(?,?,?,?)''', (datetime.now(),user,money,comment))
#    cur.execute('INSERT INTO stat (id, date, user, money, comment) VALUES(NULL, "' + date.today() + '", "' + user + '", "' + money + '", "' + comment + '")')
    con.commit()
    con.close()
    return show_table()

@app.route('/', methods=['GET', 'POST'])
def main_form():
    if request.method == 'POST':
        return add_record(request.form['user'],
                          request.form['money'],
                          request.form['comment'])
    else:
        return show_table()


if __name__ == '__main__':
    app.run(debug=True)

