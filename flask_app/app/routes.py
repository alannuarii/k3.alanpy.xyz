import os
from app import app
from flask import render_template, request, redirect, session, url_for
from app.k3 import K3
from app.user import User
from app.utils import Absen
from app.kinerja import Kinerja
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from werkzeug.utils import secure_filename


@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''

    session.clear()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        object_user = User()
        user = object_user.get_user(username)

        if user == None:
            msg = 'Username Incorrect'
        else:
            if username == user['username'] and not object_user.check_password(user['password'], password):
                msg = 'Password Incorrect'
            elif object_user.check_password(user['password'], password) and username == user['username']:
                session['loggedin'] = True
                session['username'] = user['username']
                session['email'] = user['email']
                session['name'] = user['name']
                return redirect(url_for('home'))
    
    return render_template('pages/auth/login.html', title='Login', msg=msg)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/register', methods=['GET','POST'])
def register():
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        object_user = User()
        password_hash = object_user.set_password(password)

        object_user.register(name=name, email=email, username=username, password=password_hash)

        return redirect(url_for('login')) 

    return render_template('pages/auth/register.html', title='Register')


@app.route('/')
def home():
    
    return render_template('pages/home/home.html', title='K3 App')


@app.route('/apar/data', methods=['GET','POST'])
def data_apar():
    object_apar = K3()
    apars = object_apar.get_apar()

    for apar in apars:
        apar['masa_berlaku'] = f"{object_apar.format_bulan(apar['masa_berlaku'])} {apar['masa_berlaku'][:-3]}"

    if 'add' in request.form and 'loggedin' in session:
        try:
            id_apar = int(request.form['id_apar'])
            lokasi = request.form['lokasi']
            merek = request.form['merek']
            tipe = request.form['tipe']
            kapasitas = request.form['kapasitas']
            jenis = request.form['jenis']
            masa_berlaku = request.form['masa_berlaku']
            foto_apar = request.files['foto_apar']

            for apar in apars:
                if id_apar == apar['id_apar']:
                    return redirect(url_for('data_apar'))

            if foto_apar:
                extension_foto = foto_apar.filename.rsplit('.',1)[1]
                if extension_foto not in app.config['ALLOWED_EXTENSIONS']:
                    return redirect(url_for('data_apar'))

                filename = secure_filename(foto_apar.filename)
                renamefile = f"id_apar={id_apar}-{filename}"
                foto_apar.save(os.path.join(app.config['FOTO_APAR'], renamefile))
            else:
                renamefile = ''

            object_apar.insert_apar(id_apar=id_apar, lokasi=lokasi, merek=merek, tipe=tipe, kapasitas=kapasitas, jenis=jenis, masa_berlaku=masa_berlaku, foto_apar=renamefile)
            
            return redirect(url_for('data_apar'))

        except Exception as error:
            print(error)

    if 'edit' in request.form and 'loggedin' in session:

        current_id = int(request.form['current_id'])
        id_apar = int(request.form['id_apar'])
        lokasi = request.form['lokasi']
        merek = request.form['merek']
        tipe = request.form['tipe']
        kapasitas = request.form['kapasitas']
        jenis = request.form['jenis']
        masa_berlaku = request.form['masa_berlaku']
        foto_apar = request.files['foto_apar']
        current_foto = request.form['current_foto']

        if foto_apar:
            extension_foto = foto_apar.filename.rsplit('.',1)[1]
            if extension_foto not in app.config['ALLOWED_EXTENSIONS']:
                return redirect(url_for('data_apar'))
            
            if current_foto != '' or None:
                foto = object_apar.get_foto_apar(current_id)
                os.remove(os.path.join(app.config['FOTO_APAR'], foto[0]['foto_apar']))
                
            filename = secure_filename(foto_apar.filename)
            renamefile = f"id_apar={id_apar}-{filename}"
            foto_apar.save(os.path.join(app.config['FOTO_APAR'], renamefile))
        else:
            renamefile = current_foto

        for apar in apars:
            if id_apar == apar['id_apar'] and id_apar != current_id:
                return redirect(url_for('data_apar'))

        object_apar.update_apar(id_apar=id_apar, lokasi=lokasi, merek=merek, tipe=tipe, kapasitas=kapasitas, jenis=jenis, masa_berlaku=masa_berlaku, foto_apar=renamefile, current_id=current_id)
            
        return redirect(url_for('data_apar'))

    return render_template('pages/apar/data-apar.html', title='Data APAR', apars=apars)


