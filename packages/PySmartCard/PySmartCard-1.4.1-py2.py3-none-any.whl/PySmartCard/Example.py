# -*- coding: utf-8 -*-

from PySmartCard.CpuCard import D8Reader
from PySmartCard.CpuCard import D6Reader
from PySmartCard.CpuCard import PcscReader
import time


def send_apdu(reader, apdu, recv_list, readertype=None):
    # Clear list
    recv_list[:] = []
    apdu = apdu.replace(" ", "")
    time1 = time.strftime("%Y_%m_%d %H:%M:%S", time.localtime(time.time()))
    showlog = "{} {} {}".format(time1, " Send: ", apdu)
    # print(time1, " Send: ", apdu)
    print(showlog)
    result = reader.send_apdu(apdu, readertype)
    time2 = time.strftime("%Y_%m_%d %H:%M:%S", time.localtime(time.time()))
    showlog = "{} {} {}".format(time2, " Recv: ", result)
    print(showlog)
    # print(time2, " Recv: ", result)
    # recv values
    recv_list.append(result[:-4])
    # SW
    recv_list.append(result[-4:])


def send_apducommand(reader, apdu, recv_list, readertype=None):
    send_apdu(reader, apdu, recv_list, readertype)
    if recv_list[1][0:2] == "61":
        apdu = "00C00000" + recv_list[1][2:4]
        send_apdu(reader, apdu, recv_list, readertype)
    elif recv_list[1][0:2] == "6C":
        apdu = apdu[0:8] + recv_list[1][2:4]
        send_apdu(reader, apdu, recv_list, readertype)


def test_d8():
    print("Test D8Reader...")
    d8 = D8Reader()

    result = d8.connect_device()
    if result < 0:
        print("ConnectDevice Failed!")
        return -1
    else:
        print("ConnectDevice Success...")

    result = d8.power_on_get_uid()
    print(result)
    return 0

    result = d8.power_on()
    if len(result) < 1:
        d8.disconnect_device()
        print("Device PowerOn Failed!")
        return -1
    else:
        print("Device PowerOn Success...")
        print("ATR: ", result)

    apdu = "0084000008"

    revc_info = []
    send_apducommand(d8, apdu, revc_info)

    if revc_info[1] != "9000":
        print("Send Apdu Failed!")
        return -1

    e_key = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    encrypt_data = d8.des3_ecb(revc_info[0], e_key, 1)

    apdu = "0082000008" + encrypt_data
    send_apducommand(d8, apdu, revc_info)
    if revc_info[1] != "9000":
        d8.disconnect_device()
        print("Send Apdu Failed!")
        return -1

    d8.disconnect_device()
    return 0


def test_d82():
    d8 = D8Reader()

    result = d8.connect_device()
    if result < 0:
        print("ConnectDevice Failed!")
        return -1
    else:
        print("ConnectDevice Success...")

    result = d8.power_on()
    if len(result) < 1:
        print("Device PowerOn Failed!")
        d8.disconnect_device()
        return -1
    else:
        print("Device PowerOn Success...")
        print("ATR: ", result)

    apdu = "00A4040008 A000000632010105"

    revc_info = []
    send_apducommand(d8, apdu, revc_info)

    if revc_info[1] != "9000":
        print("Send Apdu Failed!")
        d8.disconnect_device()
        return -1

    d8.disconnect_device()
    return 0


def test_pcsc():
    print("Test PcscReader...")
    pcsc = PcscReader()
    result = pcsc.get_pcsc_readerlist()
    readername = result.split(";")
    for iname in range(len(readername) - 1):
        showlog = "{} {} : {}".format("reader", iname, readername[iname])
        print(showlog)

    # Identive CLOUD 4700 F Contact Reader 0
    # Identive CLOUD 4700 F Contactless Reader 1

    # linux readername
    # Contact Reader: Identive Identive CLOUD 4500 F Dual Interface Reader
    #                 [CLOUD 4700 F Contact Reader] (53201441201079) 00 00
    # Ctless Reader:Identive Identive CLOUD 4500 F Dual Interface Reader
    #               [CLOUD4700 F Contactless Reader] (53201441201079) 01 00

    readername = "Identive CLOUD 4700 F Contact Reader 0"
    # readername = "Identive CLOUD 4700 F Contactless Reader 1 "

    result = pcsc.connect_device(readername)
    if len(result) == 0:
        print("ConnectDevice Failed!")
        return -1
    else:
        print("ConnectDevice Success...")
        print("ATR: ", result)

    # 1-contact reader 2-contactless reader
    readertype = 1

    result = pcsc.power_on(readertype)
    if result != 0:
        pcsc.disconnect_device()
        print("Device PowerOn Failed!")
        return -1
    else:
        print("Device PowerOn Success...")

    apdu = "0084000008"
    apdu = "00A4040008 A000000632010105"
    apdu = "00A4040008 A000000333010101"
    revc_info = []
    send_apducommand(pcsc, apdu, revc_info, readertype)
    if revc_info[1] != "9000":
        pcsc.disconnect_device()
        print("Send Apdu Failed!")
        return -1

    apdu = "00B2010C00"
    icount = 1
    while(1):
        send_apducommand(pcsc, apdu, revc_info, readertype)
        if revc_info[1] != "9000":
            print("Send Apdu Failed!")
            return -1
        icount = icount + 1
        if icount > 50:
            break

    pcsc.disconnect_device()
    return 0


def test_d6():
    print("Test D6Reader...")
    d6 = D6Reader()

    result = d6.connect_device()
    if result < 0:
        print("ConnectDevice Failed!")
        return -1
    else:
        print("ConnectDevice Success...")

    result = d6.power_on()
    if len(result) < 1:
        d6.disconnect_device()
        print("Device PowerOn Failed!")
        return -1
    else:
        print("Device PowerOn Success...")
        print("ATR: ", result)

    apdu = "0084000008"

    revc_info = []

    send_apducommand(d6, apdu, revc_info)
    if revc_info[1] != "9000":
        print("Send Apdu Failed!")
        d6.disconnect_device()
        return -1

    d6.disconnect_device()
    return 0


if __name__ == '__main__':
    if test_pcsc() == 0:
        print("Test OK...")
    else:
        print("Test Failed!")
