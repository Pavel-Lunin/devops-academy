# Индекс программы

Статус: **черновик программы, структурно проверяется отдельно**. Зарегистрировано 17 модулей, 28 разделов, 135 микрозанятий, 45 плановых lab-блоков. Три урока S01 Networking и офлайн-lab W03 подготовлены и проверены в пределах синтетической модели; остальные уроки/labs — **запланировано**.

| Модуль / syllabus | Недели | Глубина | Входной prerequisite | Новая Т, ч | Интервью, ч | Lab, ч | Диагностика, ч | Всего, ч |
|---|---|---|---|---|---|---|---|---|
| [A-M01 — Linux CLI и безопасная лаборатория](A-M01-linux-start/SYLLABUS.md) | 1–2 | J0 | входной профиль | 6 | 2 | 6 | 2 | 16 |
| [A-M02 — Сети и безопасность соединений с нуля](A-M02-networking/SYLLABUS.md) | 3–6 | J0 | A-M01-S01-L06 | 12 | 4 | 12 | 4 | 32 |
| [A-M03 — Linux administration, Bash и диагностика](A-M03-linux-admin/SYLLABUS.md) | 7–11 | J0/J1 | A-M02-S04-L03 | 15 | 5 | 15 | 5 | 40 |
| [A-M04 — Эксплуатация TS API, Docker и PostgreSQL](A-M04-containers-app/SYLLABUS.md) | 12–14 | J0/J1 | A-M03-S03-L03 | 9 | 3 | 9 | 3 | 24 |
| [A-M05 — Monitoring I: метрики, логи и сигналы](A-M05-monitoring/SYLLABUS.md) | 15–16 | J0 | A-M04-S02-L03 | 6 | 2 | 6 | 2 | 16 |
| [A-M06 — Jenkins CI/CD и безопасная доставка](A-M06-cicd/SYLLABUS.md) | 17–20 | J0/J1 | A-M05-S01-L06 | 12 | 4 | 12 | 4 | 32 |
| [A-M07 — Ansible и небольшая автоматизация Python](A-M07-automation/SYLLABUS.md) | 21–23 | J0/J1 | A-M06-S02-L06 | 9 | 3 | 9 | 3 | 24 |
| [A-M08 — Kubernetes fundamentals и troubleshooting](A-M08-kubernetes/SYLLABUS.md) | 24–27 | J0/J1 | A-M07-S02-L03 | 12 | 4 | 12 | 4 | 32 |
| [A-M09 — Cloud/IaC и Terraform intro без расходов](A-M09-cloud-iac/SYLLABUS.md) | 28–29 | J1 | A-M08-S02-L06 | 6 | 2 | 6 | 2 | 16 |
| [A-M10 — Junior capstone и пробное интервью](A-M10-junior-capstone/SYLLABUS.md) | 30–30 | J0 | A-M09-S01-L06 | 3 | 1 | 3 | 1 | 8 |
| [B-M01 — Kubernetes глубже и Helm](B-M01-kubernetes-helm/SYLLABUS.md) | 31–33 | M | A-M10-S01-L03 | 9 | 3 | 9 | 3 | 24 |
| [B-M02 — GitOps / Argo CD](B-M02-gitops/SYLLABUS.md) | 34–35 | M | B-M01-S02-L03 | 6 | 2 | 6 | 2 | 16 |
| [B-M03 — Terraform, state, IAM и границы Cloud](B-M03-terraform/SYLLABUS.md) | 36–38 | M | B-M02-S01-L06 | 9 | 3 | 9 | 3 | 24 |
| [B-M04 — Vault, секреты и supply chain](B-M04-secrets-supply-chain/SYLLABUS.md) | 39–40 | M | B-M03-S02-L03 | 6 | 2 | 6 | 2 | 16 |
| [B-M05 — Observability II и reliability](B-M05-observability/SYLLABUS.md) | 41–42 | M | B-M04-S01-L06 | 6 | 2 | 6 | 2 | 16 |
| [B-M06 — Интеграция, backup/restore и инциденты](B-M06-integration-incidents/SYLLABUS.md) | 43–44 | M | B-M05-S01-L06 | 6 | 2 | 6 | 2 | 16 |
| [B-M07 — Platform Engineering и план рабочего опыта](B-M07-platform-next/SYLLABUS.md) | 45–45 | M/J1 | B-M06-S01-L06 | 3 | 1 | 3 | 1 | 8 |

A: 240 ч; B: 120 ч; всего 360 ч. Каждый из 45 недельных блоков: 3 + 1 + 3 + 1 = 8 ч. Подробная недельная сетка и правила резервов — в [бюджете](../docs/time-budget.md).

## Как читать программу

Внутри syllabus: оглавление разделов → ID уроков по 60 мин с конкретными понятиями, глубиной, prerequisite, быстрым вопросом и 1–2 источниками → план самостоятельной lab с тремя часовыми контрольными точками, артефактом, негативным кейсом и критерием → мини-интервью и экзамен. Практика диагностики и заметок учтена отдельно.

Ссылка на запланированный ID ведёт в его якорь syllabus, а не в несуществующий урок. Обязательные prerequisites образуют последовательный маршрут; это входная учебная зависимость, не запрет возвращаться к старой теме. Завершение блока проверяется по навыкам, не по чтению программы.

Первый подготовленный сетевой урок: [A-M02-S01-L01](A-M02-networking/lessons/A-M02-S01-L01-participants.md). [Система интервью и восемь примеров](../interviews/README.md) подготовлены; авторская партия [первых трёх уроков Networking](A-M02-networking/SYLLABUS.md#a-m02-s01) подготовлена с явной проверкой Linux CLI prerequisites A-M01. Не считать вводный Linux-модуль пройденным и не перескакивать этот вход.

Навигация: [ROADMAP](../ROADMAP.md) · [PROGRESS](../PROGRESS.md) · [аудит программы](../docs/curriculum-review.md) · [ID/статусы](../docs/material-conventions.md).
