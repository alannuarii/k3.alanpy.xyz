import mysql.connector

# Domainesia
# conn = mysql.connector.connect(host='vicenza.id.domainesia.com',
#                                database='alanwebi_k3',
#                                user='alanwebi_k3',
#                                password='So!4-uQ7D?&f')

# AWS 
conn = mysql.connector.connect(
        host = 'k3database.cjbgtbz37j5g.ap-southeast-3.rds.amazonaws.com', 
        port = 3306,
        user = 'admin', 
        password = 'admin123',
        db = 'k3database',  
        )

# Local 
# conn = mysql.connector.connect(host='localhost',
#                                database='k3',
#                                user='root',
#                                password='1sampai8')

cur = conn.cursor(dictionary=True)


# CREATE TABLE apar
# (
#     id_apar INT NOT NULL,
#     lokasi VARCHAR(30) NOT NULL,
#     merek VARCHAR(20),
#     tipe VARCHAR(10),
#     kapasitas VARCHAR(5),
#     jenis VARCHAR(15) NOT NULL,
#     masa_berlaku VARCHAR(20),
#     foto_p3k VARCHAR(100),
#     PRIMARY KEY (id_apar)
# );



# CREATE TABLE checklist_apar
# (
#     id_checklist_apar INT NOT NULL AUTO_INCREMENT,
#     tanggal DATE NOT NULL,
#     fisik BOOLEAN NOT NULL,
#     kartu_gantung BOOLEAN NOT NULL,
#     seal BOOLEAN NOT NULL,
#     pin BOOLEAN NOT NULL,
#     meter BOOLEAN NOT NULL,
#     selang_corong BOOLEAN NOT NULL,
#     keterangan TEXT,
#     apar_id INT NOT NULL,
#     PRIMARY KEY (id_checklist_apar),
#     CONSTRAINT fk_checklist_apar FOREIGN KEY (apar_id) REFERENCES apar (id_apar)
# );

# CREATE TABLE p3k
# (
#     id_p3k INT NOT NULL AUTO_INCREMENT,
#     nama_barang VARCHAR(70) NOT NULL,
#     satuan VARCHAR(10) NOT NULL,
#     saldo_kantor INT NOT NULL,
#     saldo_ccr INT NOT NULL,
#     saldo_tps INT NOT NULL,
#     saldo_pos INT NOT NULL,
#     stock INT NOT NULL,
#     kadaluarsa VARCHAR(20),
#     foto_p3k VARCHAR(100),
#     PRIMARY KEY (id_p3k)
# );

# CREATE TABLE kantor
# (
#     id_kantor INT NOT NULL AUTO_INCREMENT,
#     tanggal DATE NOT NULL,
#     masuk INT,
#     keluar INT,
#     p3k_id INT NOT NULL,
#     PRIMARY KEY (id_kantor),
#     CONSTRAINT fk_kantor_p3k FOREIGN KEY (p3k_id) REFERENCES p3k (id_p3k)
# );

# CREATE TABLE ccr
# (
#     id_ccr INT NOT NULL AUTO_INCREMENT,
#     tanggal DATE NOT NULL,
#     masuk INT,
#     keluar INT,
#     p3k_id INT NOT NULL,
#     PRIMARY KEY (id_ccr),
#     CONSTRAINT fk_ccr_p3k FOREIGN KEY (p3k_id) REFERENCES p3k (id_p3k)
# );

# CREATE TABLE tps
# (
#     id_tps INT NOT NULL AUTO_INCREMENT,
#     tanggal DATE NOT NULL,
#     masuk INT,
#     keluar INT,
#     p3k_id INT NOT NULL,
#     PRIMARY KEY (id_tps),
#     CONSTRAINT fk_tps_p3k FOREIGN KEY (p3k_id) REFERENCES p3k (id_p3k)
# );

# CREATE TABLE pos
# (
#     id_pos INT NOT NULL AUTO_INCREMENT,
#     tanggal DATE NOT NULL,
#     masuk INT,
#     keluar INT,
#     p3k_id INT NOT NULL,
#     PRIMARY KEY (id_pos),
#     CONSTRAINT fk_pos_p3k FOREIGN KEY (p3k_id) REFERENCES p3k (id_p3k)
# );

# CREATE TABLE stock
# (
#     id_stock INT NOT NULL AUTO_INCREMENT,
#     tgl_stock DATE NOT NULL,
#     masuk_stock INT,
#     keluar_stock INT,
#     p3k_id INT NOT NULL,
#     PRIMARY KEY (id_stock),
#     CONSTRAINT fk_stock_p3k FOREIGN KEY (p3k_id) REFERENCES p3k (id_p3k)
# );

