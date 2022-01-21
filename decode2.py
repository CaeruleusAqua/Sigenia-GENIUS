import struct
import datetime
import base64


class Buffer:
    def __init__(self, buf: bytearray):
        self.buf = buf
        # self.buf.reverse()

    def getShort(self):
        tmp = self.buf[:2]
        self.buf = self.buf[2:]
        integer = struct.unpack('>H', tmp)
        return integer[0]

    def getInt(self):
        tmp = self.buf[:4]
        self.buf = self.buf[4:]
        integer = struct.unpack('>I', tmp)
        return integer[0]

    def getByte(self):
        tmp = self.buf[0]
        self.buf = self.buf[1:]
        return tmp

    def advance(self, n: int):
        self.buf = self.buf[n:]

    def isEmpty(self):
        return len(self.buf) == 0


class ProtocollDecode1:
    def __init__(self, userdict: dict):
        self.userdict = userdict

        self.userType = {0: "Other", 1: "User", 2: "Admin"}

    def getAcsState(self, b):
        if b == 1:
            return "abgelehnt"
        if b == 2:
            return "erfolgreich"
        if b == 3:
            return "Keyless wartet auf zweites Merkmal"

        return "kein Match zu prüfen"

    def getUser(self, ID):
        if ID in self.userdict:
            return self.userdict[ID]
        else:
            return "Unkown User"

    def decode(self, coded_string):
        buffer = Buffer(bytearray(base64.b64decode(coded_string)))

        while not buffer.isEmpty():

            buffer.getShort()
            time = buffer.getInt()
            time = datetime.datetime.fromtimestamp(time)
            print(time,end = ' ')
            v1 = buffer.getByte()
            v2 = buffer.getByte()

            if v1 == 1:
                user = self.getUser(buffer.getShort())
                short12 = buffer.getShort()
                value13 = buffer.getByte()
                value14 = buffer.getByte()
                b = value14 >> 4
                b2 = value14 & 0xF
                value15 = buffer.getByte()

                #print("value15: " + str(value15))

                acsState = self.getAcsState(value15)

                state = "Aus"
                if b2 == 1:
                    state = "An"

                format_string = "Zutrittsversuch durch Benutzer \"%s\" mit Merkmal-ID %d (Typ: %d). Matchergebnis: %s. Keyless %s, Sicherheitsstufe: %d." % (
                    user, short12, value13, acsState, state, b)
                print(format_string)

            elif v1 == 2:

                user = self.getUser(buffer.getShort())
                value11 = int(buffer.getByte())
                value12 = int(buffer.getByte())
                format_string = "Neuer Benutzer \"%s\" angelegt. Status: %s. Ergebnis %d." % (user, hex(value11), value12)
                print(format_string)

            elif v1 == 3:

                user = self.getUser(buffer.getShort())
                value9 = buffer.getByte()
                result = buffer.getByte()
                format_string = "Benutzer \"%s\" geändert. Status: %s. Ergebnis %s." % (user, hex(value9), result)
                print(format_string)

            elif v1 == 4:
                user = self.getUser(buffer.getShort())
                format_string = "Benutzer \"%s\" gelöscht." % user
                print(format_string)

            elif v1 == 5:

                user = self.getUser(buffer.getShort())
                short7 = int(buffer.getShort())
                value8 = int(buffer.getByte())

                format_string = "Benutzer \"%s\" legt neues Zutrittsmerkmal mit Merkmal-ID %s (Typ: %s) an." % (user, short7, value8)
                print(format_string)

            elif v1 == 6:

                ID = int(buffer.getShort())

                format_string = "Zutrittsmerkmal mit ID %s wurde gelöscht." % ID
                print(format_string)

            elif v1 == 7:
                tmp = ""
                short4 = buffer.getShort()
                value6 = buffer.getByte()
                value7 = buffer.getByte()
                if value7 == 0:
                    tmp = "Other"

                elif value7 == 1:
                    tmp = "User"

                elif value7 == 2:
                    tmp = "Admin"
                else:
                    tmp = "unknown"

                format_string = "App-Login des Benutzers \"%s\". Status: %s. Level: %s." % (self.getUser(short4), hex(value6), tmp)

                print(format_string)

            elif v1 == 8:

                value4 = int(buffer.getByte())
                value5 = int(buffer.getByte())

                format_string = "Änderung der Keyless-Sicherheits-Stufe. Alt: %s. Neu: %s." % (value4, value5)
                print(format_string)

            elif v1 == 9:

                user0 = self.getUser(buffer.getShort())

                user1 = self.getUser(buffer.getShort())

                result = str(buffer.getByte())

                format_string = "Benutzer \"%s\" ändert das Passwort von Benutzer \"%s\". Ergebnis: %s." % (

                    user0, user1, result)

                print(format_string)

            elif v1 == 10:

                user = self.getUser(buffer.getShort())

                format_string = "App-Logout des Benutzers \"%s\"." % (user)

                print(format_string)


            else:
                print("Error while parsing")

            buffer.advance(8 - v2)
