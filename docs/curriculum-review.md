# Аудит детальной программы — шаг 02

Дата: **2026-10-18**. Статус: **структурная проверка пройдена**, программа по содержанию остаётся черновиком до первых занятий. Проверяется программа, не освоение студентом и не работоспособность будущих лабораторий.

## Область

17 модулей, 28 разделов, 135 запланированных микрозанятий по 60 минут; 45 плановых самостоятельных lab-блоков; 28 банков с 224 авторскими вопросами и отдельными критериями. Полнотекстовые уроки, исполняемые lab и готовые экзамены не создавались.

## Проверка

Read-only инструмент: `python3 -B scripts/check_curriculum.py`. Самопроверка валидатора на синтетических ошибках: `python3 -B scripts/check_curriculum.py --self-test`. Никаких сетевых действий, изменения прогресса, установки зависимостей или выполнения labs эти команды не делают.

| Проверка | Результат |
|---|---|
| Самопроверка валидатора | 7 тестов: корректная модель, неправильное время, отсутствующий prerequisite, ссылка вперёд/цикл, дублирование ID, M внутри A, пропущенное микрозанятие — успешно |
| ID и зависимости | 17 модулей / 28 разделов / 135 уроков; проверка существования prerequisites и отсутствия ссылок вперёд/циклов — успешно |
| Время | Все 45 недель по 180/60/180/60 минут; A=240 ч, B=120 ч, всего 360 ч — успешно |
| Практика | 45 lab-ID; у каждой недели конкретные контрольные точки, артефакт, негативный кейс и критерий — успешно |
| Интервью | 224 уникальных Q-ID; 5 базовых + 2 troubleshooting + 1 tradeoff на раздел, ключи отдельно — успешно |
| Ссылки и формат | 865 локальных ссылок, в том числе якоря ID: цели существуют; UTF-8/переводы строк/пробелы проверены во всех изменённых документах |
| Исходные материалы и личные записи | SHA-256 14 исходных файлов/правил/личных индексов совпадает со снимком: 8 промптов, 2 расшифровки, README_START, AGENTS, notes/README и results/README; ответы/даты/баллы студента не созданы |

## Педагогический аудит

- В A приоритет Linux/Networking/диагностики; J0/J1 указаны у каждой темы. Helm/Argo/Vault и углублённая устойчивость не являются prerequisites первой Junior-оценки.
- Каждое микрозанятие содержит конкретные понятия, быстрый Junior-вопрос/сценарий, prerequisite и 1–2 точных привязки к бесплатным первичным материалам. У разделов есть отдельные банки без раскрытых ответов.
- Экзамен заменяет часть обычной lab/диагностики/интервью последней недели модуля; чтение и подготовка среды входят в план. Ретесты +7/+30 и смешанная проверка раз в 4 недели не добавляют часов.
- Обязательный маршрут — 30 + 15 недель. Резервы для среды/CIDR/сетей/Linux назначаются только по фактическому пробелу: A=240+8r, всего=360+8r. Нельзя прятать дополнительное время или незакрытый J0 в B.

## Ограничения

Часы — оценка автора, пока не проверенная темпом студента. Не выбраны и не проверены VM/runtime, версии/ARM64-образы, Jenkins plugins, локальный кластер и совокупный ресурсный бюджет. Лаборатории не выполнялись, команды не объявлены runtime-проверенными, TachoApp не читался и не менялся.

Cloud/IAM/remote backend частично изучаются по документации/схеме; фактическая практика Terraform бесплатна и локальна. Это не подтверждает cloud apply/remote locking/production IAM. У GNU Bash manual и SLSA 1.2 чтение не удалось; альтернативы и точные ограничения записаны в resources/SOURCES.md. Бесплатность всех KodeKloud/LabEx labs не установлена.

Прогресс освоения, подтверждённые навыки, ответы, даты проверок и учебные часы студента не заполнялись. В PROGRESS обновлена только следующая авторская задача и журнал подготовки материалов. Commit/push автор не выполнял.

## Следующее действие

Запустить [промпт 03](../prompts/03-interview-system.md): уточнить рабочую репетицию, результаты и очередь повторений на основе созданных банков, без фиктивных интервью. Далее [промпт 04](../prompts/04-first-networking-module.md) — первые 2–3 настоящих урока Networking; не считать Linux CLI A-M01 пройденным, заранее учесть его prerequisites и среду.

## Файлы этого шага

Изменено 15 существующих файлов:

```text
PROGRESS.md
README.md
ROADMAP.md
curriculum/INDEX.md
docs/README.md
docs/learning-method.md
docs/learning-scope.md
docs/material-conventions.md
docs/time-budget.md
interviews/README.md
interviews/answer-keys/README.md
interviews/questions/README.md
interviews/review-schedule.md
projects/devops-lab/README.md
resources/SOURCES.md
```

