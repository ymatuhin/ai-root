# Скиллы

Глобальные скиллы для Claude Code, Codex и OpenCode. Источник — эта папка; подключение через символические ссылки описано в [README репозитория](../README.md).

Основа — копия скиллов [Matt Pocock](https://github.com/mattpocock/skills), сверенная с коммитом [`49dd158`](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336). Каталоги скиллов размещены в корне; файлы `agents/openai.yaml` содержат локальные метаданные Codex.

Что добавлено, изменено и удалено относительно оригинала — в [CHANGELOG.md](CHANGELOG.md).

## Основной flow

Основные команды:

- [explore](explore/SKILL.md) — выбрать подход, когда он ещё не определён. Исследование, сравнение и проверка сложности подключаются по необходимости.
- [design-plan](design-plan/SKILL.md) — подготовить выбранное решение к реализации и согласовать существенные вопросы.
- [implement](implement/SKILL.md) — выполнить понятную задачу или согласованный план. Для плана из нескольких задач сам подключает [implement-plan](implement-plan/SKILL.md).
- [review-changes](review-changes/SKILL.md) — проверить изменения без правок.

Для понятной задачи достаточно implement. Если сначала нужно выбрать и уточнить решение: explore → design-plan → согласование → implement. Ревью входит в реализацию; отдельно его вызывают для самостоятельной проверки.

Остальные навыки подключаются по условиям и остаются доступны для прямого вызова. write-spec, split-work и отдельные проходы ревью не требуют ручного запуска на каждом этапе.

| Группа | Навыки и назначение |
| --- | --- |
| Подготовка решения и выполнение плана | explore — подход; design-plan — пакет решения; implement-plan — внутреннее выполнение согласованных задач |
| Отдельные операции | [research](research/SKILL.md) — факты; [brainstorm](brainstorm/SKILL.md) — подходы; [doubt](doubt/SKILL.md) — необходимость и сложность будущего решения |
| Подготовка решения | [grilling](grilling/SKILL.md) — уточнение; [domain-modeling](domain-modeling/SKILL.md) — термины и ADR; [write-spec](write-spec/SKILL.md) — требования; [split-work](split-work/SKILL.md) — задачи и зависимости |
| Выполнение и проверка | implement; [tdd](tdd/SKILL.md) — тесты и рефакторинг на зелёном; [review-bugs](review-bugs/SKILL.md) — дефекты; [review-standards](review-standards/SKILL.md) — документированные правила; [review-spec](review-spec/SKILL.md) — требования; [simplify-code](simplify-code/SKILL.md) — упрощение существующего кода |
| Дополнительные оркестраторы | [review-changes](review-changes/SKILL.md) — общее ревью; [design-options](design-options/SKILL.md) — варианты интерфейса |
| Справочники и правила | [codebase-design](codebase-design/SKILL.md), [frontend-design](frontend-design/SKILL.md), [good-naming](good-naming/SKILL.md), [good-css](good-css/SKILL.md), [writing-for-agents](writing-for-agents/SKILL.md) |
| Дополнительные операции | [handoff](handoff/SKILL.md) — передача контекста на любом этапе; [prototype](prototype/SKILL.md) — отдельный эксперимент; [teach](teach/SKILL.md), [retro](retro/SKILL.md) |

При отсутствии субагентов оркестраторы выполняют проходы последовательно. Нет обязательной зависимости от конкретного Skill tool, MCP, трекера или PR. Спецификации, планы и задачи по умолчанию хранятся в локальной папке `.scratch/<тема>/`; публикация выполняется по запросу. Для переноса набора копируй `skills/` целиком: межнавыковые ссылки относительные. При переносе одного навыка включи его явно указанные зависимости.

Ревью использует [единый контракт изменений](review-changes/CHANGES.md), включая staged, unstaged и untracked. Проверки читают одно состояние без правок. Исполнители завершают работу по [правилам отчёта](implement/REPORT.md).

## Миграция имён

| Было | Стало |
| --- | --- |
| code-review | review-standards + review-spec + simplify-code, оркестрация в review-changes |
| to-spec / to-tickets | write-spec / split-work |
| grill-with-docs | design-plan |
| implement-spec | implement-plan |

Из инструкций [PR-Agent](https://github.com/The-PR-Agent/pr-agent/tree/1fa93c85b64065d8944e6ac612605e4a27212361) сохранены адаптированные методики review-bugs, simplify-code и отчёта исполнителя. Ссылки на исходники находятся в соответствующих документах.

## Лицензии

Авторская лицензия MIT сохранена в [LICENSE](LICENSE). У `frontend-design` своя лицензия Apache 2.0: [frontend-design/LICENSE.txt](frontend-design/LICENSE.txt). `good-css` взят из vojtaholik/good-css: [версия и обновление](good-css/SOURCE.md), [лицензия MIT](good-css/LICENSE.txt).
