from app.conn import cur, conn
from app.k3 import K3
from datetime import date
import base64
from PIL import Image
from io import BytesIO


class Absen(K3):
    def get_hari(self, day):
        if day == 'Monday':
            return 'Senin'
        elif day == 'Tuesday':
            return 'Selasa'
        elif day == 'Wednesday':
            return 'Rabu'
        elif day == 'Thursday':
            return 'Kamis'
        elif day == 'Friday':
            return 'Jumat'
        elif day == 'Saturday':
            return 'Sabtu'
        elif day == 'Sunday':
            return 'Minggu'


    def get_date_format(self, tanggal:date):
        hari = tanggal.strftime('%A')
        tanggal_format = f"{self.get_hari(hari)}, {self.get_tanggal_format(tanggal)}"
        return tanggal_format

    def insert_agenda(self, agenda_rapat, tanggal, waktu, lokasi, link):
        cur.execute(f"INSERT INTO agenda (agenda_rapat, tanggal, waktu, lokasi, link) VALUES ('{agenda_rapat}', '{tanggal}', '{waktu}', '{lokasi}', '{link}')")
        conn.commit()

    def insert_absen(self, nama, instansi, jabatan, email, hp, agenda_id, ttd):
        cur.execute(f"INSERT INTO absen (nama, instansi, jabatan, email, hp, agenda_id, checkin, ttd) VALUES ('{nama}', '{instansi}', '{jabatan}', '{email}', '{hp}', {agenda_id}, NOW(), '{ttd}')")
        conn.commit()

    def get_agenda(self):
        cur.execute(f"SELECT *, COUNT(nama) nama_count FROM agenda LEFT JOIN absen ON agenda.id_agenda = absen.agenda_id GROUP BY agenda_rapat ORDER BY tanggal")
        result = cur.fetchall()
        return result

    def get_agenda_id(self, id):
        cur.execute(f"SELECT * FROM agenda WHERE id_agenda = {id}")
        result = cur.fetchone()
        return result

    def get_absen_id(self, id):
        cur.execute(f"SELECT * FROM absen JOIN agenda ON absen.agenda_id = agenda.id_agenda WHERE agenda_id = {id} ORDER BY id_absen")
        result = cur.fetchall()
        return result

    def base64tojpg(self, pic:str):
        new_ttd = pic.replace('data:image/png;base64,', '')
        bytes_decoded = base64.b64decode(new_ttd)
        img = Image.open(BytesIO(bytes_decoded))
        return img

