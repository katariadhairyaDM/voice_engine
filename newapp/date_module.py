
import itertools
from dateutil import parser
from datetime import datetime, timedelta, date



def date_module(given_str):
    given_str = given_str.lower()

    lst1 = []
    lst2 = []
    list_words = ['today', 'yesterday', 'now', 'week', 'month', 'day', 'year']
    for word in list_words:
        if word in given_str: 
            print(word)
            if word in ['today', 'now']:
                lst1.append(datetime.today())
            elif word == 'yesterday':
                lst1.append(datetime.today() - timedelta(days=1))
            else:
                str_words = given_str.split(' ')
                if 'last' in str_words:
                    idx = str_words.index('last')
                    if str_words[idx+1].isdigit():
                        num = int(str_words[idx+1])
                        lst1.append(datetime.today())
                        if str_words[idx+2] in ['day', 'days']:
                            lst1.append(datetime.today() - timedelta(days=1*num))
                        elif str_words[idx+2] in ['week', 'weeks']:
                            lst1.append(datetime.today() - timedelta(days=7*num))
                        elif str_words[idx+2] in ['month', 'months']:
                            lst1.append(datetime.today() - timedelta(days=30*num))
                        elif str_words[idx+2] in ['year', 'years']:
                            lst1.append(datetime.today() - timedelta(days=365*num))
                    else:
                        if str_words[idx+1] in ['day', 'days']:
                            lst1.append(datetime.today() - timedelta(days=1))
                        elif str_words[idx+1] in ['week', 'weeks']:
                            lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday()))
                            lst1.append(datetime.today() - timedelta(days=7+datetime.today().isoweekday()))
                        elif str_words[idx+1] in ['month', 'months']:
                            lst1.append(date.today().replace(day=1) - timedelta(days=1))
                            lst1.append(date.today().replace(day=1) - timedelta(days=lst1[0].day))
                        elif str_words[idx+1] in ['year', 'years']:
                            lst1.append(date.today().replace(day=31, month=12, year=datetime.now().year-1))
                            lst1.append(date.today().replace(day=1, month=1, year=datetime.now().year-1))

                    if 'monday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 1 + 7))
                    elif 'tuesday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 2 + 7))
                    elif 'wednesday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 3 + 7))
                    elif 'thursday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 4 + 7))
                    elif 'friday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 5 + 7))
                    elif 'saturday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 6 + 7))
                    elif 'sunday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 7 + 7))  


                elif 'this' in str_words:
                    idx = str_words.index('this')
                    if str_words[idx+1] in ['week', 'weeks', 'weak', 'weaks']:
                        lst1.append(datetime.today())
                        lst1.append(datetime.today() - timedelta(days=datetime.today().weekday()))
                    elif str_words[idx+1] in ['month', 'months']:
                        lst1.append(date.today())
                        lst1.append(date.today().replace(day=1))
                    elif str_words[idx+1] in ['year', 'years']:
                        lst1.append(datetime.today())
                        lst1.append(datetime.today() - timedelta(days=365))

                    if 'monday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 1))
                    elif 'tuesday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 2))
                    elif 'wednesday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 3))
                    elif 'thursday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 4))
                    elif 'friday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 5))
                    elif 'saturday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 6))
                    elif 'sunday' in str_words:
                        lst1.append(datetime.today() - timedelta(days = datetime.today().isoweekday() - 7))
                end_date = str(lst1[0]).split(' ')[0]
                start_date = str(lst1[-1]).split(' ')[0]
                    
                return (start_date, end_date)

    # print('lst-1 ', lst1)

    jumpwords = set(parser.parserinfo.JUMP)
    keywords = set(kw.lower() for kw in itertools.chain(
        parser.parserinfo.UTCZONE,
        parser.parserinfo.PERTAIN,
        (x for s in parser.parserinfo.WEEKDAYS for x in s),
        (x for s in parser.parserinfo.MONTHS for x in s),
        (x for s in parser.parserinfo.HMS for x in s),
        (x for s in parser.parserinfo.AMPM for x in s),
    ))


    def parse_multiple(s):
        def is_valid_kw(s):
            try:  # is it a number?
                float(s)
                return True
            except ValueError:
                return s.lower() in keywords

        def _split(s):
            kw_found = False
            tokens = parser._timelex.split(s)
            for i in range(len(tokens)):
                if tokens[i] in jumpwords:
                    continue 
                if not kw_found and is_valid_kw(tokens[i]):
                    kw_found = True
                    start = i
                elif kw_found and not is_valid_kw(tokens[i]):
                    kw_found = False
                    yield "".join(tokens[start:i])
            # handle date at end of input str
            if kw_found:
                yield "".join(tokens[start:])

        return [parser.parse(x) for x in _split(s)]

    lst2 = parse_multiple(given_str)
    lst = lst2+lst1
    # print('lst-2 ', lst2)
    # print('final list ', lst)
    if len(lst) == 0:
        lst = date_module('last 14 days')
    if lst[0]>lst[0]:
        end_date = str(lst[0]).split(' ')[0]
        start_date = str(lst[-1]).split(' ')[0]
    else:
        end_date = str(lst[-1]).split(' ')[0]
        start_date = str(lst[0]).split(' ')[0]
    return (start_date, end_date)

if __name__ == '__main__':
    print(date_module("last 2 year"))
