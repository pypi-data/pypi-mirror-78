# -*- coding: utf-8 -*-

import ctypes
import platform
import os


class SmartCardAlgo(object):
    """

    SmartCardAlgo is the base class of PCSC/D6/T6/D8 readers and
    encapsulates some common algorithms in the field of smart cards[CPU card].

    Attributes:
        reader_lib: Handle of the underlying library.
        ispython2: if ispython2 = True means that current python is version
        islinux: If the current system is linux, its value is equal to True,
                 otherwise it is equal to False.
        is64bit_python: if is64bit_python = True means that current python is
                        64-bit, otherwise 32-bit

    """

    reader_lib = None
    ispython2 = False
    islinux = False
    is64bit_python = False

    def __init__(self, likes_spam=False):
        """Inits SmartCardAlgo ."""

        oldcwd = os.getcwd()

        py_version = platform.architecture()
        if py_version[0] != "32bit":
            self.is64bit_python = True

        path = os.path.split(os.path.realpath(__file__))[0]

        if platform.system() == "Linux":
            if self.is64bit_python:
                path = os.path.join(path, "libReaderlib_64.so")
                if not os.path.exists(path):
                    path = "libReaderlib_64.so"
            else:
                path = os.path.join(path, "libReaderlib.so")
                if not os.path.exists(path):
                    path = "libReaderlib.so"
            self.islinux = True
        else:
            if self.is64bit_python:
                path = os.path.join(path, "ReaderLib_64.dll")
                if not os.path.exists(path):
                    path = "ReaderLib_64.dll"
            else:
                path = os.path.join(path, "ReaderLib2.dll")
                if not os.path.exists(path):
                    path = "ReaderLib.dll"

        self.reader_lib = ctypes.cdll.LoadLibrary(path)

        py_version = platform.python_version()
        self.ispython2 = False
        if py_version[0] == "2":
            self.ispython2 = True

    def des3_ecb(self, data, key, type):
        """

        3DES_ECB encryption and decryption operation

        Args:
            data: Input data,The length of the key must be a even number and
                  less than 2048[1024 bytes].
                  If the length of input data is not a multiple of 8,
                  will use 8000000000000000 for the complement.
            key: Key value,The length of the key must be 32 [16 byets].
            type: 0-Decrypt 1-Encrypt

        Returns:
            Returns the result data if the execution succeeds, otherwise None.

        Raises:
         IOError: An error occurred when the length of data/key is incorrect.

        """

        if len(key) != 32:
            raise Exception("the legth of key[parameter] must be 32[16 bytes]")

        if len(data) % 2 != 0:
            raise Exception("the legth of data[parameter] must be a even "
                            "number")

        if len(data) > 2048:
            raise Exception("the legth of data[parameter] must be less than "
                            "2049[1024 bytes] ")

        if type != 1 and type != 0:
            raise Exception("the value of type[parameter] must be 0 or 1  ")

        padding = len(data) / 2 % 8
        if padding != 0:
            padding_buf = "8000000000000000"
            data = data + padding_buf[0:int(16 - padding * 2)]

        result = "R" * len(data)

        if self.ispython2 is False:
            data = bytes(data, "utf-8")
            result = bytes(result, "utf-8")
            key = bytes(key, "utf-8")

        self.reader_lib.Triple_ECB(data, key, result, type)
        if self.ispython2 is False:
            result = result.decode()

        return result

    def des3_cbc(self, data, key, type, initial_vector="0000000000000000"):
        """

        3DES_CBC encryption and decryption operation

        Args:
            data: Input data,The length of the key must be a even number and
                  less than 2048[1024 bytes].
                  If the length of input data is not a multiple of 8,
                  will use 8000000000000000 for the complement.
            key: Key value,The length of the key must be 32 [16 byets].
            type: 0-Decrypt 1-Encrypt
            initial_vector: the Initial vector of CBC,The default value is
                            0000000000000000

        Returns:
            Returns the result data if the execution succeeds, otherwise None.

        Raises:
            IOError: An error occurred when the length of data/key is
                  incorrect.
        """

        if len(key) != 32:
            raise Exception("the length of key[parameter] must be 32"
                            "[16 bytes]")

        if len(data) % 2 != 0:
            raise Exception("the length of data[parameter] must be a even "
                            "number")

        if len(data) > 2048:
            raise Exception("the length of data[parameter] must be less than "
                            "2049[1024 bytes] ")

        if type != 1 and type != 0:
            raise Exception("the value of type[parameter] must be 0 or 1  ")

        if len(initial_vector) != 16:
            raise Exception("the length of data[parameter] must be a even "
                            "number")

        padding = len(data) / 2 % 8
        if padding != 0:
            padding_buf = "8000000000000000"
            data = data + padding_buf[0:int(16 - padding * 2)]

        result = "R" * len(data)

        if self.ispython2 is False:
            data = bytes(data, "utf-8")
            result = bytes(result, "utf-8")
            key = bytes(key, "utf-8")
            initial_vector = bytes(initial_vector, "utf-8")

        self.reader_lib.Triple_CBC(data, key, result, type, initial_vector)
        if self.ispython2 is False:
            result = result.decode()

        return result

    def des_ecb(self, data, key, type):
        """

        DES_ECB encryption and decryption operation

        Args:
            data: Input data,The length of the key must be a even number and
                  less than2048[1024 bytes].
                  If the length of input data is not a multiple of 8,
                  will use 8000000000000000 for the complement.
            key: Key value,The length of the key must be 16 [8 byets].
            type: 0-Decrypt 1-Encrypt

        Returns:
            Returns the result data if the execution succeeds, otherwise None.

        Raises:
            IOError: An error occurred when the length of data/key is
                    incorrect.

        """

        if len(key) != 16:
            raise Exception("the length of key[parameter] must be 16[8 bytes]")

        if len(data) % 2 != 0:
            raise Exception("the length of data[parameter] must be a even "
                            "number")

        if len(data) > 2048:
            raise Exception("the length of data[parameter] must be less "
                            "than 2049[1024 bytes] ")

        if type != 1 and type != 0:
            raise Exception("the value of type[parameter] must be 0 or 1  ")

        padding = len(data) / 2 % 8
        if padding != 0:
            padding_buf = "8000000000000000"
            data = data + padding_buf[0:int(16 - padding * 2)]

        result = "R" * len(data)

        if self.ispython2 is False:
            data = bytes(data, "utf-8")
            result = bytes(result, "utf-8")
            key = bytes(key, "utf-8")

        self.reader_lib.Single_ECB(data, key, result, type)
        if self.ispython2 is False:
            result = result.decode()

        return result

    def sm4_ecb(self, data, key, type):
        """

        SM4_ECB encryption and decryption operation

        Args:
            data: Input data,The length of the key must be a even number
                  and less than 2048[1024 bytes].and the length of input
                  data must be a multipleof 32[16bytes].
            key: Key value,The length of the key must be 32 [16 byets].
            type: 0-Decrypt 1-Encrypt

        Returns:
            Returns the result data if the execution succeeds, otherwise None.

        Raises:
            IOError: An error occurred when the length of
                     data/key is incorrect.

        """

        if len(key) != 32:
            raise Exception("the length of key[parameter] must be "
                            "32[16 bytes]")

        if len(data) % 2 != 0:
            raise Exception("the length of data[parameter] must be a "
                            "even number")

        if len(data) > 2048:
            raise Exception("the length of data[parameter] must be less "
                            "than 2049[1024 bytes] ")

        if len(data) % 32 != 0:
            raise Exception("the length of data[parameter] must be must "
                            "be a multiple of 32")

        if type != 1 and type != 0:
            raise Exception("the value of type[parameter] must be 0 or 1  ")

        result = "R" * len(data)

        if self.ispython2 is False:
            data = bytes(data, "utf-8")
            result = bytes(result, "utf-8")
            key = bytes(key, "utf-8")

        self.reader_lib.SM4_ECB(data, key, result, type)

        if self.ispython2 is False:
            result = result.decode()

        return result

    def sm4_cbc(self, data, key, type,
                initial_vector="00000000000000000000000000000000"):
        """

        SM4_CBC encryption and decryption operation

        Args:
            data: Input data,The length of the key must be a even number and
                  less than 2048[1024 bytes].and the length of input data must
                  be a multiple of 32[16bytes].
            key: Key value,The length of the key must be 32 [16 byets].
            type: 0-Decrypt 1-Encrypt
            initial_vector: the Initial vector of CBC,The default value
                            is 00000000000000000000000000000000

        Returns:
            Returns the result data if the execution succeeds, otherwise None.

        Raises:
            IOError: An error occurred when the length of data/key
                     is incorrect.

        """

        if len(key) != 32:
            raise Exception("the length of key[parameter] must be "
                            "32[16 bytes]")

        if len(data) % 2 != 0:
            raise Exception("the length of data[parameter] must be a "
                            "even number")

        if len(data) > 2048:
            raise Exception("the length of data[parameter] must be less "
                            "than 2049[1024 bytes] ")

        if len(data) % 32 != 0:
            raise Exception("the length of data[parameter] must be must "
                            "be a multiple of 32")

        if type != 1 and type != 0:
            raise Exception("the value of type[parameter] must be 0 or 1  ")

        if len(initial_vector) != 32:
            raise Exception("the length of initial_vector[parameter] must "
                            "be 32[16 bytes]")

        result = "R" * len(data)

        if self.ispython2 is False:
            data = bytes(data, "utf-8")
            result = bytes(result, "utf-8")
            key = bytes(key, "utf-8")
            initial_vector = bytes(initial_vector, "utf-8")

        self.reader_lib.SM4_CBC(data, key, result, type, initial_vector)
        if self.ispython2 is False:
            result = result.decode()

        return result

    def get_mac(self, data, key, random_mac=""):
        """

        Get mac number[3des_ecb]

        Args:
            data: Input data,The length of the key must be a even number and
                  less than 2048[1024 bytes].and the length of input data
                  must be a multiple of 32[16bytes].
            key: Key value,The length of the key must be 32 [16 byets].
            random_mac: Random number.Its value can be a 16-bit random
                        number[8 bytes]or empry string The default value is ""

        Returns:
            Returns the result data if the execution succeeds, otherwise None.

        Raises:
            IOError: An error occurred when the length of data/key
                     is incorrect.

        """

        if len(key) != 32:
            raise Exception("the length of key[parameter] must be "
                            "32[16 bytes]")

        if len(data) % 2 != 0:
            raise Exception("the length of data[parameter] must be a "
                            "even number")

        if len(data) > 2048:
            raise Exception("the length of data[parameter] must be less "
                            "than 2049[1024 bytes] ")

        if len(random_mac) > 0:
            if len(random_mac) != 16:
                raise Exception("the length of random_mac[parameter] must "
                                "be 16[8 bytes]")

        result = "R" * 8

        if self.ispython2 is False:
            data = bytes(data, "utf-8")
            result = bytes(result, "utf-8")
            key = bytes(key, "utf-8")
            random_mac = bytes(random_mac, "utf-8")

        self.reader_lib.MAC(data, key, result, random_mac)
        if self.ispython2 is False:
            result = result.decode()

        return result

    def get_mac_sm4(self, data, key, random_mac=""):
        """

        Get mac(sm4) number[3des_ecb]

        Args:
            data: Input data,The length of the key must be a even number and
                  less than 2048[1024 bytes].and the length of input data
                  must be a multiple of 32[16bytes].
            key: Key value,The length of the key must be 32 [16 byets].
            random_mac: Random number.Its value can be a 32-bit random number
                        [16 bytes] or empry string The default value is ""

        Returns:
            Returns the result data if the execution succeeds, otherwise None.

        Raises:
            IOError: An error occurred when the length of data/key
                     is incorrect.

        """

        if len(key) != 32:
            raise Exception("the length of key[parameter] must be "
                            "32[16 bytes]")

        if len(data) % 2 != 0:
            raise Exception("the length of data[parameter] must be a "
                            "even number")

        if len(data) > 2048:
            raise Exception("the length of data[parameter] must be "
                            "less than 2049[1024 bytes] ")

        if len(random_mac) > 0:
            if len(random_mac) != 32:
                raise Exception("the length of random_mac[parameter] "
                                "must be 32[16 bytes]")

        result = "R" * 8

        if self.ispython2 is False:
            data = bytes(data, "utf-8")
            result = bytes(result, "utf-8")
            key = bytes(key, "utf-8")
            random_mac = bytes(random_mac, "utf-8")

        self.reader_lib.MAC_SM4(data, key, result, random_mac)
        if self.ispython2 is False:
            result = result.decode()

        return result