Добавлено 76 файлов:

```text
curriculum/A-M01-linux-start/SYLLABUS.md
curriculum/A-M02-networking/SYLLABUS.md
curriculum/A-M03-linux-admin/SYLLABUS.md
curriculum/A-M04-containers-app/SYLLABUS.md
curriculum/A-M05-monitoring/SYLLABUS.md
curriculum/A-M06-cicd/SYLLABUS.md
curriculum/A-M07-automation/SYLLABUS.md
curriculum/A-M08-kubernetes/SYLLABUS.md
curriculum/A-M09-cloud-iac/SYLLABUS.md
curriculum/A-M10-junior-capstone/SYLLABUS.md
curriculum/B-M01-kubernetes-helm/SYLLABUS.md
curriculum/B-M02-gitops/SYLLABUS.md
curriculum/B-M03-terraform/SYLLABUS.md
curriculum/B-M04-secrets-supply-chain/SYLLABUS.md
curriculum/B-M05-observability/SYLLABUS.md
curriculum/B-M06-integration-incidents/SYLLABUS.md
curriculum/B-M07-platform-next/SYLLABUS.md
docs/curriculum-review.md
docs/source-roadmap-comparison.md
interviews/answer-keys/INT-A-M01-S01.md
interviews/answer-keys/INT-A-M02-S01.md
interviews/answer-keys/INT-A-M02-S02.md
interviews/answer-keys/INT-A-M02-S03.md
interviews/answer-keys/INT-A-M02-S04.md
interviews/answer-keys/INT-A-M03-S01.md
interviews/answer-keys/INT-A-M03-S02.md
interviews/answer-keys/INT-A-M03-S03.md
interviews/answer-keys/INT-A-M04-S01.md
interviews/answer-keys/INT-A-M04-S02.md
interviews/answer-keys/INT-A-M05-S01.md
interviews/answer-keys/INT-A-M06-S01.md
interviews/answer-keys/INT-A-M06-S02.md
interviews/answer-keys/INT-A-M07-S01.md
interviews/answer-keys/INT-A-M07-S02.md
interviews/answer-keys/INT-A-M08-S01.md
interviews/answer-keys/INT-A-M08-S02.md
interviews/answer-keys/INT-A-M09-S01.md
interviews/answer-keys/INT-A-M10-S01.md
interviews/answer-keys/INT-B-M01-S01.md
interviews/answer-keys/INT-B-M01-S02.md
interviews/answer-keys/INT-B-M02-S01.md
interviews/answer-keys/INT-B-M03-S01.md
interviews/answer-keys/INT-B-M03-S02.md
interviews/answer-keys/INT-B-M04-S01.md
interviews/answer-keys/INT-B-M05-S01.md
interviews/answer-keys/INT-B-M06-S01.md
interviews/answer-keys/INT-B-M07-S01.md
interviews/questions/INT-A-M01-S01.md
interviews/questions/INT-A-M02-S01.md
interviews/questions/INT-A-M02-S02.md
interviews/questions/INT-A-M02-S03.md
interviews/questions/INT-A-M02-S04.md
interviews/questions/INT-A-M03-S01.md
interviews/questions/INT-A-M03-S02.md
interviews/questions/INT-A-M03-S03.md
interviews/questions/INT-A-M04-S01.md
interviews/questions/INT-A-M04-S02.md
interviews/questions/INT-A-M05-S01.md
interviews/questions/INT-A-M06-S01.md
interviews/questions/INT-A-M06-S02.md
interviews/questions/INT-A-M07-S01.md
interviews/questions/INT-A-M07-S02.md
interviews/questions/INT-A-M08-S01.md
interviews/questions/INT-A-M08-S02.md
interviews/questions/INT-A-M09-S01.md
interviews/questions/INT-A-M10-S01.md
interviews/questions/INT-B-M01-S01.md
interviews/questions/INT-B-M01-S02.md
interviews/questions/INT-B-M02-S01.md
interviews/questions/INT-B-M03-S01.md
interviews/questions/INT-B-M03-S02.md
interviews/questions/INT-B-M04-S01.md
interviews/questions/INT-B-M05-S01.md
interviews/questions/INT-B-M06-S01.md
interviews/questions/INT-B-M07-S01.md
scripts/check_curriculum.py
```

Все 91 новых/изменённых файлов повторно прочитаны. Исторический отчёт шага 01 сохранён. Веб-проверка: 8 исходных кандидатов и 52 тематические страницы доступны; GNU Bash manual и SLSA 1.2 помечены «не проверено» с причиной. Состояние источника не означает проверенную команду/среду.

Итоговые проверки: `python3 -B scripts/check_curriculum.py --self-test` — 7/7; `python3 -B scripts/check_curriculum.py` — PASS; `git diff --check` — без ошибок. Статический аудит не проверяет педагогический темп, внешнюю среду и навыки студента.
