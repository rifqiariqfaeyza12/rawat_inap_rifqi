<<<<<<< HEAD
=======
import os
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107
from flask import Flask, render_template, request, redirect, url_for, make_response
from datetime import datetime
from fpdf import FPDF
import mysql.connector
<<<<<<< HEAD
from io import BytesIO
=======
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107

app = Flask(__name__)

# Konfigurasi Database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rawat_inap_rifqi'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

<<<<<<< HEAD
=======
# FUNGSI GENERATE ID DENGAN PREFIX & ZFILL (Lengkap & Benar)
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107
def generate_id(prefix, table, column):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
<<<<<<< HEAD
        query = f"SELECT {column} FROM {table}"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        max_num = 0
        if rows:
            for row in rows:
                id_val = str(row[0])
                numbers = re.findall(r'\d+', id_val)
                if numbers:
                    val = int(numbers[0])
                    if val > max_num:
                        max_num = val
            new_num = max_num + 1
        else:
            new_num = 1
        return f"{prefix}{str(new_num).zfill(3)}"
    except Exception as e:
        print(f"Error Generate ID: {e}")
        return f"{prefix}001"
=======
        query = f"SELECT {column} FROM {table} WHERE {column} LIKE '{prefix}%' ORDER BY {column} DESC LIMIT 1"
        cursor.execute(query)
        last_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if last_data:
            last_id = last_data[0]
            number_part = int(last_id.replace(prefix, ''))
            new_number = number_part + 1
        else:
            new_number = 1
        return f"{prefix}{new_number:06d}"
    except Exception as e:
        print(f"Error ID: {e}")
        return f"{prefi}001"

>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107

