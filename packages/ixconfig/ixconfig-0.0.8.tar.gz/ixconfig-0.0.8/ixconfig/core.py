import subprocess
from .util import execmatch, matchmany, as_tuple, cached_property
import logging

log = logging.getLogger(__name__)

class _BaseConfig:
    PARAM_PATTERNS = []
    error_msgs = None

    def __init__(self, iface):
        self.iface = iface

    def get_output(self):
        cmd = self.cmd
        return subprocess.check_output(
            cmd.split(' ') if isinstance(cmd, str) else cmd,
            ).decode('utf-8')

    @property
    def cmd(self):
        raise NotImplementedError()

    @cached_property
    def params(self):
        '''Get current wireless connection info'''
        out = self.get_output()
        if not out or any(msg.lower() in out.lower() for msg in as_tuple(self.error_msgs)):
            return {}

        return matchmany(out, self.PARAM_PATTERNS)

    def __getattr__(self, k):
        return self.params.get(k)


class Ifc(_BaseConfig):
    '''
    wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.236  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::c082:c63f:7206:6148  prefixlen 64  scopeid 0x20<link>
        ether 74:da:38:5c:68:33  txqueuelen 1000  (Ethernet)
        RX packets 47295  bytes 6606945 (6.3 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 14509  bytes 2908876 (2.7 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
    '''
    PARAM_PATTERNS = [
        r'^(?P<iface>\w+\d+)',
        r'mtu\s*(?P<mtu>[\d]*)',
        r'inet\s*(?P<ip>[\d.]+)',
        r'inet6\s*(?P<ipv6>[\w\d:%]*)',
        r'netmask\s*(?P<netmask>[\d.]*)',
        r'ether\s*(?P<mac>[\w\d:]*)',
        r'inet\s.*broadcast\s*(?P<broadcast>[\d.]*)',
        r'inet\s.*peer\s*(?P<tun_gw>[^\s]*)',
    ]
    error_msgs = ('error', 'device not found', 'does not exist')

    @property
    def cmd(self):
        return 'ifconfig {}'.format(self.iface)

    @property
    def id(self):
        return (self.mac or '').replace(":", "").lower()


class Iwc(_BaseConfig):
    '''

    Example Output:
        wlan0     IEEE 802.11  ESSID:"MySpectrumWiFicc-2G"
              Mode:Managed  Frequency:2.462 GHz  Access Point: A0:8E:78:59:45:D2
              Bit Rate=72.2 Mb/s   Tx-Power=20 dBm
              Retry short limit:7   RTS thr=2347 B   Fragment thr:off
              Power Management:off
              Link Quality=70/70  Signal level=-40 dBm
              Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
              Tx excessive retries:0  Invalid misc:271   Missed beacon:0
    '''
    PARAM_PATTERNS = [
        r'ESSID:"(?P<ssid>[^"]*)"',
        r'Mode:(?P<mode>[^\s]*)',
        r'Frequency:(?P<freq>[\d.]*)\s*(?P<freq_unit>\w*)',
        r'Access Point:\s*(?P<ap>[\w\d:-]*)',
        r'Bit Rate=\s*(?P<bitrate>[\d.]*)\s*(?P<bitrate_unit>[\w\/]*)',
        r'Power Management:(?P<power_mgmt>\w*)',
        r'Link Quality=(?P<quality>[\d\/]*)',
        r'Signal level=(?P<strength>[-\d.]*)\s*(?P<strength_unit>\w*)',
        # r'Noise level=(?P<noise>[^\d.]*)',
        # r'Sensitivity:(?P<sensitivity>[^\s^\\N]*)',
        # r'Encryption key:(?P<enc_key>[^\s^\\N]*)',
    ]

    error_msgs = 'no such device', 'no wireless extensions'

    @property
    def cmd(self):
        return 'iwconfig {}'.format(self.iface)

    def get(self, *keys):
        return {k: self.params[k] for k in keys}

    @property
    def quality(self):
        if 'quality' not in self.params:
            return None
        q, qmax = self.params['quality'].split('/')
        return int(100 * float(q) / float(qmax))

def ifcget(iface, *keys):
    return Ifc(iface).get(*keys)

def iwcget(iface, *keys):
    return Iwc(iface).get(*keys)
