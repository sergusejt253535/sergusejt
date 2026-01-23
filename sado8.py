<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>SADO VURGUN TAKİP MERKEZİ</title>
    <style>
        body { background-color: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; }
        .container { margin-top: 50px; border: 2px solid #00ff00; display: inline-block; padding: 20px; }
        .price-box { font-size: 24px; margin: 20px; border-bottom: 1px solid #333; padding: 10px; }
        .lang-en { color: #888; font-size: 14px; display: block; }
        .lang-tr { color: #fff; font-size: 18px; font-weight: bold; }
        h1 { text-shadow: 2px 2px #ff0000; }
    </style>
</head>
<body>
    <h1>SADO VURGUN TAKİP - LIVE DATA</h1>
    <div class="container" id="crypto-prices">
        <p>Veriler yükleniyor / Loading data...</p>
    </div>

    <script>
        async function getPrices() {
            try {
                const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin&vs_currencies=usd');
                const data = await response.json();
                
                document.getElementById('crypto-prices').innerHTML = `
                    <div class="price-box">
                        <span class="lang-en">Bitcoin (BTC) Price:</span>
                        <span class="lang-tr">Bitcoin Fiyatı: $${data.bitcoin.usd}</span>
                    </div>
                    <div class="price-box">
                        <span class="lang-en">Ethereum (ETH) Price:</span>
                        <span class="lang-tr">Ethereum Fiyatı: $${data.ethereum.usd}</span>
                    </div>
                    <div class="price-box">
                        <span class="lang-en">Binance Coin (BNB) Price:</span>
                        <span class="lang-tr">BNB Fiyatı: $${data.binancecoin.usd}</span>
                    </div>
                `;
            } catch (error) {
                document.getElementById('crypto-prices').innerHTML = "Hata! Veri alınamadı. / Error fetching data.";
            }
        }
        setInterval(getPrices, 30000); // 30 saniyede bir günceller
        getPrices();
    </script>
</body>
</html>
