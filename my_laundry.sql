-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 21, 2023 at 07:47 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `my_laundry`
--

-- --------------------------------------------------------

--
-- Table structure for table `jenis_paket`
--

CREATE TABLE `jenis_paket` (
  `jenis_laundry` varchar(10) NOT NULL,
  `harga` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jenis_paket`
--

INSERT INTO `jenis_paket` (`jenis_laundry`, `harga`) VALUES
('EXPRESS', 10000),
('KILAT', 10000),
('REGULER', 5000);

-- --------------------------------------------------------

--
-- Table structure for table `karyawan`
--

CREATE TABLE `karyawan` (
  `id_karyawan` varchar(4) NOT NULL,
  `kode_karyawan` varchar(2) NOT NULL,
  `nama` varchar(35) NOT NULL,
  `kontak` varchar(15) DEFAULT NULL,
  `alamat` varchar(30) NOT NULL,
  `jam_kerja` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `karyawan`
--

INSERT INTO `karyawan` (`id_karyawan`, `kode_karyawan`, `nama`, `kontak`, `alamat`, `jam_kerja`) VALUES
('A01', 'A', 'Sumarni', '087654327890', 'Condongcatur, Depok, Sleman', 7),
('A02', 'A', 'Sugeng', '089212345678', 'Mancasan Lor', 6),
('A03', 'A', 'Sumarni', '083838202066', 'Condongcatur', 6),
('B01', 'B', 'Mulyani', '076512340909', 'Yogyakarta, Sleman', 4),
('B02', 'B', 'Supri', '089212345678', 'Sleman', 6),
('C01', 'C', 'Sutomo', '084523450001', 'Mancasan Lor', 7);

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `username` varchar(20) NOT NULL,
  `password` varchar(10) NOT NULL,
  `level` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`username`, `password`, `level`) VALUES
('Admin', '12345', 'karyawan'),
('Manajer', '1234', 'manajer');

-- --------------------------------------------------------

--
-- Table structure for table `pelanggan`
--

CREATE TABLE `pelanggan` (
  `id_pelanggan` int(4) UNSIGNED ZEROFILL NOT NULL,
  `nama` varchar(35) NOT NULL,
  `alamat` varchar(50) DEFAULT NULL,
  `kontak` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pelanggan`
--

INSERT INTO `pelanggan` (`id_pelanggan`, `nama`, `alamat`, `kontak`) VALUES
(0001, 'Mufidatul Ngazizah', 'Sleman', '087654327890'),
(0002, 'Salsabila', 'Condongcatur', '076512340909'),
(0003, 'Alif', 'Condongcatur', '076512340909'),
(0004, 'Dary', 'Condongcatur', '076512340909'),
(0005, 'Cindi', 'Condongcatur', '076512340909'),
(0006, 'Devita', 'Condongcatur', '076512340909'),
(0007, 'Jhingga', 'Condongcatur', '076512340909'),
(0008, 'Putri Amalia', 'Mancasan', '084523450001'),
(0010, 'Putri', 'Mancasan', '084523450001'),
(0011, 'Amalia', 'Mancasan', '084523450001'),
(0012, 'Kamelia', 'Mancasan', '084523450001'),
(0013, 'Mila', 'Mancasan', '084523450001'),
(0014, 'Lilis Sarifah', 'Ngringin', '087612347890'),
(0016, 'Arya', 'Condongcatur, Depok, Sleman', '089212345678'),
(0017, 'Cindi', 'Condongcatur, Depok, Sleman', '089212345678');

-- --------------------------------------------------------

--
-- Table structure for table `posisi`
--

CREATE TABLE `posisi` (
  `kode_karyawan` varchar(2) NOT NULL,
  `jobdesk` varchar(15) NOT NULL,
  `gaji_pokok` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posisi`
--

INSERT INTO `posisi` (`kode_karyawan`, `jobdesk`, `gaji_pokok`) VALUES
('A', 'Mencuci', 40000),
('B', 'Menyetrika', 30000),
('C', 'Packing', 10000);

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `id_nota` varchar(15) NOT NULL,
  `id_pelanggan` int(4) UNSIGNED ZEROFILL NOT NULL,
  `jenis_laundry` varchar(10) NOT NULL,
  `berat` int(2) NOT NULL,
  `tanggal_masuk` datetime NOT NULL,
  `tanggal_keluar` date DEFAULT NULL,
  `id_karyawan` varchar(35) NOT NULL,
  `status` varchar(10) NOT NULL,
  `status_pembayaran` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaksi`
--

INSERT INTO `transaksi` (`id_nota`, `id_pelanggan`, `jenis_laundry`, `berat`, `tanggal_masuk`, `tanggal_keluar`, `id_karyawan`, `status`, `status_pembayaran`) VALUES
('001E020723', 0001, 'EXPRESS', 4, '2023-07-02 15:43:00', '2023-07-02', 'A01', 'DIAMBIL', 'LUNAS'),
('001E050723', 0002, 'EXPRESS', 2, '2023-07-05 12:42:00', '2023-07-10', 'A01', 'DIAMBIL', 'LUNAS'),
('001E100723', 0014, 'EXPRESS', 3, '2023-07-10 19:26:00', '2023-07-10', 'B01', 'DIAMBIL', 'LUNAS'),
('001E120723', 0006, 'EXPRESS', 5, '2023-07-12 00:04:00', NULL, 'A02', 'DITERIMA', 'BELUM BAYAR'),
('001K020723', 0001, 'KILAT', 4, '2023-07-02 09:30:00', '2023-07-12', 'B01', 'DIAMBIL', 'LUNAS'),
('001K030723', 0006, 'KILAT', 3, '2023-07-03 10:07:00', NULL, 'B01', 'DITERIMA', 'BELUM BAYAR'),
('001K210623', 0003, 'KILAT', 3, '2023-06-21 00:00:00', '2023-07-02', 'B01', 'DITERIMA', 'LUNAS'),
('001R020723', 0001, 'EXPRESS', 5, '2023-07-02 09:10:00', '2023-07-02', 'C01', 'SELESAI', 'LUNAS'),
('001R270623', 0002, 'KILAT', 3, '2023-06-27 00:00:00', '2023-06-27', 'B01', 'DITERIMA', 'LUNAS'),
('002E020723', 0001, 'EXPRESS', 6, '2023-07-02 20:35:00', '2023-07-09', 'A01', 'SELESAI', 'LUNAS'),
('002E100723', 0001, 'EXPRESS', 3, '2023-07-10 21:21:00', NULL, 'B02', 'DITERIMA', 'LUNAS'),
('002E120723', 0006, 'EXPRESS', 5, '2023-07-12 08:06:00', NULL, 'A01', 'DITERIMA', 'LUNAS'),
('002K030723', 0001, 'KILAT', 2, '2023-07-03 10:08:00', '0000-00-00', 'B01', 'SELESAI', 'LUNAS'),
('002R210623', 0002, 'REGULER', 3, '2023-06-21 00:00:00', '2023-06-23', 'B01', 'SELESAI', 'LUNAS'),
('002R270623', 0002, 'REGULER', 6, '2023-06-27 00:00:00', NULL, 'A01', 'DIAMBIL', 'LUNAS'),
('003E020723', 0004, 'EXPRESS', 5, '2023-07-02 20:42:00', '0000-00-00', 'B01', 'PROSES', 'LUNAS'),
('003E120723', 0005, 'EXPRESS', 3, '2023-07-12 08:17:00', NULL, 'A02', 'DITERIMA', 'BELUM BAYAR'),
('003R210623', 0003, 'KILAT', 2, '2023-06-21 00:00:00', '2023-06-21', 'B01', 'SELESAI', 'LUNAS'),
('003R270623', 0003, 'REGULER', 5, '2023-06-27 00:00:00', NULL, 'A01', 'PROSES', 'LUNAS'),
('004E020723', 0006, 'EXPRESS', 5, '2023-07-02 20:55:00', '0000-00-00', 'A01', 'DITERIMA', 'LUNAS'),
('004E270623', 0001, 'EXPRESS', 2, '2023-06-27 00:00:00', '0000-00-00', 'A01', 'DITERIMA', 'LUNAS'),
('004K020623', 0003, 'KILAT', 3, '2023-07-02 11:05:00', '0000-00-00', 'C01', 'DITERIMA', 'LUNAS'),
('004K270623', 0002, 'KILAT', 2, '2023-06-27 00:00:00', '0000-00-00', 'C01', 'DITERIMA', 'LUNAS'),
('004R210623', 0002, 'KILAT', 2, '2023-06-21 00:00:00', '2023-06-21', 'B01', 'DITERIMA', 'LUNAS'),
('005E020723', 0001, 'EXPRESS', 5, '2023-07-02 21:10:00', '0000-00-00', 'B01', 'DITERIMA', 'LUNAS'),
('005K270623', 0002, 'KILAT', 2, '2023-06-27 00:00:00', '0000-00-00', 'C01', 'PROSES', 'LUNAS'),
('005R020723', 0001, 'REGULER', 2, '2023-07-02 14:37:00', '0000-00-00', 'A01', 'PROSES', 'LUNAS'),
('005R210623', 0002, 'REGULER', 5, '2023-06-21 00:00:00', '0000-00-00', 'C01', 'DITERIMA', 'LUNAS'),
('005R230623', 0001, 'EXPRESS', 6, '2023-06-23 00:00:00', NULL, 'B01', 'PROSES', 'LUNAS'),
('005R270623', 0001, 'REGULER', 1, '2023-06-27 00:00:00', '0000-00-00', 'A01', 'PROSES', 'LUNAS'),
('006R020723', 0002, 'REGULER', 5, '2023-07-02 15:48:00', '0000-00-00', 'A01', 'PROSES', 'LUNAS'),
('006R270623', 0003, 'REGULER', 5, '2023-06-27 04:55:00', '0000-00-00', 'A01', 'DITERIMA', 'LUNAS'),
('010K270623', 0001, 'KILAT', 3, '2023-06-27 12:00:00', '0000-00-00', 'C01', 'PROSES', 'LUNAS');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `jenis_paket`
--
ALTER TABLE `jenis_paket`
  ADD PRIMARY KEY (`jenis_laundry`);

--
-- Indexes for table `karyawan`
--
ALTER TABLE `karyawan`
  ADD PRIMARY KEY (`id_karyawan`),
  ADD KEY `kode_karyawan` (`kode_karyawan`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pelanggan`
--
ALTER TABLE `pelanggan`
  ADD PRIMARY KEY (`id_pelanggan`);

--
-- Indexes for table `posisi`
--
ALTER TABLE `posisi`
  ADD PRIMARY KEY (`kode_karyawan`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id_nota`),
  ADD KEY `fk_jenis_laundry` (`jenis_laundry`),
  ADD KEY `fk_karyawan` (`id_karyawan`),
  ADD KEY `id_pelanggan` (`id_pelanggan`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pelanggan`
--
ALTER TABLE `pelanggan`
  MODIFY `id_pelanggan` int(4) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `karyawan`
--
ALTER TABLE `karyawan`
  ADD CONSTRAINT `kode_karyawan` FOREIGN KEY (`kode_karyawan`) REFERENCES `posisi` (`kode_karyawan`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD CONSTRAINT `fk_jenis_laundry` FOREIGN KEY (`jenis_laundry`) REFERENCES `jenis_paket` (`jenis_laundry`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_karyawan` FOREIGN KEY (`id_karyawan`) REFERENCES `karyawan` (`id_karyawan`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `transaksi_ibfk_1` FOREIGN KEY (`id_pelanggan`) REFERENCES `pelanggan` (`id_pelanggan`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
