from flask import Flask, flash, jsonify
from flask import render_template
from flask import request, redirect, url_for, session
from mysql import connector
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'many random bytes'

#open conection
db = connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '',
    database = 'my_laundry'
)

if db.is_connected():
    print('conection successfull')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # level = request.form['password']
        cursor = db.cursor()
        cursor.execute(
                'SELECT level FROM login WHERE username = %s AND password = %s',
                    (username, password, ))
        user = cursor.fetchone()
        if user[0] == 'karyawan':
            session['loggedin'] = True
            message = 'Logged in successfully !'
            return redirect('/dashboard_kasir/')
        elif user[0] == 'manajer':
            session['loggedin'] = True
            message = 'Logged in successfully !'
            return redirect('/dashboard_manajer/')
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html',message=message)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        # Jika pengguna tidak terotentikasi, alihkan ke halaman login
        return redirect('/login')
    else:
        # Tampilkan halaman utama jika pengguna terotentikasi
        return redirect('/dashboard_kasir')

# Route Dashboard Kasir
@app.route('/dashboard_kasir/')
def dash_kasir():
    cursor = db.cursor()
    cursor.execute(
        "select count(id_pelanggan) from pelanggan;"
    )
    jml_pelanggan = str(cursor.fetchall()[0][0])
    cursor.execute(
        "select count(id_nota) from transaksi")
    jml_pesanan = str(cursor.fetchall()[0][0])
    cursor.execute("select count(id_nota) from  transaksi where status = 'PROSES' OR status = 'DITERIMA'")
    belum_selesai = str(cursor.fetchall()[0][0])
    cursor.close()
    return render_template('kasir/dash_kasir.html', jml_pelanggan = jml_pelanggan, 
                           jml_pesanan = jml_pesanan, belum_selesai=belum_selesai)



# Jumlah Pelanggan
@app.route('/jumlahPelanggan/')
def jumlah_pelanggan():
    cursor = db.cursor()
    cursor.execute(
        '''
        select count(id_pelanggan) from pelanggan;
        '''
    )
    jml_pelanggan = str(cursor.fetchall()[0][0])
    cursor.close()
    # return jsonify(jml_pelanggan)
    return redirect('/base_kasir/', jml_pelanggan )

@app.route('/tambah_pesanan/')
def tambah_pesanan():
    return render_template('kasir/tambah_pesanan.html')

@app.route('/pelanggan/')
def pelanggan():
    q = request.args.get('q','')
    # return param
    cursor = db.cursor()
    cursor.execute(
        "select id_pelanggan,nama from pelanggan where nama like %s",  ("%{}%".format(q),)
        )
    result = cursor.fetchall()

    cursor.close()
    pelanggan = [{'id': user[0], 'text': user[1]} for user in result]
    return jsonify(pelanggan)

@app.route('/karyawan/')
def karyawan():
    q = request.args.get('q','')
    cursor = db.cursor()
    cursor.execute(
        "SELECT id_karyawan,nama from karyawan where nama like %s", ("%{}%".format(q),)
        )
    result = cursor.fetchall()
    cursor.close()
    # return result
    karyawan = [{'id': user[0], 'text': user[1]} for user in result]
    return jsonify(karyawan)

@app.route('/harga/')
def harga():
    cursor = db.cursor()
    cursor.execute('SELECT * from jenis_paket')
    result = cursor.fetchall()
    expres = (jsonify(str(result[0][1])))
    return expres

@app.route('/transaksi/', methods = ['POST'])
def transaksi():
    id_pelanggan = request.form['id_pelanggan']
    jenis_laundry = request.form['jenis_laundry']
    berat = request.form['berat']
    tanggal_masuk = request.form['tanggal_masuk']
    nama_karyawan = request.form['nama_karyawan']
    status_pembayaran = request.form['status_pembayaran']
    status_pesanan = 'DITERIMA'
    suffix = jenis_laundry[0] + datetime.today().strftime('%d%m%y')
    cur = db.cursor()
    cur.execute('''
                SELECT IFNULL(LEFT(MAX(id_nota),3),0) as last_nota 
                FROM 
                transaksi 
                WHERE 
                RIGHT(
                id_nota,7) = %s;
                ''', [suffix,])
    last_nota = cur.fetchone()[0]

    new_order = "00" + str(int(last_nota) + 1)
    new_nota = new_order[-3 : ] + suffix
    cur.execute('''INSERT INTO transaksi
                (id_nota,id_pelanggan,jenis_laundry,
                berat,tanggal_masuk,id_karyawan,
                status_pembayaran,status) 
                values (%s,%s,%s,%s,%s,%s,%s,%s)''', 
                (new_nota,id_pelanggan,jenis_laundry,
                 berat,tanggal_masuk,nama_karyawan,
                 status_pembayaran,status_pesanan))
    db.commit()
    return redirect('/nota_transaksi/' + new_nota)

