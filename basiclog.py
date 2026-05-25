
import time
#ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def log(x,file="log.log"):
    #ts=datetime.now().strftime("[%Y-%m-%d Ymd %H:%M:%S HMS] ")
    ts = time.strftime("[%Y%m%d%H%M%S]", time.localtime())
    y=open(file,"a")
    y.write(f"{ts} {x}\n")
