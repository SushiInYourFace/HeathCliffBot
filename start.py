import logging
import subprocess
import sys

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

if not (sys.version_info[0] >= 3 and sys.version_info[1] >= 8):
    logging.warning("Python version 3.8+ is required, you are running this with " + ".".join([str(i) for i in sys.version_info[:3]]))
    exit()


run = True
while run:
    code = subprocess.run([sys.executable,"bot.py"],stdout=subprocess.PIPE).returncode
    if code == 0:
        run = False

logging.info("Bot stopped!")