@app.route('/no_nota/')
def no_nota():
    suffix = datetime.today().strftime('%d%m%y')
    cur = db.cursor()
    cur.execute('''
    SELECT 
        IFNULL(
            LEFT(
            MAX(id_nota),
            3
            ), 
            0
        ) as last_nota 
    FROM 
        transaksi 
    WHERE 
        RIGHT(
            id_nota, 
            7
        ) = %s;
    ''', [suffix,])
    last_nota = cur.fetchone()[0]

    new_order = "00" + str(int(last_nota) + 1)
    new_nota = new_order[-3 : ] + suffix
    db.commit()
    return  jsonify( new_nota)


    
    

#Route Tambah Pelanggan
@app.route('/tambah_pelanggan/')
def tambah_pelanggan():
    return render_template('kasir/tambah_pelanggan.html')

@app.route('/proses_tambah/', methods = ['POST'])
def proses_tambah_pelanggan():
    # id_pelanggan = request.form['id_pelanggan']
    nama = request.form['nama']
    alamat = request.form['alamat']
    kontak = request.form['kontak']
    cur = db.cursor()
    cur.execute('INSERT INTO pelanggan (nama, alamat,kontak) VALUES (%s,%s,%s)',
    (nama, alamat, kontak ))
    db.commit()
    return redirect('/tambah_pelanggan/')

#Route Data Pelanggan
@app.route('/data_pelanggan/')
def data_pelanggan():
    cursor = db.cursor()
    cursor.execute('''SELECT LPAD(id_pelanggan, 4, '0') AS id_pelanggan_zerofill,
                   nama, kontak, alamat FROM pelanggan''')
    result = cursor.fetchall()
    cursor = db.cursor()
    cursor.close()
    return render_template('kasir/data_pelanggan.html', dt_pelanggan = result,)

#Route Ubah Data Pelanggan
#Route untuk ke halaman ubah data pesanan
@app.route('/ubah_pelanggan/<id_pelanggan>')
def ubah_data_pelanggan(id_pelanggan):
    cur = db.cursor()
    cur.execute('SELECT * FROM pelanggan where id_pelanggan=%s', (id_pelanggan,))
    res = cur.fetchall()
    cur.close()
    return render_template ('kasir/ubah_data_pelanggan.html', data = res)

#Route proses ubah
@app.route('/proses_ubah_pelanggan/', methods=['POST'])
def proses_ubah_pelanggan():
    id_pelanggan = request.form['id_pelanggan']
    nama = request.form['nama']
    kontak = request.form['kontak']
    alamat = request.form['alamat']
    cur = db.cursor()
    sql = "UPDATE pelanggan SET nama=%s, kontak=%s, alamat=%s WHERE id_pelanggan=%s"
    value = (nama, kontak, alamat, id_pelanggan)
    cur.execute(sql,value)
    db.commit()
    return redirect(url_for('data_pelanggan'))

#Route untuk menghapus data pelanggan
@app.route('/hapus/<id_pelanggan>', methods=['GET'])
def hapus_data(id_pelanggan):
    cur = db.cursor()
    cur.execute('DELETE from pelanggan where id_pelanggan=%s', (id_pelanggan,))
    db.commit()
    return redirect(url_for('data_pelanggan'))

#Route Riwayat Pesanan
#Ambil data transaksi
@app.route('/riwayat_pesanan/')
def riwayat_pesanan():
    cursor = db.cursor()
    cursor.execute('''SELECT transaksi.id_nota, pelanggan.nama,
                   transaksi.jenis_laundry,
                   transaksi.berat,transaksi.tanggal_masuk,
                   (transaksi.berat * jenis_paket.harga), karyawan.nama
                   FROM transaksi
                   INNER JOIN
                   pelanggan
                   ON transaksi.id_pelanggan = pelanggan.id_pelanggan
                   INNER JOIN
                   karyawan
                   ON transaksi.id_karyawan = karyawan.id_karyawan
                   INNER JOIN
                   jenis_paket
                   ON transaksi.jenis_laundry = jenis_paket.jenis_laundry
                   ORDER BY transaksi.id_nota asc;''')
    result = cursor.fetchall()
    cursor.close()
    return render_template('kasir/riwayat_pesanan.html', transaksi = result)

