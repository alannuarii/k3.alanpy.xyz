from unittest import result
from app.conn import cur, conn
from datetime import date, timedelta, datetime

class K3:
    data_dummy = {
        'id_apar' : 32,
        'lokasi' : 'Tangki Curah',
        'merek' : 'Viking',
        'tipe' : 'ABCE',
        'kapasitas' : '6 kg',
        'jenis' : 'Powder',
        'masa_berlaku' : '2023-01'
    }

    def month_id(self, bulan:str):
        if bulan == '01':
            return 'Januari'
        elif bulan == '02':
            return 'Februari'
        elif bulan == '03':
            return 'Maret'
        elif bulan == '04':
            return 'April'
        elif bulan == '05':
            return 'Mei'
        elif bulan == '06':
            return 'Juni'
        elif bulan == '07':
            return 'Juli'
        elif bulan == '08':
            return 'Agustus'
        elif bulan == '09':
            return 'September'
        elif bulan == '10':
            return 'Oktober'
        elif bulan == '11':
            return 'November'
        elif bulan == '12':
            return 'Desember'

    def format_bulan(self, tanggal):
        if len(tanggal) == 10:
            bulan = tanggal[3:-5]
            return self.month_id(bulan)
        elif len(tanggal) == 7:
            bulan = tanggal[5:]
            return self.month_id(bulan)
        else:
            return ''

    def get_date(self, date_str:str):
        tanggal = datetime.strptime(date_str, '%Y-%m-%d').date()
        return tanggal

    def get_friday(self, tanggal:date):
        getday = date.strftime(tanggal, '%A')
        if getday == 'Saturday':
            deltafriday = tanggal + timedelta(days=-0)
            return [deltafriday, deltafriday + timedelta(days=+6)]
        if getday == 'Sunday':
            deltafriday = tanggal + timedelta(days=-1)
            return [deltafriday, deltafriday + timedelta(days=+6)]
        if getday == 'Monday':
            deltafriday = tanggal + timedelta(days=-2)
            return [deltafriday, deltafriday + timedelta(days=+6)]
        if getday == 'Tuesday':
            deltafriday = tanggal + timedelta(days=-3)
            return [deltafriday, deltafriday + timedelta(days=+6)]
        if getday == 'Wednesday':
            deltafriday = tanggal + timedelta(days=-4)
            return [deltafriday, deltafriday + timedelta(days=+6)]
        if getday == 'Thursday':
            deltafriday = tanggal + timedelta(days=-5)
            return [deltafriday, deltafriday + timedelta(days=+6)]
        if getday == 'Friday':
            deltafriday = tanggal + timedelta(days=-6)
            return [deltafriday, deltafriday + timedelta(days=+6)]

    def get_friday_format(self, tanggal:date):
        list_date = self.get_friday(tanggal)
        result = []
        for date in list_date:
            new_date = date.strftime('%d-%m-%Y')
            month_id = self.format_bulan(new_date)
            date_id = f"{new_date[:-8]} {month_id} {new_date[6:]}"
            result.append(date_id)
        return result

    def get_apar(self):
        cur.execute("SELECT * FROM apar")
        result = cur.fetchall()
        return result

    def insert_apar(self, id_apar, lokasi, merek, tipe, kapasitas, jenis, masa_berlaku, foto_apar):
        cur.execute(f"INSERT INTO apar (id_apar, lokasi, merek, tipe, kapasitas, jenis, masa_berlaku, foto_apar) VALUES ({id_apar}, '{lokasi}', '{merek}', '{tipe}', '{kapasitas}', '{jenis}', '{masa_berlaku}', '{foto_apar}')")
        conn.commit()

    def update_apar(self, id_apar, lokasi, merek, tipe, kapasitas, jenis, masa_berlaku, current_id, foto_apar):
        cur.execute(f"UPDATE apar SET id_apar={id_apar}, lokasi='{lokasi}', merek='{merek}', tipe='{tipe}', kapasitas='{kapasitas}', jenis='{jenis}', masa_berlaku='{masa_berlaku}', foto_apar='{foto_apar}' WHERE id_apar={current_id}")
        conn.commit()

    def delete_apar(self, id_apar):
        cur.execute(f"DELETE FROM apar WHERE id_apar={id_apar}")
        conn.commit()

    def get_foto_apar(self, id_apar):
        cur.execute(f"SELECT foto_apar FROM apar WHERE id_apar={id_apar}")
        result = cur.fetchall()
        return result

    def get_checklist_apar(self, awal, akhir):
        cur.execute(f"SELECT DISTINCT(apar_id) FROM checklist_apar WHERE tanggal >= '{awal}' AND tanggal <= '{akhir}' GROUP BY apar_id")
        result = cur.fetchall()
        return result

    def get_apar_inspection(self, awal, akhir):
        cur.execute(f"SELECT * FROM checklist_apar JOIN apar ON checklist_apar.apar_id = apar.id_apar WHERE tanggal >= '{awal}' AND tanggal <= '{akhir}' GROUP BY id_apar ORDER BY id_apar")
        result = cur.fetchall()
        return result

    def get_checklist_month(self, month):
        cur.execute(f"SELECT DISTINCT(tanggal) FROM checklist_apar WHERE tanggal LIKE '%{month}%'")
        result = cur.fetchall()
        return result

    def insert_checklist_apar(self, fisik, kartu_gantung, seal, pin, meter, selang_corong, keterangan, apar_id):
        cur.execute(f"INSERT INTO checklist_apar (tanggal, fisik, kartu_gantung, seal, pin, meter, selang_corong, keterangan, apar_id) VALUES (NOW(), {fisik}, {kartu_gantung}, {seal}, {pin}, {meter}, {selang_corong}, '{keterangan}', {apar_id})")
        conn.commit()

    def update_checklist_apar(self, fisik, kartu_gantung, seal, pin, meter, selang_corong, keterangan, id_checklist_apar):
        cur.execute(f"UPDATE checklist_apar SET fisik={fisik}, kartu_gantung={kartu_gantung}, seal={seal}, pin={pin}, meter={meter}, selang_corong={selang_corong}, keterangan='{keterangan}', tanggal=NOW() WHERE id_checklist_apar={id_checklist_apar}")
        conn.commit()

    def get_p3k(self):
        cur.execute(f"SELECT *, saldo_kantor + saldo_ccr + saldo_tps + saldo_pos + stock AS 'total' FROM p3k")
        result = cur.fetchall()
        return result

    def insert_p3k(self, nama_barang, satuan, saldo_kantor, saldo_ccr, saldo_tps, saldo_pos, stock, kadaluarsa, foto_p3k):
        cur.execute(f"INSERT INTO p3k (nama_barang, satuan, saldo_kantor, saldo_ccr, saldo_tps, saldo_pos, stock, kadaluarsa, foto_p3k) VALUES ('{nama_barang}', '{satuan}', {saldo_kantor}, {saldo_ccr}, {saldo_tps}, {saldo_pos}, {stock}, '{kadaluarsa}', '{foto_p3k}')")
        conn.commit()

    def update_p3k(self, nama_barang, satuan, saldo_kantor, saldo_ccr, saldo_tps, saldo_pos, stock, kadaluarsa, foto_p3k, id_p3k):
        cur.execute(f"UPDATE p3k SET nama_barang='{nama_barang}', satuan='{satuan}', saldo_kantor={saldo_kantor}, saldo_ccr={saldo_ccr}, saldo_tps={saldo_tps}, saldo_pos={saldo_pos}, stock={stock}, kadaluarsa='{kadaluarsa}', foto_p3k='{foto_p3k}' WHERE id_p3k={id_p3k}")
        conn.commit()

    def delete_p3k(self, id_p3k):
        cur.execute(f"DELETE FROM p3k WHERE id_p3k={id_p3k}")
        conn.commit()

    def get_foto_p3k(self, id_p3k):
        cur.execute(f"SELECT foto_p3k FROM p3k WHERE id_p3k={id_p3k}")
        result = cur.fetchall()
        return result

    def get_persediaan_kantor(self):
        cur.execute(f"SELECT id_p3k, nama_barang, saldo_kantor, satuan FROM p3k WHERE saldo_kantor > 0")
        result =  cur.fetchall()
        return result

    def get_saldo_kantor(self):
        cur.execute(f"SELECT (saldo_kantor + SUM(masuk_kantor) - SUM(keluar_kantor)) AS pers_kantor FROM p3k LEFT JOIN kantor ON p3k.id_p3k = kantor.p3k_id GROUP BY id_p3k")
        result = cur.fetchall()
        return result

    def insert_kantor(self, tgl_kantor, masuk_kantor, keluar_kantor, p3k_id):
        cur.execute(f"INSERT INTO kantor (tgl_kantor, masuk_kantor, keluar_kantor, p3k_id) VALUES ('{tgl_kantor}', {masuk_kantor}, {keluar_kantor}, {p3k_id})")
        conn.commit()

    def get_persediaan_ccr(self):
        cur.execute(f"SELECT id_p3k, nama_barang, saldo_ccr, satuan FROM p3k WHERE saldo_ccr > 0")
        result =  cur.fetchall()
        return result

    def get_saldo_ccr(self):
        cur.execute(f"SELECT (saldo_ccr + SUM(masuk_ccr) - SUM(keluar_ccr)) AS pers_ccr FROM p3k LEFT JOIN ccr ON p3k.id_p3k = ccr.p3k_id GROUP BY id_p3k")
        result = cur.fetchall()
        return result

    def insert_ccr(self, tgl_ccr, masuk_ccr, keluar_ccr, p3k_id):
        cur.execute(f"INSERT INTO ccr (tgl_ccr, masuk_ccr, keluar_ccr, p3k_id) VALUES ('{tgl_ccr}', {masuk_ccr}, {keluar_ccr}, {p3k_id})")
        conn.commit()

    def get_persediaan_tps(self):
        cur.execute(f"SELECT id_p3k, nama_barang, saldo_tps, satuan FROM p3k WHERE saldo_tps > 0")
        result =  cur.fetchall()
        return result

    def get_saldo_tps(self):
        cur.execute(f"SELECT (saldo_tps + SUM(masuk_tps) - SUM(keluar_tps)) AS pers_tps FROM p3k LEFT JOIN tps ON p3k.id_p3k = tps.p3k_id GROUP BY id_p3k")
        result = cur.fetchall()
        return result

    def insert_tps(self, tgl_tps, masuk_tps, keluar_tps, p3k_id):
        cur.execute(f"INSERT INTO tps (tgl_tps, masuk_tps, keluar_tps, p3k_id) VALUES ('{tgl_tps}', {masuk_tps}, {keluar_tps}, {p3k_id})")
        conn.commit()

    def get_persediaan_pos(self):
        cur.execute(f"SELECT id_p3k, nama_barang, saldo_pos, satuan FROM p3k WHERE saldo_pos > 0")
        result =  cur.fetchall()
        return result

    def get_saldo_pos(self):
        cur.execute(f"SELECT (saldo_pos + SUM(masuk_pos) - SUM(keluar_pos)) AS pers_pos FROM p3k LEFT JOIN pos ON p3k.id_p3k = pos.p3k_id GROUP BY id_p3k")
        result = cur.fetchall()
        return result

    def insert_pos(self, tgl_pos, masuk_pos, keluar_pos, p3k_id):
        cur.execute(f"INSERT INTO pos (tgl_pos, masuk_pos, keluar_pos, p3k_id) VALUES ('{tgl_pos}', {masuk_pos}, {keluar_pos}, {p3k_id})")
        conn.commit()
        

