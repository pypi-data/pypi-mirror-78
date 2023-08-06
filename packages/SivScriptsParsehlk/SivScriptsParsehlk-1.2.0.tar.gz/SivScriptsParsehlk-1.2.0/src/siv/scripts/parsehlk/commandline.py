import argparse
import logging
import sys
import sqlalchemy
from sqlalchemy import  create_engine
import mysql.connector

from siv.scripts.parsehlk import scan_folder

def get_parser():
    parser = argparse.ArgumentParser(description='biostool')
    parser.add_argument("--folder", default="//WIN-6HNS1UBI6D7.hf.intel.com/HLKLogs/6-25-2020")
    return parser

def main():
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.INFO,
        stream=sys.stdout)
    logger = logging.getLogger()

    parser = get_parser()
    args = parser.parse_args()

    scan_folder(args.folder)
    conn=mysql.connector.connect(host="maria3860-us-fm-in.iglb.intel.com",

    user="wsivauto_so ",passwd="gYd3fX9NfA89qUy ", port=3307,

    ssl_ca="C:\Migration-APT\SSL Connection\IntelSHA256RootCA-Base64.crt")
    c=conn.cursor()
    engine = create_engine("mysql+pymysql://wsivauto_so:gYd3fX9NfA89qUy@maria3860-us-fm-in.iglb.intel.com/wsivauto")


    df1=pd.read_csv("rim.csv")
    df1.to_sql(name="HCKLogsTable",
           con=engine,
           index=False,
           if_exists='append')
