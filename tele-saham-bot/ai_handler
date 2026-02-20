import random
from datetime import datetime

class AIHandler:
    def __init__(self):
        self.context = {}
    
    async def ask(self, question):
        """Proses pertanyaan dan berikan jawaban"""
        
        question_lower = question.lower()
        
        # Deteksi keyword
        if "rsi" in question_lower:
            return self._answer_rsi(question)
        elif "macd" in question_lower:
            return self._answer_macd(question)
        elif "double bottom" in question_lower or "double bottom" in question_lower:
            return self._answer_double_bottom(question)
        elif "candlestick" in question_lower or "candle" in question_lower:
            return self._answer_candlestick(question)
        elif "pe" in question_lower or "p/e" in question_lower or "price to earning" in question_lower:
            return self._answer_pe(question)
        elif "day trade" in question_lower or "daytrade" in question_lower:
            return self._answer_daytrade(question)
        elif "swing" in question_lower:
            return self._answer_swing(question)
        elif "bbca" in question_lower:
            return self._answer_bbca(question)
        else:
            return self._answer_default(question)
    
    def _answer_rsi(self, question):
        return """
📊 *RELATIVE STRENGTH INDEX (RSI)*

RSI adalah indikator momentum yang mengukur kecepatan dan perubahan pergerakan harga.

🔴 *INTERPRETASI:*
• RSI > 70 = Overbought (jenuh beli) - potensi koreksi
• RSI < 30 = Oversold (jenuh jual) - potensi rebound
• RSI 30-70 = Normal

📌 *CONTOH:* 
Jika RSI BBCA 34.7, artinya mendekati oversold, tekanan jual mulai berkurang, potensi rebound.

🎯 *PENGGUNAAN:*
• Cari sinyal beli saat RSI < 30 dan mulai naik
• Cari sinyal jual saat RSI > 70 dan mulai turun
• Kombinasikan dengan support resistance dan volume

⚠️ *CATATAN:* 
RSI tidak boleh digunakan sendirian. Selalu kombinasikan dengan indikator lain!
        """
    
    def _answer_macd(self, question):
        return """
📊 *MOVING AVERAGE CONVERGENCE DIVERGENCE (MACD)*

MACD adalah indikator trend-following yang menunjukkan hubungan antara dua moving average.

🔴 *KOMPONEN MACD:*
• MACD Line (Cepat) - EMA 12
• Signal Line (Lambat) - EMA 26
• Histogram - Selisih MACD dan Signal

📌 *SINYAL:*
• MACD crossover (MACD potong Signal ke atas) = BULLISH
• MACD crossunder (MACD potong Signal ke bawah) = BEARISH
• Histogram hijau = Momentum naik
• Histogram merah = Momentum turun

🎯 *STRATEGI:*
• Beli saat MACD crossover dan histogram mulai positif
• Jual saat MACD crossunder dan histogram mulai negatif
• Divergence MACD bisa menandakan reversal
        """
    
    def _answer_double_bottom(self, question):
        return """
📊 *POLA DOUBLE BOTTOM (W-SHAPED)*

Double Bottom adalah pola reversal bullish yang terbentuk setelah tren turun.

🔍 *KARAKTERISTIK:*
• Bottom 1: Harga turun ke level terendah
• Rebound: Harga naik sementara (neckline)
• Bottom 2: Harga turun lagi ke level yang sama
• Breakout: Harga menembus neckline

📌 *KONFIRMASI VALID:*
• Jarak antar bottom: 1-4 minggu
• Bottom 2 tidak lebih rendah dari bottom 1
• Volume lebih besar di bottom 2
• Breakout dengan volume minimal 1.5x

📈 *TARGET HARGA:*
Tinggi pola (neckline - bottom) diproyeksikan ke atas
Contoh: Neckline 7,350 - Bottom 7,025 = 325 poin
Target: 7,350 + 325 = 7,675

⚠️ *RISIKO:*
• False breakout
• Bottom failure
• Butuh konfirmasi 2-3 hari
        """
    
    def _answer_candlestick(self, question):
        return """
📊 *POLA CANDLESTICK*

Candlestick adalah metode charting yang menunjukkan 4 harga: Open, High, Low, Close.

🕯️ *BAGIAN CANDLESTICK:*
• Body: Selisih Open dan Close
• Shadow/Wick: Harga tertinggi/terendah
• Bullish (hijau/putih): Close > Open
• Bearish (merah/hitam): Close < Open

📈 *POLA BULLISH:*
• Hammer: Bottom reversal
• Engulfing Bullish: Body besar telan body kecil
• Morning Star: 3 candle reversal
• Doji: Indecision, potensi reversal

📉 *POLA BEARISH:*
• Shooting Star: Top reversal
• Engulfing Bearish: Body besar telan body kecil
• Evening Star: 3 candle reversal
• Hanging Man: Potensi top

🎯 *STRATEGI:*
• Kombinasikan dengan support resistance
• Perhatikan volume di pola konfirmasi
• Tunggu close untuk validasi
        """
    
    def _answer_pe(self, question):
        return """
💰 *PRICE TO EARNING RATIO (P/E)*

P/E Ratio adalah valuasi yang membandingkan harga saham dengan laba per saham.

📊 *RUMUS:*
P/E = Harga Saham / Earning Per Share (EPS)

🔴 *INTERPRETASI:*
• P/E Tinggi (>20): Growth stock, overvalued, ekspektasi tinggi
• P/E Rendah (<10): Value stock, undervalued, mungkin ada masalah
• P/E Wajar (10-20): Normal untuk pasar Indonesia

📌 *CONTOH PERBANDINGAN:*
• BBCA P/E 21.5: Growth, kualitas bagus
• BBRI P/E 15.3: Value, masih wajar
• TLKM P/E 12.1: Murah, mungkin kurang growth

⚠️ *CATATAN PENTING:*
• Bandingkan dengan P/E sektor dan historis
• P/E rendah belum tentu murah
• P/E tinggi belum tentu mahal
• Kombinasikan dengan PBV, ROE, dan DER
        """
    
    def _answer_daytrade(self, question):
        return """
⚡ *STRATEGI DAY TRADE UNTUK PEMULA*

Day trade adalah strategi membeli dan menjual saham dalam 1 hari yang sama.

📋 *PERSIAPAN:*
1. Modal minimal Rp 10-20 juta
2. Pilih saham likuid (LQ45/IDX30)
3. Siapkan platform real-time
4. Tentukan target profit & cut loss

🎯 *KRITERIA SAHAM DAY TRADE:*
• Volume tinggi (>10M/hari)
• Volatilitas cukup (2-5% pergerakan)
• Spread tipis (beda beli-jual kecil)
• Trending di 30 menit pertama

📊 *INDIKATOR FAVORIT:*
• RSI (14) untuk momentum
• Volume untuk konfirmasi
• Support Resistance intraday
• Moving Average 5 & 20

💡 *STRATEGI DASAR:*
1. *Breakout:* Beli saat tembus resist dengan volume
2. *Pullback:* Beli di support saat uptrend
3. *Reversal:* Beli di oversold dengan konfirmasi

⚠️ *RISIKO & MANAJEMEN:*
• Target profit 1-3%, cut loss 1%
• Maksimal 2-3 transaksi per hari
• Jangan averaging loss
• Istirahat jika 2 kali loss berturut-turut

📌 *GOLDEN RULES:*
• Cut loss cepat, profit berjalan
• Jangan serakah, ambil profit bertahap
• Hindari trading di berita besar
• Evaluasi setiap transaksi
        """
    
    def _answer_swing(self, question):
        return """
📊 *STRATEGI SWING TRADING*

Swing trading adalah strategi memegang saham 3 hari hingga 1 bulan.

📋 *KARAKTERISTIK:*
• Timeframe: 3 hari - 1 bulan
• Target profit: 5-15%
• Stop loss: 3-5%
• Frekuensi: 3-5 transaksi/bulan

🎯 *KRITERIA SAHAM SWING:*
• Trending (uptrend/downtrend jelas)
• Volume konsisten
• Support resistance kuat
• Indikator menunjukkan momentum

📊 *INDIKATOR FAVORIT:*
• MA20 & MA50 untuk trend
• RSI untuk entry point
• MACD untuk konfirmasi
• Volume untuk validasi

💡 *STRATEGI DASAR:*
1. *Trend Following:* Beli di pullback saat uptrend
2. *Breakout:* Beli saat tembus resist dengan volume
3. *Reversal:* Beli di oversold dengan konfirmasi pola

⚠️ *RISIKO & MANAJEMEN:*
• Risk/reward minimal 1:2
• Diversifikasi 3-5 saham
• Cut loss disiplin
• Ambil profit bertahap
        """
    
    def _answer_bbca(self, question):
        return """
📊 *ANALISIS BBCA (Bank Central Asia Tbk)*

💰 *HARGA: Rp 7.175* (-1.37%)

📊 *TEKNIKAL:*
• RSI: 34.7 (Mendekati oversold)
• MA5: 7.285 (DI ATAS HARGA) - Bearish
• MA20: 7.290 (DI ATAS HARGA) - Bearish
• MA50: 7.150 (DI BAWAH HARGA) - Bullish
• MA100: 7.050 (DI BAWAH HARGA) - Bullish

📈 *KESIMPULAN:*
• Short term: Bearish (tekanan jual)
• Long term: Bullish (trend naik)
• Potensi rebound dalam waktu dekat

🎯 *LEVEL PENTING:*
• Support: 7.050 (MA100) | 6.850
• Resistance: 7.550 | 7.950

⚡ *REKOMENDASI:*
• Day Trade: Buy di 7.139-7.175, target 7.246-7.320
• Swing: Buy di 7.031-7.175, target 7.550-7.950
• Long Term: Accumulate di 7.050-7.175
        """
    
    def _answer_default(self, question):
        answers = [
            "Untuk pertanyaan spesifik tentang saham, silakan tanya dengan lebih detail. Contoh: 'Apa itu RSI?' atau 'Bagaimana analisis BBCA?'",
            
            "Saya bisa membantu analisis teknikal, fundamental, atau strategi trading. Coba tanya tentang indikator tertentu atau saham tertentu!",
            
            "Maaf, saya belum bisa menjawab pertanyaan itu. Coba tanya tentang: RSI, MACD, Double Bottom, Candlestick, P/E Ratio, atau strategi Day Trade.",
            
            "Untuk informasi lebih akurat, silakan gunakan fitur Analisis Saham di menu utama. Di sana ada data real-time dan indikator lengkap.",
            
            "Pertanyaan bagus! Tapi saya perlu informasi lebih spesifik. Bisa tanya tentang saham tertentu (BBCA, TLKM) atau indikator tertentu (RSI, MACD)?"
        ]
        return random.choice(answers)
