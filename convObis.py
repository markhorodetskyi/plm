class ConvObis:

    def toHex(self, obis):
        import binascii
        toHex=binascii.hexlify(obis.encode('utf8'))
        toHex=toHex.decode('utf-8')
        hex1=bytes.fromhex(toHex)
        hex1 = hex1.decode('utf-8')
        r1='\x52\x31\x02'+hex1+'\x28\x29\x03'
        checksum = 0
        for i in r1:
            checksum ^= ord(i)
        checksum = str(hex(checksum))
        r1 = '523102' + toHex + '282903'
        self.command = '01'+r1+checksum[2:4]+'0d0a'