@app.route('/apar/data/<id_apar>')
def delete_apar(id_apar):

    object_apar = K3()
    foto = object_apar.get_foto_apar(id_apar)
    if 'loggedin' in session:
        if foto[0]['foto_apar'] != '' or None:
            os.remove(os.path.join(app.config['FOTO_APAR'], foto[0]['foto_apar']))
        object_apar.delete_apar(id_apar)

    return redirect(url_for('data_apar'))


@app.route('/apar/checklist', methods=['GET','POST'])
def checklist_apar():
    object_apar = K3()
    all_apar = object_apar.get_apar()
    date_range = object_apar.get_friday(date.today())
    check_apar = object_apar.get_checklist_apar(date_range[0], date_range[1])
    apars = object_apar.get_apar_inspection(date_range[0], date_range[1])
    
    for apar in apars:
        if apar['fisik']:
            apar['fisik'] = 'checked'
        else:
            apar['fisik'] = '' 
        if apar['kartu_gantung']:
            apar['kartu_gantung'] = 'checked'
        else:
            apar['kartu_gantung'] = '' 
        if apar['seal']:
            apar['seal'] = 'checked'
        else:
            apar['seal'] = '' 
        if apar['pin']:
            apar['pin'] = 'checked'
        else:
            apar['pin'] = '' 
        if apar['meter']:
            apar['meter'] = 'checked'
        else:
            apar['meter'] = '' 
        if apar['selang_corong']:
            apar['selang_corong'] = 'checked'
        else:
            apar['selang_corong'] = '' 

    if 'kirim' in request.form and 'loggedin' in session:
        try:
            if 'fisik' in request.form:
                fisik = request.form['fisik']
            else:
                fisik = 0
            if 'kartu_gantung' in request.form:
                kartu_gantung = request.form['kartu_gantung']
            else:
                kartu_gantung = 0
            if 'seal' in request.form:
                seal = request.form['seal']
            else:
                seal = 0
            if 'pin' in request.form:
                pin = request.form['pin']
            else:
                pin = 0
            if 'meter' in request.form:
                meter = request.form['meter']
            else:
                meter = 0
            if 'selang_corong' in request.form:
                selang_corong = request.form['selang_corong']
            else:
                selang_corong = 0
            keterangan = request.form['keterangan']
            apar_id = int(request.form['apar_id'])

            object_apar.insert_checklist_apar(fisik=fisik, kartu_gantung=kartu_gantung, seal=seal, pin=pin, meter=meter, selang_corong=selang_corong, keterangan=keterangan, apar_id=apar_id)

            return redirect(url_for('checklist_apar'))

        except Exception as error:
            print(error)
    
    if 'update' in request.form and 'loggedin' in session:
        try:
            if 'fisik' in request.form:
                fisik = request.form['fisik']
            else:
                fisik = 0
            if 'kartu_gantung' in request.form:
                kartu_gantung = request.form['kartu_gantung']
            else:
                kartu_gantung = 0
            if 'seal' in request.form:
                seal = request.form['seal']
            else:
                seal = 0
            if 'pin' in request.form:
                pin = request.form['pin']
            else:
                pin = 0
            if 'meter' in request.form:
                meter = request.form['meter']
            else:
                meter = 0
            if 'selang_corong' in request.form:
                selang_corong = request.form['selang_corong']
            else:
                selang_corong = 0
            keterangan = request.form['keterangan']
            id_checklist_apar = int(request.form['id_checklist_apar'])

            object_apar.update_checklist_apar(fisik=fisik, kartu_gantung=kartu_gantung, seal=seal, pin=pin, meter=meter, selang_corong=selang_corong, keterangan=keterangan, id_checklist_apar=id_checklist_apar)

            return redirect(url_for('checklist_apar'))

        except Exception as error:
            print(error)

    checks = []
    for check in check_apar:
        checks.append(check['apar_id'])

    return render_template('pages/apar/checklist.html', title='Checklist APAR', apars=all_apar, checks=checks)


