#!flask/bin/python
from app import app

import sys
if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
	app.run(debug=True)