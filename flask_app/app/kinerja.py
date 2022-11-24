from app.conn import cur, conn

class Kinerja:
    kpi = ['EAF', 'EFOR', 'SOF', 'CF', 'SdOF', 'PS', 'SFC']
    rsh = '(ph - ((po + mo + fo) + sh))'
    total_derating = '(epdh + eudh + esdh)'
    total_ps = '(ps_sentral + ps_trafo)'
    produksi_netto = f'(produksi - {total_ps})'
    dtp_ph = '(dtp * ph)'
    dmn_ph = '(dmn * ph)'
    dmn_ph_der = f'(dmn * (sh + {rsh} - {total_derating}))'
    dmn_fo_eudh = '(dmn * (fo + eudh))'
    dmn_fo_sh_efdhrs = '(dmn * (fo + sh + efdhrs))'
    dmn_har = '(dmn * (po + mo))'
    sdof = 'trip_internal'

    def eaf_unit_bulanan(self, periode) -> dict:
        cur.execute(f"SELECT ROUND((SUM({self.dmn_ph_der}) / SUM({self.dmn_ph}) * 100), 3) AS 'eaf_unit' FROM pengusahaan WHERE periode = '{periode}'")
        result = cur.fetchone()
        return result

    def efor_unit_bulanan(self, periode) -> dict:
        cur.execute(f"SELECT ROUND((SUM({self.dmn_fo_eudh}) / SUM({self.dmn_fo_sh_efdhrs}) * 100), 3) AS 'efor_unit' FROM pengusahaan WHERE periode = '{periode}'")
        result = cur.fetchone()
        return result

    def sof_unit_bulanan(self, periode) -> dict:
        cur.execute(f"SELECT ROUND((SUM({self.dmn_har}) / SUM({self.dmn_ph}) * 100), 3) AS 'sof_unit' FROM pengusahaan WHERE periode = '{periode}'")
        result = cur.fetchone()
        return result

    def sfc_unit_bulanan(self, periode) -> dict:
        cur.execute(f"SELECT ROUND((SUM(bbm) / SUM(produksi)), 3) AS 'sfc_unit' FROM pengusahaan WHERE periode = '{periode}'")
        result = cur.fetchone()
        return result

    def ps_unit_bulanan(self, periode) -> dict:
        cur.execute(f"SELECT ROUND((SUM({self.total_ps}) / SUM(produksi) * 100), 3) AS 'ps_unit' FROM pengusahaan WHERE periode = '{periode}'")
        result = cur.fetchone()
        return result

    def kinerja_unit_bulanan(self, periode):
        eaf = self.eaf_unit_bulanan(periode)
        efor = self.efor_unit_bulanan(periode)
        sof = self.sof_unit_bulanan(periode)
        sfc = self.sfc_unit_bulanan(periode)
        ps = self.ps_unit_bulanan(periode)

        kinerja = eaf | efor | sof | sfc | ps

        if kinerja['eaf_unit'] is None:
            kinerja['eaf_unit'] = 0.0
        if kinerja['efor_unit'] is None:
            kinerja['efor_unit'] = 0.0
        if kinerja['sof_unit'] is None:
            kinerja['sof_unit'] = 0.0
        if kinerja['sfc_unit'] is None:
            kinerja['sfc_unit'] = 0.0
        if kinerja['ps_unit'] is None:
            kinerja['ps_unit'] = 0.0

        return kinerja