#Route Status Pesanan
#Ambil Data Status
@app.route('/status_pesanan/')
def status_pesanan():
    cursor = db.cursor()
    cursor.execute('''
                   SELECT transaksi.id_nota,
                   pelanggan.nama,
                   transaksi.status,
                   transaksi.status_pembayaran,
                   transaksi.tanggal_keluar
                   FROM transaksi 
                   INNER JOIN
                   pelanggan
                   on transaksi.id_pelanggan = pelanggan.id_pelanggan;''')
    result = cursor.fetchall()
    cursor.close()
    return render_template('kasir/status_pesanan.html', status = result)

#Ubah Status Pemesanan

#Route ke Halaman Ubah Status
@app.route('/ubah_status/<id_nota>')
def ubah_status(id_nota):
    cur = db.cursor()
    cur.execute('''
    select transaksi.id_nota, pelanggan.nama, transaksi.status, transaksi.status_pembayaran, transaksi.tanggal_keluar
    from transaksi 
    inner join
    pelanggan
    on transaksi.id_pelanggan = pelanggan.id_pelanggan
    where id_nota=%s;
    ''', (id_nota,))
    res = cur.fetchall()
    cur.close()
    return render_template('kasir/ubah_status.html', status = res)

#Proses ubah status pesanan
@app.route('/proses_ubah_status/', methods=['POST'])
def proses_ubah_status():
    id_nota = request.form['id_nota']
    status= request.form['status_pesanan']
    status_pembayaran = request.form['status_pembayaran']
    tanggal_keluar = request.form['tanggal_keluar']
    cur = db.cursor()
    sql = "update transaksi set status=%s, status_pembayaran=%s, tanggal_keluar=%s where id_nota=%s"
    value = (status, status_pembayaran, tanggal_keluar, id_nota)
    cur.execute(sql,value)
    db.commit()
    return redirect(url_for('status_pesanan'))

#Halaman Nota
@app.route('/nota_transaksi/<id_nota>')
def nota(id_nota):
    cursor = db.cursor()
    cursor.execute("""select transaksi.id_nota,
    pelanggan.nama, transaksi.jenis_laundry, transaksi.berat, transaksi.tanggal_masuk, (transaksi.berat * jenis_paket.harga) , transaksi.status_pembayaran
    from transaksi
    inner join
    pelanggan
    on transaksi.id_pelanggan = pelanggan.id_pelanggan
    inner join
    jenis_paket
    on transaksi.jenis_laundry = jenis_paket.jenis_laundry
    where id_nota = %s;
    """, [id_nota,])
    result = cursor.fetchone()
    cursor.close()
    print(result)
    return render_template('kasir/nota.html', hasil = result)
    
#Halaman Informasi Harga
@app.route('/informasi_harga/')
def info_harga():
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM jenis_paket"
    )
    res = cur.fetchall()
    cur.close()
    return render_template('kasir/info_paket.html', paket = res)


#Dashboard Menejer
#Route Dashboard Manajer
@app.route('/dashboard_manajer/')
def dash_manajer():
    cursor = db.cursor()
    cursor.execute("select count(id_nota) from transaksi")
    result = cursor.fetchall()[0][0]
    cursor.execute("select count(id_pelanggan) from pelanggan")
    jml_pelanggan = cursor.fetchall()[0][0]
    cursor.execute("select count(id_karyawan) from karyawan")
    jml_karyawan = cursor.fetchall()[0][0]
    cursor.close()
    return render_template('manajer/dash_manajer.html', jml_pesanan = result, jml_pelanggan= jml_pelanggan, jml_karyawan = jml_karyawan)


#Route data karyawan
@app.route('/data_karyawan/')
def data_karyawan():
    cursor = db.cursor()
    cursor.execute('''select karyawan.id_karyawan,karyawan.kode_karyawan, karyawan.nama, karyawan.kontak, karyawan.alamat, karyawan.jam_kerja,
                   (karyawan.jam_kerja * posisi.gaji_pokok) as 'gaji'
                   from karyawan, posisi
                   WHERE karyawan.kode_karyawan = posisi.kode_karyawan''')
    result = cursor.fetchall()
    cursor.close()
    return render_template('manajer/data_karyawan.html', dt_karyawan = result)

