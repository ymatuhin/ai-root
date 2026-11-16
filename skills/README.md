# Скиллы

Глобальные скиллы для Claude Code, Codex, OpenCode и Antigravity. Источник — эта папка; подключение через символические ссылки описано в [README репозитория](../README.md).

Основа — копия скиллов [Matt Pocock](https://github.com/mattpocock/skills), сверенная с коммитом [`49dd158`](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336). Каталоги скиллов размещены в корне; файлы `agents/openai.yaml` содержат локальные метаданные Codex.

Что добавлено, изменено и удалено относительно оригинала — в [CHANGELOG.md](CHANGELOG.md).

## Основной flow

Основные команды:

- [explore](explore/SKILL.md) — выбрать подход, когда он ещё не определён. Исследование, сравнение и проверка сложности подключаются по необходимости.
- [design-plan](design-plan/SKILL.md) — подготовить выбранное решение к реализации и согласовать существенные вопросы.
- [implement](implement/SKILL.md) — выполнить понятную задачу или согласованный план: для локальных правок работает быстрый путь с самопроверкой и кратким отчётом, для сложных и рискованных — полный цикл ревью; порядок работы с несколькими задачами описан в [PLAN.md](implement/PLAN.md).
- [review-changes](review-changes/SKILL.md) — проверить изменения без правок (внутри лежат методики [BUGS.md](review-changes/BUGS.md), [STANDARDS.md](review-changes/STANDARDS.md) и [SPEC.md](review-changes/SPEC.md)).

Для понятной задачи достаточно implement. Если сначала нужно выбрать и уточнить решение: explore → design-plan → согласование → implement. Перепроверка новых имён по [good-naming](good-naming/SKILL.md) входит в implement и review-changes.

Остальные навыки подключаются по условиям и остаются доступны для прямого вызова. write-spec и split-work вызываются внутри design-plan по необходимости.

| Группа | Навыки и назначение |
| --- | --- |
| Подготовка решения и выполнение плана | explore — подход; design-plan — пакет решения; implement — задача или план |
| Отдельные операции | [research](research/SKILL.md) — факты; [brainstorm](brainstorm/SKILL.md) — сравнение подходов; [doubt](doubt/SKILL.md) — необходимость и сложность будущего решения |
| Подготовка решения | [domain-modeling](domain-modeling/SKILL.md) — термины и ADR; [write-spec](write-spec/SKILL.md) — требования; [split-work](split-work/SKILL.md) — задачи и зависимости |
| Выполнение и упрощение | implement; [tdd](tdd/SKILL.md) — red-green-refactor; [simplify-code](simplify-code/SKILL.md) — упрощение существующего кода |
| Ревью | [review-changes](review-changes/SKILL.md) — общий проход для небольшой правки или углублённая проверка по [BUGS.md](review-changes/BUGS.md), [STANDARDS.md](review-changes/STANDARDS.md), [SPEC.md](review-changes/SPEC.md), [good-naming](good-naming/SKILL.md) и [simplify-code](simplify-code/SKILL.md) |
| Справочники и правила | [codebase-design](codebase-design/SKILL.md), [frontend-design](frontend-design/SKILL.md), [good-naming](good-naming/SKILL.md), [modern-web-guidance](modern-web-guidance/SKILL.md), [writing-for-agents](writing-for-agents/SKILL.md) |
| Ручные команды (`disable-model-invocation`) | [grilling](grilling/SKILL.md) — подробное интервью раундами; [handoff](handoff/SKILL.md) — передача контекста; [teach](teach/SKILL.md); [retro](retro/SKILL.md) |
| Дополнительные операции | [prototype](prototype/SKILL.md) — одноразовый эксперимент |

При отсутствии субагентов оркестраторы выполняют проходы последовательно. Нет обязательной зависимости от конкретного Skill tool, MCP, трекера или PR. Спецификации, планы и задачи по умолчанию хранятся в локальной папке `.scratch/<тема>/` (игнорируемой через глобальный Git-игнор без правок `.gitignore` репозиториев); публикация выполняется по запросу. Для переноса набора копируй `skills/` целиком: межнавыковые ссылки относительные. При переносе одного навыка включи его явно указанные зависимости.

Ревью использует [единый контракт изменений](review-changes/CHANGES.md), включая staged, unstaged и untracked (кроме `.scratch/` и чужих грязных файлов вне задачи). Проверки читают одно состояние без правок. Для сложных задач исполнители завершают работу по [правилам отчёта](implement/REPORT.md). Сравнение вариантов интерфейса находится в справочнике [codebase-design/INTERFACES.md](codebase-design/INTERFACES.md).

## Миграция имён

| Было | Стало |
| --- | --- |
| code-review | review-changes (+ внутренние методики BUGS.md, STANDARDS.md, SPEC.md и внешний simplify-code) |
| review-bugs / review-standards / review-spec | review-changes/BUGS.md, review-changes/STANDARDS.md, review-changes/SPEC.md |
| to-spec / to-tickets | write-spec / split-work |
| grill-with-docs | design-plan |
| implement-spec / implement-plan | implement, работа с планом — implement/PLAN.md |
| design-options | codebase-design, сравнение — codebase-design/INTERFACES.md |

Из инструкций [PR-Agent](https://github.com/The-PR-Agent/pr-agent/tree/1fa93c85b64065d8944e6ac612605e4a27212361) сохранены адаптированные методики [review-changes/BUGS.md](review-changes/BUGS.md), [simplify-code](simplify-code/SKILL.md) и [отчёта исполнителя](implement/REPORT.md). Ссылки на исходники находятся в соответствующих документах.

## Лицензии

Авторская лицензия MIT сохранена в [LICENSE](LICENSE). У `frontend-design` своя лицензия Apache 2.0: [frontend-design/LICENSE.txt](frontend-design/LICENSE.txt). `good-css` перенесён в [архив](../archive/skills/good-css/SOURCE.md). `modern-web-guidance` взят из [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance), [лицензия Apache 2.0](modern-web-guidance/LICENSE).
