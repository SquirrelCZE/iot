import configparser
import psycopg2
import os

config = configparser.ConfigParser()
config.read_file(open(os.getenv("HOME") + "/.iot", "r"))

vals = dict(config.items("db"))

conn = psycopg2.connect(
    host=vals["host"],
    database=vals["database"],
    user=vals["user"],
    password=vals["password"],
)