@app.route('/apar/report')
def report_apar():
    list_periode = []
    list_date = []
    month = None

    if 'month' in request.args:
        query = request.args.get('month')

        object_apar = K3()
        get_month = object_apar.get_checklist_month(query)

        for bulan in get_month:
            date_range_id = object_apar.get_friday_format(bulan['tanggal'])
            if date_range_id not in list_periode:
                list_periode.append(date_range_id)
            
            date_friday = object_apar.get_friday(bulan['tanggal'])[1]
            if date_friday not in list_date:
                list_date.append(date_friday)
        
        month = object_apar.format_bulan(query)
    
    return render_template('pages/apar/report.html', title='Report APAR', periodes=list_periode, dates=list_date, month=month)

@app.route('/apar/report/<tanggal>', methods=['GET','POST'])
def print_report_apar(tanggal):
    object_apar = K3()
    object_sign = Absen()
    date_range = object_apar.get_friday(datetime.strptime(tanggal, '%Y-%m-%d').date())
    datas = object_apar.get_apar_inspection(date_range[0], date_range[1])

    tanggal = object_apar.get_friday_format(date_range[0])

    for data in datas:
        data['masa_berlaku'] = f"{object_apar.format_bulan(data['masa_berlaku'])} {data['masa_berlaku'][:-3]}"

    sign_manager = object_apar.get_sign_manager(request.path)
    sign_k3l = object_apar.get_sign_k3l(request.path)
    print(sign_k3l)

    if 'token' in request.form:
        if request.form['token'] == '112220':
            session['token'] = 112220

        return redirect(url_for('print_report_apar', tanggal=tanggal)) 

    if 'ttd' in request.form:
        role = request.form['role']
        path = request.form['path']
        ttd = request.form['ttd']
        foto_ttd = object_sign.base64tojpg(ttd)
        filename = f"{role}_{path.replace('/', '_')}.png"
        foto_ttd.save(os.path.join(app.config['FOTO_APAR_TTD'], filename))

        object_apar.insert_sign(role=role, path=path, ttd=filename)

        return redirect(url_for('print_report_apar', tanggal=tanggal))

    return render_template('pages/apar/print-report.html', title='Report APAR', datas=datas, tanggal=tanggal[1], bulan=tanggal[1][3:], manager=sign_manager, k3l=sign_k3l)