class D8Reader(SmartCardAlgo):
    """

    D8Reader is a class of D8 reader, inherits from SmartCardAlgo,
    and encapsulates functions that operate readers.

    D6/T6/D8 readers only provide support for Windows systems currently.

    D8Reader does not support 64-bit python, only supports 32-bit python,
    if you are using a 64-bit system, please install 32-bit python.

    If you use D6/D8/T6 reader under Windows system, you need to
    ensure that there are no other versions of drcf32.dll and
    dici32.dll files in the environment path directory. Otherwise,
    calling the card reader may have abnormal behavior.
    The D8/DT/T6 reader depends on the software and hardware
    support provided by the reader manufacturer. If the reader
    you use corresponds to a special version dynamic library, please replace
    the corresponding library in the installation directory.

    Attributes:
        handle: Handle of D8 reader.
    """

    handle = -1

    def __init__(self, likes_spam=False):
        """Inits D8Reader ."""
        SmartCardAlgo.__init__(self)

        if self.islinux is True:
            raise Exception("D6Reader/D8Reader is not supported on Linux "
                            "systems currently, please use PcscReader")

        if self.is64bit_python is True:
            raise Exception("D6Reader/D8Reader is not supported on 64-bit "
                        "python currently, please use 32-bit python or PcscReader")

    def connect_device(self, baud_rate=115200):
        """

        Link D8 reader

        Args:
            baud_rate: Specify the baud rate at which the card communicates
                       with the reader.The default value is 115200

        Returns:
            Returns 0 if the execution succeeds, otherwise returns -1.

        """
        if self.islinux is True:
            self.handle = self.reader_lib.ConnectDevice(2, baud_rate)
        else:
            self.handle = self.reader_lib.ConnectDevice(100, baud_rate)
        if self.handle <= 0:
            return -1
        else:
            return 0

    def power_on(self):
        """

        Power-on and reset card to obtain card reset information

        Args:
            None.

        Returns:
            Returns reset information if the execution succeeds,
            otherwise returns "".

        """

        if self.handle < 0:
            raise Exception("D8 reader has not connected yet. ")

        atr_info = "R" * 100
        if self.ispython2 is False:
            atr_info = bytes(atr_info, "utf-8")
        result = self.reader_lib.PowerOn(self.handle, atr_info)
        if result < 0:
            return ""
        else:
            if self.ispython2 is False:
                atr_info = atr_info.decode()
            atr_info = atr_info.replace("R", "")
            return atr_info

    def power_on_get_uid(self):
        """

        Power-on and reset card to obtain card reset information and card uid

        Args:
            None.

        Returns:
            Returns reset information and card uidif the execution succeeds,
            otherwise returns "".
            The returned data is atr, non-IOS standard uid, ISO standard uid,
            these three values are separated by ";"

        """

        if self.handle < 0:
            raise Exception("D8 reader has not connected yet. ")

        atr_info = "R" * 130
        if self.ispython2 is False:
            atr_info = bytes(atr_info, "utf-8")
        result = self.reader_lib.PowerOn_d8_uid(self.handle, atr_info)
        if result < 0:
            return ""
        else:
            if self.ispython2 is False:
                atr_info = atr_info.decode()
            atr_info = atr_info.replace("R", "")
            return atr_info

    def send_apdu(self, apdu, readertype=None):
        """

        Send apdu command to the reader

        Args:
            apdu: Apdu command
            readertype: This parameter has not been used for the time being.

        Returns:
            Returns the return value of the apducommunication.
            The return value is a value of type list, the first
            element is the real return value, and the second element is SW.

        """
        if self.handle < 0:
            raise Exception("D8 reader has not connected yet. ")

        if len(apdu) % 2 != 0:
            raise Exception("the length of apdu[parameter] must be a "
                            "even number")

        recv_info = "R" * 700
        if self.ispython2 is False:
            recv_info = bytes(recv_info, "utf-8")
            apdu = bytes(apdu, "utf-8")

        self.reader_lib.SendApdu(self.handle, apdu, recv_info)

        if self.ispython2 is False:
            recv_info = recv_info.decode()
        recv_info = recv_info.replace("R", "")
        return recv_info

    def disconnect_device(self):
        """

        Disconnect D8 reader

        Args:
            None.

        Returns:
            No returns

        """

        self.reader_lib.DisConnectDevice(self.handle)
        self.handle = -1


