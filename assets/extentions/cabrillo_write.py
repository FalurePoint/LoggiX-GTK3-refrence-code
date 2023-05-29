# Most work by Daniel Weinhold (NC8R).

import os
from assets.extentions import hlfio
def begin_cabrillo(user_data, cab_file=None):
    if cab_file is None:
        cab_file = '/home/' + os.getlogin() + '/Documents/LoggiX/' + "KL5IS" + '.log'
    try:
        os.system(f'mkdir {"/home/" + os.getlogin() + "/Documents/LoggiX/"}')
    except:
        pass
    os.system(f"touch {cab_file}")

    with open(cab_file, 'w') as cab:
        cab.write('START-OF-LOG: 3.0 \n')
        cab.write('CALLSIGN: ' + "KL5IS" +'\n')
        cab.write('CONTEST: ' + user_data[16] + '\n')
        # cab.write('CATEGORY-ASSISTED: ' + user_data['assistcat'] + '\n')
        cab.write('CATEGORY-BAND: ' + user_data[19] + '\n')
        cab.write('CATEGORY-MODE: ' + user_data[20] + ' \n')
        cab.write('CATEGORY-OPERATOR: ' + user_data[23] + ' \n')
        cab.write('CATEGORY-POWER: ' + user_data[21] + ' \n')
        cab.write('CATEGORY-STATION: ' + user_data[22] + '\n')
        cab.write('CATEGORY-TIME: ' + user_data[25] + '\n')
        # cab.write('CATEGORY-TRANSMITTER: ' + user_data['xmtr'] + '\n')
        cab.write('CATEGORY-OVERLAY: ' + user_data[18] + '\n')
        # cab.write('CLAIMED-SCORE: \n')
        cab.write('CLUB: ' + user_data[17] + '\n')
        cab.write('CREATED-BY: LoggiX ' + user_data[26] + ' - https://github.com/FalurePoint/LoggiX \n')
        cab.write('EMAIL: '+ user_data[11] + ' \n')
        cab.write('GRID-LOCATOR: '+ user_data[14] + ' \n')
        cab.write('LOCATION: ' + user_data[13] + ' \n')
        cab.write('NAME: ' + user_data[15] + ' \n')
        cab.write('ADDRESS: ' + user_data[12] + '\n')
        # cab.write('ADDRESS: ' + user_data['ctyst']+ ' \n')
        cab.write('ADDRESS: ' + user_data[27] + '\n')
        cab.write('ADDRESS: \n')
        # cab.write('OPERATORS: ' + user_data[] + '\n')
        cab.write('SOAPBOX:' + user_data[28]+ '\n')


def write_cabrillo(cab_file=None):
    my_callsign = "KL5IS"
    if cab_file is None:
        cab_file = '/home/' + os.getlogin() + '/Documents/LoggiX/' + my_callsign + '.log'
    for count in range(1, len(open(hlfio.log, 'r').readlines())):
        #str(user_data['callsign'])
        freq = hlfio.get("freq", count + 1)
        callsign = hlfio.get("callsign", count + 1)
        time = hlfio.get("time", count + 1)
        mode = hlfio.get("mode", count + 1)
        txch = hlfio.get("tx_exchange", count + 1)
        rxch = hlfio.get("rx_exchange", count + 1)
        txrst = hlfio.get("txrst", count + 1)
        rxrst = hlfio.get("rxrst", count + 1)
        if mode == "SSB":
            cabrillo_mode = "PH"
        else:
           cabrillo_mode = mode
        date = hlfio.get("date", count + 1)
        time = time.replace(":", "")
        
        qso = "QSO: "+freq+' '+cabrillo_mode+' '+date+' '+time+' '+my_callsign+' '+rxrst+' '+txch+' '+callsign+' '+txrst+' '+rxch   


        cabfile = open(cab_file, 'a')
        cabfile.write(qso + '\n')
        cabfile.flush()

        count += 1

    cabfile = open(cab_file, 'a')
    cabfile.write('END-OF-LOG:')
        