@app.route('/p3k/data', methods=['GET','POST'])
def data_p3k():
    object_p3k = K3()
    all_p3k = object_p3k.get_p3k()
    get_saldo_kantor = object_p3k.get_saldo_kantor()
    get_saldo_ccr = object_p3k.get_saldo_ccr()
    get_saldo_tps = object_p3k.get_saldo_tps()
    get_saldo_pos = object_p3k.get_saldo_pos()
    get_saldo_stock = object_p3k.get_saldo_stock()

    for p3k in all_p3k:
        p3k['kadaluarsa'] = f"{object_p3k.format_bulan(p3k['kadaluarsa'])} {p3k['kadaluarsa'][:-3]}"

    if 'input' in request.form and 'loggedin' in session:
        nama_barang = request.form['nama_barang']
        satuan = request.form['satuan']
        kadaluarsa = request.form['kadaluarsa']
        
        foto_p3k = request.files['foto_p3k']
        extension_foto = foto_p3k.filename.rsplit('.',1)[1]
        if extension_foto not in app.config['ALLOWED_EXTENSIONS']:
            return redirect(url_for('data_p3k'))

        filename = secure_filename(foto_p3k.filename)
        renamefile = f"{nama_barang}-{filename}"
        foto_p3k.save(os.path.join(app.config['FOTO_P3K'], renamefile))

        object_p3k.insert_p3k(nama_barang=nama_barang, satuan=satuan, kadaluarsa=kadaluarsa, foto_p3k=renamefile)

        return redirect(url_for('data_p3k'))

    if 'edit' in request.form and 'loggedin' in session:
        id_p3k = request.form['id_p3k']
        nama_barang = request.form['nama_barang']
        satuan = request.form['satuan']
        kadaluarsa = request.form['kadaluarsa']
        current_foto = request.form['current_foto']
        foto_p3k = request.files['foto_p3k']

        if foto_p3k:
            extension_foto = foto_p3k.filename.rsplit('.',1)[1]
            if extension_foto not in app.config['ALLOWED_EXTENSIONS']:
                return redirect(url_for('data_p3k'))
                    
            foto = object_p3k.get_foto_p3k(id_p3k)
            os.remove(os.path.join(app.config['FOTO_P3K'], foto[0]['foto_p3k']))
                
            filename = secure_filename(foto_p3k.filename)
            renamefile = f"{nama_barang}-{filename}"
            foto_p3k.save(os.path.join(app.config['FOTO_P3K'], renamefile))
        else:
            renamefile = current_foto

        object_p3k.update_p3k(nama_barang=nama_barang, satuan=satuan, kadaluarsa=kadaluarsa, foto_p3k=renamefile, id_p3k=id_p3k)
            
        return redirect(url_for('data_p3k'))

    if 'kantor' in request.form and 'loggedin' in session:
        p3k_id = request.form['p3k_id']
        tanggal = request.form['tanggal']
        masuk = request.form['masuk']
        keluar = request.form['keluar']

        object_p3k.insert_kantor(tgl_kantor=tanggal, masuk_kantor=masuk, keluar_kantor=keluar, p3k_id=p3k_id)

        return redirect(url_for('data_p3k'))

    if 'ccr' in request.form and 'loggedin' in session:
        p3k_id = request.form['p3k_id']
        tanggal = request.form['tanggal']
        masuk = request.form['masuk']
        keluar = request.form['keluar']

        object_p3k.insert_ccr(tgl_ccr=tanggal, masuk_ccr=masuk, keluar_ccr=keluar, p3k_id=p3k_id)

        return redirect(url_for('data_p3k'))

    if 'tps' in request.form and 'loggedin' in session:
        p3k_id = request.form['p3k_id']
        tanggal = request.form['tanggal']
        masuk = request.form['masuk']
        keluar = request.form['keluar']

        object_p3k.insert_tps(tgl_tps=tanggal, masuk_tps=masuk, keluar_tps=keluar, p3k_id=p3k_id)

        return redirect(url_for('data_p3k'))

    if 'pos' in request.form and 'loggedin' in session:
        p3k_id = request.form['p3k_id']
        tanggal = request.form['tanggal']
        masuk = request.form['masuk']
        keluar = request.form['keluar']

        object_p3k.insert_pos(tgl_pos=tanggal, masuk_pos=masuk, keluar_pos=keluar, p3k_id=p3k_id)

        return redirect(url_for('data_p3k'))

    if 'stock' in request.form and 'loggedin' in session:
        p3k_id = request.form['p3k_id']
        tanggal = request.form['tanggal']
        masuk = request.form['masuk']
        keluar = request.form['keluar']

        object_p3k.insert_stock(tgl_stock=tanggal, masuk_stock=masuk, keluar_stock=keluar, p3k_id=p3k_id)

        return redirect(url_for('data_p3k'))

    return render_template('pages/p3k/data-p3k.html', title='Mutasi P3K', all_p3k=all_p3k, pers_kantor=get_saldo_kantor, pers_ccr=get_saldo_ccr, pers_tps=get_saldo_tps, pers_pos=get_saldo_pos, pers_stock=get_saldo_stock)


