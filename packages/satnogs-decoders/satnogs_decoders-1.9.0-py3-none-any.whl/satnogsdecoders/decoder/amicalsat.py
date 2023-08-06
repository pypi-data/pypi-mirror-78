# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Amicalsat(KaitaiStruct):
    """Author  : C. Mercier for AMSAT-Francophone
    Adapted for SatNOGS and modified by deckbsd
    
    :field dst_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field src_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field ctl: ax25_frame.ax25_header.ctl
    :field pid: ax25_frame.payload.pid
    :field tlm_area: ax25_frame.payload.ax25_info.tlm_area
    :field tlm_type: ax25_frame.payload.ax25_info.tlm_type
    :field cpu_voltage_volt: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.cpu_voltage_volt
    :field boot_number_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.boot_number_int
    :field cpu_temperature_degree: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.cpu_temperature_degree
    :field up_time_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.up_time_int
    :field imc_aocs_ok: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.imc_aocs_ok
    :field imc_cu_l_ok: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.imc_cu_l_ok
    :field imc_cu_r_ok: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.imc_cu_r_ok
    :field imc_vhf1_ok: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.imc_vhf1_ok
    :field imc_uhf2_ok: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.imc_uhf2_ok
    :field vhf1_downlink: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.vhf1_downlink
    :field uhf2_downlink: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.uhf2_downlink
    :field imc_check: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.imc_check
    :field beacon_mode: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.beacon_mode
    :field cyclic_reset_on: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.cyclic_reset_on
    :field survival_mode: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.survival_mode
    :field payload_off: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.payload_off
    :field cu_auto_off: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.cu_auto_off
    :field tm_log: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.tm_log
    :field cul_on: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.cul_on
    :field cul_faut: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.cul_faut
    :field cur_on: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.cur_on
    :field cur_fault: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.cur_fault
    :field cu_on: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.cu_on
    :field cul_dead: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.cul_dead
    :field cur_dead: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.cur_dead
    :field fault_3v_r: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.fault_3v_r
    :field fault_3v_m: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.fault_3v_m
    :field charge_r: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.charge_r
    :field charge_m: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.charge_m
    :field long_log: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.long_log
    :field log_to_flash: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.log_to_flash
    :field plan: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.plan
    :field stream: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.stream
    :field vhf1_packet_ready: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.vhf1_packet_ready
    :field uhf2_packet_ready: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.uhf2_packet_ready
    :field survival_start: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.survival_start
    :field survival_end: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.survival_end
    :field timestamp_int: ax25_frame.payload.ax25_info.tlm_area_switch.timestamp_int
    :field timestamp_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.timestamp_int
    :field timestamp_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.timestamp_int
    :field detumbling: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.detumbling
    :field adcs_on_off: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.adcs_on_off
    :field detumbling_status: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.detumbling_status
    :field manual: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.manual
    :field act_on_off: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.act_on_off
    :field sun_contr: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.sun_contr
    :field sens_on_off: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.sens_on_off
    :field act_man_contr: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.act_man_contr
    :field act_limited_contr: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.act_limited_contr
    :field gyro_acc_fault: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.gyro_acc_fault
    :field mag_fault: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.mag_fault
    :field sun_fault: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.sun_fault
    :field l1_fault: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.l1_fault
    :field l2_fault: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.l2_fault
    :field l3_fault: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.l3_fault
    :field mag_x_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.mag_x_int
    :field mag_y_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.mag_y_int
    :field mag_z_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.mag_z_int
    :field gyro_x_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.gyro_x_int
    :field gyro_y_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.gyro_y_int
    :field gyro_z_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.gyro_z_int
    :field latitude_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.latitude_int
    :field longitude_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlm_sw.longitude_int
    :field tlmsw_boot_number_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.boot_number_int
    :field input_voltage_volt: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.input_voltage_volt
    :field input_current_ma: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.input_current_ma
    :field input_power_mw: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.input_power_mw
    :field peak_power_mw: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.peak_power_mw
    :field solar_panel_voltage_volt: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.solar_panel_voltage_volt
    :field v_in_volt: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.v_in_volt
    :field v_solar_volt: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.v_solar_volt
    :field i_in_ma: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.i_in_ma
    :field p_in_mw: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.p_in_mw
    :field p_peak_mw: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.p_peak_mw
    :field t_cpu_degree: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.t_cpu_degree
    :field v_cpu_volt: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.v_cpu_volt
    :field battery_voltage: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.battery_voltage
    :field tlmsw_cpu_voltage_volt: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.cpu_voltage_volt
    :field battery_voltage_volt: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.battery_voltage_volt
    :field tlmsw_cpu_temperature_degree: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.cpu_temperature_degree
    :field amplifier_temperature_degree: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.amplifier_temperature_degree
    :field fec: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.fec
    :field downlink: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.downlink
    :field band_lock: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.band_lock
    :field xor: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.xor
    :field aes_128: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.aes_128
    :field amp_ovt: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.amp_ovt
    :field current_rssi: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.current_rssi
    :field latch_rssi: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.latch_rssi
    :field a_f_c_offset: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.a_f_c_offset
    :field current_rssi_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.current_rssi_int
    :field latch_rssi_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.latch_rssi_int
    :field a_f_c_offset_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.a_f_c_offset_int
    :field return_value_int: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.return_value_int
    :field onyx_on: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.onyx_on
    :field llc_onyx_fault: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.llc_onyx_fault
    :field llc_sram_fault: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.llc_sram_fault
    :field fault_1v8_r: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.fault_1v8_r
    :field fault_1v8_m: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.fault_1v8_m
    :field fault_3v3_12v: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.fault_3v3_12v
    :field pic_ready_conv: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.pic_ready_conv
    :field pic_ready_compressed: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.pic_ready_compressed
    :field pic_ready_compressed_8: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.pic_ready_compressed_8
    :field sd_pic_write_ok: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.sd_pic_write_ok
    :field sd_pic_read_ok: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.sd_pic_read_ok
    :field sd_get_info_ok: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.sd_get_info_ok
    :field sd_erase_ok: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.sd_erase_ok
    :field sd_full: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.sd_full
    :field adc_ready: ax25_frame.payload.ax25_info.tlm_area_switch.tlmsw.adc_ready
    :field aprs_message: ax25_frame.payload.ax25_info.aprs_message
    
    .. seealso::
       Source - https://gitlab.com/librespacefoundation/satnogs-ops/uploads/f6fde8b864f8cdf37d65433bd958e138/AmicalSat_downlinks_v0.3.pdf
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = self._root.Ax25Frame(self._io, self, self._root)

    class EmmnType(KaitaiStruct):
        """[EM/ER];MN;[Timestamp];[V in];[V solar];[I in];[P in];[P peak];[T cpu];[V cpu]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.v_in = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.v_solar = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.i_in = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.p_in = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.p_peak = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.t_cpu = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.v_cpu = (self._io.read_bytes_full()).decode(u"ASCII")

        @property
        def p_peak_mw(self):
            if hasattr(self, '_m_p_peak_mw'):
                return self._m_p_peak_mw if hasattr(self, '_m_p_peak_mw') else None

            self._m_p_peak_mw = int(self.p_peak)
            return self._m_p_peak_mw if hasattr(self, '_m_p_peak_mw') else None

        @property
        def t_cpu_degree(self):
            if hasattr(self, '_m_t_cpu_degree'):
                return self._m_t_cpu_degree if hasattr(self, '_m_t_cpu_degree') else None

            self._m_t_cpu_degree = int(self.t_cpu)
            return self._m_t_cpu_degree if hasattr(self, '_m_t_cpu_degree') else None

        @property
        def v_solar_volt(self):
            if hasattr(self, '_m_v_solar_volt'):
                return self._m_v_solar_volt if hasattr(self, '_m_v_solar_volt') else None

            self._m_v_solar_volt = (int(self.v_solar) / 1000.0)
            return self._m_v_solar_volt if hasattr(self, '_m_v_solar_volt') else None

        @property
        def v_in_volt(self):
            if hasattr(self, '_m_v_in_volt'):
                return self._m_v_in_volt if hasattr(self, '_m_v_in_volt') else None

            self._m_v_in_volt = (int(self.v_in) / 1000.0)
            return self._m_v_in_volt if hasattr(self, '_m_v_in_volt') else None

        @property
        def p_in_mw(self):
            if hasattr(self, '_m_p_in_mw'):
                return self._m_p_in_mw if hasattr(self, '_m_p_in_mw') else None

            self._m_p_in_mw = int(self.p_in)
            return self._m_p_in_mw if hasattr(self, '_m_p_in_mw') else None

        @property
        def i_in_ma(self):
            if hasattr(self, '_m_i_in_ma'):
                return self._m_i_in_ma if hasattr(self, '_m_i_in_ma') else None

            self._m_i_in_ma = int(self.i_in)
            return self._m_i_in_ma if hasattr(self, '_m_i_in_ma') else None

        @property
        def v_cpu_volt(self):
            if hasattr(self, '_m_v_cpu_volt'):
                return self._m_v_cpu_volt if hasattr(self, '_m_v_cpu_volt') else None

            self._m_v_cpu_volt = (int(self.v_cpu) / 1000.0)
            return self._m_v_cpu_volt if hasattr(self, '_m_v_cpu_volt') else None


    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = self._root.Ax25Header(self._io, self, self._root)
            _on = (self.ax25_header.ctl & 19)
            if _on == 0:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 3:
                self.payload = self._root.UiFrame(self._io, self, self._root)
            elif _on == 19:
                self.payload = self._root.UiFrame(self._io, self, self._root)
            elif _on == 16:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 18:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 2:
                self.payload = self._root.IFrame(self._io, self, self._root)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = self._root.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = self._root.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = self._root.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = self._root.SsidMask(self._io, self, self._root)
            if (self.src_ssid_raw.ssid_mask & 1) == 0:
                self.repeater = self._root.Repeater(self._io, self, self._root)

            self.ctl = self._io.read_u1()


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self._raw_ax25_info = self._io.read_bytes_full()
            io = KaitaiStream(BytesIO(self._raw_ax25_info))
            self.ax25_info = self._root.Ax25InfoData(io, self, self._root)


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class A1PositionType(KaitaiStruct):
        """A1;POSITION;[Current timestamp];[Latitude];[Longitude]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.timestamp = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.latitude = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.longitude = (self._io.read_bytes_full()).decode(u"ASCII")

        @property
        def latitude_int(self):
            if hasattr(self, '_m_latitude_int'):
                return self._m_latitude_int if hasattr(self, '_m_latitude_int') else None

            self._m_latitude_int = int(self.latitude)
            return self._m_latitude_int if hasattr(self, '_m_latitude_int') else None

        @property
        def longitude_int(self):
            if hasattr(self, '_m_longitude_int'):
                return self._m_longitude_int if hasattr(self, '_m_longitude_int') else None

            self._m_longitude_int = int(self.longitude)
            return self._m_longitude_int if hasattr(self, '_m_longitude_int') else None

        @property
        def timestamp_int(self):
            if hasattr(self, '_m_timestamp_int'):
                return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

            self._m_timestamp_int = int(self.timestamp)
            return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None


    class M1Type(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.timestamp = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            _on = self._parent.tlm_type
            if _on == u"LOG":
                self.tlm_sw = self._root.LogType(self._io, self, self._root)
            elif _on == u"FLAGS":
                self.tlm_sw = self._root.FlagsType(self._io, self, self._root)

        @property
        def timestamp_int(self):
            if hasattr(self, '_m_timestamp_int'):
                return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

            self._m_timestamp_int = int(self.timestamp)
            return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None


    class EmLogType(KaitaiStruct):
        """EM;LOG;[Timestamp];[Boot number];[Input voltage];[Input current];[Input power];[Peak Power];[Solar panel voltage]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.boot_number = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.input_voltage = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.input_current = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.input_power = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.peak_power = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.solar_panel_voltage = (self._io.read_bytes_full()).decode(u"ASCII")

        @property
        def input_current_ma(self):
            if hasattr(self, '_m_input_current_ma'):
                return self._m_input_current_ma if hasattr(self, '_m_input_current_ma') else None

            self._m_input_current_ma = int(self.input_current)
            return self._m_input_current_ma if hasattr(self, '_m_input_current_ma') else None

        @property
        def peak_power_mw(self):
            if hasattr(self, '_m_peak_power_mw'):
                return self._m_peak_power_mw if hasattr(self, '_m_peak_power_mw') else None

            self._m_peak_power_mw = int(self.peak_power)
            return self._m_peak_power_mw if hasattr(self, '_m_peak_power_mw') else None

        @property
        def input_power_mw(self):
            if hasattr(self, '_m_input_power_mw'):
                return self._m_input_power_mw if hasattr(self, '_m_input_power_mw') else None

            self._m_input_power_mw = int(self.input_power)
            return self._m_input_power_mw if hasattr(self, '_m_input_power_mw') else None

        @property
        def boot_number_int(self):
            if hasattr(self, '_m_boot_number_int'):
                return self._m_boot_number_int if hasattr(self, '_m_boot_number_int') else None

            self._m_boot_number_int = int(self.boot_number)
            return self._m_boot_number_int if hasattr(self, '_m_boot_number_int') else None

        @property
        def input_voltage_volt(self):
            if hasattr(self, '_m_input_voltage_volt'):
                return self._m_input_voltage_volt if hasattr(self, '_m_input_voltage_volt') else None

            self._m_input_voltage_volt = (int(self.input_voltage) / 1000.0)
            return self._m_input_voltage_volt if hasattr(self, '_m_input_voltage_volt') else None

        @property
        def solar_panel_voltage_volt(self):
            if hasattr(self, '_m_solar_panel_voltage_volt'):
                return self._m_solar_panel_voltage_volt if hasattr(self, '_m_solar_panel_voltage_volt') else None

            self._m_solar_panel_voltage_volt = (int(self.solar_panel_voltage) / 1000.0)
            return self._m_solar_panel_voltage_volt if hasattr(self, '_m_solar_panel_voltage_volt') else None


    class A1FlagType(KaitaiStruct):
        """A1;FLAGS;[mode];[flags];[faults]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.timestamp = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.adcs_mode = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.a1_flags = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.faults = (self._io.read_bytes_full()).decode(u"ASCII")

        @property
        def sens_on_off(self):
            if hasattr(self, '_m_sens_on_off'):
                return self._m_sens_on_off if hasattr(self, '_m_sens_on_off') else None

            self._m_sens_on_off = ((int(self.a1_flags, 16) & 4) >> 2)
            return self._m_sens_on_off if hasattr(self, '_m_sens_on_off') else None

        @property
        def l3_fault(self):
            if hasattr(self, '_m_l3_fault'):
                return self._m_l3_fault if hasattr(self, '_m_l3_fault') else None

            self._m_l3_fault = ((int(self.faults, 16) & 32) >> 5)
            return self._m_l3_fault if hasattr(self, '_m_l3_fault') else None

        @property
        def manual(self):
            if hasattr(self, '_m_manual'):
                return self._m_manual if hasattr(self, '_m_manual') else None

            self._m_manual = ((int(self.adcs_mode, 16) & 240) >> 4)
            return self._m_manual if hasattr(self, '_m_manual') else None

        @property
        def sun_contr(self):
            if hasattr(self, '_m_sun_contr'):
                return self._m_sun_contr if hasattr(self, '_m_sun_contr') else None

            self._m_sun_contr = ((int(self.a1_flags, 16) & 2) >> 1)
            return self._m_sun_contr if hasattr(self, '_m_sun_contr') else None

        @property
        def gyro_acc_fault(self):
            if hasattr(self, '_m_gyro_acc_fault'):
                return self._m_gyro_acc_fault if hasattr(self, '_m_gyro_acc_fault') else None

            self._m_gyro_acc_fault = (int(self.faults, 16) & 1)
            return self._m_gyro_acc_fault if hasattr(self, '_m_gyro_acc_fault') else None

        @property
        def l1_fault(self):
            if hasattr(self, '_m_l1_fault'):
                return self._m_l1_fault if hasattr(self, '_m_l1_fault') else None

            self._m_l1_fault = ((int(self.faults, 16) & 8) >> 3)
            return self._m_l1_fault if hasattr(self, '_m_l1_fault') else None

        @property
        def act_man_contr(self):
            if hasattr(self, '_m_act_man_contr'):
                return self._m_act_man_contr if hasattr(self, '_m_act_man_contr') else None

            self._m_act_man_contr = ((int(self.a1_flags, 16) & 8) >> 3)
            return self._m_act_man_contr if hasattr(self, '_m_act_man_contr') else None

        @property
        def timestamp_int(self):
            if hasattr(self, '_m_timestamp_int'):
                return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

            self._m_timestamp_int = int(self.timestamp)
            return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

        @property
        def adcs_on_off(self):
            if hasattr(self, '_m_adcs_on_off'):
                return self._m_adcs_on_off if hasattr(self, '_m_adcs_on_off') else None

            self._m_adcs_on_off = ((int(self.adcs_mode, 16) & 2) >> 1)
            return self._m_adcs_on_off if hasattr(self, '_m_adcs_on_off') else None

        @property
        def detumbling_status(self):
            if hasattr(self, '_m_detumbling_status'):
                return self._m_detumbling_status if hasattr(self, '_m_detumbling_status') else None

            self._m_detumbling_status = ((int(self.adcs_mode, 16) & 12) >> 2)
            return self._m_detumbling_status if hasattr(self, '_m_detumbling_status') else None

        @property
        def act_limited_contr(self):
            if hasattr(self, '_m_act_limited_contr'):
                return self._m_act_limited_contr if hasattr(self, '_m_act_limited_contr') else None

            self._m_act_limited_contr = ((int(self.a1_flags, 16) & 16) >> 4)
            return self._m_act_limited_contr if hasattr(self, '_m_act_limited_contr') else None

        @property
        def act_on_off(self):
            if hasattr(self, '_m_act_on_off'):
                return self._m_act_on_off if hasattr(self, '_m_act_on_off') else None

            self._m_act_on_off = (int(self.a1_flags, 16) & 1)
            return self._m_act_on_off if hasattr(self, '_m_act_on_off') else None

        @property
        def mag_fault(self):
            if hasattr(self, '_m_mag_fault'):
                return self._m_mag_fault if hasattr(self, '_m_mag_fault') else None

            self._m_mag_fault = ((int(self.faults, 16) & 2) >> 1)
            return self._m_mag_fault if hasattr(self, '_m_mag_fault') else None

        @property
        def sun_fault(self):
            if hasattr(self, '_m_sun_fault'):
                return self._m_sun_fault if hasattr(self, '_m_sun_fault') else None

            self._m_sun_fault = ((int(self.faults, 16) & 4) >> 2)
            return self._m_sun_fault if hasattr(self, '_m_sun_fault') else None

        @property
        def l2_fault(self):
            if hasattr(self, '_m_l2_fault'):
                return self._m_l2_fault if hasattr(self, '_m_l2_fault') else None

            self._m_l2_fault = ((int(self.faults, 16) & 16) >> 4)
            return self._m_l2_fault if hasattr(self, '_m_l2_fault') else None

        @property
        def detumbling(self):
            if hasattr(self, '_m_detumbling'):
                return self._m_detumbling if hasattr(self, '_m_detumbling') else None

            self._m_detumbling = (int(self.adcs_mode, 16) & 1)
            return self._m_detumbling if hasattr(self, '_m_detumbling') else None


    class FlagsType(KaitaiStruct):
        """M1;FLAGS;[Timestamp];[Hex flags];
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.hex_part = (self._io.read_bytes_term(120, False, True, True)).decode(u"ASCII")
            self.flags = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")

        @property
        def beacon_mode(self):
            if hasattr(self, '_m_beacon_mode'):
                return self._m_beacon_mode if hasattr(self, '_m_beacon_mode') else None

            self._m_beacon_mode = ((int(self.flags, 16) & 256) >> 8)
            return self._m_beacon_mode if hasattr(self, '_m_beacon_mode') else None

        @property
        def cur_dead(self):
            if hasattr(self, '_m_cur_dead'):
                return self._m_cur_dead if hasattr(self, '_m_cur_dead') else None

            self._m_cur_dead = ((int(self.flags, 16) & 4026531840) >> 28)
            return self._m_cur_dead if hasattr(self, '_m_cur_dead') else None

        @property
        def cur_on(self):
            if hasattr(self, '_m_cur_on'):
                return self._m_cur_on if hasattr(self, '_m_cur_on') else None

            self._m_cur_on = ((int(self.flags, 16) & 262144) >> 18)
            return self._m_cur_on if hasattr(self, '_m_cur_on') else None

        @property
        def stream(self):
            if hasattr(self, '_m_stream'):
                return self._m_stream if hasattr(self, '_m_stream') else None

            self._m_stream = ((int(self.flags, 16) & 281474976710656) >> 48)
            return self._m_stream if hasattr(self, '_m_stream') else None

        @property
        def imc_aocs_ok(self):
            if hasattr(self, '_m_imc_aocs_ok'):
                return self._m_imc_aocs_ok if hasattr(self, '_m_imc_aocs_ok') else None

            self._m_imc_aocs_ok = (int(self.flags, 16) & 1)
            return self._m_imc_aocs_ok if hasattr(self, '_m_imc_aocs_ok') else None

        @property
        def uhf2_downlink(self):
            if hasattr(self, '_m_uhf2_downlink'):
                return self._m_uhf2_downlink if hasattr(self, '_m_uhf2_downlink') else None

            self._m_uhf2_downlink = ((int(self.flags, 16) & 64) >> 6)
            return self._m_uhf2_downlink if hasattr(self, '_m_uhf2_downlink') else None

        @property
        def cul_on(self):
            if hasattr(self, '_m_cul_on'):
                return self._m_cul_on if hasattr(self, '_m_cul_on') else None

            self._m_cul_on = ((int(self.flags, 16) & 65536) >> 16)
            return self._m_cul_on if hasattr(self, '_m_cul_on') else None

        @property
        def payload_off(self):
            if hasattr(self, '_m_payload_off'):
                return self._m_payload_off if hasattr(self, '_m_payload_off') else None

            self._m_payload_off = ((int(self.flags, 16) & 2048) >> 11)
            return self._m_payload_off if hasattr(self, '_m_payload_off') else None

        @property
        def cu_auto_off(self):
            if hasattr(self, '_m_cu_auto_off'):
                return self._m_cu_auto_off if hasattr(self, '_m_cu_auto_off') else None

            self._m_cu_auto_off = ((int(self.flags, 16) & 4096) >> 12)
            return self._m_cu_auto_off if hasattr(self, '_m_cu_auto_off') else None

        @property
        def survival_start(self):
            if hasattr(self, '_m_survival_start'):
                return self._m_survival_start if hasattr(self, '_m_survival_start') else None

            self._m_survival_start = ((int(self.flags, 16) & 2251799813685248) >> 51)
            return self._m_survival_start if hasattr(self, '_m_survival_start') else None

        @property
        def fault_3v_m(self):
            if hasattr(self, '_m_fault_3v_m'):
                return self._m_fault_3v_m if hasattr(self, '_m_fault_3v_m') else None

            self._m_fault_3v_m = ((int(self.flags, 16) & 2199023255552) >> 41)
            return self._m_fault_3v_m if hasattr(self, '_m_fault_3v_m') else None

        @property
        def plan(self):
            if hasattr(self, '_m_plan'):
                return self._m_plan if hasattr(self, '_m_plan') else None

            self._m_plan = ((int(self.flags, 16) & 140737488355328) >> 47)
            return self._m_plan if hasattr(self, '_m_plan') else None

        @property
        def vhf1_downlink(self):
            if hasattr(self, '_m_vhf1_downlink'):
                return self._m_vhf1_downlink if hasattr(self, '_m_vhf1_downlink') else None

            self._m_vhf1_downlink = ((int(self.flags, 16) & 32) >> 5)
            return self._m_vhf1_downlink if hasattr(self, '_m_vhf1_downlink') else None

        @property
        def cyclic_reset_on(self):
            if hasattr(self, '_m_cyclic_reset_on'):
                return self._m_cyclic_reset_on if hasattr(self, '_m_cyclic_reset_on') else None

            self._m_cyclic_reset_on = ((int(self.flags, 16) & 512) >> 9)
            return self._m_cyclic_reset_on if hasattr(self, '_m_cyclic_reset_on') else None

        @property
        def uhf2_packet_ready(self):
            if hasattr(self, '_m_uhf2_packet_ready'):
                return self._m_uhf2_packet_ready if hasattr(self, '_m_uhf2_packet_ready') else None

            self._m_uhf2_packet_ready = ((int(self.flags, 16) & 1125899906842624) >> 50)
            return self._m_uhf2_packet_ready if hasattr(self, '_m_uhf2_packet_ready') else None

        @property
        def cur_fault(self):
            if hasattr(self, '_m_cur_fault'):
                return self._m_cur_fault if hasattr(self, '_m_cur_fault') else None

            self._m_cur_fault = ((int(self.flags, 16) & 524288) >> 19)
            return self._m_cur_fault if hasattr(self, '_m_cur_fault') else None

        @property
        def vhf1_packet_ready(self):
            if hasattr(self, '_m_vhf1_packet_ready'):
                return self._m_vhf1_packet_ready if hasattr(self, '_m_vhf1_packet_ready') else None

            self._m_vhf1_packet_ready = ((int(self.flags, 16) & 562949953421312) >> 49)
            return self._m_vhf1_packet_ready if hasattr(self, '_m_vhf1_packet_ready') else None

        @property
        def cul_faut(self):
            if hasattr(self, '_m_cul_faut'):
                return self._m_cul_faut if hasattr(self, '_m_cul_faut') else None

            self._m_cul_faut = ((int(self.flags, 16) & 131072) >> 17)
            return self._m_cul_faut if hasattr(self, '_m_cul_faut') else None

        @property
        def tm_log(self):
            if hasattr(self, '_m_tm_log'):
                return self._m_tm_log if hasattr(self, '_m_tm_log') else None

            self._m_tm_log = ((int(self.flags, 16) & 8192) >> 13)
            return self._m_tm_log if hasattr(self, '_m_tm_log') else None

        @property
        def long_log(self):
            if hasattr(self, '_m_long_log'):
                return self._m_long_log if hasattr(self, '_m_long_log') else None

            self._m_long_log = ((int(self.flags, 16) & 35184372088832) >> 45)
            return self._m_long_log if hasattr(self, '_m_long_log') else None

        @property
        def imc_uhf2_ok(self):
            if hasattr(self, '_m_imc_uhf2_ok'):
                return self._m_imc_uhf2_ok if hasattr(self, '_m_imc_uhf2_ok') else None

            self._m_imc_uhf2_ok = ((int(self.flags, 16) & 16) >> 4)
            return self._m_imc_uhf2_ok if hasattr(self, '_m_imc_uhf2_ok') else None

        @property
        def imc_check(self):
            if hasattr(self, '_m_imc_check'):
                return self._m_imc_check if hasattr(self, '_m_imc_check') else None

            self._m_imc_check = ((int(self.flags, 16) & 128) >> 7)
            return self._m_imc_check if hasattr(self, '_m_imc_check') else None

        @property
        def charge_m(self):
            if hasattr(self, '_m_charge_m'):
                return self._m_charge_m if hasattr(self, '_m_charge_m') else None

            self._m_charge_m = ((int(self.flags, 16) & 8796093022208) >> 43)
            return self._m_charge_m if hasattr(self, '_m_charge_m') else None

        @property
        def survival_end(self):
            if hasattr(self, '_m_survival_end'):
                return self._m_survival_end if hasattr(self, '_m_survival_end') else None

            self._m_survival_end = ((int(self.flags, 16) & 4503599627370496) >> 52)
            return self._m_survival_end if hasattr(self, '_m_survival_end') else None

        @property
        def fault_3v_r(self):
            if hasattr(self, '_m_fault_3v_r'):
                return self._m_fault_3v_r if hasattr(self, '_m_fault_3v_r') else None

            self._m_fault_3v_r = ((int(self.flags, 16) & 1099511627776) >> 40)
            return self._m_fault_3v_r if hasattr(self, '_m_fault_3v_r') else None

        @property
        def survival_mode(self):
            if hasattr(self, '_m_survival_mode'):
                return self._m_survival_mode if hasattr(self, '_m_survival_mode') else None

            self._m_survival_mode = ((int(self.flags, 16) & 1024) >> 10)
            return self._m_survival_mode if hasattr(self, '_m_survival_mode') else None

        @property
        def imc_cu_r_ok(self):
            if hasattr(self, '_m_imc_cu_r_ok'):
                return self._m_imc_cu_r_ok if hasattr(self, '_m_imc_cu_r_ok') else None

            self._m_imc_cu_r_ok = ((int(self.flags, 16) & 4) >> 2)
            return self._m_imc_cu_r_ok if hasattr(self, '_m_imc_cu_r_ok') else None

        @property
        def cul_dead(self):
            if hasattr(self, '_m_cul_dead'):
                return self._m_cul_dead if hasattr(self, '_m_cul_dead') else None

            self._m_cul_dead = ((int(self.flags, 16) & 251658240) >> 24)
            return self._m_cul_dead if hasattr(self, '_m_cul_dead') else None

        @property
        def charge_r(self):
            if hasattr(self, '_m_charge_r'):
                return self._m_charge_r if hasattr(self, '_m_charge_r') else None

            self._m_charge_r = ((int(self.flags, 16) & 4398046511104) >> 42)
            return self._m_charge_r if hasattr(self, '_m_charge_r') else None

        @property
        def imc_vhf1_ok(self):
            if hasattr(self, '_m_imc_vhf1_ok'):
                return self._m_imc_vhf1_ok if hasattr(self, '_m_imc_vhf1_ok') else None

            self._m_imc_vhf1_ok = ((int(self.flags, 16) & 8) >> 3)
            return self._m_imc_vhf1_ok if hasattr(self, '_m_imc_vhf1_ok') else None

        @property
        def cu_on(self):
            if hasattr(self, '_m_cu_on'):
                return self._m_cu_on if hasattr(self, '_m_cu_on') else None

            self._m_cu_on = ((int(self.flags, 16) & 1048576) >> 20)
            return self._m_cu_on if hasattr(self, '_m_cu_on') else None

        @property
        def log_to_flash(self):
            if hasattr(self, '_m_log_to_flash'):
                return self._m_log_to_flash if hasattr(self, '_m_log_to_flash') else None

            self._m_log_to_flash = ((int(self.flags, 16) & 70368744177664) >> 46)
            return self._m_log_to_flash if hasattr(self, '_m_log_to_flash') else None

        @property
        def imc_cu_l_ok(self):
            if hasattr(self, '_m_imc_cu_l_ok'):
                return self._m_imc_cu_l_ok if hasattr(self, '_m_imc_cu_l_ok') else None

            self._m_imc_cu_l_ok = ((int(self.flags, 16) & 2) >> 1)
            return self._m_imc_cu_l_ok if hasattr(self, '_m_imc_cu_l_ok') else None


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self._raw_ax25_info = self._io.read_bytes_full()
            io = KaitaiStream(BytesIO(self._raw_ax25_info))
            self.ax25_info = self._root.Ax25InfoData(io, self, self._root)


    class U2RlType(KaitaiStruct):
        """[U2];RL;[Timestamp],[CPU voltage];[Battery voltage];[CPU temperature];[Amplifier temperature];[Flags]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.timestamp = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.cpu_voltage = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.battery_voltage = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.cpu_temperature = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.amplifier_temperature = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.flagsmagic = self._io.ensure_fixed_contents(b"\x30\x78")
            self.flags = (self._io.read_bytes(1)).decode(u"ASCII")

        @property
        def cpu_temperature_degree(self):
            if hasattr(self, '_m_cpu_temperature_degree'):
                return self._m_cpu_temperature_degree if hasattr(self, '_m_cpu_temperature_degree') else None

            self._m_cpu_temperature_degree = int(self.cpu_temperature)
            return self._m_cpu_temperature_degree if hasattr(self, '_m_cpu_temperature_degree') else None

        @property
        def fec(self):
            if hasattr(self, '_m_fec'):
                return self._m_fec if hasattr(self, '_m_fec') else None

            self._m_fec = (int(self.flags, 16) & 1)
            return self._m_fec if hasattr(self, '_m_fec') else None

        @property
        def timestamp_int(self):
            if hasattr(self, '_m_timestamp_int'):
                return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

            self._m_timestamp_int = int(self.timestamp)
            return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

        @property
        def band_lock(self):
            if hasattr(self, '_m_band_lock'):
                return self._m_band_lock if hasattr(self, '_m_band_lock') else None

            self._m_band_lock = ((int(self.flags, 16) & 4) >> 2)
            return self._m_band_lock if hasattr(self, '_m_band_lock') else None

        @property
        def cpu_voltage_volt(self):
            if hasattr(self, '_m_cpu_voltage_volt'):
                return self._m_cpu_voltage_volt if hasattr(self, '_m_cpu_voltage_volt') else None

            self._m_cpu_voltage_volt = (int(self.cpu_voltage) / 1000.0)
            return self._m_cpu_voltage_volt if hasattr(self, '_m_cpu_voltage_volt') else None

        @property
        def aes_128(self):
            if hasattr(self, '_m_aes_128'):
                return self._m_aes_128 if hasattr(self, '_m_aes_128') else None

            self._m_aes_128 = ((int(self.flags, 16) & 16) >> 4)
            return self._m_aes_128 if hasattr(self, '_m_aes_128') else None

        @property
        def amplifier_temperature_degree(self):
            if hasattr(self, '_m_amplifier_temperature_degree'):
                return self._m_amplifier_temperature_degree if hasattr(self, '_m_amplifier_temperature_degree') else None

            self._m_amplifier_temperature_degree = int(self.amplifier_temperature)
            return self._m_amplifier_temperature_degree if hasattr(self, '_m_amplifier_temperature_degree') else None

        @property
        def amp_ovt(self):
            if hasattr(self, '_m_amp_ovt'):
                return self._m_amp_ovt if hasattr(self, '_m_amp_ovt') else None

            self._m_amp_ovt = ((int(self.flags, 16) & 32) >> 5)
            return self._m_amp_ovt if hasattr(self, '_m_amp_ovt') else None

        @property
        def xor(self):
            if hasattr(self, '_m_xor'):
                return self._m_xor if hasattr(self, '_m_xor') else None

            self._m_xor = ((int(self.flags, 16) & 8) >> 3)
            return self._m_xor if hasattr(self, '_m_xor') else None

        @property
        def downlink(self):
            if hasattr(self, '_m_downlink'):
                return self._m_downlink if hasattr(self, '_m_downlink') else None

            self._m_downlink = ((int(self.flags, 16) & 2) >> 1)
            return self._m_downlink if hasattr(self, '_m_downlink') else None

        @property
        def battery_voltage_volt(self):
            if hasattr(self, '_m_battery_voltage_volt'):
                return self._m_battery_voltage_volt if hasattr(self, '_m_battery_voltage_volt') else None

            self._m_battery_voltage_volt = (int(self.battery_voltage) / 1000.0)
            return self._m_battery_voltage_volt if hasattr(self, '_m_battery_voltage_volt') else None


    class SsidMask(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ssid_mask = self._io.read_u1()

        @property
        def ssid(self):
            if hasattr(self, '_m_ssid'):
                return self._m_ssid if hasattr(self, '_m_ssid') else None

            self._m_ssid = ((self.ssid_mask & 15) >> 1)
            return self._m_ssid if hasattr(self, '_m_ssid') else None


    class CuLogType(KaitaiStruct):
        """[CU_R/CU_L];LOG;[Timestamp];[CPU voltage];[CPU temperature];[flags]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cpu_voltage = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.cpu_temperature = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.flagsmagic = self._io.ensure_fixed_contents(b"\x30\x78")
            self.cu_flags = (self._io.read_bytes_full()).decode(u"ASCII")

        @property
        def cpu_temperature_degree(self):
            if hasattr(self, '_m_cpu_temperature_degree'):
                return self._m_cpu_temperature_degree if hasattr(self, '_m_cpu_temperature_degree') else None

            self._m_cpu_temperature_degree = int(self.cpu_temperature)
            return self._m_cpu_temperature_degree if hasattr(self, '_m_cpu_temperature_degree') else None

        @property
        def sd_pic_write_ok(self):
            if hasattr(self, '_m_sd_pic_write_ok'):
                return self._m_sd_pic_write_ok if hasattr(self, '_m_sd_pic_write_ok') else None

            self._m_sd_pic_write_ok = ((int(self.cu_flags, 16) & 1024) >> 10)
            return self._m_sd_pic_write_ok if hasattr(self, '_m_sd_pic_write_ok') else None

        @property
        def sd_pic_read_ok(self):
            if hasattr(self, '_m_sd_pic_read_ok'):
                return self._m_sd_pic_read_ok if hasattr(self, '_m_sd_pic_read_ok') else None

            self._m_sd_pic_read_ok = ((int(self.cu_flags, 16) & 2048) >> 11)
            return self._m_sd_pic_read_ok if hasattr(self, '_m_sd_pic_read_ok') else None

        @property
        def pic_ready_conv(self):
            if hasattr(self, '_m_pic_ready_conv'):
                return self._m_pic_ready_conv if hasattr(self, '_m_pic_ready_conv') else None

            self._m_pic_ready_conv = ((int(self.cu_flags, 16) & 128) >> 7)
            return self._m_pic_ready_conv if hasattr(self, '_m_pic_ready_conv') else None

        @property
        def fault_1v8_r(self):
            if hasattr(self, '_m_fault_1v8_r'):
                return self._m_fault_1v8_r if hasattr(self, '_m_fault_1v8_r') else None

            self._m_fault_1v8_r = ((int(self.cu_flags, 16) & 8) >> 3)
            return self._m_fault_1v8_r if hasattr(self, '_m_fault_1v8_r') else None

        @property
        def fault_1v8_m(self):
            if hasattr(self, '_m_fault_1v8_m'):
                return self._m_fault_1v8_m if hasattr(self, '_m_fault_1v8_m') else None

            self._m_fault_1v8_m = ((int(self.cu_flags, 16) & 16) >> 4)
            return self._m_fault_1v8_m if hasattr(self, '_m_fault_1v8_m') else None

        @property
        def llc_sram_fault(self):
            if hasattr(self, '_m_llc_sram_fault'):
                return self._m_llc_sram_fault if hasattr(self, '_m_llc_sram_fault') else None

            self._m_llc_sram_fault = ((int(self.cu_flags, 16) & 4) >> 2)
            return self._m_llc_sram_fault if hasattr(self, '_m_llc_sram_fault') else None

        @property
        def fault_3v3_12v(self):
            if hasattr(self, '_m_fault_3v3_12v'):
                return self._m_fault_3v3_12v if hasattr(self, '_m_fault_3v3_12v') else None

            self._m_fault_3v3_12v = ((int(self.cu_flags, 16) & 32) >> 5)
            return self._m_fault_3v3_12v if hasattr(self, '_m_fault_3v3_12v') else None

        @property
        def llc_onyx_fault(self):
            if hasattr(self, '_m_llc_onyx_fault'):
                return self._m_llc_onyx_fault if hasattr(self, '_m_llc_onyx_fault') else None

            self._m_llc_onyx_fault = ((int(self.cu_flags, 16) & 2) >> 1)
            return self._m_llc_onyx_fault if hasattr(self, '_m_llc_onyx_fault') else None

        @property
        def sd_erase_ok(self):
            if hasattr(self, '_m_sd_erase_ok'):
                return self._m_sd_erase_ok if hasattr(self, '_m_sd_erase_ok') else None

            self._m_sd_erase_ok = ((int(self.cu_flags, 16) & 8192) >> 13)
            return self._m_sd_erase_ok if hasattr(self, '_m_sd_erase_ok') else None

        @property
        def sd_get_info_ok(self):
            if hasattr(self, '_m_sd_get_info_ok'):
                return self._m_sd_get_info_ok if hasattr(self, '_m_sd_get_info_ok') else None

            self._m_sd_get_info_ok = ((int(self.cu_flags, 16) & 4096) >> 12)
            return self._m_sd_get_info_ok if hasattr(self, '_m_sd_get_info_ok') else None

        @property
        def onyx_on(self):
            if hasattr(self, '_m_onyx_on'):
                return self._m_onyx_on if hasattr(self, '_m_onyx_on') else None

            self._m_onyx_on = (int(self.cu_flags, 16) & 1)
            return self._m_onyx_on if hasattr(self, '_m_onyx_on') else None

        @property
        def pic_ready_raw(self):
            if hasattr(self, '_m_pic_ready_raw'):
                return self._m_pic_ready_raw if hasattr(self, '_m_pic_ready_raw') else None

            self._m_pic_ready_raw = ((int(self.cu_flags, 16) & 64) >> 6)
            return self._m_pic_ready_raw if hasattr(self, '_m_pic_ready_raw') else None

        @property
        def cpu_voltage_volt(self):
            if hasattr(self, '_m_cpu_voltage_volt'):
                return self._m_cpu_voltage_volt if hasattr(self, '_m_cpu_voltage_volt') else None

            self._m_cpu_voltage_volt = (int(self.cpu_voltage) / 1000.0)
            return self._m_cpu_voltage_volt if hasattr(self, '_m_cpu_voltage_volt') else None

        @property
        def sd_full(self):
            if hasattr(self, '_m_sd_full'):
                return self._m_sd_full if hasattr(self, '_m_sd_full') else None

            self._m_sd_full = ((int(self.cu_flags, 16) & 16384) >> 14)
            return self._m_sd_full if hasattr(self, '_m_sd_full') else None

        @property
        def pic_ready_compressed_8(self):
            if hasattr(self, '_m_pic_ready_compressed_8'):
                return self._m_pic_ready_compressed_8 if hasattr(self, '_m_pic_ready_compressed_8') else None

            self._m_pic_ready_compressed_8 = ((int(self.cu_flags, 16) & 512) >> 9)
            return self._m_pic_ready_compressed_8 if hasattr(self, '_m_pic_ready_compressed_8') else None

        @property
        def adc_ready(self):
            if hasattr(self, '_m_adc_ready'):
                return self._m_adc_ready if hasattr(self, '_m_adc_ready') else None

            self._m_adc_ready = ((int(self.cu_flags, 16) & 32768) >> 15)
            return self._m_adc_ready if hasattr(self, '_m_adc_ready') else None

        @property
        def pic_ready_compressed(self):
            if hasattr(self, '_m_pic_ready_compressed'):
                return self._m_pic_ready_compressed if hasattr(self, '_m_pic_ready_compressed') else None

            self._m_pic_ready_compressed = ((int(self.cu_flags, 16) & 256) >> 8)
            return self._m_pic_ready_compressed if hasattr(self, '_m_pic_ready_compressed') else None


    class V1RlType(KaitaiStruct):
        """[V1];RL;[Timestamp],[CPU voltage];[Battery voltage];[CPU temperature];[Amplifier temperature];[Flags]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.timestamp = (self._io.read_bytes_term(44, False, True, True)).decode(u"ASCII")
            self.cpu_voltage = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.battery_voltage = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.cpu_temperature = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.amplifier_temperature = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.flagsmagic = self._io.ensure_fixed_contents(b"\x30\x78")
            self.flags = (self._io.read_bytes(1)).decode(u"ASCII")

        @property
        def cpu_temperature_degree(self):
            if hasattr(self, '_m_cpu_temperature_degree'):
                return self._m_cpu_temperature_degree if hasattr(self, '_m_cpu_temperature_degree') else None

            self._m_cpu_temperature_degree = int(self.cpu_temperature)
            return self._m_cpu_temperature_degree if hasattr(self, '_m_cpu_temperature_degree') else None

        @property
        def fec(self):
            if hasattr(self, '_m_fec'):
                return self._m_fec if hasattr(self, '_m_fec') else None

            self._m_fec = (int(self.flags, 16) & 1)
            return self._m_fec if hasattr(self, '_m_fec') else None

        @property
        def timestamp_int(self):
            if hasattr(self, '_m_timestamp_int'):
                return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

            self._m_timestamp_int = int(self.timestamp)
            return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

        @property
        def band_lock(self):
            if hasattr(self, '_m_band_lock'):
                return self._m_band_lock if hasattr(self, '_m_band_lock') else None

            self._m_band_lock = ((int(self.flags, 16) & 4) >> 2)
            return self._m_band_lock if hasattr(self, '_m_band_lock') else None

        @property
        def cpu_voltage_volt(self):
            if hasattr(self, '_m_cpu_voltage_volt'):
                return self._m_cpu_voltage_volt if hasattr(self, '_m_cpu_voltage_volt') else None

            self._m_cpu_voltage_volt = (int(self.cpu_voltage) / 1000.0)
            return self._m_cpu_voltage_volt if hasattr(self, '_m_cpu_voltage_volt') else None

        @property
        def aes_128(self):
            if hasattr(self, '_m_aes_128'):
                return self._m_aes_128 if hasattr(self, '_m_aes_128') else None

            self._m_aes_128 = ((int(self.flags, 16) & 16) >> 4)
            return self._m_aes_128 if hasattr(self, '_m_aes_128') else None

        @property
        def amplifier_temperature_degree(self):
            if hasattr(self, '_m_amplifier_temperature_degree'):
                return self._m_amplifier_temperature_degree if hasattr(self, '_m_amplifier_temperature_degree') else None

            self._m_amplifier_temperature_degree = int(self.amplifier_temperature)
            return self._m_amplifier_temperature_degree if hasattr(self, '_m_amplifier_temperature_degree') else None

        @property
        def amp_ovt(self):
            if hasattr(self, '_m_amp_ovt'):
                return self._m_amp_ovt if hasattr(self, '_m_amp_ovt') else None

            self._m_amp_ovt = ((int(self.flags, 16) & 32) >> 5)
            return self._m_amp_ovt if hasattr(self, '_m_amp_ovt') else None

        @property
        def xor(self):
            if hasattr(self, '_m_xor'):
                return self._m_xor if hasattr(self, '_m_xor') else None

            self._m_xor = ((int(self.flags, 16) & 8) >> 3)
            return self._m_xor if hasattr(self, '_m_xor') else None

        @property
        def downlink(self):
            if hasattr(self, '_m_downlink'):
                return self._m_downlink if hasattr(self, '_m_downlink') else None

            self._m_downlink = ((int(self.flags, 16) & 2) >> 1)
            return self._m_downlink if hasattr(self, '_m_downlink') else None

        @property
        def battery_voltage_volt(self):
            if hasattr(self, '_m_battery_voltage_volt'):
                return self._m_battery_voltage_volt if hasattr(self, '_m_battery_voltage_volt') else None

            self._m_battery_voltage_volt = (int(self.battery_voltage) / 1000.0)
            return self._m_battery_voltage_volt if hasattr(self, '_m_battery_voltage_volt') else None


    class Repeaters(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_callsign_raw = self._root.CallsignRaw(self._io, self, self._root)
            self.rpt_ssid_raw = self._root.SsidMask(self._io, self, self._root)


    class Repeater(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_instance = []
            i = 0
            while True:
                _ = self._root.Repeaters(self._io, self, self._root)
                self.rpt_instance.append(_)
                if (_.rpt_ssid_raw.ssid_mask & 1) == 1:
                    break
                i += 1


    class OnyxType(KaitaiStruct):
        """[CU_R/CU_L];ONYX SENSOR T;[Timestamp];[Return value]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.timestamp = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.return_value = (self._io.read_bytes_full()).decode(u"ASCII")

        @property
        def return_value_int(self):
            if hasattr(self, '_m_return_value_int'):
                return self._m_return_value_int if hasattr(self, '_m_return_value_int') else None

            self._m_return_value_int = int(self.return_value)
            return self._m_return_value_int if hasattr(self, '_m_return_value_int') else None

        @property
        def timestamp_int(self):
            if hasattr(self, '_m_timestamp_int'):
                return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

            self._m_timestamp_int = int(self.timestamp)
            return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None


    class EmerType(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.timestamp = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            _on = self._parent.tlm_type
            if _on == u"LOG":
                self.tlmsw = self._root.EmLogType(self._io, self, self._root)
            elif _on == u"MN":
                self.tlmsw = self._root.EmmnType(self._io, self, self._root)

        @property
        def timestamp_int(self):
            if hasattr(self, '_m_timestamp_int'):
                return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

            self._m_timestamp_int = int(self.timestamp)
            return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None


    class CuType(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.timestamp = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            _on = self._parent.tlm_type
            if _on == u"ONYX SENSOR T":
                self.tlmsw = self._root.OnyxType(self._io, self, self._root)
            elif _on == u"LOG":
                self.tlmsw = self._root.CuLogType(self._io, self, self._root)

        @property
        def timestamp_int(self):
            if hasattr(self, '_m_timestamp_int'):
                return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

            self._m_timestamp_int = int(self.timestamp)
            return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None


    class A1GyroType(KaitaiStruct):
        """A1;GYRO;[Current timestamp];[GyroX];[GyroY];[GyroZ]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.timestamp = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.giro_x = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.giro_y = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.giro_z = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")

        @property
        def gyro_x_int(self):
            if hasattr(self, '_m_gyro_x_int'):
                return self._m_gyro_x_int if hasattr(self, '_m_gyro_x_int') else None

            self._m_gyro_x_int = int(self.giro_x)
            return self._m_gyro_x_int if hasattr(self, '_m_gyro_x_int') else None

        @property
        def gyro_y_int(self):
            if hasattr(self, '_m_gyro_y_int'):
                return self._m_gyro_y_int if hasattr(self, '_m_gyro_y_int') else None

            self._m_gyro_y_int = int(self.giro_y)
            return self._m_gyro_y_int if hasattr(self, '_m_gyro_y_int') else None

        @property
        def gyro_z_int(self):
            if hasattr(self, '_m_gyro_z_int'):
                return self._m_gyro_z_int if hasattr(self, '_m_gyro_z_int') else None

            self._m_gyro_z_int = int(self.giro_z)
            return self._m_gyro_z_int if hasattr(self, '_m_gyro_z_int') else None

        @property
        def timestamp_int(self):
            if hasattr(self, '_m_timestamp_int'):
                return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

            self._m_timestamp_int = int(self.timestamp)
            return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None


    class A1MagType(KaitaiStruct):
        """A1;MAG;[Current timestamp];[MagX];[MagY];[MagZ]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.timestamp = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.mag_x = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.mag_y = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.mag_z = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")

        @property
        def mag_x_int(self):
            if hasattr(self, '_m_mag_x_int'):
                return self._m_mag_x_int if hasattr(self, '_m_mag_x_int') else None

            self._m_mag_x_int = int(self.mag_x)
            return self._m_mag_x_int if hasattr(self, '_m_mag_x_int') else None

        @property
        def mag_y_int(self):
            if hasattr(self, '_m_mag_y_int'):
                return self._m_mag_y_int if hasattr(self, '_m_mag_y_int') else None

            self._m_mag_y_int = int(self.mag_y)
            return self._m_mag_y_int if hasattr(self, '_m_mag_y_int') else None

        @property
        def mag_z_int(self):
            if hasattr(self, '_m_mag_z_int'):
                return self._m_mag_z_int if hasattr(self, '_m_mag_z_int') else None

            self._m_mag_z_int = int(self.mag_z)
            return self._m_mag_z_int if hasattr(self, '_m_mag_z_int') else None

        @property
        def timestamp_int(self):
            if hasattr(self, '_m_timestamp_int'):
                return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

            self._m_timestamp_int = int(self.timestamp)
            return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None


    class A1Type(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self._parent.tlm_type
            if _on == u"FLAGS":
                self.tlm_sw = self._root.A1FlagType(self._io, self, self._root)
            elif _on == u"MAG":
                self.tlm_sw = self._root.A1MagType(self._io, self, self._root)
            elif _on == u"GYRO":
                self.tlm_sw = self._root.A1GyroType(self._io, self, self._root)
            elif _on == u"POSITION":
                self.tlm_sw = self._root.A1PositionType(self._io, self, self._root)


    class MsType(KaitaiStruct):
        """[V1/U2];MS;[Timestamp];[Current rssi];[Latch rssi];[AFC offset]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.timestamp = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.current_rssi = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.latch_rssi = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.a_f_c_offset = (self._io.read_bytes_full()).decode(u"ASCII")

        @property
        def current_rssi_int(self):
            if hasattr(self, '_m_current_rssi_int'):
                return self._m_current_rssi_int if hasattr(self, '_m_current_rssi_int') else None

            self._m_current_rssi_int = int(self.current_rssi)
            return self._m_current_rssi_int if hasattr(self, '_m_current_rssi_int') else None

        @property
        def latch_rssi_int(self):
            if hasattr(self, '_m_latch_rssi_int'):
                return self._m_latch_rssi_int if hasattr(self, '_m_latch_rssi_int') else None

            self._m_latch_rssi_int = int(self.latch_rssi)
            return self._m_latch_rssi_int if hasattr(self, '_m_latch_rssi_int') else None

        @property
        def a_f_c_offset_int(self):
            if hasattr(self, '_m_a_f_c_offset_int'):
                return self._m_a_f_c_offset_int if hasattr(self, '_m_a_f_c_offset_int') else None

            self._m_a_f_c_offset_int = int(self.a_f_c_offset)
            return self._m_a_f_c_offset_int if hasattr(self, '_m_a_f_c_offset_int') else None

        @property
        def timestamp_int(self):
            if hasattr(self, '_m_timestamp_int'):
                return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None

            self._m_timestamp_int = int(self.timestamp)
            return self._m_timestamp_int if hasattr(self, '_m_timestamp_int') else None


    class LogType(KaitaiStruct):
        """M1;LOG;[Timestamp];[Boot number];[Up time];[CPU voltage];[CPU temperature]
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.boot_number = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.up_time = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.cpu_voltage = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.cpu_temperature = (self._io.read_bytes_full()).decode(u"ASCII")

        @property
        def cpu_voltage_volt(self):
            if hasattr(self, '_m_cpu_voltage_volt'):
                return self._m_cpu_voltage_volt if hasattr(self, '_m_cpu_voltage_volt') else None

            self._m_cpu_voltage_volt = (int(self.cpu_voltage) / 1000.0)
            return self._m_cpu_voltage_volt if hasattr(self, '_m_cpu_voltage_volt') else None

        @property
        def boot_number_int(self):
            if hasattr(self, '_m_boot_number_int'):
                return self._m_boot_number_int if hasattr(self, '_m_boot_number_int') else None

            self._m_boot_number_int = int(self.boot_number)
            return self._m_boot_number_int if hasattr(self, '_m_boot_number_int') else None

        @property
        def cpu_temperature_degree(self):
            if hasattr(self, '_m_cpu_temperature_degree'):
                return self._m_cpu_temperature_degree if hasattr(self, '_m_cpu_temperature_degree') else None

            self._m_cpu_temperature_degree = int(self.cpu_temperature)
            return self._m_cpu_temperature_degree if hasattr(self, '_m_cpu_temperature_degree') else None

        @property
        def up_time_int(self):
            if hasattr(self, '_m_up_time_int'):
                return self._m_up_time_int if hasattr(self, '_m_up_time_int') else None

            self._m_up_time_int = int(self.up_time)
            return self._m_up_time_int if hasattr(self, '_m_up_time_int') else None


    class CallsignRaw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw__raw_callsign_ror = self._io.read_bytes(6)
            self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
            io = KaitaiStream(BytesIO(self._raw_callsign_ror))
            self.callsign_ror = self._root.Callsign(io, self, self._root)


    class V1Type(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self._parent.tlm_type
            if _on == u"RL":
                self.tlmsw = self._root.V1RlType(self._io, self, self._root)
            elif _on == u"MS":
                self.tlmsw = self._root.MsType(self._io, self, self._root)


    class U2Type(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self._parent.tlm_type
            if _on == u"RL":
                self.tlmsw = self._root.U2RlType(self._io, self, self._root)
            elif _on == u"MS":
                self.tlmsw = self._root.MsType(self._io, self, self._root)


    class Ax25InfoData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.start = self._io.read_u1()
            self.tlm_area = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            self.tlm_type = (self._io.read_bytes_term(59, False, True, True)).decode(u"ASCII")
            _on = self.tlm_area
            if _on == u"EM":
                self.tlm_area_switch = self._root.EmerType(self._io, self, self._root)
            elif _on == u"M1":
                self.tlm_area_switch = self._root.M1Type(self._io, self, self._root)
            elif _on == u"V1":
                self.tlm_area_switch = self._root.V1Type(self._io, self, self._root)
            elif _on == u"U2":
                self.tlm_area_switch = self._root.U2Type(self._io, self, self._root)
            elif _on == u"A1":
                self.tlm_area_switch = self._root.A1Type(self._io, self, self._root)
            elif _on == u"CU_L":
                self.tlm_area_switch = self._root.CuType(self._io, self, self._root)
            elif _on == u"CU_R":
                self.tlm_area_switch = self._root.CuType(self._io, self, self._root)
            elif _on == u"ER":
                self.tlm_area_switch = self._root.EmerType(self._io, self, self._root)

        @property
        def aprs_message(self):
            if hasattr(self, '_m_aprs_message'):
                return self._m_aprs_message if hasattr(self, '_m_aprs_message') else None

            _pos = self._io.pos()
            self._io.seek(0)
            self._m_aprs_message = (self._io.read_bytes_full()).decode(u"utf-8")
            self._io.seek(_pos)
            return self._m_aprs_message if hasattr(self, '_m_aprs_message') else None