class D6Reader(SmartCardAlgo):
    """

    D6Reader is a class of D6/T6 reader, inherits from SmartCardAlgo,
    and encapsulates functions that operate readers.

    D6/T6/D8 readers only provide support for Windows systems currently.

    D6Reader does not support 64-bit python, only supports 32-bit python,
    if you are using a 64-bit system, please install 32-bit python

    If you use D6/D8/T6 reader under Windows system, you need to
    ensure that there are no other versions of drcf32.dll and
    dici32.dll files in the environment path directory. Otherwise,
    calling the card reader may have abnormal behavior.
    The D8/DT/T6 reader depends on the software and hardware
    support provided by the reader manufacturer. If the reader
    you use corresponds to a special version dynamic library, please replace
    the corresponding library in the installation directory.

    Attributes:
        handle: Handle of D6/T6 reader.

    """

    handle = -1

    def __init__(self, likes_spam=False):
        """Inits D6Reader ."""
        SmartCardAlgo.__init__(self)

        if self.islinux is True:
            raise Exception("D6Reader/D8Reader is not supported on Linux "
                            "systems currently, please use PcscReader")

        if self.is64bit_python is True:
            raise Exception("D6Reader/D8Reader is not supported on 64-bit "
                            "python currently, please use 32-bit python or PcscReader")

    def connect_device(self):
        """

        Link D6/T6 reader

        Args:
            None.

        Returns:
            Returns 0 if the execution succeeds, otherwise returns -1.

        """
        self.handle = self.reader_lib.ConnectDevice_d6(100, 115200)
        if self.handle <= 0:
            return -1
        else:
            return 0

    def power_on(self):
        """

        Power-on and reset card to obtain card reset information

        Args:
            None.

        Returns:
            Returns reset information if the execution succeeds,
            otherwise returns "".

        """

        if self.handle < 0:
            raise Exception("D6/T6 reader has not connected yet. ")

        atr_info = "R" * 100
        if self.ispython2 is False:
            atr_info = bytes(atr_info, "utf-8")
        result = self.reader_lib.PowerOn_d6(self.handle, atr_info)
        if result < 0:
            return ""
        else:
            if self.ispython2 is False:
                atr_info = atr_info.decode()
            atr_info = atr_info.replace("R", "")
            return atr_info

    def send_apdu(self, apdu, readertype=None):
        """

        Send apdu command to the reader

        Args:
            apdu: Apdu command
            readertype: This parameter has not been used for the time being.

        Returns:
            Returns the return value of the apducommunication.
            The return value is a value of type list, the first
            element is the real return value, and the second element is SW.

        """
        if self.handle < 0:
            raise Exception("D6/T6 reader has not connected yet. ")

        if len(apdu) % 2 != 0:
            raise Exception("the length of apdu[parameter] must be a "
                            "even number")

        recv_info = "R" * 700
        if self.ispython2 is False:
            recv_info = bytes(recv_info, "utf-8")
            apdu = bytes(apdu, "utf-8")

        self.reader_lib.SendApdu_d6(self.handle, apdu, recv_info)

        if self.ispython2 is False:
            recv_info = recv_info.decode()
        recv_info = recv_info.replace("R", "")
        return recv_info

    def disconnect_device(self):
        """

        Disconnect D6 reader

        Args:
            None.

        Returns:
            No returns

        """

        self.reader_lib.DisConnectDevice_d6(self.handle)
        self.handle = -1


