from datetime import date, timedelta, datetime

today = date.today()


hari = date.strftime(today, '%A')

deltaawal = today + timedelta(days=-3)
deltaakhir = today + timedelta(days=3)
print(deltaawal)
print(deltaakhir)

while deltaawal < deltaakhir:
    print(deltaawal + timedelta(days=1))
    deltaawal += timedelta(days=1)
    

jumat = '2020-10-20'

jumatx = datetime.strptime(jumat, '%Y-%m-%d').date()

tanggal = '20-10-2020'

bulan = tanggal[6:]
bulanx = '2020-10'

data = [
    {'id': 1,
    'nama': 'Alan'},
    {'id':2,
    'nama': 'Aura'},
    {'id':3,
    'nama': 'Gagi'}
]

nomor = 'nama'

def uji(nomor):
    # if nomor in data.values:
    #     print('Ada')
    # else:
    #     print('Tidak Ada')
    for d in data:
        if nomor in d.values():
            print('Ada')
        else:
            print('Tidak Ada')


nama_file = 'foto_apar.jpg.png'

result = nama_file.rsplit('.', 1)[1]

extention = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# for ext in extention:
#     print(ext)

