import csv
import grs
import datetime
import time

def roc_time_to_west_time(roc_time, ):
    time_peace = roc_time.split("/")
    time_peace[0] = str(int(time_peace[0])-105+2016)

    west_time = '-'.join(time_peace)
    return west_time


def get_year(date):
    return date.split("-")[0]


class  feed_twgrs:
    def __init__(self, tw_stock_id,instruments, from_year, to_year, storage="."):
        self.__tw_stock_id = instruments
        self.__from_year = from_year

        self.__to_year = to_year
        self.__storage = storage
        #month_interval +=1ou
        time.sleep(1)
        month_interval = (int(datetime.datetime.today().strftime("%Y")) - from_year) * 12 + int(datetime.datetime.today().strftime("%m"))

        #print "month interval %d " % month_interval
        file_name = storage+"/tw"+tw_stock_id+".csv"
        self.__file = file_name

        self.__stock = grs.Stock(tw_stock_id,month_interval)
        due_year = to_year + 1

        with open(self.__file, 'wb') as csvfile:
            csv_out = csv.writer(csvfile)
            csv_out.writerow(["Date", "Open", "High", "Low", "Close", "Volume", "Adj Close"])

            for x in self.__stock.raw:
                # print x

                x[0] = roc_time_to_west_time(x[0])
                if int(get_year( x[0])) == due_year:
                    print "due year",due_year,x[0]
                    break
                #to do : Adj Close
                west_fmt = [x[0], x[3], x[4], x[5], x[6], str(int(x[1])), x[4]]
                csv_out.writerow(west_fmt)
        pass

    def get_file(self):
        return self.__file


    pass



