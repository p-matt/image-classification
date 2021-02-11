import psycopg2
import base64
import os
from python.Utils import get_images_label
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.sql import Identifier, SQL

cursor = ""


def create_filled_tables():
    for image_label in get_images_label():
        cursor.execute(SQL("CREATE TABLE {} (id  SERIAL, data BYTEA)").format(Identifier(image_label)))
        files = next(os.walk(os.getcwd() + "\\assets\\img\\" + image_label))[2]
        location = "assets/img/" + image_label + "/"
        for file in files:
            with open(location + file, "rb") as img:
                data = base64.b64encode(img.read())
                cursor.execute(SQL("INSERT INTO {} (data) VALUES (%s)").format(Identifier(image_label)), [data])


def get_data_from_db(label):
    cursor.execute(SQL("SELECT data FROM {} ORDER BY random() limit 30").format(Identifier(label)))
    return cursor.fetchall()


def connect():
    global cursor
    con = psycopg2.connect(database="d2oftsg6prl7ft", user="onhhktvrnvbiuv",
                           password="907843eea3c9672ea019569874aa942a1b51d49ed5e887614b7a2cc5f9915e00",
                           host="ec2-54-220-35-19.eu-west-1.compute.amazonaws.com", port="5432")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()
