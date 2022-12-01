from datetime import date, timedelta, datetime

today = date.today()


hari = date.strftime(today, '%A')

deltaawal = today + timedelta(days=-3)
deltaakhir = today + timedelta(days=3)


# while deltaawal < deltaakhir:
#     print(deltaawal + timedelta(days=1))
#     deltaawal += timedelta(days=1)
    

jumat = '2020-10-20'

jumatx = datetime.strptime(jumat, '%Y-%m-%d').date()

tanggal = '20-10-2020'

bulan = tanggal[3:-5]

data = [
    {'id': 1,
    'nama': 'Alan'},
    {'id':2,
    'nama': 'Aura'},
    {'id':3,
    'nama': 'Gagi'}
]

data2 = {'komp_a':123, 'komp_b': 456, 'komp_c': 789}

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

hari = today.strftime('%A')

kinerja = {'eaf_unit': 100.0, 'efor_unit': None, 'sof_unit': 0.0, 'sfc_unit': 0.274, 'ps_unit': 5.014}


new_dict = []
for i in data2.items():
    new_dict.append(tuple([i[0], i[1]*2]))

print(data2.items())
print(dict(new_dict))

