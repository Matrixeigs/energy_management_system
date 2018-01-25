# The web scraping function from EMA to obtain the prices
import requests
import bs4
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, FLOAT, INTEGER,create_engine
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.blocking import BlockingScheduler  # Time scheduler

root_url = 'http://www.emcsg.com'
index_url = root_url + '/marketdata/priceinformation'

emc_data_base = \
    {
        "db_str" : 'mysql+pymysql://' + 'lems' + ':' + '3' + '@' + 'localhost' + '/' + 'emc_data'
    }

Base = declarative_base()

class emc_history_data(Base):
    # one minute data
    __tablename__ = 'half_hour_data'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    Demand = Column(FLOAT)
    TCL = Column(FLOAT)
    USEP = Column(FLOAT)
    EHEUR = Column(FLOAT)
    LCP = Column(FLOAT)
    Regulation = Column(FLOAT)
    Primary = Column(FLOAT)
    Secondary = Column(FLOAT)
    Contingency = Column(FLOAT)

def get_data():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text,"html5lib")
    price = soup.find_all("table", {"ptable realtimePriceTable"})
    previous = price[1].text.splitlines()
    return previous

def store_data(*args):
    # Using the database to store EMC data
    Target_time = args[0]
    session = args[1]
    data = args[2]
    if session.query(emc_history_data).filter(emc_history_data.TIME_STAMP == Target_time).count() == 0:
        session.add(data)
        session.commit()
    else:
        print("There exist previous data, and they will be updated!")
        row = session.query(emc_history_data).filter(emc_history_data.TIME_STAMP == Target_time).first()
        row.Demand = data.Demand
        row.TCL = data.TCL
        row.USEP = data.USEP
        row.EHEUR = data.EHEUR
        row.LCP = data.LCP
        row.Regulation = data.Regulation
        row.Primary = data.Primary
        row.Secondary = data.Secondary
        row.Contingency = data.Contingency
        session.commit()

def run():
    db_str = emc_data_base["db_str"]
    engine = create_engine(db_str, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    # print(data)
    start = 3
    T = 12
    data = get_data()

    info = data[start+T*2:start+T*3]
    data_time = info[0]+" "+info[1][0:5]+":00"
    data_time_int = time.mktime(time.strptime(data_time, '%d %b %Y %H:%M:%S'))
    info_len = len(info)
    for i in range(2,info_len):
        try:
            info[i]=float(info[i])
        except:
            info[i] = pow(2,16)

    data_update = emc_history_data(TIME_STAMP = data_time_int,
                                   Demand = info[2],
                                   TCL = info[3],
                                   USEP = info[4],
                                   EHEUR = info[5],
                                   LCP = info[6],
                                   Regulation = info[7],
                                   Primary = info[8],
                                   Secondary = info[9],
                                   Contingency = info[10],)

    store_data(data_time_int,session,data_update)

if __name__ == "__main__":
    sched_scarping = BlockingScheduler()
    sched_scarping.add_job(run,'cron',minute='*/30',second='30')
    sched_scarping.start()