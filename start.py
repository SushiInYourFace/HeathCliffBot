import logging
import subprocess
import sys

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

if not (sys.version_info[0] >= 3 and sys.version_info[1] >= 8):
    logging.warning("Python version 3.8+ is required, you are running this with " + ".".join([str(i) for i in sys.version_info[:3]]))
    exit()


run = True
while run:
    subprocess.run(["git","fetch","origin"])
    b = subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "HEAD"],stdout=subprocess.PIPE)
    branch = b.communicate()[0].decode().replace("\n","")
    local = subprocess.Popen(["git", "log", "--name-only", "origin/"+branch+"..HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = local.communicate()
    if not out:
        incoming = subprocess.Popen(["git", "diff", "--name-only", "HEAD", "origin/"+branch], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = incoming.communicate()
        if out:
            subprocess.run(["git", "pull"], stdout=subprocess.PIPE)
            logging.info("Updated!")
        else:
            logging.info("No Update Required.")
    else:
        logging.info("Committed changes, not updating.")
    code = subprocess.run([sys.executable,"bot.py"],stdout=subprocess.PIPE).returncode
    if code == 0:
        run = False

logging.info("Bot stopped!")


