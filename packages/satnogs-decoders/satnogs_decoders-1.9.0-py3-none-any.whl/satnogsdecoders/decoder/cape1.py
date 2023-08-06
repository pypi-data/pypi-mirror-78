# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Cape1(KaitaiStruct):
    """:field callsign: callsign
    :field pkt_type: pkt_type
    :field mpb_voltage: payload.mpb_voltage.as_int
    :field hpb_voltage: payload.hpb_voltage.as_int
    :field battery_1_voltage: payload.battery_1_voltage.as_int
    :field battery_2_voltage: payload.battery_2_voltage.as_int
    :field battery_1_current_generated: payload.battery_1_current_generated.as_int
    :field battery_1_current_absorbed: payload.battery_1_current_absorbed.as_int
    :field battery_2_current_generated: payload.battery_2_current_generated.as_int
    :field battery_2_current_absorbed: payload.battery_2_current_absorbed.as_int
    :field temp_battery_1: payload.temp_battery_1.as_int
    :field temp_px_face: payload.temp_px_face.as_int
    :field temp_nx_face: payload.temp_nx_face.as_int
    :field temp_py_face: payload.temp_py_face.as_int
    :field temp_ny_face: payload.temp_ny_face.as_int
    :field temp_pz_face: payload.temp_pz_face.as_int
    :field temp_nz_face: payload.temp_nz_face.as_int
    :field temp_rf_amp: payload.temp_rf_amp.as_int
    :field temp_battery_2: payload.temp_battery_2.as_int
    :field panel_px_face: payload.panel_px_face.as_int
    :field panel_nx_face: payload.panel_nx_face.as_int
    :field panel_py_face: payload.panel_py_face.as_int
    :field panel_ny_face: payload.panel_ny_face.as_int
    :field panel_pz_face: payload.panel_pz_face.as_int
    :field panel_nz_face: payload.panel_nz_face.as_int
    
    .. seealso::
       Source - http://www.dk3wn.info/sat/afu/sat_cape.shtml
       https://www.pe0sat.vgnet.nl/download/CAPE/cape-1_02-07-2020_1940UTC.PNG
       https://www.pe0sat.vgnet.nl/download/CAPE/cape-1_02-07-2020_1940UTC.txt
       https://www.pe0sat.vgnet.nl/download/CAPE/tlm_info.txt
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.check_callsign = self._io.ensure_fixed_contents(b"\x4B\x35\x55\x53\x4C")
        self.pkt_type = (self._io.read_bytes(1)).decode(u"ascii")
        _on = self.pkt_type
        if _on == u"1":
            self.payload = self._root.PktType1(self._io, self, self._root)
        elif _on == u"2":
            self.payload = self._root.PktType2(self._io, self, self._root)
        elif _on == u"3":
            self.payload = self._root.PktType3(self._io, self, self._root)

    class HexInt(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.as_str = (self._io.read_bytes(2)).decode(u"ASCII")

        @property
        def as_int(self):
            if hasattr(self, '_m_as_int'):
                return self._m_as_int if hasattr(self, '_m_as_int') else None

            self._m_as_int = (int(self.as_str, 16) if int(self.as_str, 16) < 128 else -(((int(self.as_str, 16) - 1) ^ 255)))
            return self._m_as_int if hasattr(self, '_m_as_int') else None


    class PktType3(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.panel_px_face = self._root.SolarCurrent(self._io, self, self._root)
            self.panel_nx_face = self._root.SolarCurrent(self._io, self, self._root)
            self.panel_py_face = self._root.SolarCurrent(self._io, self, self._root)
            self.panel_ny_face = self._root.SolarCurrent(self._io, self, self._root)
            self.panel_pz_face = self._root.SolarCurrent(self._io, self, self._root)
            self.panel_nz_face = self._root.SolarCurrent(self._io, self, self._root)


    class HexUint(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.as_str = (self._io.read_bytes(2)).decode(u"ASCII")

        @property
        def as_int(self):
            if hasattr(self, '_m_as_int'):
                return self._m_as_int if hasattr(self, '_m_as_int') else None

            self._m_as_int = int(self.as_str, 16)
            return self._m_as_int if hasattr(self, '_m_as_int') else None


    class PktType1(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.mpb_voltage = self._root.Voltage(self._io, self, self._root)
            self.hpb_voltage = self._root.Voltage(self._io, self, self._root)
            self.battery_1_voltage = self._root.Voltage(self._io, self, self._root)
            self.battery_2_voltage = self._root.Voltage(self._io, self, self._root)
            self.battery_1_current_generated = self._root.HexUint(self._io, self, self._root)
            self.battery_1_current_absorbed = self._root.HexUint(self._io, self, self._root)
            self.battery_2_current_generated = self._root.HexUint(self._io, self, self._root)
            self.battery_2_current_absorbed = self._root.HexUint(self._io, self, self._root)


    class SolarCurrent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.as_str = (self._io.read_bytes(2)).decode(u"ASCII")

        @property
        def as_int(self):
            """(I * 10) [mA]."""
            if hasattr(self, '_m_as_int'):
                return self._m_as_int if hasattr(self, '_m_as_int') else None

            self._m_as_int = int(self.as_str, 16)
            return self._m_as_int if hasattr(self, '_m_as_int') else None


    class PktType2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.temp_battery_1 = self._root.HexInt(self._io, self, self._root)
            self.temp_px_face = self._root.HexInt(self._io, self, self._root)
            self.temp_nx_face = self._root.HexInt(self._io, self, self._root)
            self.temp_py_face = self._root.HexInt(self._io, self, self._root)
            self.temp_ny_face = self._root.HexInt(self._io, self, self._root)
            self.temp_pz_face = self._root.HexInt(self._io, self, self._root)
            self.temp_nz_face = self._root.HexInt(self._io, self, self._root)
            self.temp_rf_amp = self._root.HexInt(self._io, self, self._root)
            self.temp_battery_2 = self._root.HexInt(self._io, self, self._root)


    class Voltage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.as_str = (self._io.read_bytes(2)).decode(u"ASCII")

        @property
        def as_int(self):
            """ (V * 0.02) [V] despite documentation indicating (V * 0.2)."""
            if hasattr(self, '_m_as_int'):
                return self._m_as_int if hasattr(self, '_m_as_int') else None

            self._m_as_int = int(self.as_str, 16)
            return self._m_as_int if hasattr(self, '_m_as_int') else None


    @property
    def callsign(self):
        if hasattr(self, '_m_callsign'):
            return self._m_callsign if hasattr(self, '_m_callsign') else None

        _pos = self._io.pos()
        self._io.seek(0)
        self._m_callsign = (self._io.read_bytes(5)).decode(u"ascii")
        self._io.seek(_pos)
        return self._m_callsign if hasattr(self, '_m_callsign') else None


