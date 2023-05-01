import re
from assets.extentions import debug
log = ""

def set_log(location):
    global log
    log = location


def get(id, entry_location_index):
    global log
    alias_list = "callsign = contact", "tx_exchange = txch", "rx_exchange = rxch", "serial_number = ser", "frequency = freq"
    f = open(log, 'r').readlines()[entry_location_index-1]
    for i, content in enumerate(alias_list):
        if id in content:
            id = alias_list[i].split("=")[1].strip()
            break
    match = re.search(fr"{id}\[(.*?)\]", f)
    try:
        final = match.group(1)
        return final
    except:
        print(f'No match was found for "{id}"')
        return "!EMPTY!"


def get_raw(entry_location_index): # legacy
    global log
    try:
        f = open(log,"r")
        log_object = f.readlines()[entry_location_index-1]
    except Exception as error:
        return "!FATAL!"
    if log_object.split("$")[0] == "entry":
        pattern = r'\[(.*?)\]'
        matches = re.findall(pattern, log_object.split("$")[1])
        return tuple(matches)
    else:
        return "!EMPTY!"


def validate_file(location=None):
    global log
    if location is None:
        f = open(log, 'r')
    else:
        f = open(location, 'r')
    try:
        log_object = f.readlines()[0]
    except:
        debug.report('hlf-I/O error: your log file appears to be blank or damaged... please refer to the hlf-v2 format specs to add a "meta$" entry to the file and initalize it... ')
    if log_object.split("$")[0] == "meta":
        try:
            version = get("format", 1).split("?")
            if version[0] == "hlf":
                print(f'Log file is a valid hlf {version[1].split("-")[0]} file.')
                print(f"Created {get('creation-date', 1)} by {get('log-origin', 1)}.")
                return True
            else:
                print("WARNING: this file seems to be a hlf file with a meta index but the format and version data is incorect or damaged.")
                print("this is not being considered a valid hlf file.")
                return False
        except:
            print("WARNING: this file seems to be a hlf file with a meta index but the format and version data is incorect or damaged.")
            print("this is not being considered a valid hlf file.")
            return False
    else:
        return False
    
def dataset():
  return get("primary-dataset", 1)


def write_to_log(contact_info):
    print("log located at: " + log)
    data = "entry${" + f"time[{contact_info[0]}]:date[{contact_info[1]}]:freq[{contact_info[2]}]:contact[{contact_info[3]}]:power[{contact_info[4]}]:mode[{contact_info[5]}]:rxrst[{contact_info[6]}]:txrst[{contact_info[7]}]:comment[{contact_info[8]}]:txch[{contact_info[9]}]:rxch[{contact_info[10]}]:ser[{contact_info[11]}]" + "}" + "\n"
    with open(log, 'r') as f:
        meta, *memory = f.readlines()
        memory = [data] + memory
        memory = [meta] + memory
    f.close()
    f = open(log, 'w')
    f.writelines(memory)
    return data, memory


def create_human_readable(line_number): # legacy
    processed = ""
    raw = get_raw(line_number)
    if raw != "!EMPTY!":
        processed = str(processed) + f"{raw[0]} | {raw[1]} | {raw[2]} | {raw [3]} | {raw[4]} | {raw[5]} | {raw[6]}/{raw[7]} | "
        if raw[9] != "":
            processed = str(processed) + f"{raw[9]} | "
        processed = str(processed) + f"{raw[10]} | #{raw[11]}"
        return processed
    else:
        return "!EMPTY!"
 