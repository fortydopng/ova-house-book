# ova-house-book

Статический сайт-книга визуализаций. Собирается из `content/book.yaml` командой `python build.py`; результат в `docs/` публикуется GitHub Pages.

Новые изображения: `python ingest.py <room-slug> <version> <png...>` → `docs/img/<room-slug>/v<version>/`, затем добавить записи в `content/book.yaml` и пересобрать.

Референсы стиля (страница `docs/references/`): содержание в `content/references.yaml` (группы, REF-ID, названия, описания, размеры).
Изображения: `python ingest.py refs 1 ref-001.jpg ref-002.jpg ...` → `docs/img/refs/v1/`, затем `python build.py`.

Варианты камина: основная страница `docs/fireplace/` — `content/fireplace.yaml` (уточнённое направление, К-46…), ранние направления `docs/fireplace/earlier/` — `content/fireplace_earlier.yaml` (К-01…К-45); нумерация К-NN сквозная по обеим страницам, изображения общие.
Изображения: `python ingest.py fireplace 1 k-01-1.png ...` → `docs/img/fireplace/v1/`, затем `python crop_fireplace.py` (вырезки для ленты) и `python build.py`.
REF-ID совпадают со стилевым альбомом v01 на Google Drive; новые изображения продолжают нумерацию.
