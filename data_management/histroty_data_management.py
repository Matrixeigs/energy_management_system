""" History data management for weather station
For incomplete information, most recent data will be used.
"""
# Generate long-term profile for the load
from configuration.configuration_database import local_load_database
from data_management.database_format import db_load_profile
from sqlalchemy import create_engine  # Import database
from sqlalchemy.orm import sessionmaker

def run():
    db_str = local_load_database["db_str"]
    engine = create_engine(db_str, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    Load = session.query(db_load_profile.Electricity).filter(db_load_profile.TIME_STAMP >= 0).all()

    Load_max = max(Load)



if __name__ == "__main__":
    ## Start the main process of local energy management system
    run()