@app.route('/p3k/data/<id_p3k>')
def delete_p3k(id_p3k):

    object_p3k = K3()
    foto = object_p3k.get_foto_p3k(id_p3k)
    if 'loggedin' in session:
        os.remove(os.path.join(app.config['FOTO_P3K'], foto[0]['foto_p3k']))
        object_p3k.delete_p3k(id_p3k)

    return redirect(url_for('data_p3k'))


@app.route('/p3k/report')
def report_p3k():
    month = None
    year = None
    next_month = None

    if 'month' in request.args:
        query = request.args.get('month')

        object_p3k = K3()
        tanggal = object_p3k.get_date(f"{query}-01")
        next_month = tanggal + relativedelta(months=+1) 
        
        month = object_p3k.format_bulan(query)
        year = str(tanggal)[:-6]
    
    return render_template('pages/p3k/report.html', title='Report P3K', month=month, year=year, tanggal=next_month)


@app.route('/p3k/report/<tanggal>', methods=['GET','POST'])
def print_report_p3k(tanggal):
    
    object_p3k = K3()
    object_sign = Absen()
    all_p3k = object_p3k.get_p3k()
    get_saldo_kantor = object_p3k.get_saldo_kantor_filter(tanggal)
    get_saldo_ccr = object_p3k.get_saldo_ccr_filter(tanggal)
    get_saldo_tps = object_p3k.get_saldo_tps_filter(tanggal)
    get_saldo_pos = object_p3k.get_saldo_pos_filter(tanggal)
    get_saldo_stock = object_p3k.get_saldo_stock_filter(tanggal)

    tanggal_date = object_p3k.get_date(tanggal) + relativedelta(months=-1) 
    bulan = object_p3k.format_bulan(str(tanggal_date))

    tanggal_format = object_p3k.get_tanggal_format(object_p3k.get_date(tanggal))

    for p3k in all_p3k:
        p3k['kadaluarsa'] = f"{object_p3k.format_bulan(p3k['kadaluarsa'])} {p3k['kadaluarsa'][:-3]}"

    sign_manager = object_p3k.get_sign_manager(request.path)
    sign_k3l = object_p3k.get_sign_k3l(request.path)

    if 'token' in request.form:
        if request.form['token'] == '112220':
            session['token'] = 112220

        return redirect(url_for('print_report_p3k', tanggal=tanggal)) 

    if 'ttd' in request.form:
        role = request.form['role']
        path = request.form['path']
        ttd = request.form['ttd']
        foto_ttd = object_sign.base64tojpg(ttd)
        filename = f"{role}_{path.replace('/', '_')}.png"
        foto_ttd.save(os.path.join(app.config['FOTO_P3K_TTD'], filename))

        object_p3k.insert_sign(role=role, path=path, ttd=filename)

        return redirect(url_for('print_report_p3k', tanggal=tanggal))
    
    return render_template('pages/p3k/print-report.html', title='Report P3K', all_p3k=all_p3k, pers_kantor=get_saldo_kantor, pers_ccr=get_saldo_ccr, pers_tps=get_saldo_tps, pers_pos=get_saldo_pos, pers_stock=get_saldo_stock, bulan=bulan, tanggal=tanggal_format, manager=sign_manager, k3l=sign_k3l)


