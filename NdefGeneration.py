import random
import re
from mFuzz import *

class NdefGeneration():
    """
        Class used to generate NDEF format from a payload
    """
    def __init__(self):
        self.len_tnf = 0
        self.payload = ''
        self.payload_length = 0
        self.ndef_payload = bytearray()
        self.header = {
            'MB' : 1, 'ME' : 1, 'CR' : 0, 'SR' : 1, 'IL' : 0, 'TNF' : '{0:03b}'.format(0)
        }

    def Bluetooth(self, payload):
        """
            An attempt to implement bluetooth ndef message generation
        """
        if re.search(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', payload):
            self.setPayload_length(len(payload.replace(':', '')))
            self.setTNF(2)
            return bytes([32,12]) + 'application/vnd.bluetooth.ep.oob'.encode('UTF-8')

    def getTNF(self):
        return self.header['TNF']

    def setTNF(self, tnf):
        print("Set tnf",tnf)
        if isinstance(tnf, int):
            self.header['TNF'] = '{0:03b}'.format(tnf)
        return None

    def getPayload_length(self):
        return self.payload_length

    def setPayload_length(self, payload):
        self.payload_length = payload

    def getlenTNF(self):
        return self.len_tnf

    def setlenTNF(self, len):
        self.len_tnf = len

    def Well_Known(self, payload):
        """
            Implementation of the Well Known type. Which decide the payload type.
            # TODO: finalize the smart poster implementation
        """
        self.payload = payload
        self.setPayload_length(payload)
        uri = self.Well_known_URI(payload)
        if self.getTNF() == "000" :
            self.setTNF(1)
        if uri :
            print(uri)
            return bytes([1,self.getPayload_length()]) + bytes([85]) + uri
        else:
            language = 'en'
            text = self.Well_Known_Text(payload, language)
            if text :
                return bytes([1,self.getPayload_length()+len(language)+1]) + text
        return None

    def Well_known_URI(self, payload):
        """
            Cross the Well_known_URI_Code, if the payload begins with
            one of the dictionnary keys, its return the payload type
        """
        Well_known_URI_Code = {'http://www.' : 1, 'https://www.' : 2, 'http://' : 3, 'https://' : 4,
         'tel:' : 5, 'mailto:' : 6, 'ftp://anonymous:anonymous@' : 7, 'ftp://ftp.' : 8,
         'ftps://' : 9, 'sftp://' : 10, 'smb://' : 11, 'nfs://' : 12, 'ftp://' : 13,
         'dav://' : 14, 'news:' : 15, 'telnet://' : 16, 'imap:' : 17, 'rtsp://' : 18,
         'urn:' : 19, 'pop:' : 20, 'sip:' : 21, 'sips:' : 22, 'tftp:' : 23, 'btspp://' : 24,
         'btl2cap://' : 25, 'btgoep://' : 26, 'tcpobex://' : 27, 'irdaobex://' : 28,
         'file://' : 29, 'urn:epc:id:' : 30, 'urn:epc:tag:' : 31, 'urn:epc:pat:' : 32,
         'urn:epc:raw:' : 33, 'urn:epc:' : 34, 'urn:nfc:' : 35}

        if re.search(r'^(?:(?:\+|00)[0-9]+[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})', payload):
            """
                Verify if the payload is a validate phone number
            """
            self.setPayload_length(len(payload)+1)
            return bytes([Well_known_URI_Code['tel:']])
        for key, value in Well_known_URI_Code.items():
            if key in payload:
                self.payload = payload.replace(key, "")
                print(self.payload)
                self.setPayload_length(len(payload)-len(key)+1)
                return bytes([value])
        return None

    def Well_Known_Text(self, payload, language):
        """
            The paylod is a Text
            Returns the payload type with its language and length language
            Default language : English
        """
        self.setPayload_length(len(payload))
        return bytes([84, len(language)]) + language.encode()

    def Well_Known_SP(self, payload):
        """
            # TODO: implement well Known type
        """
        pass

    def MIME(self, payload):
        """
            # TODO: implement Mime type
        """
        pass


    def Absolute_URI(self, payload):
        """
            Verify if the payload is a URL
            Set tnf type to 3
            Retrun payload length
        """
        tmp = re.search(r'^www?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$', payload)
        if tmp:
            self.setTNF(3)
            self.payload = payload
            return bytes([len(self.payload), 0])
        return None

    def Unknow(self, payload):
        pass

    def External(self, payload):
        pass

    def Unchanged(self, payload):
        pass

    def setRandMB(self):
        """
            Randomize MB header field
            Used to fuzz the MB header field
        """
        self.header['MB'] =  '{0:08b}'.format(random.randint(0,255))
    def setRandME(self):
        """
            Randomize ME header field
            Used to fuzz the ME header field
        """
        self.header['ME'] = '{0:08b}'.format(random.randint(0,255))
    def setRandCR(self):
        """
            Randomize CR header field
            Used to fuzz the CR header field
        """
        self.header['CR'] = '{0:08b}'.format(random.randint(0,255))
    def setRandSR(self):
        """
            Randomize SR header field
            Used to fuzz the SR header field
        """
        self.header['SR'] = '{0:08b}'.format(random.randint(0,255))
    def setRandIL(self):
        """
            Randomize IL header field
            Used to fuzz the IL header field
        """
        self.header['IL'] = '{0:08b}'.format(random.randint(0,255))
    def setRandTNF(self):
        """
            Randomize TNF header field
            Used to fuzz the TNF header field
        """
        self.header['TNF'] = '{0:08b}'.format(random.randint(0,255))

    def Empty(self, payload):
        """
            implement the empty type
        """
        if not payload or payload is " ":
            if self.getTNF() == "000" :
                self.setTNF(1)
            return bytes([1,len(payload)])
        return None

    def bitstring_to_bytes(self, s, fuzz):
        """
            Transform bitstring to bytes
            And randomize it if fuzz = 1
        """
        if fuzz :
            randbool = bool(random.getrandbits(1))
            return int(s, 2).to_bytes(32 // 8, byteorder='big', signed=randbool)
        return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

    def getNdef_payload(self, payload, fuzz, fields):
        """
            We're going to assume that an NDEF message is not truncated
            So it will be sent in full.
            Return the NDEF bytearray
        """
        if len(payload) < 1024 :
            empty = self.Empty(payload)

            header = ''.join(str(value) for key,value in self.header.items())
            if not payload or payload is " ":
                if fuzz :
                    mutated_sample = mutate(bytearray(payload.encode()), 10)
                    self.payload = mutated_sample
                    self.ndef_payload = bytearray(self.bitstring_to_bytes(header, fields)) + empty + bytearray(self.payload)
                elif fields :
                    self.ndef_payload = bytearray(self.bitstring_to_bytes(header, fields)) + empty + bytearray(self.payload.encode("UTF-8"))
                else:
                    self.ndef_payload = bytearray(self.bitstring_to_bytes(header, fields)) + empty + bytearray(self.payload.encode("UTF-8"))

            else:
                absolute_uri = self.Absolute_URI(payload)
                if absolute_uri :
                    header = ''.join(str(value) for key,value in self.header.items())
                    self.ndef_payload = bytearray(self.bitstring_to_bytes(header, fields)) + absolute_uri + bytearray(self.payload.encode("UTF-8"))
                else :
                    bluetooth = self.Bluetooth(payload)
                    if bluetooth:
                        header = ''.join(str(value) for key,value in self.header.items())
                        bytes_payload = bytearray(payload.replace(':', '').encode('UTF-8'))
                        self.ndef_payload = bytearray(self.bitstring_to_bytes(header, fields)) + bluetooth + bytes([12]) + bytes_payload + bytes([3, 3]) + bytes([6, 11])
                    else:
                        well_known = self.Well_Known(payload)
                        if well_known :
                            if fuzz :
                                header = ''.join(str(value) for key,value in self.header.items())
                                mutated_sample = mutate(bytearray(payload.encode()),10)
                                self.payload = mutated_sample
                                self.ndef_payload = bytearray(self.bitstring_to_bytes(header, fields)) + well_known + bytearray(self.payload)
                            elif fields :
                                self.ndef_payload = bytearray(self.bitstring_to_bytes(header, fields)) + well_known + bytearray(self.payload.encode("UTF-8"))
                            else:
                                header = ''.join(str(value) for key,value in self.header.items())
                                self.ndef_payload = bytearray(self.bitstring_to_bytes(header, fields)) + well_known + bytearray(self.payload.encode("UTF-8"))
            print(self.header)
            return self.ndef_payload
        return None
