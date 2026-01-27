import os
from flask import Flask, render_template, request, redirect, url_for, make_response
from datetime import datetime
from fpdf import FPDF
import mysql.connector

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

# FUNGSI GENERATE ID DENGAN PREFIX & ZFILL (Lengkap & Benar)
def generate_id(prefix, table, column):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
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


@app.route('/')
def datatransaksi():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Query join untuk mendapatkan detail nama pasien dan data rawat
    query = """
        SELECT t.id_transaksi, t.id_pasien, r.id_rawat, p.nama, 
               t.total_biaya, t.status_pembayaran, t.tgl 
        FROM transaksi_rifqi t 
        INNER JOIN pasien_rifqi p ON t.id_pasien = p.id_pasien 
        INNER JOIN rawat_inap_rifqi r ON r.id_pasien = p.id_pasien
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('connection_Rifqi.html', transaksi=result)

@app.route('/data', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
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

@app.route('/edit_transaksi/<id_transaksi>', methods=['GET', 'POST'])
def edit_transaksi(id_transaksi):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        id_transaksi_baru = request.form['id_transaksi_baru']
        id_pasien = request.form['id_pasien']
        total_biaya = request.form['total_biaya']
        status_pembayaran = request.form['status_pembayaran']
        tgl = request.form['tgl']
        cursor.execute("UPDATE transaksi_rifqi SET id_transaksi=%s, id_pasien=%s, total_biaya=%s, status_pembayaran=%s, tgl=%s WHERE id_transaksi=%s",
                       (id_transaksi_baru, id_pasien, total_biaya, status_pembayaran, tgl, id_transaksi))
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

@app.route('/cetak')
def cetak():
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
        
        col_id_rifqi = 30
        col_nama_rifqi = 50
        col_alamat_rifqi = 70
        col_kontak_rifqi = 30

        pdf.cell(col_id, 10, 'ID Pasien', border=1, align='C', fill=True)
        pdf.cell(col_nama, 10, 'Nama', border=1, align='C', fill=True)
        pdf.cell(col_alamat, 10, 'Alamat', border=1, align='C', fill=True)
        pdf.cell(col_kontak, 10, 'Kontak', border=1, align='C', fill=True)
        pdf.ln()

        pdf.set_font('Helvetica', '', 10)
        for row in data_pasien:
            pdf.cell(col_id_rifqi, 10, str(row['id_pasien']), border=1)
            pdf.cell(col_nama_rifqi, 10, str(row['nama']), border=1)
            pdf.cell(col_alamat_rifqi, 10, str(row['alamat']), border=1)
            pdf.cell(col_kontak_rifqi, 10, str(row['kontak']), border=1)
            pdf.ln()

        pdf_bytes = pdf.output()
        
        response = make_response(bytes(pdf_bytes))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=laporan_pasien_rifqi.pdf'
        return response

    except Exception as e:
        return f"<h1>Gagal Mencetak PDF</h1><p>Error: {e}</p>"

if __name__ == '__main__':
    app.run(debug=True)