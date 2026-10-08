# Doğrulama / Verification
`pytest`: **4 passed**. Komutlar, dil, kullanıcı ayrımı, özel sohbet kısıtı, girdi doğrulama, kalıcılık ve çevrimdışı SDK kurulumu / Commands, language, user isolation, private-chat restriction, validation, persistence, and offline SDK construction.

`python bot.py --demo` başarılı; bu önceki çevrimdışı kontrol ağ bağlantısı kullanmadı. / The earlier offline demo succeeded without a network connection.

## Gerçek bot elle testi / Real-bot manual testing

8 Ekim / October 2026 — Kullanıcı tarafından gerçek Telegram botuyla elle test edildi: /add, /list, /done, /lang. / Manually tested by the author with a real Telegram bot: /add, /list, /done, /lang.

Kaynak: kullanıcının bu sohbetteki test bildirimi; asistan Telegram’a bağlanmadı. / Source: the author’s test report in this chat; the assistant did not connect to Telegram.

/delete ve ağ kesintisi senaryoları gerçek botla doğrulanmadı. / Real-bot /delete and network outage scenarios remain unverified.
