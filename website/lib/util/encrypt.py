# coding=utf-8


import base64
import struct
import re

from Crypto.Cipher import AES
from django.conf import settings


#AES_BLOCK_SIZE = 32
#AES_SECRET_PASSWORD = 'AF616756C6E3C98ADA8A20624D5368E9'


def _padding(text):
    """
        Add the needed chars to fill the block size,
        The chars added are the ASCII value of the number
        needed
    """
    num = settings.AES_BLOCK_SIZE - (len(text) % settings.AES_BLOCK_SIZE)
    return text + chr(num) * num

def _unpadding(text):
    if len(text) == 0:
        return text
    
    lastchar = ord(text[-1])
    if lastchar > settings.AES_BLOCK_SIZE: # no padding
        return text
    return text.rstrip(unichr(lastchar))


def encode(text, cipher = None):
    """
        Encode the text, adding the padding needed,
        if not cipher is set, uses AES encryption
    """
    if cipher is None:
        cipher = AES.new(settings.AES_SECRET_PASSWORD)
        
    return armor(base64.b64encode(cipher.encrypt(_padding(text))))


def decode(text, cipher = None):
    if cipher is None:
        cipher = AES.new(settings.AES_SECRET_PASSWORD)
        
    return _unpadding(cipher.decrypt(base64.b64decode(dearmor(text))))

# ==========================
# from django-pgcrypto: https://bitbucket.org/dcwatson/django-pgcrypto
# ==========================
CRC24_INIT = 0xB704CE
CRC24_POLY = 0x1864CFB

def crc24( data ):
        crc = CRC24_INIT
        for byte in data:
                crc ^= (ord(byte) << 16)
                for i in xrange(8):
                        crc <<= 1
                        if crc & 0x1000000:
                                crc ^= CRC24_POLY
        return crc & 0xFFFFFF


def armor( data ):
        """
        Returns a string in ASCII Armor format, for the given binary data. The
        output of this is compatiple with pgcrypto's armor/dearmor functions.
        """
        template = '-----BEGIN PGP MESSAGE-----\n%(headers)s\n\n%(body)s\n=%(crc)s\n-----END PGP MESSAGE-----'
        headers = ['Version: django-pgcrypto 1.0']
        body = base64.b64encode( data )
        # The 24-bit CRC should be in big-endian, strip off the first byte (it's already masked in crc24).
        crc = base64.b64encode(struct.pack('>L', crc24(data))[1:])
        return template % {
                'headers': '\n'.join(headers),
                'body': body,
                'crc': crc
        }

class BadChecksumError (Exception):
        pass

def dearmor( text, verify=True ):
        """
        Given a string in ASCII Armor format, returns the decoded binary data.
        If verify=True (the default), the CRC is decoded and checked against that 
        of the decoded data, otherwise it is ignored. If the checksum does not
        match, a BadChecksumError exception is raised.
        """
        lines = text.strip().split( '\n' )
        data_lines = []
        check_data = None
        started = False
        in_body = False
        
        if verify:
            check_data = re.search('(?<=^=)\w+', text, re.MULTILINE).group(0)

        data = base64.b64decode(re.search('(?<=\n\n)\w+[=](?=\n=)', text,).group(0))
        if verify and check_data:
                # The 24-bit CRC is in big-endian, so we add a null byte to the beginning.
                crc = struct.unpack( '>L', '\0'+base64.b64decode(check_data) )[0]
                if crc != crc24(data):
                        raise BadChecksumError()
        """                
        for line in lines:
                if line.startswith('-----BEGIN'):
                        started = True
                elif line.startswith('-----END'):
                        break
                elif started:
                        if in_body:
                                if line.startswith('='):
                                        # Once we get the checksum data, we're done.
                                        check_data = line[1:5]
                                        break
                                else:
                                        # This is part of the base64-encoded data.
                                        data_lines.append( line )
                        else:
                                if line.strip():
                                        # This is a header line, which we basically ignore for now.
                                        pass
                                else:
                                        # The data starts after an empty line.
                                        in_body = True
        data = base64.b64decode( ''.join(data_lines) )
        if verify and check_data:
                # The 24-bit CRC is in big-endian, so we add a null byte to the beginning.
                crc = struct.unpack( '>L', '\0'+base64.b64decode(check_data) )[0]
                if crc != crc24(data):
                        raise BadChecksumError()
        """
        return data