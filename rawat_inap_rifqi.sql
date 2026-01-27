-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 13 Jan 2026 pada 03.23
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rawat_inap_rifqi`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `kamar_rifqi`
--

CREATE TABLE `kamar_rifqi` (
  `id_kamar` varchar(3) NOT NULL,
  `no_kamar` varchar(3) NOT NULL,
  `kelas` varchar(15) NOT NULL,
  `status_kamar` varchar(15) NOT NULL,
  `harga` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `kamar_rifqi`
--

INSERT INTO `kamar_rifqi` (`id_kamar`, `no_kamar`, `kelas`, `status_kamar`, `harga`) VALUES
('K01', '101', 'Kelas A', 'Tesedia', 500000),
('K02', '102', 'Kelas C', 'Tidak Tesedia', 250000),
('K03', '103', 'Kelas B', 'Tidak Tesedia', 300000),
('K04', '104', 'Kelas C', 'Tesedia', 250000),
('K05', '105', 'Kelas A', 'Tidak Tesedia', 500000);

-- --------------------------------------------------------

--
-- Struktur dari tabel `pasien_rifqi`
--

CREATE TABLE `pasien_rifqi` (
  `id_pasien` varchar(5) NOT NULL,
  `nama` varchar(25) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `kontak` int(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `pasien_rifqi`
--

INSERT INTO `pasien_rifqi` (`id_pasien`, `nama`, `alamat`, `kontak`) VALUES
('PA001', 'Rifqi Ariq', 'Jl. Cimindi No 24D', 896834522),
('PA002', 'Ahmad Boriq', 'Jl. Ciwidey No 114A', 894325478),
('PA003', 'Rizal Ahmad', 'Jl. Cigugur Tengah No 14', 896834545),
('PA004', 'Faeyza Rifqi', 'Jl. Pesantren No 111B', 894325471),
('PA005', ' Ariq', 'Jl. Danurasmaya Kiara Green No 14G', 896834244);

-- --------------------------------------------------------

--
-- Struktur dari tabel `rawat_inap_rifqi`
--

CREATE TABLE `rawat_inap_rifqi` (
  `id_rawat` varchar(3) NOT NULL,
  `id_pasien` varchar(5) NOT NULL,
  `id_kamar` varchar(3) NOT NULL,
  `tgl_masuk` date NOT NULL,
  `tgl_keluar` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `rawat_inap_rifqi`
--

INSERT INTO `rawat_inap_rifqi` (`id_rawat`, `id_pasien`, `id_kamar`, `tgl_masuk`, `tgl_keluar`) VALUES
('R01', 'PA001', 'K01', '2026-01-01', '2026-01-09'),
('R02', 'PA002', 'K02', '2026-01-07', '2026-01-13'),
('R03', 'PA003', 'K03', '2026-01-06', '2026-01-16'),
('R04', 'PA004', 'K04', '2026-01-12', '2026-01-13'),
('R05', 'PA005', 'K05', '2026-01-07', '2026-01-10');

-- --------------------------------------------------------

--
-- Struktur dari tabel `transaksi_rifqi`
--

CREATE TABLE `transaksi_rifqi` (
  `id_transaksi` varchar(5) NOT NULL,
  `id_pasien` varchar(5) NOT NULL,
  `total_biaya` int(11) NOT NULL,
  `status_pembayaran` varchar(20) NOT NULL,
  `tgl` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `transaksi_rifqi`
--

INSERT INTO `transaksi_rifqi` (`id_transaksi`, `id_pasien`, `total_biaya`, `status_pembayaran`, `tgl`) VALUES
('TR001', 'PA001', 500000, 'Belum Terbayar', '2026-01-09'),
('TR002', 'PA002', 250000, 'Terbayar', '2026-01-13'),
('TR003', 'PA003', 300000, 'Belum Terbayar', '2026-01-16'),
('TR004', 'PA004', 250000, 'Terbayar', '2026-01-13'),
('TR005', 'PA005', 500000, 'Belum Terbayar', '2026-01-10');

-- --------------------------------------------------------

--
-- Struktur dari tabel `user_rifqi`
--

CREATE TABLE `user_rifqi` (
  `id_user` varchar(3) NOT NULL,
  `username` varchar(25) NOT NULL,
  `password` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `user_rifqi`
--

INSERT INTO `user_rifqi` (`id_user`, `username`, `password`) VALUES
('001', 'Ariq12@gmail.com', 'Boriq12'),
('002', 'Tat145@gmail.com', 'Tatyuya'),
('003', 'Borrq@gmail.com', 'mAsariq45'),
('004', 'Mesutbotak@gmail.com', 'Mesut170509'),
('005', 'ariq17@gmail.com', 'Ar1709');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `kamar_rifqi`
--
ALTER TABLE `kamar_rifqi`
  ADD PRIMARY KEY (`id_kamar`);

--
-- Indeks untuk tabel `pasien_rifqi`
--
ALTER TABLE `pasien_rifqi`
  ADD PRIMARY KEY (`id_pasien`);

--
-- Indeks untuk tabel `rawat_inap_rifqi`
--
ALTER TABLE `rawat_inap_rifqi`
  ADD PRIMARY KEY (`id_rawat`),
  ADD KEY `id_pasien` (`id_pasien`),
  ADD KEY `id_kamar` (`id_kamar`);

--
-- Indeks untuk tabel `transaksi_rifqi`
--
ALTER TABLE `transaksi_rifqi`
  ADD PRIMARY KEY (`id_transaksi`),
  ADD KEY `id_pasien` (`id_pasien`);

--
-- Indeks untuk tabel `user_rifqi`
--
ALTER TABLE `user_rifqi`
  ADD PRIMARY KEY (`id_user`);

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `rawat_inap_rifqi`
--
ALTER TABLE `rawat_inap_rifqi`
  ADD CONSTRAINT `rawat_inap_rifqi_ibfk_2` FOREIGN KEY (`id_pasien`) REFERENCES `pasien_rifqi` (`id_pasien`),
  ADD CONSTRAINT `rawat_inap_rifqi_ibfk_3` FOREIGN KEY (`id_kamar`) REFERENCES `kamar_rifqi` (`id_kamar`);

--
-- Ketidakleluasaan untuk tabel `transaksi_rifqi`
--
ALTER TABLE `transaksi_rifqi`
  ADD CONSTRAINT `transaksi_rifqi_ibfk_1` FOREIGN KEY (`id_pasien`) REFERENCES `pasien_rifqi` (`id_pasien`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
