import datetime as dt

def get_time():
    now = dt.datetime.now()
    return now.strftime("%Y%m%d--%H:%M:%S")

def info(message, level=0):
    write_message(message, "INFO", level=level)
    
def error(message):
    write_message(message, "ERROR")

def warning(message, level=0):
    write_message(message, "WARNING", level=level)

def write_message(message, type, level=0):
    time = get_time()
    print(f"{time}--{type}--{message}") 
    
    if(level == 0):
        print(50*'=')
    elif(level == 1):
        print(50*'-')
    