from enum import StrEnum

class WifiSecurity(StrEnum):
    WEP='WEP'
    WPA='WPA'
    OPEN='nopass'

def generate_wifi_connect(ssid: str, password: str, security: WifiSecurity, hidden: bool | None = None):
    ct_str = f'WIFI:S:{ssid};T:{security};P:{password};'
    if hidden is not None:
        ct_str += 'H:true;' if hidden else 'H:false;'
    ct_str += ';'
    return ct_str
