import mysql.connector

# Niagahoster
# conn = mysql.connector.connect(host='srv152.niagahoster.com',
#                                database='u1724208_k3',
#                                user='u1724208_k3',
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