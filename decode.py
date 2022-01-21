import struct
import datetime
import base64

userType = {0: "Other",
            1: "User",
            2: "Admin"}


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


def getUser(short):
    return str(short)


def getAcsState(b):
    if b == 1:
        return "abgelehnt"
    if b == 2:
        return "erfolgreich"
    if b == 3:
        return "Keyless wartet auf zweites Merkmal"

    return "kein Match zu prüfen"


coded_string = "Ag5g5edQBwQAADECABEC/wINYOXnOQkFAAAAAAERAv8CDGDl5ygDBAAAMQX/EQH/Agtg5ecjCQUAAAAAAREC/wIKYOXm/AcEAAAxAgARAv8CCWDl5tcHBAAAMQL/EQH/Aghg5ebEBwQAADEC/xEB/wIHYOXmfgcEAAMwAQARAv8CBmDl5mwHBAAAMQD/EQH/AgVg5eYOBwQAADEC/xEB/wIEYOXl8goCAAAABAARAv8CA2Dl5aIHBAAAMQIAEQL/AgJg5eVQCgIAAAAAABEC/wIBYOXk8AcEAAAxAgARAv8CAGDl47UKAgAA//7/EQH/Af9g5eOWBwQAADECABEC/wH+YOXjDwoCAAAABAARAv8B/WDl4lQHBAAAMQL/EQH/Afxg5eIdCgIAAP/+/xEB/wH7YOXhzAcEAAAxAgARAv8B+mDl4YIKAgAA//7/EQH/Aflg5eEuBwQAADECABEC/wH4YOXgUAoCAAD//v8RAf8B92Dl36wHBAAAMQIAEQL/AfZg5dv9AQf////+/xEB/wH1YOXb+wEHAAAAAAARAv8B9GDl2/oBB/////7/EQH/AfNg5dv4AQf////+/xEB/wHyYOXb9gEH/////v8RAf8B8WDl2/UBB/////7/EQH/AfBg5dvyAQf////+/xEB/wHvYOXb8gEH/////v8RAf8B7mDlWTsKAgAAAAAAEQL/Ae1g5VicBwQAADEC/xEB/wHsYOU54AEHAAEABQERAv8B62DlAhMKAgADAAAAEQL/Aepg5QISBwQAAzABABEC/wHpYOUB7QoCAAP//v8RAf8B6GDlAewHBAADMAEAEQL/Aedg5QHdCgIAA//+/xEB/wHmYOUB3AcEAAMwAQARAv8B5WDlAYAKAgAD//7/EQH/AeRg5QF+BwQAAzABABEC/wHjYOUBfAoCAAAABAARAv8B4mDlAXMHBAADMAL/EQH/AeFg5QFVAgQAAzABABEC/wHgYOUBMwcEAAAxAv8RAf8B32DlARkHBP///wD/EQH/Ad5g5QAHCgIAAP/+/xEB/wHdYOT/qAcEAAAxAgARAv8B3GDk/ewKAgAAAAAAEQL/Adtg5P3dBwQAADEC/xEB/wHaYOT91AoCAAAAAAARAv8B2WDk/UoHBAAAMQIAEQL/Adhg5OP5CgIAAAAEABEC/wHXYOTjrAcEAAAxAgARAv8B1mDk15gKAgAAAAAAEQL/AdVg5Nd5BwQAADECABEC/wHUYOTXcgoCAAD//v8RAf8B02Dk11MHBAAAMQIAEQL/AdJg5J1UAQcAAQAFAREC/wHRYOSdUAEH/////v8RAf8B0GDknU4BB/////7/EQH/Ac9g5J1MAQf////+/xEB/wHOYOSdSgEH/////v8RAf8BzWDknUgBB/////7/EQH/Acxg5J1GAQf////+/xEB/wHLYOSdRgEH/////v8RAf8BymDknUMBB/////7/EQH/Aclg5JElAQcAAAAAABEC/wHIYOSRJAEH/////v8RAf8Bx2DkkSIBB/////7/EQH/AcZg5JEgAQf////+/xEB/wHFYOSRIAEH/////v8RAf8BxGDjPp0BBwAAAAAAEQL/AcNg4z6bAQcAAAAAABEC/wHCYOMZVAEHAAEABAARAv8BwWDhCREBB/////7/EQH/AcBg4QkPAQcAAAAAABEC/wG/YOEJDQEH/////v8RAf8BvmDhCQsBB/////7/EQH/Ab1g4QGiAQcAAAAAABEC/wG8YOCcngEHAAEABAARAv8Bu2DgnFEBB/////7/EQH/Abpg4E3LAQcAAQAEABEC/wG5YOA/zwEH/////v8RAf8BuGDfhYQBBwAAAAAAEQL/Abdg3zbjAQcAAAAAABEC/wG2YN824gEH/////v8RAf8BtWDfNnoBB/////7/EQH/AbRg3x28AQcAAAAAABEC/wGzYN7UzAEH/////v8RAf8BsmDc//wBBwABAAQAEQL/AbFg3KNmAQf////+/xEB/wGwYNyjZAEHAAAAAAARAv8Br2Dco2IBB/////7/EQH/Aa5g3KNhAQf////+/xEB/wGtYNyjXwEH/////v8RAf8BrGDcjOEBB/////7/EQH/Aatg3IzeAQcAAQAEABEC/w=="
buffer = Buffer(bytearray(base64.b64decode(coded_string)))

while not buffer.isEmpty():

    buffer.getShort()
    time = buffer.getInt()
    time = datetime.datetime.fromtimestamp(time)
    print(time)
    v1 = buffer.getByte()
    v2 = buffer.getByte()

    n = 0

    print(v1)

    if v1 == 1:
        user = getUser(buffer.getShort())
        short12 = buffer.getShort()
        value13 = buffer.getByte()
        value14 = buffer.getByte()
        b = value14 >> 4
        b2 = value14 & 0xF
        value15 = buffer.getByte()

        print("value15: " + str(value15))

        acsState = getAcsState(value15)

        state = "Aus"
        if b2 == 1:
            state = "An"

        format_string = "Zutrittsversuch durch Benutzer \"%s\" mit Merkmal-ID %d (Typ: %d). Matchergebnis: %s. Keyless %s, Sicherheitsstufe: %d." % (
        user, short12, value13, acsState, state, b)

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

        format_string = "App-Login des Benutzers \"%s\". Status: %s. Level: %s." % (getUser(short4), hex(value6), tmp)

        print(format_string)


    elif v1 == 9:

        user0 = getUser(buffer.getShort())

        user1 = getUser(buffer.getShort())

        result = str(buffer.getByte())

        format_string = "Benutzer \"%s\" ändert das Passwort von Benutzer \"%s\". Ergebnis: %s." % (

            user0, user1, result)

        print(format_string)

    elif v1 == 10:

        user = getUser(buffer.getShort())

        format_string = "App-Logout des Benutzers \"%s\"." % (user)

        print(format_string)

    elif v1 == 3:

        user = getUser(buffer.getShort())
        value9 = buffer.getByte()
        result = buffer.getByte()

        format_string = "Benutzer \"%s\" geändert. Status: %s. Ergebnis %s." % (user, hex(value9), result)

        print(format_string)

    buffer.advance(8 - v2)
