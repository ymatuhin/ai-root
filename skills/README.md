# Скиллы

Глобальные скиллы для Claude Code, Codex, OpenCode и Antigravity. Источник — эта папка; подключение через символические ссылки описано в [README репозитория](../README.md).

## Активные скиллы (11)

### Автовызов (9)

| Навык | Назначение |
| --- | --- |
| [explore](explore/SKILL.md) | Поиск и выбор подхода: факты по первоисточникам, таблица вариантов (от «ничего не делать») и проверка на избыточность |
| [grilling](grilling/SKILL.md) | Пошаговое интервью раундами для согласования 3+ связанных развилок требований и узких кейсов |
| [domain-modeling](domain-modeling/SKILL.md) | Предметная модель, словарь терминов ([GLOSSARY-FORMAT.md](domain-modeling/GLOSSARY-FORMAT.md)) и запись ADR ([ADR-FORMAT.md](domain-modeling/ADR-FORMAT.md)) |
| [implement](implement/SKILL.md) | Выполнение задачи в коде со встроенным ревью, исправлением очевидных дефектов и согласованием спорных пунктов |
| [review](review/SKILL.md) | Ревью diff, ветки или локальных изменений без правки кода ([BUGS.md](review/BUGS.md), [STANDARDS.md](review/STANDARDS.md), [SPEC.md](review/SPEC.md), [CHANGES.md](review/CHANGES.md)) |
| [simplify-code](simplify-code/SKILL.md) | Упрощение существующего кода и логики (правки без смены поведения + блок «На обсуждение») |
| [good-naming](good-naming/SKILL.md) | Чеклист выбора и перепроверки имён в коде |
| [frontend-design](frontend-design/SKILL.md) | Визуальное направление, типографика и композиция интерфейсов |
| [modern-web-guidance](modern-web-guidance/SKILL.md) | Справочник современных веб-API и UI-паттернов |

### Ручные (`disable-model-invocation: true`) (2)

| Навык | Назначение |
| --- | --- |
| [handoff](handoff/SKILL.md) | Сводка сессии в `.scratch/` для продолжения в новой сессии |
| [retro](retro/SKILL.md) | Ретроспектива сессии и предложения по улучшению правил и окружения |

## Архив

Неиспользуемые навыки сохранены в [archive/skills/](../archive/skills/): `codebase-design`, `doubt`, `good-css`, `prepare`, `prototype`, `tdd`, `teach`, `writing-for-agents`.

## Лицензии

Основа части навыков — [Matt Pocock](https://github.com/mattpocock/skills), лицензия MIT в [LICENSE](LICENSE). У `frontend-design` — Apache 2.0 ([frontend-design/LICENSE.txt](frontend-design/LICENSE.txt)). `modern-web-guidance` — из [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance), Apache 2.0 ([modern-web-guidance/LICENSE](modern-web-guidance/LICENSE)). История изменений — в [CHANGELOG.md](CHANGELOG.md).
