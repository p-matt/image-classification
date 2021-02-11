import sys
from python.WebManager import WebManager
from python.Utils import load_ML_model
import python.Database
sys.path.insert(0, './python')

python.Database.connect()
# python.Database.create_filled_tables() create and fill tables only once


load_ML_model()
wm = WebManager()
server = wm.server

if __name__ == '__main__':
    wm.run()

