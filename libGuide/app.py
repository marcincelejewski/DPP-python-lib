import sqlite3
import sys
from time import strftime


class App:

    def __init__(self):
        self.current = 0
        self.list = []
        self.conn = sqlite3.connect("C:/Users?Marcin/guidesDB.db")
        cursor = self.conn.execute("select * from guides")
        for row in cursor:
            guide = Guide(row[0], row[1], row[2], row[3], row[4], row[5])
            self.list.append(guide)
        if len(self.list) <= 0:
            print("Baza danych jest pusta")
            sys.exit(666)
        self.print_guide()

    def __del__(self):
        self.conn.close()
        self.list.clear()

    def print_guide(self):
        print(self.list[self.current])

    def next(self):
        self.current += 1
        if self.current >= len(self.list):
            self.current = 0
        self.print_guide()

    def previous(self):
        self.current -= 1
        if self.current < 0:
            self.current = (len(self.list)) - 1
        self.print_guide()

    def edit(self):
        print("Wpisz swoje poprawki i nacisnij ENTER")
        edit = str(input())
        self.conn.execute(
            "update guides set content = '{}' where id = {}".format(
                self.list[self.current].content + "\nedit: " +
                edit, str(self.list[self.current].id)))
        self.conn.commit()
        self.list[self.current].content =\
            self.list[self.current].content + "\nedit: " + edit

    def show_comments(self):
        cursor = self.conn.execute("select * from comments where guide_id={}"
                                   .format(str(self.list[self.current].id)))
        print("Komentarze\n---------------------------------------------")
        for row in cursor:
            print(row[2] + "\n" + row[3] +
                  "\n---------------------------------------------")

    def add_comment(self):
        print("Wpisz swoj komentarz i nacisnij ENTER")
        comm = str(input())
        date = strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute("insert into comments(guide_id, comment, add_date) \
            values({},'{}','{}')".format(
            str(self.list[self.current].id), comm, date))

        self.conn.commit()

    def rate(self):
        print("Wpisz swoja ocene i nacisnij ENTER (1-5)")
        rate = 0
        while rate < 1 or rate > 5:
            rate = int(input())
            if rate < 1 or rate > 5:
                print("Nieprawidlowa ocena, wpisz ponownie!")

        rate = float((self.list[self.current].rate *
                      self.list[self.current].rate_num + rate) / (
                self.list[self.current].rate_num + 1))

        self.conn.execute(
            "update guides set rate = {},"
            "rate_number = {} where id = {}".format(
                rate, self.list[self.current].rate_num + 1,
                str(self.list[self.current].id)))
        self.conn.commit()
        self.list[self.current].rate = rate
        self.list[self.current].rate_num += 1



class Guide():

    def __init__(self, id, title, content, add_date, rate, rate_num):
        self.id = id
        self.title = title
        self.content = content
        self.rate = rate
        self.rate_num = rate_num
        self.add_date = add_date

    def __str__(self):
        rate_str = "*"
        if float(self.rate) >= 1.5:
            rate_str = "**"
        if float(self.rate) >= 2.5:
            rate_str = "***"
        if float(self.rate) >= 3.5:
            rate_str = "****"
        if float(self.rate) >= 4.5:
            rate_str = "*****"
        return "\nPoradnik\n" + self.title + "\n" + "Ocena: " + \
               rate_str + "\n" + \
               self.content + "\nData dodania: " + str(self.add_date) + "\n"
