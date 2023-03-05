import datetime
def analyze(input_tuple):
    values = input_tuple
    # check time input
    try:
        time = values[0].split(":")
        try:
            if time[0] <= 24 and time[1] <= 60:
                time_scan = True
            else:
                return "!TIME_ERROR!"
        except:
            if time[0] <= 24 and time[1] <= 60 and time[2] <= 60:
                time_scan = True
        else:
            print("time error")
            return "!TIME_ERROR!"
    except:
        pass

    # check date input TODO: This thing sucks... it needs fixed to support more formats.
    try:
        date_processing = datetime.datetime.strptime(str(values[1]), '%m/%d/%Y')
        if date_processing.date() <= datetime.datetime.today().date():
            date_scan = True
    except ValueError as e:
        print(f"date error: {e}")
        return "!DATE_ERROR!"

    return (values[0], values[1], ''.join(char for char in values[2] if not char.isalpha()), values[3].upper(),
    ''.join(char for char in values[4] if not char.isalpha()), values[5].upper(), values[6], values[7])