class PcscReader(SmartCardAlgo):
    """

    PcscReader is a class of PCSC reader, inherits from SmartCardAlgo,
    and encapsulates functions that operate readers.

    PcscReader can be used under windows/linux system.

    PcscReader support 32-bit/64-bit python.

    Attributes:
        handle: Handle of pcsc reader.

    """

    handle = -1

    def __init__(self, likes_spam=False):
        """Inits PcscReader ."""
        SmartCardAlgo.__init__(self)

    def get_pcsc_readerlist(self):
        """

        Get a list of PCSC reader names that aleady connected to the computer

        Args:
            None.

        Returns:
            Returns readerlist information if the execution succeeds[
            The name of each reader is separated by ';'],otherwise returns "".

        """

        readerlist = "~" * 600
        if self.ispython2 is False:
            readerlist = bytes(readerlist, "utf-8")

        result = self.reader_lib.GetPcscReaderName(readerlist)
        if result < 0:
            return ""
        else:
            if self.ispython2 is False:
                readerlist = readerlist.decode()
            readerlist = readerlist.replace("~", "")
            return readerlist

    def connect_device(self, readername):
        """

        Link PCSC reader

        Args:
            readername: Contact/Contactless reader name

        Returns:
            Returns reset information if the execution succeeds,
            otherwise returns "".

        """

        if len(readername) < 0:
            raise Exception("readername[parameter] can not be empty. ")

        atr_info = "R" * 100
        if self.ispython2 is False:
            atr_info = bytes(atr_info, "utf-8")
            readername = bytes(readername, "utf-8")

        # windows 64-bit python
        if self.islinux is False and self.is64bit_python is True:
            self.reader_lib.ConnectDevice_pcsc.restype = ctypes.c_ulonglong
        else:
            self.reader_lib.ConnectDevice_pcsc.restype = ctypes.c_ulong

        self.handle = self.reader_lib.ConnectDevice_pcsc(readername,
                                                         atr_info)
        if self.handle < 0:
            return ""
        else:
            if self.ispython2 is False:
                atr_info = atr_info.decode()
            atr_info = atr_info.replace("R", "")
            return atr_info

    def power_on(self, protocol_type):
        """

        Power-on and reset card

        Args:
            protocol_type: Specifies communication protocol
                        1-SCARD_PROTOCOL_T0 2-SCARD_PROTOCOL_T1
        Returns:
            Returns 0 if the execution succeeds, otherwise returns -1.

        """

        if self.handle < 0:
            raise Exception("PCSC reader has not connected yet. ")

        if protocol_type != 1 and protocol_type != 2:
            raise Exception("the value of protocol_type[parameter]"
                            " must be 1 or 2  ")

        # windows 64-bit python
        if self.islinux is False and self.is64bit_python is True:
            self.reader_lib.PowerOn_pcsc.argtypes = [ctypes.c_ulonglong,
                                                     ctypes.c_int]

        result = self.reader_lib.PowerOn_pcsc(self.handle, protocol_type)
        if result < 0:
            return -1
        else:
            return 0

    def send_apdu(self, apdu, protocol_type):
        """

        Send apdu command to the reader

        Args:
            apdu: Apdu command
            protocol_type: Specifies communication protocol
                        1-SCARD_PROTOCOL_T0 2-SCARD_PROTOCOL_T1
        Returns:
            Returns the return value of the apducommunication.
            The return value is a value of type list, the first
            element is the real return value, and the second element is SW.

        """
        if self.handle < 0:
            raise Exception("PCSC reader has not connected yet. ")

        if len(apdu) % 2 != 0:
            raise Exception("the length of apdu[parameter] must be a \
                even number")

        if protocol_type != 1 and protocol_type != 2:
            raise Exception("the value of protocol_type[parameter]\
                must be 1 or 2  ")

        recv_info = "R" * 700
        if self.ispython2 is False:
            recv_info = bytes(recv_info, "utf-8")
            apdu = bytes(apdu, "utf-8")

        # windows 64-bit python
        if self.islinux is False and self.is64bit_python is True:
            self.reader_lib.SendApdu_pcsc.argtypes = [ctypes.c_ulonglong,
                                                      ctypes.c_int,
                                                      ctypes.c_char_p,
                                                      ctypes.c_char_p]

        self.reader_lib.SendApdu_pcsc(self.handle, protocol_type, apdu, recv_info)

        if self.ispython2 is False:
            recv_info = recv_info.decode()
        recv_info = recv_info.replace("R", "")
        return recv_info

    def disconnect_device(self):
        """

        Disconnect PCSC reader

        Args:
            None.

        Returns:
            No returns

        """

        # windows 64-bit python
        if self.islinux is False and self.is64bit_python is True:
            self.reader_lib.DisConnectDevice_pcsc.argtypes = [ctypes.c_ulonglong]

        self.reader_lib.DisConnectDevice_pcsc(self.handle)
        self.handle = -1


def main():
    d8 = D8Reader()

    result = d8.connect_device()
    if result < 0:
        print("ConnectDevice Failed")
        return
    else:
        print("ConnectDevice Success")

    result = d8.power_on()
    if len(result) < 1:
        print("Device PowerOn Failed")
        return
    else:
        print("Device PowerOn Success")
        print("ATR: ", result)

    apdu = "0084000008"

    result = d8.send_apdu(apdu)
    if len(result) < 1:
        print("Send Apdu Failed")
        return
    else:
        print("Send Apdu Success")
        print("Recv: ", result)

    d8.disconnect_device()
    print("DisConnectDevice Success")


if __name__ == '__main__':
    main()