# CREATE TABLE hydrant 
# (
#         id_hydrant INT NOT NULL AUTO_INCREMENT,
#         nama_peralatan VARCHAR(50) NOT NULL,
#         merek VARCHAR(20),
#         tipe VARCHAR(20),
#         jumlah INT NOT NULL,
#         satuan VARCHAR(10) NOT NULL,
#         keterangan TEXT,
#         foto_p3k VARCHAR(100),
#         PRIMARY KEY (id_hydrant)
# );

# CREATE TABLE kondisi_hydrant
# (
#         id_kondisi_hydrant INT NOT NULL AUTO_INCREMENT,
#         tanggal DATE NOT NULL,
#         kondisi VARCHAR(10) NOT NULL,
#       hydrant_id INT NOT NULL,
#       PRIMARY KEY (id_kondisi_hydrant),
#       CONSTRAINT fk_kondisi_hydrant FOREIGN KEY (hydrant_id) REFERENCES hydrant (id_hydrant)
# )

# CREATE TABLE user 
# (
#         username VARCHAR(15) NOT NULL,
#         name VARCHAR(30) NOT NULL,
#         email VARCHAR(30) NOT NULL,
#         password VARCHAR(250) NOT NULL,
#         PRIMARY KEY (username)
# );

# CREATE TABLE agenda
# (
#         id_agenda INT NOT NULL AUTO_INCREMENT,
#         tanggal DATE NOT NULL,
#         waktu TIME NOT NULL,
#         agenda_rapat VARCHAR(100) NOT NULL,
#         lokasi VARCHAR(30) NOT NULL,
#         link VARCHAR(50)
#         PRIMARY KEY (id_agenda)
# )

# CREATE TABLE absen
# (
#         id_absen INT NOT NULL AUTO_INCREMENT,
#         nama VARCHAR(30) NOT NULL,
#         instansi VARCHAR(50),
#         jabatan VARCHAR(30),
#         email VARCHAR(25),
#         hp VARCHAR(15),
#         ttd VARCHAR(50) NOT NULL,
#         checkin TIMESTAMP NOT NULL,
#         agenda_id INT NOT NULL,
#         PRIMARY KEY (id_absen),
#         CONSTRAINT fk_absen_agenda FOREIGN KEY (agenda_id) REFERENCES agenda (id_agenda)
# )

# CREATE TABLE signature
# (
#         id_sign INT NOT NULL AUTO_INCREMENT,
#         role VARCHAR(15) NOT NULL,
#         path VARCHAR(50) NOT NULL,
#         ttd VARCHAR(50) NOT NULL,
#         PRIMARY KEY (id_sign)
# )

# CREATE TABLE unit
# (
#         id_unit INT NOT NULL,
#         merek VARCHAR(10) NOT NULL,
#         tipe VARCHAR(20),
#         serial_number VARCHAR(10),
#         tahun_operasi VARCHAR(4),
#         PRIMARY KEY (id_unit)
# )

# CREATE TABLE pengusahaan
# (
#         id_pengusahaan INT NOT NULL AUTO_INCREMENT,
#         periode DATE NOT NULL,
#         dtp INT NOT NULL,
#         dmn INT NOT NULL,
#         produksi FLOAT NOT NULL,
#         ps_sentral FLOAT NOT NULL,
#         ps_trafo FLOAT NOT NULL,
#         bbm FLOAT NOT NULL,
#         po FLOAT NOT NULL,
#         mo FLOAT NOT NULL,
#         fo FLOAT NOT NULL,
#         fo_omc FLOAT NOT NULL,
#         sh FLOAT NOT NULL,
#         ph INT NOT NULL,
#         epdh FLOAT NOT NULL,
#         eudh FLOAT NOT NULL,
#         esdh FLOAT NOT NULL,
#         efdhrs FLOAT NOT NULL,
#         trip_int INT NOT NULL,
#         trip_eks INT NOT NULL,
#         mesin_id INT NOT NULL,
#         PRIMARY KEY (id_pengusahaan),
#         CONSTRAINT fk_pengusahaan_mesin FOREIGN KEY (mesin_id) REFERENCES unit (id_unit)
# )

# CREATE TABLE target
# (
#         id_target INT NOT NULL AUTO_INCREMENT,
#         kpi VARCHAR(10) NOT NULL,
#         nilai_target FLOAT NOT NULL,
#         satuan VARCHAR(10),
#         tahun VARCHAR(4) NOT NULL,
#         PRIMARY KEY (id_target)
# )