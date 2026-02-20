from datetime import datetime
import random
import json

class SahamHandler:
    def __init__(self):
        self.saham_data = {
            # ============================================
            # SEKTOR KEUANGAN (BANK)
            # ============================================
            "BBCA": {
                "name": "Bank Central Asia Tbk",
                "sektor": "Keuangan",
                "sub_sektor": "Bank",
                "harga": 7175,
                "change": -100,
                "change_pct": "-1.37%",
                "ma5": 7285,
                "ma20": 7290,
                "ma50": 7150,
                "ma100": 7050,
                "rsi": 34.7,
                "macd": -172.08,
                "volume": 15234500,
                "pe": 21.5,
                "pbv": 3.2,
                "roe": 21.1
            },
            "BBRI": {
                "name": "Bank Rakyat Indonesia Tbk",
                "sektor": "Keuangan",
                "sub_sektor": "Bank",
                "harga": 5450,
                "change": 75,
                "change_pct": "+1.40%",
                "ma5": 5420,
                "ma20": 5380,
                "ma50": 5320,
                "ma100": 5250,
                "rsi": 48.2,
                "macd": -45.3,
                "volume": 78500000,
                "pe": 15.3,
                "pbv": 2.1,
                "roe": 18.5
            },
            "BBNI": {
                "name": "Bank Negara Indonesia Tbk",
                "sektor": "Keuangan",
                "sub_sektor": "Bank",
                "harga": 4890,
                "change": 45,
                "change_pct": "+0.93%",
                "ma5": 4850,
                "ma20": 4820,
                "ma50": 4780,
                "ma100": 4700,
                "rsi": 52.3,
                "macd": 25.7,
                "volume": 32100000,
                "pe": 12.8,
                "pbv": 1.5,
                "roe": 14.2
            },
            "BMRI": {
                "name": "Bank Mandiri Tbk",
                "sektor": "Keuangan",
                "sub_sektor": "Bank",
                "harga": 10325,
                "change": 345,
                "change_pct": "+3.45%",
                "ma5": 10200,
                "ma20": 10050,
                "ma50": 9850,
                "ma100": 9600,
                "rsi": 62.5,
                "macd": 125.3,
                "volume": 45200000,
                "pe": 14.2,
                "pbv": 2.3,
                "roe": 19.8
            },
            "BTPS": {
                "name": "Bank BTPN Syariah Tbk",
                "sektor": "Keuangan",
                "sub_sektor": "Bank Syariah",
                "harga": 1250,
                "change": 25,
                "change_pct": "+2.04%",
                "ma5": 1230,
                "ma20": 1210,
                "ma50": 1180,
                "ma100": 1150,
                "rsi": 58.7,
                "macd": 15.2,
                "volume": 12500000,
                "pe": 18.5,
                "pbv": 2.8,
                "roe": 16.3
            },
            "BNGA": {
                "name": "Bank CIMB Niaga Tbk",
                "sektor": "Keuangan",
                "sub_sektor": "Bank",
                "harga": 1850,
                "change": -15,
                "change_pct": "-0.80%",
                "ma5": 1870,
                "ma20": 1880,
                "ma50": 1820,
                "ma100": 1780,
                "rsi": 42.5,
                "macd": -8.3,
                "volume": 18500000,
                "pe": 10.2,
                "pbv": 0.9,
                "roe": 11.5
            },
            
            # ============================================
            # SEKTOR INFRASTRUKTUR (TELCO)
            # ============================================
            "TLKM": {
                "name": "Telkom Indonesia Tbk",
                "sektor": "Infrastruktur",
                "sub_sektor": "Telekomunikasi",
                "harga": 3890,
                "change": -85,
                "change_pct": "-2.14%",
                "ma5": 3920,
                "ma20": 3950,
                "ma50": 3880,
                "ma100": 3820,
                "rsi": 32.1,
                "macd": -98.5,
                "volume": 178000000,
                "pe": 12.1,
                "pbv": 1.8,
                "roe": 15.3
            },
            "EXCL": {
                "name": "XL Axiata Tbk",
                "sektor": "Infrastruktur",
                "sub_sektor": "Telekomunikasi",
                "harga": 2150,
                "change": 35,
                "change_pct": "+1.65%",
                "ma5": 2120,
                "ma20": 2100,
                "ma50": 2050,
                "ma100": 1980,
                "rsi": 55.8,
                "macd": 22.4,
                "volume": 45200000,
                "pe": 18.3,
                "pbv": 1.2,
                "roe": 8.7
            },
            "ISAT": {
                "name": "Indosat Tbk",
                "sektor": "Infrastruktur",
                "sub_sektor": "Telekomunikasi",
                "harga": 8750,
                "change": 125,
                "change_pct": "+1.45%",
                "ma5": 8600,
                "ma20": 8450,
                "ma50": 8200,
                "ma100": 7900,
                "rsi": 58.2,
                "macd": 75.3,
                "volume": 12300000,
                "pe": 22.5,
                "pbv": 2.1,
                "roe": 12.4
            },
            "TOWR": {
                "name": "Sarana Menara Nusantara Tbk",
                "sektor": "Infrastruktur",
                "sub_sektor": "Menara Telekomunikasi",
                "harga": 795,
                "change": -5,
                "change_pct": "-0.62%",
                "ma5": 800,
                "ma20": 805,
                "ma50": 790,
                "ma100": 770,
                "rsi": 45.2,
                "macd": -3.5,
                "volume": 85600000,
                "pe": 25.3,
                "pbv": 2.8,
                "roe": 10.1
            },
            "TBIG": {
                "name": "Tower Bersama Infrastructure Tbk",
                "sektor": "Infrastruktur",
                "sub_sektor": "Menara Telekomunikasi",
                "harga": 1950,
                "change": 15,
                "change_pct": "+0.78%",
                "ma5": 1940,
                "ma20": 1930,
                "ma50": 1900,
                "ma100": 1850,
                "rsi": 52.8,
                "macd": 8.2,
                "volume": 32500000,
                "pe": 23.8,
                "pbv": 2.5,
                "roe": 9.8
            },
            
            # ============================================
            # SEKTOR ENERGI (BATUBARA, MINYAK)
            # ============================================
            "ADRO": {
                "name": "Adaro Energy Indonesia Tbk",
                "sektor": "Energi",
                "sub_sektor": "Batubara",
                "harga": 2575,
                "change": 125,
                "change_pct": "+5.10%",
                "ma5": 2500,
                "ma20": 2450,
                "ma50": 2400,
                "ma100": 2350,
                "rsi": 62.5,
                "macd": 45.3,
                "volume": 125000000,
                "pe": 5.2,
                "pbv": 0.9,
                "roe": 18.5
            },
            "PTBA": {
                "name": "Bukit Asam Tbk",
                "sektor": "Energi",
                "sub_sektor": "Batubara",
                "harga": 3850,
                "change": 150,
                "change_pct": "+4.05%",
                "ma5": 3750,
                "ma20": 3650,
                "ma50": 3550,
                "ma100": 3400,
                "rsi": 65.2,
                "macd": 85.7,
                "volume": 45200000,
                "pe": 4.8,
                "pbv": 1.1,
                "roe": 22.3
            },
            "BUMI": {
                "name": "Bumi Resources Tbk",
                "sektor": "Energi",
                "sub_sektor": "Batubara",
                "harga": 460,
                "change": 50,
                "change_pct": "+12.20%",
                "ma5": 440,
                "ma20": 420,
                "ma50": 400,
                "ma100": 380,
                "rsi": 72.5,
                "macd": 25.8,
                "volume": 892000000,
                "pe": 3.2,
                "pbv": 0.5,
                "roe": 15.7
            },
            "ITMG": {
                "name": "Indo Tambangraya Megah Tbk",
                "sektor": "Energi",
                "sub_sektor": "Batubara",
                "harga": 25200,
                "change": 800,
                "change_pct": "+3.28%",
                "ma5": 24800,
                "ma20": 24200,
                "ma50": 23800,
                "ma100": 23000,
                "rsi": 58.9,
                "macd": 450,
                "volume": 5230000,
                "pe": 4.5,
                "pbv": 1.2,
                "roe": 25.8
            },
            "MEDC": {
                "name": "Medco Energi Internasional Tbk",
                "sektor": "Energi",
                "sub_sektor": "Minyak & Gas",
                "harga": 1250,
                "change": 35,
                "change_pct": "+2.88%",
                "ma5": 1220,
                "ma20": 1200,
                "ma50": 1150,
                "ma100": 1100,
                "rsi": 55.2,
                "macd": 18.5,
                "volume": 45200000,
                "pe": 8.5,
                "pbv": 0.7,
                "roe": 12.3
            },
            
            # ============================================
            # SEKTOR KONSUMER (MAKANAN, MINUMAN)
            # ============================================
            "ICBP": {
                "name": "Indofood CBP Sukses Makmur Tbk",
                "sektor": "Konsumer",
                "sub_sektor": "Makanan & Minuman",
                "harga": 10350,
                "change": 125,
                "change_pct": "+1.22%",
                "ma5": 10250,
                "ma20": 10100,
                "ma50": 9900,
                "ma100": 9600,
                "rsi": 55.8,
                "macd": 85.3,
                "volume": 12500000,
                "pe": 18.5,
                "pbv": 2.8,
                "roe": 16.2
            },
            "INDF": {
                "name": "Indofood Sukses Makmur Tbk",
                "sektor": "Konsumer",
                "sub_sektor": "Makanan & Minuman",
                "harga": 6750,
                "change": 50,
                "change_pct": "+0.75%",
                "ma5": 6700,
                "ma20": 6650,
                "ma50": 6550,
                "ma100": 6400,
                "rsi": 52.3,
                "macd": 25.7,
                "volume": 18500000,
                "pe": 12.3,
                "pbv": 1.5,
                "roe": 14.8
            },
            "UNVR": {
                "name": "Unilever Indonesia Tbk",
                "sektor": "Konsumer",
                "sub_sektor": "Kosmetik & Barang Rumah Tangga",
                "harga": 3850,
                "change": -75,
                "change_pct": "-1.91%",
                "ma5": 3900,
                "ma20": 3950,
                "ma50": 4000,
                "ma100": 4100,
                "rsi": 32.5,
                "macd": -45.8,
                "volume": 32500000,
                "pe": 25.3,
                "pbv": 18.5,
                "roe": 35.2
            },
            "HMSP": {
                "name": "HM Sampoerna Tbk",
                "sektor": "Konsumer",
                "sub_sektor": "Rokok",
                "harga": 795,
                "change": -5,
                "change_pct": "-0.62%",
                "ma5": 800,
                "ma20": 805,
                "ma50": 810,
                "ma100": 820,
                "rsi": 42.5,
                "macd": -5.2,
                "volume": 85600000,
                "pe": 12.5,
                "pbv": 3.2,
                "roe": 28.5
            },
            "GGRM": {
                "name": "Gudang Garam Tbk",
                "sektor": "Konsumer",
                "sub_sektor": "Rokok",
                "harga": 21500,
                "change": 250,
                "change_pct": "+1.18%",
                "ma5": 21200,
                "ma20": 21000,
                "ma50": 20500,
                "ma100": 19800,
                "rsi": 55.8,
                "macd": 350,
                "volume": 3250000,
                "pe": 8.5,
                "pbv": 1.2,
                "roe": 14.5
            },
            
            # ============================================
            # SEKTOR OTOMOTIF
            # ============================================
            "ASII": {
                "name": "Astra International Tbk",
                "sektor": "Otomotif",
                "sub_sektor": "Otomotif & Komponen",
                "harga": 7945,
                "change": -190,
                "change_pct": "-2.34%",
                "ma5": 8050,
                "ma20": 8100,
                "ma50": 7900,
                "ma100": 7750,
                "rsi": 31.5,
                "macd": -125.3,
                "volume": 45200000,
                "pe": 11.5,
                "pbv": 1.2,
                "roe": 15.8
            },
            "AUTO": {
                "name": "Astra Otoparts Tbk",
                "sektor": "Otomotif",
                "sub_sektor": "Otomotif & Komponen",
                "harga": 1850,
                "change": 25,
                "change_pct": "+1.37%",
                "ma5": 1820,
                "ma20": 1800,
                "ma50": 1750,
                "ma100": 1700,
                "rsi": 58.2,
                "macd": 15.3,
                "volume": 12500000,
                "pe": 8.2,
                "pbv": 0.7,
                "roe": 10.5
            },
            
            # ============================================
            # SEKTOR PROPERTI
            # ============================================
            "BSDE": {
                "name": "Bumi Serpong Damai Tbk",
                "sektor": "Properti",
                "sub_sektor": "Properti & Real Estate",
                "harga": 1125,
                "change": 15,
                "change_pct": "+1.35%",
                "ma5": 1110,
                "ma20": 1100,
                "ma50": 1050,
                "ma100": 1000,
                "rsi": 55.2,
                "macd": 8.5,
                "volume": 45200000,
                "pe": 9.5,
                "pbv": 0.6,
                "roe": 6.5
            },
            "PWON": {
                "name": "Pakuwon Jati Tbk",
                "sektor": "Properti",
                "sub_sektor": "Properti & Real Estate",
                "harga": 485,
                "change": 5,
                "change_pct": "+1.04%",
                "ma5": 480,
                "ma20": 475,
                "ma50": 460,
                "ma100": 450,
                "rsi": 58.5,
                "macd": 3.2,
                "volume": 85600000,
                "pe": 8.2,
                "pbv": 0.8,
                "roe": 7.8
            },
            "CTRA": {
                "name": "Ciputra Development Tbk",
                "sektor": "Properti",
                "sub_sektor": "Properti & Real Estate",
                "harga": 1050,
                "change": -10,
                "change_pct": "-0.94%",
                "ma5": 1060,
                "ma20": 1070,
                "ma50": 1040,
                "ma100": 1000,
                "rsi": 42.5,
                "macd": -5.3,
                "volume": 32500000,
                "pe": 10.5,
                "pbv": 0.7,
                "roe": 5.8
            },
            
            # ============================================
            # SEKTOR TEKNOLOGI
            # ============================================
            "GOTO": {
                "name": "GoTo Gojek Tokopedia Tbk",
                "sektor": "Teknologi",
                "sub_sektor": "Digital",
                "harga": 345,
                "change": 45,
                "change_pct": "+15.00%",
                "ma5": 320,
                "ma20": 310,
                "ma50": 295,
                "ma100": 280,
                "rsi": 72.5,
                "macd": 15.2,
                "volume": 1200000000,
                "pe": -5.2,
                "pbv": 1.8,
                "roe": -8.5
            },
            "BUKA": {
                "name": "Bukalapak.com Tbk",
                "sektor": "Teknologi",
                "sub_sektor": "Digital",
                "harga": 195,
                "change": 5,
                "change_pct": "+2.63%",
                "ma5": 190,
                "ma20": 185,
                "ma50": 175,
                "ma100": 165,
                "rsi": 58.5,
                "macd": 3.5,
                "volume": 452000000,
                "pe": -8.5,
                "pbv": 1.2,
                "roe": -12.5
            },
            
            # ============================================
            # SEKTOR KESEHATAN
            # ============================================
            "SILO": {
                "name": "Siloam Hospitals Tbk",
                "sektor": "Kesehatan",
                "sub_sektor": "Rumah Sakit",
                "harga": 1850,
                "change": 35,
                "change_pct": "+1.93%",
                "ma5": 1820,
                "ma20": 1800,
                "ma50": 1750,
                "ma100": 1700,
                "rsi": 62.5,
                "macd": 18.5,
                "volume": 12500000,
                "pe": 22.5,
                "pbv": 3.2,
                "roe": 12.5
            },
            "HEAL": {
                "name": "Medikaloka Hermina Tbk",
                "sektor": "Kesehatan",
                "sub_sektor": "Rumah Sakit",
                "harga": 1250,
                "change": 15,
                "change_pct": "+1.21%",
                "ma5": 1240,
                "ma20": 1230,
                "ma50": 1200,
                "ma100": 1150,
                "rsi": 55.8,
                "macd": 8.5,
                "volume": 18500000,
                "pe": 18.5,
                "pbv": 2.5,
                "roe": 14.5
            },
            "KLBF": {
                "name": "Kalbe Farma Tbk",
                "sektor": "Kesehatan",
                "sub_sektor": "Farmasi",
                "harga": 1550,
                "change": -15,
                "change_pct": "-0.96%",
                "ma5": 1560,
                "ma20": 1570,
                "ma50": 1550,
                "ma100": 1520,
                "rsi": 45.2,
                "macd": -5.3,
                "volume": 45200000,
                "pe": 19.5,
                "pbv": 3.5,
                "roe": 16.5
            },
            
            # ============================================
            # SEKTOR LOGAM & MINERAL
            # ============================================
            "ANTM": {
                "name": "Aneka Tambang Tbk",
                "sektor": "Logam & Mineral",
                "sub_sektor": "Pertambangan Logam",
                "harga": 1850,
                "change": 35,
                "change_pct": "+1.93%",
                "ma5": 1820,
                "ma20": 1800,
                "ma50": 1750,
                "ma100": 1700,
                "rsi": 58.5,
                "macd": 18.5,
                "volume": 85600000,
                "pe": 12.5,
                "pbv": 1.5,
                "roe": 10.5
            },
            "INCO": {
                "name": "Vale Indonesia Tbk",
                "sektor": "Logam & Mineral",
                "sub_sektor": "Pertambangan Logam",
                "harga": 4850,
                "change": 125,
                "change_pct": "+2.64%",
                "ma5": 4750,
                "ma20": 4650,
                "ma50": 4500,
                "ma100": 4300,
                "rsi": 62.5,
                "macd": 85.3,
                "volume": 12500000,
                "pe": 15.5,
                "pbv": 1.8,
                "roe": 12.5
            },
            "MDKA": {
                "name": "Merdeka Copper Gold Tbk",
                "sektor": "Logam & Mineral",
                "sub_sektor": "Pertambangan Logam",
                "harga": 2450,
                "change": 35,
                "change_pct": "+1.45%",
                "ma5": 2420,
                "ma20": 2400,
                "ma50": 2350,
                "ma100": 2250,
                "rsi": 55.8,
                "macd": 22.5,
                "volume": 45200000,
                "pe": 25.5,
                "pbv": 3.2,
                "roe": 8.5
            },
            
            # ============================================
            # SEKTOR TRANSPORTASI
            # ============================================
            "JSMR": {
                "name": "Jasa Marga Tbk",
                "sektor": "Transportasi",
                "sub_sektor": "Jalan Tol",
                "harga": 4850,
                "change": 75,
                "change_pct": "+1.57%",
                "ma5": 4800,
                "ma20": 4750,
                "ma50": 4650,
                "ma100": 4500,
                "rsi": 58.5,
                "macd": 45.3,
                "volume": 18500000,
                "pe": 12.5,
                "pbv": 1.2,
                "roe": 10.5
            },
            "TLKM": {
                "name": "Telkom Indonesia Tbk",
                "sektor": "Infrastruktur",
                "sub_sektor": "Telekomunikasi",
                "harga": 3890,
                "change": -85,
                "change_pct": "-2.14%",
                "ma5": 3920,
                "ma20": 3950,
                "ma50": 3880,
                "ma100": 3820,
                "rsi": 32.1,
                "macd": -98.5,
                "volume": 178000000,
                "pe": 12.1,
                "pbv": 1.8,
                "roe": 15.3
            }
        }
        
        # Daftar semua kode saham
        self.daftar_saham = list(self.saham_data.keys())
        
    def get_analisis(self, kode):
        """Dapatkan data analisis saham"""
        kode = kode.upper()
        
        # Jika kode tidak ditemukan, return None
        if kode not in self.saham_data:
            return None
            
        data = self.saham_data[kode]
        harga = data["harga"]
        
        # Tentukan status RSI
        if data["rsi"] < 35:
            rsi_status = "OVERSOLD"
        elif data["rsi"] > 70:
            rsi_status = "OVERBOUGHT"
        else:
            rsi_status = "NETRAL"
        
        # Tentukan sinyal MACD
        macd_signal = "BEARISH" if data["macd"] < 0 else "BULLISH"
        
        # Tentukan sinyal MA
        ma5_signal = "DI BAWAH" if harga < data["ma5"] else "DI ATAS"
        ma20_signal = "DI BAWAH" if harga < data["ma20"] else "DI ATAS"
        ma50_signal = "DI BAWAH" if harga < data["ma50"] else "DI ATAS"
        ma100_signal = "DI BAWAH" if harga < data["ma100"] else "DI ATAS"
        
        # Hitung support resistance
        support1 = int(min(harga * 0.98, data["ma50"]))
        support2 = int(harga * 0.955)
        support3 = int(harga * 0.89)
        resistance1 = int(max(harga * 1.05, data["ma20"]))
        resistance2 = int(harga * 1.11)
        resistance3 = int(harga * 1.15)
        
        return {
            "timestamp": datetime.now().strftime('%d/%m/%Y %H:%M WIB'),
            "nama": data["name"],
            "sektor": data["sektor"],
            "sub_sektor": data["sub_sektor"],
            "harga": harga,
            "change": data["change"],
            "change_pct": data["change_pct"],
            
            "daytrade": {
                "entry_min": int(harga * 0.995),
                "entry_max": harga,
                "target1": int(harga * 1.01),
                "target2": int(harga * 1.02),
                "target3": int(harga * 1.03),
                "stop_loss": int(harga * 0.99)
            },
            
            "swing": {
                "entry_min": int(harga * 0.98),
                "entry_max": harga,
                "target1": int(harga * 1.05),
                "target2": int(harga * 1.11),
                "target3": int(harga * 1.15),
                "stop_loss": int(harga * 0.955)
            },
            
            "ma5": data["ma5"],
            "ma5_signal": ma5_signal,
            "ma20": data["ma20"],
            "ma20_signal": ma20_signal,
            "ma50": data["ma50"],
            "ma50_signal": ma50_signal,
            "ma100": data["ma100"],
            "ma100_signal": ma100_signal,
            
            "rsi": data["rsi"],
            "rsi_status": rsi_status,
            "macd": data["macd"],
            "macd_signal": macd_signal,
            "volume": data["volume"],
            
            "pe": data["pe"],
            "pbv": data["pbv"],
            "roe": data["roe"],
            
            "asing": "+125.5 M",
            "asing_ng": "+78.2 M",
            "retail": "-45.3 M",
            "mutual": "+22.1 M",
            "bandar_kesimpulan": "💡 Asing akumulasi 5 hari berturut-turut",
            
            "r3": resistance3,
            "r2": resistance2,
            "r1": resistance1,
            "s1": support1,
            "s2": support2,
            "s3": support3
        }
    
    def cari_saham(self, keyword):
        """Cari saham berdasarkan keyword"""
        keyword = keyword.upper()
        hasil = []
        
        for kode, data in self.saham_data.items():
            if keyword in kode or keyword in data["name"].upper():
                hasil.append({
                    "kode": kode,
                    "nama": data["name"],
                    "harga": data["harga"],
                    "change": data["change"],
                    "change_pct": data["change_pct"],
                    "sektor": data["sektor"]
                })
        
        return hasil[:10]  # Maksimal 10 hasil
    
    def get_screening(self, kategori):
        """Screening saham berdasarkan kategori"""
        hasil = []
        
        if kategori == "gainer":
            # Top gainer (urutkan berdasarkan change_pct tertinggi)
            saham_list = [(kode, data) for kode, data in self.saham_data.items()]
            saham_list.sort(key=lambda x: float(x[1]["change_pct"].replace("+", "").replace("%", "")), reverse=True)
            
            for kode, data in saham_list[:10]:
                hasil.append({
                    "kode": kode,
                    "nama": data["name"],
                    "harga": data["harga"],
                    "change": data["change"],
                    "change_pct": data["change_pct"],
                    "volume": data["volume"]
                })
        
        elif kategori == "loser":
            # Top loser (urutkan berdasarkan change_pct terendah)
            saham_list = [(kode, data) for kode, data in self.saham_data.items()]
            saham_list.sort(key=lambda x: float(x[1]["change_pct"].replace("-", "").replace("%", "")))
            
            for kode, data in saham_list[:10]:
                hasil.append({
                    "kode": kode,
                    "nama": data["name"],
                    "harga": data["harga"],
                    "change": data["change"],
                    "change_pct": data["change_pct"],
                    "volume": data["volume"]
                })
        
        elif kategori == "oversold":
            # Saham oversold (RSI < 35)
            for kode, data in self.saham_data.items():
                if data["rsi"] < 35:
                    hasil.append({
                        "kode": kode,
                        "nama": data["name"],
                        "harga": data["harga"],
                        "rsi": data["rsi"],
                        "change": data["change"],
                        "change_pct": data["change_pct"]
                    })
            hasil = sorted(hasil, key=lambda x: x["rsi"])[:10]
        
        elif kategori == "overbought":
            # Saham overbought (RSI > 70)
            for kode, data in self.saham_data.items():
                if data["rsi"] > 70:
                    hasil.append({
                        "kode": kode,
                        "nama": data["name"],
                        "harga": data["harga"],
                        "rsi": data["rsi"],
                        "change": data["change"],
                        "change_pct": data["change_pct"]
                    })
            hasil = sorted(hasil, key=lambda x: x["rsi"], reverse=True)[:10]
        
        elif kategori == "volume":
            # Volume tertinggi
            saham_list = [(kode, data) for kode, data in self.saham_data.items()]
            saham_list.sort(key=lambda x: x[1]["volume"], reverse=True)
            
            for kode, data in saham_list[:10]:
                hasil.append({
                    "kode": kode,
                    "nama": data["name"],
                    "harga": data["harga"],
                    "volume": data["volume"],
                    "change": data["change"],
                    "change_pct": data["change_pct"]
                })
        
        return hasil
    
    def get_ihsg(self):
        """Dapatkan data IHSG"""
        # Hitung IHSG berdasarkan rata-rata pergerakan saham
        total_perubahan = 0
        total_saham = len(self.saham_data)
        
        for data in self.saham_data.values():
            change_val = float(data["change_pct"].replace("+", "").replace("%", "").replace("-", ""))
            if "-" in data["change_pct"]:
                total_perubahan -= change_val
            else:
                total_perubahan += change_val
        
        ihsg_change = total_perubahan / total_saham if total_saham > 0 else 0.63
        
        return {
            "timestamp": datetime.now().strftime('%d/%m/%Y %H:%M WIB'),
            "ihsg": 7234.56,
            "change": f"{'+' if ihsg_change > 0 else ''}{ihsg_change:.2f}",
            "change_pct": f"{'+' if ihsg_change > 0 else ''}{ihsg_change:.2f}%",
            "lq45": 987.65,
            "lq45_change": "+8.76",
            "lq45_change_pct": "+0.89%",
            "idx30": 543.21,
            "idx30_change": "-2.34",
            "idx30_change_pct": "-0.43%",
            "support": 7150,
            "resistance": 7350,
            "volume": "12.5M"
        }
    
    def get_all_saham(self):
        """Dapatkan semua daftar saham"""
        return self.daftar_saham
