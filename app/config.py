def config_read():
    try: 
        with open('.cache', 'r') as file:
            prevUsername = file.read()
    except:
        prevUsername = ''
        