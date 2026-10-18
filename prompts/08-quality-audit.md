# Промпт 08 — Независимая ревизия качества Academy (по мере необходимости)

Роль: строгий технический рецензент программы Junior DevOps в 2026 году. **Не выполняй студенческие лабораторные**. Прочитай источники пользователя в `resources/source-roadmaps/`, `ROADMAP.md`, `docs/source-roadmap-comparison.md` (если есть), syllabus, `AGENTS.md`, interview-систему и созданные уроки.

## 1. Проверить соответствие целям

- Реальный профиль: React Native/TypeScript + Git Flow, начальные Jenkins/Concourse/Docker/Linux, отсутствие фундаментальных сетей.
- 30 недель 240 часов — Junior; 15 недель 120 часов — Junior+ / основа Middle; право добавлять недели при пробелах.
- 8 ч/неделя: 3 теория + 1 интервью/повторение + 3 lab + 1 диагностика/заметки, строго 50/50.
- Нет Obsidian, только Markdown в VS Code/Git.
- DevOps Lab отдельна от реального TachoApp; DevOps-проекты не являются самоцелью.
- Не заявлять, что учебная лаборатория сама присваивает Middle-грейд.

## 2. Проверить полноту и разумность сложности

**Junior J0:** Linux users/permissions/files/processes/systemd/logs/SSH/shell, DNS/IP/CIDR/routes/TCP/UDP/HTTP/TLS/firewall, Docker images/networks/volumes/Compose, базовые метрики/логи, CI build/test/publish/deploy/rollback, Ansible basics, Kubernetes базовые workloads/networking/kubectl/troubleshooting, Terraform Cloud intro.

**Middle M позднее:** Helm/ArgoCD, Kubernetes RBAC/storage/networking глубже, advanced Terraform state/modules, Vault, supply chain, OpenTelemetry overview, SLI/SLO, incident-response/backup/restore, Platform Engineering основы.

**Необязательно O сейчас:** Backstage глубокий, Service Mesh, Kubespray, Terragrunt глубоко, multi-cloud, full Windows AD lab, продвинутый Go/Python, MLOps.

Мониторинг должен встречаться дважды: I до CI/CD/Kubernetes, II после Kubernetes. Python минимален, опираться на TS-навыки. Для интервью требования Junior понятнее и важнее случайных сертификаций.

## 3. Проверить источники

Прочитай 2 приложенные видеорасшифровки. Проверь, какие идеи учитываются, какие сознательно отложены; не утверждай, что была прямая проверка видео, если доступны только расшифровки.

Если веб-доступ есть, проверяй актуальные официальные материалы: roadmap.sh DevOps, Kubernetes docs, Docker docs, HashiCorp docs, CNCF, Linux Foundation и документацию CI инструментов. Если нет — пометь непроверенное и не вводи выдуманных публикаций, курсов, дат, «популярных вопросов интервью».

## 4. Проверить учебные единицы

По выборке 3 готовых уроков в текущем модуле:
- Реально ли учить с нуля и без технического диплома?
- Нет ли нерасшифрованных терминов?
- Достаточно ли причинно-следственного объяснения?
- Реалистично ли выполнить за заявленные часы?
- Есть ли честно выполнимая лаборатория и диагностика?
- Безопасен ли Linux/macOS-эксперимент на Apple Silicon?
- Можно ли проверить результат независимо?
- Не раскрывается ли ответ до попытки?
- Есть ли вопросы интервью в текущей теме и ретест?
- Нет ли ненужной Middle/Senior-глубины в J0?

## 5. Результат

Создай `docs/quality-audit-<date>.md` (используй текущую локальную дату без выдумывания); сгруппируй замечания: `critical`, `important`, `nice to have`. Приводи ссылку на конкретный файл/раздел и предлагаемое исправление.

**По умолчанию только аудит и предложения, без массовых правок.** Не меняй syllabus, готовые уроки или PROGRESS без моей отдельной команды. В конце дай краткий перечень пяти самых важных улучшений и ожидаемое влияние на длительность обучения.
