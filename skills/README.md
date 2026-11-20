# Скиллы

Глобальные скиллы для Claude Code, Codex, OpenCode и Antigravity. Источник — эта папка; подключение через символические ссылки описано в [README репозитория](../README.md).

Основа — копия скиллов [Matt Pocock](https://github.com/mattpocock/skills), сверенная с коммитом [`49dd158`](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336). Каталоги скиллов размещены в корне; файлы `agents/openai.yaml` содержат локальные метаданные Codex.

Что добавлено, изменено и удалено относительно оригинала — в [CHANGELOG.md](CHANGELOG.md).

## Основной маршрут

Основной маршрут для задачи: `explore` → `prepare` → `implement` (с согласованием после `prepare`). Для понятной локальной задачи достаточно сразу [implement](implement/SKILL.md).

- [explore](explore/SKILL.md) — выбрать подход, при необходимости собрать факты и сравнить варианты; завершается командой `/prepare` или `/implement`.
- [prepare](prepare/SKILL.md) — подготовить самодостаточный пакет в `.scratch/YYYY-MM-DD-<тема>/` ([SPEC.md](prepare/SPEC.md), [SPLIT.md](prepare/SPLIT.md)), согласовать открытые вопросы и вывести `/implement ./<путь-к-плану>` для новой сессии.
- [implement](implement/SKILL.md) — выполнить план или задачу как оркестратор с экономией контекста и ревью: быстрый путь (1–2 файла) проверяется в контексте; планы `.scratch/` и сложные правки делегируются субагентам-исполнителям с полным [review](review/SKILL.md) и [LOOP.md](review/LOOP.md) в read-only субагенте (несколько задач — [PLAN.md](implement/PLAN.md)).

Отдельно вызывать [review](review/SKILL.md) после `implement` не нужно: ревью и исправления уже проводятся в рамках `implement` (для плана из нескольких задач — на общем результате после интеграции). Самостоятельный `review` нужен для отдельной проверки изменений, коммитов или PR без правок кода (внутри лежат методики [BUGS.md](review/BUGS.md), [STANDARDS.md](review/STANDARDS.md) и [SPEC.md](review/SPEC.md)).

Перепроверка новых имён по [good-naming](good-naming/SKILL.md) входит в `implement` и `review`. Остальные навыки подключаются по условиям и остаются доступны для прямого вызова. [SPEC.md](prepare/SPEC.md) и [SPLIT.md](prepare/SPLIT.md) вызываются внутри `prepare` или напрямую при запросе ТЗ и декомпозиции.

| Группа | Навыки и назначение |
| --- | --- |
| Основной маршрут | `explore` — подход и сравнение вариантов; `prepare` — пакет решения (`SPEC.md`, `SPLIT.md`); `implement` — выполнение задачи или плана со встроенным ревью |
| Отдельные операции и модель | [doubt](doubt/SKILL.md) — необходимость и сложность будущего решения; [domain-modeling](domain-modeling/SKILL.md) — термины и ADR |
| Выполнение и упрощение | `implement`; [tdd](tdd/SKILL.md) — red-green-refactor; [simplify-code](simplify-code/SKILL.md) — упрощение существующего кода и логики |
| Ревью | [review](review/SKILL.md) — отдельная проверка изменений, коммитов или PR без правок (при работе через `implement` не вызывается отдельно): общий проход для небольшой правки или углублённая проверка по [BUGS.md](review/BUGS.md), [STANDARDS.md](review/STANDARDS.md), [SPEC.md](review/SPEC.md), [good-naming](good-naming/SKILL.md) и [simplify-code](simplify-code/SKILL.md) |
| Справочники и правила | [codebase-design](codebase-design/SKILL.md), [frontend-design](frontend-design/SKILL.md), [good-naming](good-naming/SKILL.md), [modern-web-guidance](modern-web-guidance/SKILL.md) |
| Ручные команды (`disable-model-invocation`) | [grilling](grilling/SKILL.md) — подробное интервью раундами; [handoff](handoff/SKILL.md) — передача контекста; [prototype](prototype/SKILL.md) — одноразовый эксперимент; [retro](retro/SKILL.md) — ретроспектива; [writing-for-agents](writing-for-agents/SKILL.md) — правила написания инструкций |

При доступности субагентов навыки по умолчанию делегируют широкое чтение, задачи плана и ревью; иначе выполняют последовательно сами. Нет обязательной зависимости от конкретного Skill tool, MCP, трекера или PR. Пакеты по умолчанию хранятся в `.scratch/YYYY-MM-DD-<тема>/` (в глобальном Git-игноре); публикация — по запросу. Для переноса копируй `skills/` целиком: ссылки относительные; при переносе одного навыка включи его зависимости.

Ревью использует [единый контракт изменений](review/CHANGES.md), включая staged, unstaged и untracked (кроме `.scratch/` и чужих грязных файлов вне задачи). Проверки читают одно состояние без правок. Для сложных задач исполнители завершают работу по [правилам отчёта](implement/REPORT.md). Сравнение вариантов интерфейса находится в справочнике [codebase-design/INTERFACES.md](codebase-design/INTERFACES.md).

## Миграция имён

| Было | Стало |
| --- | --- |
| code-review / review-changes | review (+ внутренние методики BUGS.md, STANDARDS.md, SPEC.md и внешний simplify-code) |
| review-bugs / review-standards / review-spec | review/BUGS.md, review/STANDARDS.md, review/SPEC.md |
| to-spec / write-spec | prepare/SPEC.md |
| to-tickets / split-work | prepare/SPLIT.md |
| brainstorm | explore |
| research | удалён (правила в AGENTS.md и explore) |
| grill-with-docs / design-plan | prepare |
| implement-spec / implement-plan | implement, работа с планом — implement/PLAN.md |
| design-options | codebase-design, сравнение — codebase-design/INTERFACES.md |

Из инструкций [PR-Agent](https://github.com/The-PR-Agent/pr-agent/tree/1fa93c85b64065d8944e6ac612605e4a27212361) сохранены адаптированные методики [review/BUGS.md](review/BUGS.md), [simplify-code](simplify-code/SKILL.md) и [отчёта исполнителя](implement/REPORT.md). Ссылки на исходники находятся в соответствующих документах.

## Лицензии

Авторская лицензия MIT сохранена в [LICENSE](LICENSE). У `frontend-design` своя лицензия Apache 2.0: [frontend-design/LICENSE.txt](frontend-design/LICENSE.txt). `good-css` перенесён в [архив](../archive/skills/good-css/SOURCE.md), `teach` — в [архив](../archive/skills/teach/SKILL.md). `modern-web-guidance` взят из [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance), [лицензия Apache 2.0](modern-web-guidance/LICENSE).