#Gaji Pokok
@app.route('/gaji_pokok/')
def gaji_pokok():
    cursor = db.cursor()
    cursor.execute('''
    select * from posisi;
    ''')
    result = cursor.fetchall()
    cursor.close()
    # return result
    return render_template('manajer/gaji_pokok.html', gaji = result)

@app.route('/tambah_posisi/', methods = ['POST'])
def tambah_posisi():
        flash("Data Inserted Successfully")
        kode_karyawan = request.form['kode_karyawan']
        jobdesk = request.form['jobdesk']
        gaji_pokok = request.form['gaji_pokok']
        cur = db.cursor()
        cur.execute ('INSERT INTO posisi (kode_karyawan, jobdesk, gaji_pokok) VALUES (%s,%s,%s)', 
        (kode_karyawan,jobdesk,gaji_pokok))
        db.commit()
        return redirect(url_for('gaji_pokok'))

@app.route('/update_gaji/', methods= ['GET','POST'])
def update_gaji():
     kode_karyawan = request.form['kode_karyawan']
     posisi = request.form['jobdesk']
     gaji_pokok = request.form['gaji_pokok']
     cursor = db.cursor()
     sql = '''
        UPDATE posisi
        SET kode_karyawan = %s,
            jobdesk = %s,
            gaji_pokok = %s
        WHERE kode_karyawan = %s
        '''
     value = (kode_karyawan, posisi, gaji_pokok, kode_karyawan)
     cursor.execute(sql,value)
     db.commit()
     return redirect(url_for('gaji_pokok'))

@app.route('/hapus_gaji/<kode_karyawan>', methods = ['GET'])
def hapus_gaji(kode_karyawan):
    flash("Record Has Been Deleted Successfully")
    cur = db.cursor()
    cur.execute("DELETE FROM posisi WHERE kode_karyawan=%s", (kode_karyawan,))
    db.commit()
    return redirect(url_for('gaji_pokok '))  

#Route Riwayat Pesanan
#Ambil data transaksi
@app.route('/M.riwayat_pesan/')
def data_Mriwayat_pesanan():
    cursor = db.cursor()
    cursor.execute('''
    select transaksi.id_nota, pelanggan.nama, transaksi.jenis_laundry,
    transaksi.berat,transaksi.tanggal_keluar,
    (transaksi.berat * jenis_paket.harga), karyawan.nama, transaksi.status
    from transaksi
    inner join
    pelanggan
    on transaksi.id_pelanggan = pelanggan.id_pelanggan
    inner join
    karyawan
    on transaksi.id_karyawan = karyawan.id_karyawan
    inner join
    jenis_paket
    on transaksi.jenis_laundry = jenis_paket.jenis_laundry
    ORDER BY transaksi.id_nota asc;''')
    result = cursor.fetchall()
    cursor.close()
    return render_template('manajer/M.riwayat_pesan.html', transaksi = result)

#Route data pelanggan
@app.route('/M.data_pelanggan/')
def Mdata_pelanggan():
    cursor = db.cursor()
    cursor.execute("select LPAD(id_pelanggan, 4, '0') AS id_pelanggan_zerofill, nama, kontak, alamat from pelanggan")
    result = cursor.fetchall()
    cursor.close()
    return render_template('manajer/M.data_pelanggan.html', dt_pelanggan = result)


@app.route('/tambah_karyawan/', methods = ['POST'])
def tambah_karyawan():
        flash("Data Inserted Successfully")
        id_karyawan = request.form['id_karyawan']
        kode_karyawan = request.form['kode_karyawan']
        nama = request.form['nama']
        kontak = request.form['kontak']
        alamat = request.form['alamat']
        jam_kerja = request.form['jam_kerja']
        # if kode_karyawan == 'A':
        #     gaji = int(jam_kerja)*20000
        # elif kode_karyawan == 'B':  
        #     gaji = int(jam_kerja)*30000
        # elif kode_karyawan == 'C':
        #     gaji = int(jam_kerja)*10000
        cur = db.cursor()
        cur.execute ('INSERT INTO karyawan (id_karyawan, kode_karyawan, nama, kontak, alamat, jam_kerja) VALUES (%s, %s, %s, %s, %s, %s)', 
        (id_karyawan, kode_karyawan, nama, kontak, alamat, jam_kerja))
        db.commit()
        return redirect(url_for('data_karyawan'))