@app.route('/hydrant/data', methods=['GET','POST'])
def data_hydrant():
    object_hydrant = K3()
    hydrants = object_hydrant.get_hydrant()

    if 'add' in request.form and 'loggedin' in session:
        try:
            nama_peralatan = request.form['nama_peralatan']
            merek = request.form['merek']
            tipe = request.form['tipe']
            jumlah = request.form['jumlah']
            satuan = request.form['satuan']
            foto_hydrant = request.files['foto_hydrant']

            if foto_hydrant:
                extension_foto = foto_hydrant.filename.rsplit('.',1)[1]
                if extension_foto not in app.config['ALLOWED_EXTENSIONS']:
                    return redirect(url_for('data_hydrant'))

                filename = secure_filename(foto_hydrant.filename)
                renamefile = f"{nama_peralatan}-{filename}"
                foto_hydrant.save(os.path.join(app.config['FOTO_HYDRANT'], renamefile))
            else:
                renamefile = ''

            object_hydrant.insert_hydrant(nama_peralatan=nama_peralatan, merek=merek, tipe=tipe, jumlah=jumlah, satuan=satuan, foto_hydrant=renamefile)
            
            return redirect(url_for('data_hydrant'))

        except Exception as error:
            print(error)

    if 'edit' in request.form and 'loggedin' in session:

        id_hydrant = request.form['id_hydrant']
        nama_peralatan = request.form['nama_peralatan']
        merek = request.form['merek']
        tipe = request.form['tipe']
        jumlah = request.form['jumlah']
        satuan = request.form['satuan']
        current_foto = request.form['current_foto']
        foto_hydrant = request.files['foto_hydrant']

        if foto_hydrant:
            extension_foto = foto_hydrant.filename.rsplit('.',1)[1]
            if extension_foto not in app.config['ALLOWED_EXTENSIONS']:
                return redirect(url_for('data_hydrant'))
            
            if current_foto != '' or None:
                foto = object_hydrant.get_foto_hydrant(id_hydrant)
                os.remove(os.path.join(app.config['FOTO_HYDRANT'], foto[0]['foto_hydrant']))
                
            filename = secure_filename(foto_hydrant.filename)
            renamefile = f"{nama_peralatan}-{filename}"
            foto_hydrant.save(os.path.join(app.config['FOTO_HYDRANT'], renamefile))
        else:
            renamefile = current_foto

        object_hydrant.update_hydrant(id_hydrant=id_hydrant, nama_peralatan=nama_peralatan, merek=merek, tipe=tipe, jumlah=jumlah, satuan=satuan, foto_hydrant=renamefile)
            
        return redirect(url_for('data_hydrant'))

    return render_template('pages/hydrant/data-hydrant.html', title='Data Hydrant', hydrants=hydrants)

@app.route('/hydrant/data/<id_hydrant>')
def delete_hydrant(id_hydrant):

    object_hydrant = K3()
    foto = object_hydrant.get_foto_hydrant(id_hydrant)
    if 'loggedin' in session:
        if foto[0]['foto_hydrant'] != '' or None:
            os.remove(os.path.join(app.config['FOTO_HYDRANT'], foto[0]['foto_hydrant']))
        object_hydrant.delete_hydrant(id_hydrant)

    return redirect(url_for('data_hydrant'))


@app.route('/hydrant/inspection', methods=['GET','POST'])
def inspection_hydrant():
    object_hydrant = K3()
    hydrants = object_hydrant.get_hydrant()
    check_hydrant = object_hydrant.get_kondisi_hydrant()

    if 'kirim' in request.form and 'loggedin' in session:
        kondisi = request.form['kondisi']
        keterangan = request.form['keterangan']
        hydrant_id = request.form['hydrant_id']

        object_hydrant.insert_kondisi_hydrant(kondisi=kondisi, keterangan=keterangan, hydrant_id=hydrant_id)

    checks = []
    for check in check_hydrant:
        checks.append(check['hydrant_id'])

    return render_template('pages/hydrant/inspection.html', title='Inspeksi Hydrant', hydrants=hydrants, checks=checks)