@app.route('/')
def datatransaksi():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
<<<<<<< HEAD
=======
    # Query join untuk mendapatkan detail nama pasien dan data rawat
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107
    query = """
        SELECT t.id_transaksi, t.id_pasien, r.id_rawat, p.nama, 
               t.total_biaya, t.status_pembayaran, t.tgl 
        FROM transaksi_rifqi t 
<<<<<<< HEAD
        JOIN pasien_rifqi p ON t.id_pasien = p.id_pasien 
        JOIN rawat_inap_rifqi r ON r.id_pasien = p.id_pasien
        GROUP BY t.id_transaksi
        ORDER BY t.id_transaksi DESC
=======
        INNER JOIN pasien_rifqi p ON t.id_pasien = p.id_pasien 
        INNER JOIN rawat_inap_rifqi r ON r.id_pasien = p.id_pasien
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('connection_Rifqi.html', transaksi=result)

@app.route('/data', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
<<<<<<< HEAD
        id_pasien = request.form.get('id_pasien') 
        nama_manual = request.form.get('nama_manual') 
        alamat_manual = request.form.get('alamat_manual')
        kontak_manual = request.form.get('kontak_manual')
        
        id_kamar = request.form.get('id_kamar')
        tgl_masuk_str = request.form.get('tgl_masuk')
        tgl_keluar_str = request.form.get('tgl_keluar')
        status_pembayaran = request.form.get('status_pembayaran')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            if not id_pasien and nama_manual:
                id_pasien = generate_id('PA', 'pasien_rifqi', 'id_pasien')
                cursor.execute(
                    "INSERT INTO pasien_rifqi (id_pasien, nama, alamat, kontak) VALUES (%s, %s, %s, %s)", 
                    (id_pasien, nama_manual, alamat_manual, kontak_manual)
                )
            
            id_transaksi = generate_id('TR', 'transaksi_rifqi', 'id_transaksi')
            id_rawat = generate_id('R', 'rawat_inap_rifqi', 'id_rawat')
            
            cursor.execute(
                "INSERT INTO rawat_inap_rifqi (id_rawat, id_pasien, id_kamar, tgl_masuk, tgl_keluar) VALUES (%s, %s, %s, %s, %s)", 
                (id_rawat, id_pasien, id_kamar, tgl_masuk_str, tgl_keluar_str)
            )
            
            cursor.execute("SELECT harga FROM kamar_rifqi WHERE id_kamar = %s", (id_kamar,))
            kamar = cursor.fetchone()
            
            d1 = datetime.strptime(tgl_masuk_str, "%Y-%m-%d")
            d2 = datetime.strptime(tgl_keluar_str, "%Y-%m-%d")
            hari = (d2 - d1).days
            total_biaya = (hari if hari > 0 else 1) * kamar['harga']
            
            cursor.execute(
                "INSERT INTO transaksi_rifqi (id_transaksi, id_pasien, total_biaya, status_pembayaran, tgl) VALUES (%s,%s,%s,%s,%s)", 
                (id_transaksi, id_pasien, total_biaya, status_pembayaran, datetime.now().date())
            )
            
            conn.commit()
            return redirect(url_for('datatransaksi'))

        except Exception as e:
            if conn: conn.rollback()
            return f"Terjadi kesalahan Database: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_pasien, nama FROM pasien_rifqi")
    pasien_list = cursor.fetchall()
    cursor.execute("SELECT id_kamar, kelas, harga FROM kamar_rifqi")
    kamar_list = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('form_Rifqi.html', pasien_list=pasien_list, kamar_list=kamar_list)
=======
        id_pasien = request.form['id_pasien']
        id_kamar = request.form['id_kamar']
        tgl_masuk_str = request.form['tgl_masuk']
        tgl_keluar_str = request.form['tgl_keluar']
        status_pembayaran = request.form['status_pembayaran']
        
        # Menggunakan prefix otomatis
        id_transaksi = generate_id('TR', 'transaksi_rifqi', 'id_transaksi', 3)
        id_rawat = generate_id('R', 'rawat_inap_rifqi', 'id_rawat', 2)
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # 1. Simpan data rawat inap
            cursor.execute("INSERT INTO rawat_inap_rifqi (id_rawat, id_pasien, id_kamar, tgl_masuk, tgl_keluar) VALUES (%s, %s, %s, %s, %s)", 
                           (id_rawat, id_pasien, id_kamar, tgl_masuk_str, tgl_keluar_str))
            
            # 2. Ambil harga kamar untuk kalkulasi
            cursor.execute("SELECT harga FROM kamar_rifqi WHERE id_kamar = %s", (id_kamar,))
            kamar = cursor.fetchone()
            
            # 3. Hitung selisih hari (Mengubah string form ke objek date)
            d1 = datetime.strptime(tgl_masuk_str, "%Y-%m-%d")
            d2 = datetime.strptime(tgl_keluar_str, "%Y-%m-%d")
            total_hari = (d2 - d1).days
            if total_hari < 1: total_hari = 1
            
            total_harga = kamar['harga'] * total_hari
            
            # 4. Simpan transaksi
            cursor.execute("INSERT INTO transaksi_rifqi (id_transaksi, id_pasien, total_biaya, status_pembayaran, tgl) VALUES (%s,%s,%s,%s,%s)", 
                           (id_transaksi, id_pasien, total_harga, status_pembayaran, datetime.now().date()))
            conn.commit()
            return redirect(url_for('datatransaksi'))
        except Exception as e:
            return f"Terjadi kesalahan: {e}"
        finally:
            cursor.close()
            conn.close()
    else:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_pasien, nama FROM pasien_rifqi")
        pasien_list = cursor.fetchall()     
        cursor.execute("SELECT id_kamar, kelas FROM kamar_rifqi")
        kamar_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('form_Rifqi.html', pasien_list=pasien_list, kamar_list=kamar_list)
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107

@app.route('/edit_transaksi/<id_transaksi>', methods=['GET', 'POST'])
def edit_transaksi(id_transaksi):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
<<<<<<< HEAD
=======
        id_transaksi_baru = request.form['id_transaksi_baru']
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107
        id_pasien = request.form['id_pasien']
        total_biaya = request.form['total_biaya']
        status_pembayaran = request.form['status_pembayaran']
        tgl = request.form['tgl']
<<<<<<< HEAD
        
        cursor.execute(
            "UPDATE transaksi_rifqi SET id_pasien=%s, total_biaya=%s, status_pembayaran=%s, tgl=%s WHERE id_transaksi=%s",
            (id_pasien, total_biaya, status_pembayaran, tgl, id_transaksi)
        )
=======
        cursor.execute("UPDATE transaksi_rifqi SET id_transaksi=%s, id_pasien=%s, total_biaya=%s, status_pembayaran=%s, tgl=%s WHERE id_transaksi=%s",
                       (id_transaksi_baru, id_pasien, total_biaya, status_pembayaran, tgl, id_transaksi))
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('datatransaksi'))
    
    cursor.execute("SELECT * FROM transaksi_rifqi WHERE id_transaksi=%s", (id_transaksi,))
    transaksi = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', transaksi=transaksi)

@app.route('/hapus_transaksi/<id_transaksi>')
def hapus_transaksi(id_transaksi):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transaksi_rifqi WHERE id_transaksi=%s", (id_transaksi,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('datatransaksi'))

@app.route('/pasien')
def datapasien():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pasien_rifqi")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pasien_rifqi.html', pasien=result)

<<<<<<< HEAD
@app.route('/cetak_pasien')
def cetak_pasien():
=======
@app.route('/cetak')
def cetak():
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pasien_rifqi")
        data_pasien = cursor.fetchall()
        cursor.close()
        conn.close()

        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 16)
        
        pdf.cell(0, 10, 'Laporan Data Pasien', align='C', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(5)

        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_fill_color(200, 220, 255)
        
<<<<<<< HEAD
        col_id_pasien = 30
        col_nama = 50
        col_alamat = 70
        col_kontak = 30

        pdf.cell(col_id_pasien, 10, 'ID Pasien', border=1, align='C', fill=True)
=======
        col_id_rifqi = 30
        col_nama_rifqi = 50
        col_alamat_rifqi = 70
        col_kontak_rifqi = 30

        pdf.cell(col_id, 10, 'ID Pasien', border=1, align='C', fill=True)
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107
        pdf.cell(col_nama, 10, 'Nama', border=1, align='C', fill=True)
        pdf.cell(col_alamat, 10, 'Alamat', border=1, align='C', fill=True)
        pdf.cell(col_kontak, 10, 'Kontak', border=1, align='C', fill=True)
        pdf.ln()

        pdf.set_font('Helvetica', '', 10)
        for row in data_pasien:
<<<<<<< HEAD
            pdf.cell(col_id_pasien, 10, str(row['id_pasien']), border=1)
            pdf.cell(col_nama, 10, str(row['nama']), border=1)
            pdf.cell(col_alamat, 10, str(row['alamat']), border=1)
            pdf.cell(col_kontak, 10, str(row['kontak']), border=1)
=======
            pdf.cell(col_id_rifqi, 10, str(row['id_pasien']), border=1)
            pdf.cell(col_nama_rifqi, 10, str(row['nama']), border=1)
            pdf.cell(col_alamat_rifqi, 10, str(row['alamat']), border=1)
            pdf.cell(col_kontak_rifqi, 10, str(row['kontak']), border=1)
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107
            pdf.ln()

        pdf_bytes = pdf.output()
        
        response = make_response(bytes(pdf_bytes))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=laporan_pasien_rifqi.pdf'
        return response

    except Exception as e:
        return f"<h1>Gagal Mencetak PDF</h1><p>Error: {e}</p>"

<<<<<<< HEAD

@app.route('/cetaktransaksi')
def cetaktransaksi():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT t.id_transaksi, t.id_pasien, r.id_rawat, p.nama, 
               t.total_biaya, t.status_pembayaran, t.tgl 
        FROM transaksi_rifqi t 
        JOIN pasien_rifqi p ON t.id_pasien = p.id_pasien 
        JOIN rawat_inap_rifqi r ON r.id_pasien = p.id_pasien
        GROUP BY t.id_transaksi
        ORDER BY t.id_transaksi 
    """)
        data_transaksi = cursor.fetchall()
        cursor.close()
        conn.close()

        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 16)
        
        pdf.cell(0, 10, 'Laporan Data Pasien', align='C', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(5)

        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_fill_color(200, 220, 255)
        

        col_id_transaksi = 30
        col_id_pasien = 30
        col_id_rawat = 30
        col_nama = 50
        col_total_biaya = 50
        col_status_pembayaran = 30
        col_tgl = 30


        pdf.cell(col_id_transaksi, 10, 'ID Transaksi', border=1, align='C', fill=True)
        pdf.cell(col_id_pasien, 10, 'ID Pasien', border=1, align='C', fill=True)
        pdf.cell(col_id_rawat, 10, 'ID Rawat', border=1, align='C', fill=True)
        pdf.cell(col_nama, 50, 'Nama Pasien', border=1, align='C', fill=True)
        pdf.cell(col_total_biaya, 10, 'Total Biaya', border=1, align='C', fill=True)
        pdf.cell(col_status_pembayaran, 10, 'Status Pembayaran', border=1, align='C', fill=True)
        pdf.cell(col_tgl, 10, 'Tanggal', border=1, align='C', fill=True)
        pdf.ln()

        pdf.set_font('Helvetica', '', 10)
        for row in data_transaksi:
            pdf.cell(col_id_transaksi, 10, str(row['id_transaksi']), border=1)
            pdf.cell(col_id_pasien, 10, str(row['id_pasien']), border=1)
            pdf.cell(col_id_rawat, 10, str(row['id_rawat']), border=1)
            pdf.cell(col_nama, 10, str(row['nama']), border=1)
            pdf.cell(col_total_biaya, 10, f"Rp {row['total_biaya']:,}", border=1) # Bonus: Format angka
            pdf.cell(col_status_pembayaran, 10, str(row['status_pembayaran']), border=1)
            tgl_fix = row['tgl'].strftime('%Y-%m-%d') if row['tgl'] else "-"
            pdf.cell(col_tgl, 10, tgl_fix, border=1)
            
            pdf.ln()

        pdf_bytes = pdf.output()
        
        response = make_response(bytes(pdf_bytes))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=laporan_transaksi_rifqi.pdf'
        return response

    except Exception as e:
        return f"<h1>Gagal Mencetak PDF</h1><p>Error: {e}</p>"



=======
>>>>>>> 0e79eb55cc2edfc29f5342f91949cfc69e03c107
if __name__ == '__main__':
    app.run(debug=True)