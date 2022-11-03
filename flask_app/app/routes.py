import os
from app import app
from flask import render_template, request, redirect
from app.k3 import K3
from datetime import date, datetime
from werkzeug.utils import secure_filename


@app.route('/')
def home():

    return render_template('pages/home/home.html', title='K3 App')


@app.route('/apar/data', methods=['GET','POST'])
def data_apar():
    object_apar = K3()
    apars = object_apar.get_apar()

    for apar in apars:
        apar['masa_berlaku'] = f"{object_apar.format_bulan(apar['masa_berlaku'])} {apar['masa_berlaku'][:-3]}"

    if 'add' in request.form:
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
                    return redirect('/')

            if foto_apar:
                extension_foto = foto_apar.filename.rsplit('.',1)[1]
                if extension_foto not in app.config['ALLOWED_EXTENSIONS']:
                    return redirect('/')

                filename = secure_filename(foto_apar.filename)
                renamefile = f"id_apar={id_apar}-{filename}"
                foto_apar.save(os.path.join(app.config['FOTO_APAR'], renamefile))
            else:
                renamefile = ''

            object_apar.insert_apar(id_apar=id_apar, lokasi=lokasi, merek=merek, tipe=tipe, kapasitas=kapasitas, jenis=jenis, masa_berlaku=masa_berlaku, foto_apar=renamefile)
            
            return redirect('/apar/data')

        except Exception as error:
            print(error)

    if 'edit' in request.form:

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
                return redirect('/')
            
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
                return redirect('/')

        object_apar.update_apar(id_apar=id_apar, lokasi=lokasi, merek=merek, tipe=tipe, kapasitas=kapasitas, jenis=jenis, masa_berlaku=masa_berlaku, foto_apar=renamefile, current_id=current_id)
            
        return redirect('/apar/data')


    return render_template('pages/apar/data-apar.html', title='Data APAR', apars=apars)


@app.route('/apar/data/<id_apar>')
def delete_apar(id_apar):

    object_apar = K3()
    foto = object_apar.get_foto_apar(id_apar)
    if foto[0]['foto_apar'] != '' or None:
        os.remove(os.path.join(app.config['FOTO_APAR'], foto[0]['foto_apar']))
    object_apar.delete_apar(id_apar)

    return redirect('/apar/data')


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

    if 'kirim' in request.form:
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

            return redirect('/apar/checklist')

        except Exception as error:
            print(error)
    
    if 'update' in request.form:
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

            return redirect('/apar/checklist')

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
            
            list_date.append(object_apar.get_friday(bulan['tanggal'])[1])
        
        month = object_apar.format_bulan(query)
    
    return render_template('pages/apar/report.html', title='Report APAR', periodes=list_periode, dates=list_date, month=month)

@app.route('/apar/report/<tanggal>')
def print_report(tanggal):
    object_apar = K3()
    date_range = object_apar.get_friday(datetime.strptime(tanggal, '%Y-%m-%d').date())
    datas = object_apar.get_apar_inspection(date_range[0], date_range[1])

    tanggal = object_apar.get_friday_format(date_range[0])

    for data in datas:
        data['masa_berlaku'] = f"{object_apar.format_bulan(data['masa_berlaku'])} {data['masa_berlaku'][:-3]}"

    return render_template('pages/apar/print-report.html', title='Report APAR', datas=datas, tanggal=tanggal[1], bulan=tanggal[1][3:])


@app.route('/p3k/data', methods=['GET','POST'])
def data_p3k():
    object_p3k = K3()
    all_p3k = object_p3k.get_p3k()

    for p3k in all_p3k:
        p3k['kadaluarsa'] = f"{object_p3k.format_bulan(p3k['kadaluarsa'])} {p3k['kadaluarsa'][:-3]}"

    if 'input' in request.form:
        nama_barang = request.form['nama_barang']
        satuan = request.form['satuan']
        saldo_kantor = request.form['saldo_kantor']
        saldo_ccr = request.form['saldo_ccr']
        saldo_tps = request.form['saldo_tps']
        saldo_pos = request.form['saldo_pos']
        stock = request.form['stock']
        kadaluarsa = request.form['kadaluarsa']
        
        foto_p3k = request.files['foto_p3k']
        extension_foto = foto_p3k.filename.rsplit('.',1)[1]
        if extension_foto not in app.config['ALLOWED_EXTENSIONS']:
            return redirect('/')

        filename = secure_filename(foto_p3k.filename)
        renamefile = f"{nama_barang}-{filename}"
        foto_p3k.save(os.path.join(app.config['FOTO_P3K'], renamefile))

        object_p3k.insert_p3k(nama_barang=nama_barang, satuan=satuan, saldo_kantor=saldo_kantor, saldo_ccr=saldo_ccr, saldo_tps=saldo_tps, saldo_pos=saldo_pos, stock=stock, kadaluarsa=kadaluarsa, foto_p3k=renamefile)

        return redirect('/p3k/data')

    if 'edit' in request.form:
        id_p3k = request.form['id_p3k']
        nama_barang = request.form['nama_barang']
        satuan = request.form['satuan']
        saldo_kantor = request.form['saldo_kantor']
        saldo_ccr = request.form['saldo_ccr']
        saldo_tps = request.form['saldo_tps']
        saldo_pos = request.form['saldo_pos']
        stock = request.form['stock']
        kadaluarsa = request.form['kadaluarsa']
        current_foto = request.form['current_foto']
        foto_p3k = request.files['foto_p3k']

        if foto_p3k:
            extension_foto = foto_p3k.filename.rsplit('.',1)[1]
            if extension_foto not in app.config['ALLOWED_EXTENSIONS']:
                return redirect('/')
                    
            foto = object_p3k.get_foto_p3k(id_p3k)
            os.remove(os.path.join(app.config['FOTO_P3K'], foto[0]['foto_p3k']))
                
            filename = secure_filename(foto_p3k.filename)
            renamefile = f"{nama_barang}-{filename}"
            foto_p3k.save(os.path.join(app.config['FOTO_P3K'], renamefile))
        else:
            renamefile = current_foto

        object_p3k.update_p3k(nama_barang=nama_barang, satuan=satuan, saldo_kantor=saldo_kantor, saldo_ccr=saldo_ccr, saldo_tps=saldo_tps, saldo_pos=saldo_pos, stock=stock, kadaluarsa=kadaluarsa, foto_p3k=renamefile, id_p3k=id_p3k)
            
        return redirect('/p3k/data')

    return render_template('pages/p3k/data-p3k.html', title='Mutasi P3K', all_p3k=all_p3k)


@app.route('/p3k/data/<id_p3k>')
def delete_p3k(id_p3k):

    object_p3k = K3()
    foto = object_p3k.get_foto_p3k(id_p3k)
    os.remove(os.path.join(app.config['FOTO_P3K'], foto[0]['foto_p3k']))
    object_p3k.delete_p3k(id_p3k)

    return redirect('/p3k/data')