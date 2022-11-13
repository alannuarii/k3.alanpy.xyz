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

    def get_this_month(self):
        today =  date.today()
        month = str(today)[5:-3]
        return month

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

    def format_bulan(self, tanggal:str):
        if len(tanggal) == 10:
            if tanggal[4] == '-':
                bulan = tanggal[5:-3]
                return self.month_id(bulan)
            elif tanggal[2] == '-':
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
        result = []
        list_date = self.get_friday(tanggal)
        for date in list_date:
            new_date = date.strftime('%d-%m-%Y')
            month_id = self.format_bulan(new_date)
            date_id = f"{new_date[:-8]} {month_id} {new_date[6:]}"
            result.append(date_id)
        return result

    def get_tanggal_format(self, tanggal:date):
        new_date = tanggal.strftime('%d-%m-%Y')
        month_id = self.format_bulan(new_date)
        date_id = f"{new_date[:-8]} {month_id} {new_date[6:]}"
        return date_id

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
        cur.execute(f"SELECT * FROM p3k")
        result = cur.fetchall()
        return result

    def insert_p3k(self, nama_barang, satuan, kadaluarsa, foto_p3k):
        cur.execute(f"INSERT INTO p3k (nama_barang, satuan, kadaluarsa, foto_p3k) VALUES ('{nama_barang}', '{satuan}', '{kadaluarsa}', '{foto_p3k}')")
        conn.commit()

    def update_p3k(self, nama_barang, satuan, kadaluarsa, foto_p3k, id_p3k):
        cur.execute(f"UPDATE p3k SET nama_barang='{nama_barang}', satuan='{satuan}', kadaluarsa='{kadaluarsa}', foto_p3k='{foto_p3k}' WHERE id_p3k={id_p3k}")
        conn.commit()

    def delete_p3k(self, id_p3k):
        cur.execute(f"DELETE FROM p3k WHERE id_p3k={id_p3k}")
        conn.commit()

    def get_foto_p3k(self, id_p3k):
        cur.execute(f"SELECT foto_p3k FROM p3k WHERE id_p3k={id_p3k}")
        result = cur.fetchall()
        return result

    def get_saldo_kantor(self):
        cur.execute(f"SELECT (SUM(masuk_kantor) - SUM(keluar_kantor)) AS pers_kantor FROM p3k LEFT JOIN kantor ON p3k.id_p3k = kantor.p3k_id GROUP BY id_p3k")
        result = cur.fetchall()
        return result

    def get_saldo_kantor_filter(self, tanggal):
        cur.execute(f"SELECT (SUM(masuk_kantor) - SUM(keluar_kantor)) AS pers_kantor FROM p3k LEFT JOIN kantor ON p3k.id_p3k = kantor.p3k_id WHERE tgl_kantor < '{tanggal}' GROUP BY id_p3k ORDER BY id_p3k")
        result = cur.fetchall()
        return result

    def insert_kantor(self, tgl_kantor, masuk_kantor, keluar_kantor, p3k_id):
        cur.execute(f"INSERT INTO kantor (tgl_kantor, masuk_kantor, keluar_kantor, p3k_id) VALUES ('{tgl_kantor}', {masuk_kantor}, {keluar_kantor}, {p3k_id})")
        conn.commit()

    def get_saldo_ccr(self):
        cur.execute(f"SELECT (SUM(masuk_ccr) - SUM(keluar_ccr)) AS pers_ccr FROM p3k LEFT JOIN ccr ON p3k.id_p3k = ccr.p3k_id GROUP BY id_p3k")
        result = cur.fetchall()
        return result

    def get_saldo_ccr_filter(self, tanggal):
        cur.execute(f"SELECT (SUM(masuk_ccr) - SUM(keluar_ccr)) AS pers_ccr FROM p3k LEFT JOIN ccr ON p3k.id_p3k = ccr.p3k_id WHERE tgl_ccr < '{tanggal}' GROUP BY id_p3k ORDER BY id_p3k")
        result = cur.fetchall()
        return result

    def insert_ccr(self, tgl_ccr, masuk_ccr, keluar_ccr, p3k_id):
        cur.execute(f"INSERT INTO ccr (tgl_ccr, masuk_ccr, keluar_ccr, p3k_id) VALUES ('{tgl_ccr}', {masuk_ccr}, {keluar_ccr}, {p3k_id})")
        conn.commit()

    def get_saldo_tps(self):
        cur.execute(f"SELECT (SUM(masuk_tps) - SUM(keluar_tps)) AS pers_tps FROM p3k LEFT JOIN tps ON p3k.id_p3k = tps.p3k_id GROUP BY id_p3k")
        result = cur.fetchall()
        return result

    def get_saldo_tps_filter(self, tanggal):
        cur.execute(f"SELECT (SUM(masuk_tps) - SUM(keluar_tps)) AS pers_tps FROM p3k LEFT JOIN tps ON p3k.id_p3k = tps.p3k_id WHERE tgl_tps < '{tanggal}' GROUP BY id_p3k ORDER BY id_p3k")
        result = cur.fetchall()
        return result

    def insert_tps(self, tgl_tps, masuk_tps, keluar_tps, p3k_id):
        cur.execute(f"INSERT INTO tps (tgl_tps, masuk_tps, keluar_tps, p3k_id) VALUES ('{tgl_tps}', {masuk_tps}, {keluar_tps}, {p3k_id})")
        conn.commit()

    def get_saldo_pos(self):
        cur.execute(f"SELECT (SUM(masuk_pos) - SUM(keluar_pos)) AS pers_pos FROM p3k LEFT JOIN pos ON p3k.id_p3k = pos.p3k_id GROUP BY id_p3k")
        result = cur.fetchall()
        return result

    def get_saldo_pos_filter(self, tanggal):
        cur.execute(f"SELECT (SUM(masuk_pos) - SUM(keluar_pos)) AS pers_pos FROM p3k LEFT JOIN pos ON p3k.id_p3k = pos.p3k_id WHERE tgl_pos < '{tanggal}' GROUP BY id_p3k ORDER BY id_p3k")
        result = cur.fetchall()
        return result

    def insert_pos(self, tgl_pos, masuk_pos, keluar_pos, p3k_id):
        cur.execute(f"INSERT INTO pos (tgl_pos, masuk_pos, keluar_pos, p3k_id) VALUES ('{tgl_pos}', {masuk_pos}, {keluar_pos}, {p3k_id})")
        conn.commit()

    def get_saldo_stock(self):
        cur.execute(f"SELECT (SUM(masuk_stock) - SUM(keluar_stock)) AS pers_stock FROM p3k LEFT JOIN stock ON p3k.id_p3k = stock.p3k_id GROUP BY id_p3k")
        result = cur.fetchall()
        return result

    def get_saldo_stock_filter(self, tanggal):
        cur.execute(f"SELECT (SUM(masuk_stock) - SUM(keluar_stock)) AS pers_stock FROM p3k LEFT JOIN stock ON p3k.id_p3k = stock.p3k_id WHERE tgl_stock < '{tanggal}' GROUP BY id_p3k ORDER BY id_p3k")
        result = cur.fetchall()
        return result

    def insert_stock(self, tgl_stock, masuk_stock, keluar_stock, p3k_id):
        cur.execute(f"INSERT INTO stock (tgl_stock, masuk_stock, keluar_stock, p3k_id) VALUES ('{tgl_stock}', {masuk_stock}, {keluar_stock}, {p3k_id})")
        conn.commit()

    def get_saldo_p3k(self, table, tgl_p3k, tanggal):
        cur.execute(f"SELECT * FROM {table} WHERE {tgl_p3k} < '{tanggal}'")
        result = cur.fetchall()
        return result
        
    def get_hydrant(self):
        cur.execute("SELECT * FROM hydrant")
        result = cur.fetchall()
        return result

    def insert_hydrant(self, nama_peralatan, merek, tipe, jumlah, satuan, foto_hydrant):
        cur.execute(f"INSERT INTO hydrant (nama_peralatan, merek, tipe, jumlah, satuan, foto_hydrant) VALUES ('{nama_peralatan}', '{merek}', '{tipe}', {jumlah}, '{satuan}', '{foto_hydrant}')")
        conn.commit()

    def update_hydrant(self, id_hydrant, nama_peralatan, merek, tipe, jumlah, satuan, foto_hydrant):
        cur.execute(f"UPDATE hydrant SET nama_peralatan='{nama_peralatan}', merek='{merek}', tipe='{tipe}', jumlah='{jumlah}', satuan='{satuan}', foto_hydrant='{foto_hydrant}' WHERE id_hydrant={id_hydrant}")
        conn.commit()

    def delete_hydrant(self, id_hydrant):
        cur.execute(f"DELETE FROM hydrant WHERE id_hydrant={id_hydrant}")
        conn.commit()

    def get_foto_hydrant(self, id_hydrant):
        cur.execute(f"SELECT foto_hydrant FROM hydrant WHERE id_hydrant={id_hydrant}")
        result = cur.fetchall()
        return result

    def insert_kondisi_hydrant(self, kondisi, keterangan, hydrant_id):
        cur.execute(f"INSERT INTO kondisi_hydrant (tanggal, kondisi, keterangan, hydrant_id) VALUES (NOW(), '{kondisi}', '{keterangan}', {hydrant_id})")
        conn.commit()

    def get_kondisi_hydrant(self):
        cur.execute(f"SELECT DISTINCT (hydrant_id) FROM kondisi_hydrant WHERE MONTH(tanggal) = '{self.get_this_month()}'")
        result = cur.fetchall()
        return result

    def get_inspection_hydrant(self, tanggal):
        cur.execute(f"SELECT * FROM hydrant JOIN kondisi_hydrant ON hydrant.id_hydrant = kondisi_hydrant.hydrant_id WHERE MONTH (tanggal) = '{tanggal}' GROUP BY id_hydrant ORDER BY id_hydrant")
        result = cur.fetchall()
        return result