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