@app.route('/hydrant/report')
def report_hydrant():
    month = None
    year = None
    next_month = None

    if 'month' in request.args:
        query = request.args.get('month')

        object_hydrant = K3()
        tanggal = object_hydrant.get_date(f"{query}-01")
        next_month = tanggal + relativedelta(months=+1) 
        
        month = object_hydrant.format_bulan(query)
        year = str(tanggal)[:-6]
    
    return render_template('pages/hydrant/report.html', title='Report Hydrant', month=month, year=year, tanggal=next_month)


@app.route('/hydrant/report/<tanggal>', methods=['GET','POST'])
def print_report_hydrant(tanggal):
    
    object_hydrant = K3()
    object_sign = Absen()
    tanggal_date = object_hydrant.get_date(tanggal) + relativedelta(months=-1) 
    all_hydrant = object_hydrant.get_inspection_hydrant(str(tanggal_date)[5:-3])

    bulan = object_hydrant.format_bulan(str(tanggal_date))
    tanggal_format = object_hydrant.get_tanggal_format(object_hydrant.get_date(tanggal))

    sign_manager = object_hydrant.get_sign_manager(request.path)
    sign_k3l = object_hydrant.get_sign_k3l(request.path)

    if 'token' in request.form:
        if request.form['token'] == '112220':
            session['token'] = 112220

        return redirect(url_for('print_report_hydrant', tanggal=tanggal)) 

    if 'ttd' in request.form:
        role = request.form['role']
        path = request.form['path']
        ttd = request.form['ttd']
        foto_ttd = object_sign.base64tojpg(ttd)
        filename = f"{role}_{path.replace('/', '_')}.png"
        foto_ttd.save(os.path.join(app.config['FOTO_HYDRANT_TTD'], filename))

        object_hydrant.insert_sign(role=role, path=path, ttd=filename)

        return redirect(url_for('print_report_hydrant', tanggal=tanggal))

    return render_template('pages/hydrant/print-report.html', title='Report Hydrant', all_hydrant=all_hydrant, bulan=bulan, tanggal=tanggal_format, manager=sign_manager, k3l=sign_k3l)


