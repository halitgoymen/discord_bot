# DJ Halit

Discord müzik botu. Sesli kanalda YouTube'dan şarkı çalar, kuyruk sistemi var.

## Komutlar

- `&p <arama/link>` — şarkı çal / kuyruğa ekle
- `&next` / `&n` — sıradaki şarkıya geç
- `&leave` — ses kanalından çık

## Teknoloji

- discord.py
- yt-dlp (YouTube ses çekme)
- ffmpeg (sistem PATH'inde kurulu olmalı — pip paketi değil)

## Kurulum

```
pip install -r requirements.txt
```

`.env` dosyasına `DISCORD_TOKEN` ekle (repo'ya commitlenmez, `.gitignore`'da).

## Çalıştırma

```
python bot.py
```

## Güvenlik notu

Bu repo'nun ilk sürümünde `.env` dosyası (içindeki `DISCORD_TOKEN` ile) yanlışlıkla
commitlenmişti. Git geçmişi temizlendi ve token rotate edildi (2026-08-29).
