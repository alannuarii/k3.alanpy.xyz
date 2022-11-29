from app.conn import cur, conn

class Kinerja:
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des']
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

    def target_kinerja(self, tahun):
        cur.execute(f"SELECT * FROM target WHERE tahun = '{tahun}'")
        result = cur.fetchall()
        return result

    def list_target_kinerja(self, kpi, tahun, length):
        cur.execute(f"SELECT nilai_target FROM target WHERE kpi = '{kpi}' AND tahun = '{tahun}'")
        result = cur.fetchone()
        list_result = []
        for i in range(len(length)):
            list_result.append(result['nilai_target'])
        return list_result

    def get_satuan(self, kpi, tahun):
        cur.execute(f"SELECT satuan FROM target WHERE kpi = '{kpi}' AND tahun = '{tahun}'")
        result = cur.fetchone()
        return result['satuan']

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

    def eaf_unit_kumulatif(self, awal, akhir):
        cur.execute(f"SELECT ROUND((SUM({self.dmn_ph_der}) / SUM({self.dmn_ph}) * 100), 3) AS 'eaf_unit' FROM pengusahaan WHERE periode BETWEEN '{awal}' AND '{akhir}'")
        result = cur.fetchone()
        return result

    def efor_unit_kumulatif(self, awal, akhir):
        cur.execute(f"SELECT ROUND((SUM({self.dmn_fo_eudh}) / SUM({self.dmn_fo_sh_efdhrs}) * 100), 3) AS 'efor_unit' FROM pengusahaan WHERE periode BETWEEN '{awal}' AND '{akhir}'")
        result = cur.fetchone()
        return result

    def sof_unit_kumulatif(self, awal, akhir):
        cur.execute(f"SELECT ROUND((SUM({self.dmn_har}) / SUM({self.dmn_ph}) * 100), 3) AS 'sof_unit' FROM pengusahaan WHERE periode BETWEEN '{awal}' AND '{akhir}'")
        result = cur.fetchone()
        return result

    def sfc_unit_kumulatif(self, awal, akhir):
        cur.execute(f"SELECT ROUND((SUM(bbm) / SUM(produksi)), 3) AS 'sfc_unit' FROM pengusahaan WHERE periode BETWEEN '{awal}' AND '{akhir}'")
        result = cur.fetchone()
        return result

    def ps_unit_kumulatif(self, awal, akhir):
        cur.execute(f"SELECT ROUND((SUM({self.total_ps}) / SUM(produksi) * 100), 3) AS 'ps_unit' FROM pengusahaan WHERE periode BETWEEN '{awal}' AND '{akhir}'")
        result = cur.fetchone()
        return result

    def list_kinerja_unit_kumulatif(self, periode, kpi):
        akhir = periode
        awal = f"{akhir[:4]}-01-01"
        list_kum = []
        if kpi == 'eaf':
            for i in range(int(akhir[5:-3])):
                kin = self.eaf_unit_kumulatif(awal, f"{akhir[:4]}-{i + 1}-01")
                list_kum.append(kin['eaf_unit'])
            return list_kum
        elif kpi == 'efor':
            for i in range(int(akhir[5:-3])):
                kin = self.efor_unit_kumulatif(awal, f"{akhir[:4]}-{i + 1}-01")
                list_kum.append(kin['efor_unit'])
            return list_kum
        elif kpi == 'sof':
            for i in range(int(akhir[5:-3])):
                kin = self.sof_unit_kumulatif(awal, f"{akhir[:4]}-{i + 1}-01")
                list_kum.append(kin['sof_unit'])
            return list_kum
        elif kpi == 'sfc':
            for i in range(int(akhir[5:-3])):
                kin = self.sfc_unit_kumulatif(awal, f"{akhir[:4]}-{i + 1}-01")
                list_kum.append(kin['sfc_unit'])
            return list_kum
        elif kpi == 'ps':
            for i in range(int(akhir[5:-3])):
                kin = self.ps_unit_kumulatif(awal, f"{akhir[:4]}-{i + 1}-01")
                list_kum.append(kin['ps_unit'])
            return list_kum

    def get_kondisi_unit(self, periode):
        cur.execute(f"SELECT id_unit, merek, tipe, kondisi, dtp, dmn FROM unit JOIN kondisi_kit ON unit.id_unit = kondisi_kit.unit_id JOIN pengusahaan ON unit.id_unit = pengusahaan.mesin_id WHERE periode = '{periode}' ORDER BY id_unit")
        result = cur.fetchall()
        return result        