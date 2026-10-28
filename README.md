# Elnur: хранение файлов любого размера в S3-совместимом облаке

Скрипт storage_local.py загружает и скачивает файлы любого размера
(большие файлы загружаются частями, multipart), создаёт временные ссылки.

## Запуск
    pip install boto3 "moto[server]"
    nohup moto_server -p 9000 > moto.log 2>&1 &
    python storage_local.py upload файл ключ
    python storage_local.py list
    python storage_local.py download ключ файл
    python storage_local.py url ключ

Код совместим с AWS S3: достаточно убрать endpoint_url и указать свои ключи.