@app.route('/hapus_karyawan/<id_karyawan>', methods = ['GET'])
def hapus_karyawan(id_karyawan):
    flash("Record Has Been Deleted Successfully")
    cur = db.cursor()
    cur.execute("DELETE FROM karyawan WHERE id_karyawan=%s", (id_karyawan,))
    db.commit()
    return redirect(url_for('data_karyawan'))

@app.route('/update_karyawan/', methods= ['GET','POST'])
def update_karyawan():
        id_karyawan = request.form['id_karyawan']
        kode_karyawan = request.form['kode_karyawan']
        nama = request.form['nama']
        kontak = request.form['kontak']
        alamat = request.form['alamat']
        jam_kerja = request.form['jam_kerja']
        # if kode_karyawan == 'A':
        #     gaji = int(jam_kerja)*20000
        # elif kode_karyawan == 'B':  
        #     gaji = int(jam_kerja)*30000
        # elif kode_karyawan == 'C':
        #     gaji = int(jam_kerja)*10000
        cursor = db.cursor()
        sql = '''UPDATE karyawan 
        SET
        kode_karyawan=%s, 
        nama=%s, 
        kontak=%s, 
        alamat=%s, 
        jam_kerja=%s
        WHERE id_karyawan=%s;'''
        value = (kode_karyawan, nama, kontak, alamat, jam_kerja, id_karyawan )
        cursor.execute(sql,value,)
        db.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('data_karyawan'))

# Route Data Paket
@app.route('/kelola_paket/')
def kelola_paket():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM jenis_paket")
    result = cursor.fetchall()
    cursor.close()
    return render_template('manajer/kelola_paket.html', paket = result)

@app.route('/update_paket/', methods= ['GET','POST'])
def update_paket():
        nama_paket = request.form['nama_paket']
        harga = request.form['harga']
        cur = db.cursor()
        sql = '''UPDATE jenis_paket
        SET jenis_laundry=%s, harga=%s
        where jenis_laundry=%s '''
        value = (nama_paket,harga,nama_paket)
        cur.execute(sql,value)
        db.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('kelola_paket'))

@app.route('/tambah_paket/', methods = ['POST'])
def tambah_paket():
        flash("Data Inserted Successfully")
        nama_paket = request.form['nama_paket']
        harga = request.form['harga']
        cur = db.cursor()
        cur.execute ('INSERT INTO jenis_paket (jenis_laundry, harga) VALUES (%s,%s)', 
        (nama_paket, harga))
        db.commit()
        return redirect(url_for('kelola_paket'))

@app.route('/hapus_paket/<nama_paket>', methods = ['GET'])
def hapus_paket(nama_paket):
    flash("Record Has Been Deleted Successfully")
    cur = db.cursor()
    cur.execute("DELETE FROM jenis_paket WHERE jenis_laundry=%s", (nama_paket,))
    db.commit()
    return redirect(url_for('kelola_paket'))



#Route data User
@app.route('/kelola_user/')
def kelola_user():
    cursor = db.cursor()
    cursor.execute('select * from login')
    result = cursor.fetchall()
    cursor.close()
    return render_template('manajer/kelola_user.html', dt_admin = result)


@app.route('/tambah_user/', methods = ['POST'])
def tambah_user():
        flash("Data Inserted Successfully")
        username = request.form['username']
        password = request.form['password']
        level = request.form['level']
        cur = db.cursor()
        cur.execute ('INSERT INTO login (username, password,level) VALUES (%s, %s,%s)', 
        (username, password,level))
        db.commit()
        return redirect(url_for('kelola_user'))

@app.route('/hapus_user/<username>', methods = ['GET'])
def hapus_user(username):
    flash("Record Has Been Deleted Successfully")
    cur = db.cursor()
    cur.execute("DELETE FROM login WHERE username=%s", (username,))
    db.commit()
    return redirect(url_for('kelola_user'))

@app.route('/update_user/', methods= ['GET','POST'])
def update_user():
        username = request.form['username']
        password = request.form['password']
        level = request.form['level']
        cur = db.cursor()
        sql = '''UPDATE login
        SET password=%s, level=%s
        where username=%s '''
        value = (password, level, username)
        cur.execute(sql,value)
        db.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('kelola_user'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()