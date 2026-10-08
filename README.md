# Telegram görev botu / Telegram task bot
**Kurgusal demo proje / Fictional demo project.**

## Türkçe
Python, python-telegram-bot ve SQLite ile özel sohbetlere ait görev listesi. Her kullanıcı kendi kayıtlarını görür. `/lang tr` ve `/lang en` ile yanıt dili değişir; `/add`, `/list`, `/done`, `/delete` komutları vardır.

Python 3.12+ sanal ortamında `python -m pip install -r requirements.txt` çalıştır. Anahtarsız kontrol:
```powershell
python -m pytest -q
python bot.py --demo
```
Gerçek kullanım için BotFather üzerinden botu sen oluştur. Tokenı terminal ortam değişkeni `TELEGRAM_BOT_TOKEN` olarak kendin ayarla, ardından `python bot.py` çalıştır. Tokenı dosyaya/README'ye yazma. `.env.example` yalnızca boş örnektir; otomatik `.env` yükleme yoktur. Veritabanı varsayılan `data/tasks.sqlite`; `TASK_DATABASE` ile değiştirilebilir. Durdurma: Ctrl+C. Son 10 görev gösterilir; kullanıcı başına en fazla 100 kayıt, görev başına en fazla 200 karakter. `/delete id` kaydı kalıcı siler.

Kullanıcı tarafından gerçek Telegram botuyla elle test edildi: /add, /list, /done, /lang. Bu doğrulama 8 Ekim 2026 tarihli kullanıcı beyanına dayanır. Ayrıca dört otomatik test, AsyncMock ve geçici SQLite ile geçti. /delete komutunun gerçek bot testi ve Telegram ağ kesintisi senaryoları doğrulanmadı.

## English
A private-chat task bot built with Python, python-telegram-bot, and SQLite. Entries are scoped to each user. Commands: `/add`, `/list`, `/done`, `/delete`, `/lang tr`, `/lang en`.

Install requirements in a Python 3.12+ virtual environment and run the tests/offline demo above. For live use, create the bot yourself through BotFather, set `TELEGRAM_BOT_TOKEN` in your terminal environment, then run `python bot.py`. Do not write the token to committed files. The blank `.env.example` is illustrative; no automatic dotenv loading. Set `TASK_DATABASE` to override the default local database. Last 10 entries are listed; up to 100 entries/user and 200 characters/task. `/delete id` permanently deletes that entry. Stop with Ctrl+C.

Manually tested by the author with a real Telegram bot: /add, /list, /done, /lang. This verification is based on the author’s report dated 8 October 2026. Four automated tests also passed using AsyncMock and temporary SQLite. Real-bot testing of /delete and Telegram network outage scenarios remain unverified.
