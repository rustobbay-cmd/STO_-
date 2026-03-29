# STO_Garag Clean

Чистая и безопасная версия Telegram-бота для записи на СТО.

## Что исправлено
- удалены секреты из репозитория;
- проект переведён на безопасную конфигурацию через `.env`;
- убран мусор: `venv`, локальная база, служебные файлы;
- монолит разбит на модули;
- SQLite вынесен в отдельный слой;
- добавлен `.gitignore`;
- добавлены инструкции для Windows и Linux.

## Важно
Старый токен бота нужно **обязательно перевыпустить** через BotFather, если он когда-либо был опубликован в GitHub.

## Структура
```
app/
  bot.py
  config.py
  states.py
  handlers/
    admin.py
    booking.py
    common.py
  keyboards/
    reply.py
    inline.py
  services/
    scheduler.py
  db/
    sqlite.py
main.py
.env.example
requirements.txt
```

## Быстрый запуск
### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# заполните BOT_TOKEN и ADMIN_ID в .env
python main.py
```

### Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# заполните BOT_TOKEN и ADMIN_ID в .env
python main.py
```

## Логика
- запись на 2 услуги: развал-схождение и ремонт ходовой;
- рабочие часы по умолчанию: 09:00–18:00;
- запись на ближайшие 7 дней;
- просмотр и отмена своих записей;
- админ видит план работ, может продлить заказ или завершить его.

## Что не хранить в Git
- `.env`
- `*.db`
- `.venv/`