@app.route('/tools/daftar-hadir/agenda/<int:page_num>', methods=['GET','POST'])
def agenda(page_num):
    
    object_absen = Absen()

    today = date.today()
    hari_ini = object_absen.get_date_format(today)

    # Pagination
    per_page = 5
    pages = object_absen.get_count_absen()[0]['pages']
    page_num = page_num
    skip = (page_num - 1) * per_page
    if pages % per_page != 0:
        last_page = (pages // per_page) + 1
    else:
        last_page = pages // per_page

    agendas = object_absen.get_agenda(skip, per_page)

    for agenda in agendas:
        agenda['tanggal'] = object_absen.get_date_format(agenda['tanggal'])
        agenda['waktu'] = str(agenda['waktu'])[:-3]

    if 'buat' in request.form:
        agenda_rapat = request.form['agenda']
        tanggal = request.form['tanggal']
        waktu = request.form['waktu']
        lokasi = request.form['lokasi']
        link = request.form['link']

        object_absen.insert_agenda(agenda_rapat=agenda_rapat, tanggal=tanggal, waktu=waktu, lokasi=lokasi, link=link)

        return redirect(url_for('agenda', page_num = 1))

    return render_template('pages/tools/daftar-hadir/agenda.html', title='Daftar Hadir', agendas=agendas, today=hari_ini, page_num=page_num, last_page=last_page)


@app.route('/tools/daftar-hadir/input/<id>', methods=['GET','POST'])
def input_daftar_hadir(id):

    object_absen = Absen()
    agenda = object_absen.get_agenda_id(id)
    agenda['tanggal'] = object_absen.get_date_format(agenda['tanggal'])
    agenda['waktu'] = str(agenda['waktu'])[:-3]
    
    if 'input' in request.form and request.form['ttd'] != '':
        nama = request.form['nama']
        instansi = request.form['instansi']
        jabatan = request.form['jabatan']
        email = request.form['email']
        hp = request.form['hp']

        ttd = request.form['ttd']
        foto_ttd = object_absen.base64tojpg(ttd)
        filename = f"{nama.replace(' ', '_')}_{datetime.now().strftime('%f')}.png"
        foto_ttd.save(os.path.join(app.config['FOTO_TTD'], filename))

        object_absen.insert_absen(nama=nama, instansi=instansi, jabatan=jabatan, email=email, hp=hp, agenda_id=id, ttd=filename)
        
        return redirect(url_for('agenda', page_num = 1))

    return render_template('pages/tools/daftar-hadir/input-daftar-hadir.html', title='Input Daftar Hadir', agenda=agenda)


@app.route('/tools/daftar-hadir/<id>', methods=['GET','POST'])
def daftar_hadir(id):

    object_absen = Absen()
    absens = object_absen.get_absen_id(id)
    for absen in absens:
        absen['tanggal'] = object_absen.get_date_format(absen['tanggal'])
        absen['waktu'] = str(absen['waktu'])[:-3]

    return render_template('pages/tools/daftar-hadir/daftar-hadir.html', title='Daftar Hadir', absens=absens)


@app.route('/tools/daftar-hadir/agenda/<id>')
def delete_agenda(id):

    object_absen = Absen()
    absen_ttd = object_absen.get_absen_ttd(id)
    if 'loggedin' in session:
        for ttd in absen_ttd:
            os.remove(os.path.join(app.config['FOTO_TTD'], ttd['ttd']))
        object_absen.delete_absen(id)
        object_absen.delete_agenda(id)

    return redirect(url_for('agenda'))


@app.route('/tools/daftar-hadir/print/<id>')
def print_absen(id):
    
    object_absen = Absen()
    absens = object_absen.get_absen_id(id)
    for absen in absens:
        absen['tanggal'] = object_absen.get_date_format(absen['tanggal'])
        absen['waktu'] = str(absen['waktu'])[:-3]
   
    return render_template('pages/tools/daftar-hadir/print-absen.html', title='Print Daftar Hadir', absens=absens)


@app.route('/tools/kinerja/')
def dashboard():

    object_kinerja = Kinerja()

    periode = '2022-10-01'

    month = datetime.strptime(periode, '%Y-%m-%d').date()
    month_1 = month - relativedelta(months=+1)

    target = object_kinerja.target_kinerja(periode[:4])
    kinerja_unit_bulanan = object_kinerja.kinerja_unit_bulanan(month)
    kinerja_unit_bulanan_prev = object_kinerja.kinerja_unit_bulanan(month_1)

    kinerja_kum = object_kinerja.list_kinerja_unit_kumulatif(periode, 'eaf')
    list_target = object_kinerja.list_target_kinerja('EAF', periode[:4], kinerja_kum)
    satuan = object_kinerja.get_satuan('EAF', periode[:4])
    kpi_ = 'EAF'

    if 'kpi' in request.args:
        kpi = request.args.get('kpi')

        kinerja_kum = object_kinerja.list_kinerja_unit_kumulatif(periode, kpi)
        for i in range(len(kinerja_kum)):
            if kinerja_kum[i] is None:
                kinerja_kum[i] = 0.0

        list_target = object_kinerja.list_target_kinerja(kpi.upper(), periode[:4], kinerja_kum)
        satuan = object_kinerja.get_satuan(kpi.upper(), periode[:4])
        kpi_ = kpi.upper()

    months = []
    for i in range(len(kinerja_kum)):
        months.append(object_kinerja.months[i])

    return render_template('pages/tools/kinerja/dashboard.html', title='Dashboard Kinerja', target=target, kin_u_bul=kinerja_unit_bulanan, kin_u_bul_prev=kinerja_unit_bulanan_prev, kinerja_kum=kinerja_kum, months=months, list_target=list_target, satuan=satuan, kpi=kpi_)