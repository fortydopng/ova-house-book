# ova-house-book

Статический сайт-книга визуализаций. Собирается из `content/book.yaml` командой `python build.py`; результат в `docs/` публикуется GitHub Pages.

Новые изображения: `python ingest.py <room-slug> <version> <png...>` → `docs/img/<room-slug>/v<version>/`, затем добавить записи в `content/book.yaml` и пересобрать.
