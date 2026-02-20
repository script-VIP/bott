from datetime import datetime
import random

class SahamHandler:
    def __init__(self):
        self.saham_data = {
            "BBCA": {
                "name": "Bank Central Asia Tbk",
                "harga": 7175,
                "change": -100,
                "change_pct": "-1.37%",
                "ma5": 7285,
                "ma20": 7290,
                "ma50": 7150,
                "ma100": 7050,
                "rsi": 34.7,
                "macd": -172.08,
                "volume": 15234500
            },
            "BBRI": {
                "name": "Bank Rakyat Indonesia Tbk",
                "harga": 5450,
                "change": 75,
                "change_pct": "+1.40%",
                "ma5": 5420,
                "ma20": 5380,
                "ma50": 5320,
                "ma100": 5250,
                "rsi": 48.2,
                "macd": -45.3,
                "volume": 78500000
            },
            "TLKM": {
                "name": "Telkom Indonesia Tbk",
                "harga": 3890,
                "change": -85,
                "change_pct": "-2.14%",
                "ma5": 3920,
                "ma20": 3950,
                "ma50": 3880,
                "ma100": 3820,
                "rsi": 32.1,
                "macd": -98.5,
                "volume": 178000000
            },
            "BMRI": {
                "name": "Bank Mandiri Tbk",
                "harga": 10325,
                "change": 345,
                "change_pct": "+3.45%",
                "ma5": 10200,
                "ma20": 10050,
                "ma50": 9850,
                "ma100": 9600,
                "rsi": 62.5,
                "macd": 125.3,
                "volume": 45200000
            },
            "GOTO": {
                "name": "GoTo Gojek Tokopedia Tbk",
                "harga": 345,
                "change": 45,
                "change_pct": "+15.00%",
                "ma5": 320,
                "ma20": 310,
                "ma50": 295,
                "ma100": 280,
                "rsi": 72.5,
                "macd": 15.2,
                "volume": 1200000000
            }
        }
    
    def get_analisis(self, kode):
        """Dapatkan data analisis saham"""
        kode = kode.upper()
        data = self.saham_data.get(kode, self.saham_data["BBCA"])
        
        # Hitung target berdasarkan harga
        harga = data["harga"]
        
        return {
            "timestamp": datetime.now().strftime('%d/%m/%Y %H:%M WIB'),
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
            "ma5_signal": "DI BAWAH" if harga < data["ma5"] else "DI ATAS",
            "ma20": data["ma20"],
            "ma20_signal": "DI BAWAH" if harga < data["ma20"] else "DI ATAS",
            "ma50": data["ma50"],
            "ma50_signal": "DI BAWAH" if harga < data["ma50"] else "DI ATAS",
            "ma100": data["ma100"],
            "ma100_signal": "DI BAWAH" if harga < data["ma100"] else "DI ATAS",
            
            "rsi": data["rsi"],
            "rsi_status": "OVERSOLD" if data["rsi"] < 35 else "OVERBOUGHT" if data["rsi"] > 70 else "NETRAL",
            "macd": data["macd"],
            "macd_signal": "BEARISH" if data["macd"] < 0 else "BULLISH",
            
            "asing": "+125.5 M" if kode == "BBCA" else "+312 M",
            "asing_ng": "+78.2 M" if kode == "BBCA" else "+145 M",
            "retail": "-45.3 M" if kode == "BBCA" else "-78 M",
            "bandar_kesimpulan": "💡 Asing akumulasi 5 hari berturut-turut",
            
            "r3": int(harga * 1.15),
            "r2": int(harga * 1.11),
            "r1": int(harga * 1.05),
            "s1": int(harga * 0.98),
            "s2": int(harga * 0.955),
            "s3": int(harga * 0.89)
        }
    
    def get_ihsg(self):
        """Dapatkan data IHSG"""
        return {
            "timestamp": datetime.now().strftime('%d/%m/%Y %H:%M WIB'),
            "ihsg": 7234.56,
            "change": "+45.67",
            "change_pct": "+0.63%",
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
