# Промпт 02 — Детальная программа с двумя уровнями и аудитом roadmap

Прочитай `AGENTS.md`, `README.md`, `ROADMAP.md`, `docs/`, оба пользовательских текста в `resources/source-roadmaps/`. Работай как опытный DevOps-методист и инженер, не как генератор поверхностных списков. **Задача — программа и индексы, пока без полнотекстовых уроков.**

## 1. Источники и ограничения

Два исходных видео обязательны для сравнения:
- №1: Networks, Windows fundamentals, Linux, Ansible, Git, CI/CD, Docker, Kubernetes/Helm/Argo CD, один cloud, Terraform/Terragrunt, Python.
- №2: Markdown-практика заметок, Linux глубже, Git, Networks/Security, Docker internals и PostgreSQL basics, monitoring **рано**, CI/CD, Ansible, Kubernetes/Helm/Vault/Argo CD, Cloud/Terraform позднее.

Внешние **кандидаты для проверки**, если есть web-доступ:
- https://roadmap.sh/devops
- https://kodekloud.com/learning-path/devops-engineer
- https://kubernetes.io/docs/
- https://docs.docker.com/
- https://developer.hashicorp.com/terraform
- https://www.cncf.io/
- https://linkmeup.gitbook.io/sdsm
- https://linuxjourney.com/

Не приписывай современным версиям рекомендаций или точных дат без проверки. Если сеть недоступна, помечай источник `не проверен`, никогда не выдумывай URL, текст статьи или статистику. Разделяй положения из двух видео, внешние сведения и собственные выводы.

## 2. Целевая сложность

Создай явное разделение:
- **J0** — обязательное для Junior: понять, самостоятельно сделать и диагностировать обычную неисправность.
- **J1** — Junior дополнительно: понять и реализовать простой пример.
- **M** — следующий уровень (Junior+/навыки Middle): самостоятельные типовые изменения, устойчивость, более сложная эксплуатация.
- **O** — опционально после курса: Service Mesh, Backstage, Kubespray, Terragrunt глубоко, Windows AD lab, Go глубоко, kernel development, MLOps и пр.

Не делай формальные сертификаты обязательными. Не требуй нескольких облаков. Python — минимальная автоматизация, не новое обучение программированию. Git — точечное повторение `rebase/cherry-pick/reset/reflog` по необходимости. Компетенции отличаются по вакансиям; никаких гарантий грейда.

## 3. Декомпозиция: от термина до урока

Для **каждого модуля** зафиксируй:
- цель, ожидаемые навыки, глубину `J0/J1/M/O`;
- prerequisites и связи между темами;
- разделы → уроки 20–75 мин → подтемы с конкретным перечнем понятий;
- что объясняется самостоятельно, что достаточно знать обзорно;
- конкретную практику (не общую фразу «изучить Docker»);
- проверяемый артефакт, негативный тест / диагностику, критерий готовности;
- 5–10 вопросов/сценариев интервью после раздела, включая ретест через 7/30 дней;
- 1–2 бесплатных источника (точная тема/раздел, язык, доступ, проверка);
- реально необходимое время, отдельно теория/практика.

Особенно подробно декомпозируй:

**Linux**: GNU/Linux, kernel/userspace, FHS, файлы/inode/links, permissions/ACL basics, users/groups/sudo, processes/signals, systemd, journald, apt, SSH, environment, piping/redirection, Bash, cron/timers, storage/mounts, CPU/RAM/disk/log troubleshooting.

**Networking/Security foundations**: Ethernet/MAC/ARP, IP/IPv4/CIDR/subnetting, default gateway, routing/NAT, DNS/DHCP, TCP handshake/retransmit/UDP/ports/socket, HTTP/HTTPS/TLS/certificates, proxy/reverse proxy, firewall/SSH hardening, диагностика ping/traceroute/dig/ss/curl/tcpdump. Без предположения инженерного диплома.

**Приложения для эксплуатации**: YAML/JSON, конфигурации, env, 12-Factor основные принципы, HTTP API на существующем TypeScript, process lifecycle, graceful shutdown, PostgreSQL basics, миграции/backup как обзор.

**Docker**: layers, build cache, multi-stage, Compose, volumes/networks, registry/digest, health checks, lifecycle, logging, namespaces/cgroups/containerd/runc обзор, сканирование образов, ARM64.

**Monitoring I**: node_exporter, метрики host/API, Prometheus, Grafana, basics logs и alerting. **Monitoring II** позднее: Kubernetes, Loki, traces/OpenTelemetry базово, SLI/SLO.

**CI/CD**: Git workflow и триггеры, PR checks, Jenkins преимущественно; GitHub Actions или GitLab CI как дополнительный инструмент, runners/agents, cache/artifacts, immutable images, registry, secrets, deploy, rollback, безопасные права, supply-chain basics/SBOM overview, Android/iOS CI/CD по полезности проекту.

**Ansible**: inventory/playbooks/modules/handlers/templates/variables/roles/idempotence, два host, check/diff, секреты, тестирование результатов.

**Python**: отличие от TS, venv, subprocess, filesystem, JSON/YAML, HTTP API, CLI, logging/errors — минимум для задач автоматизации.

**Kubernetes J0**: architecture, Pod/Deployment, Service/cluster DNS, Namespace, ConfigMap/Secret, health probes, scaling/rollout, Ingress, resources/PVC основы, kubectl/logs/events/troubleshooting. **M**: RBAC, networking/CNI overview, storage/CSI overview, Helm, GitOps, Vault, SLO.

**Cloud/Terraform**: IaaS, VM/network/IAM, Terraform HCL/resource/state/init/plan/apply/destroy для Junior; далее remote state/modules/drift/locking/environments, ограничения затрат.

**Reliability**: incident, availability, alert quality, runbooks, backup/restore, SLI/SLO; основы DORA-метрик и Platform Engineering позднее.

## 4. Бюджет недель (стартовое разбиение, не жертвовать базой ради дат)

**A. Junior, 30 недель = 240 ч**:
- 1–2 Linux CLI survival + настройка учебной среды и Markdown-заметок.
- 3–6 Networking и безопасность соединений.
- 7–11 Linux administration, Bash, troubleshooting.
- 12–14 Docker, Compose и эксплуатация простого TypeScript API/PostgreSQL.
- 15–16 Monitoring I.
- 17–20 Jenkins CI/CD, registry, delivery/rollback и безопасность.
- 21–23 Ansible + небольшая автоматизация Bash/Python.
- 24–27 Kubernetes fundamentals и диагностика.
- 28–29 Intro Cloud/Terraform.
- 30 самостоятельно выполняемый Junior capstone + интервью.

**B. Junior+ / Middle fundamentals, 15 недель = 120 ч**:
- 31–33 Kubernetes глубже + Helm.
- 34–35 GitOps/Argo CD.
- 36–38 Terraform/Cloud/IAM/network/state/modules глубже.
- 39–40 Vault/secrets + CI security/supply chain.
- 41–42 Observability II / reliability / SLI/SLO.
- 43–44 integration project + controlled incidents.
- 45 Platform Engineering overview, интервью и план получения рабочего опыта.

Если выяснится, что текущий уровень по Linux/Networks слабее ожидаемого, отметь запасные недели и возможность растянуть этап A. Не перекладывай незавершённое Junior в Middle без пояснения.

Каждая неделя **ровно 8 запланированных часов**: 3 новая теория + 1 интервью/повторение, 3 lab + 1 диагностика/заметки. Повторение не должно бесконечно расширять бюджет.

## 5. Самостоятельная лаборатория

Основная DevOps Lab отдельна от TachoApp: маленький TypeScript HTTP API (health, ready, version; потом простое обращение к PostgreSQL), который обрастает Linux, Docker, monitoring, CI/CD, Ansible, Kubernetes, Helm/Argo, Terraform. Не тратить время на бизнес-логику backend. Строить изолированно на Apple Silicon. На реальные расходы всегда спрашивать разрешение. TachoApp — только для действительно полезных инфраструктурных задач.

## 6. Interview-ready с первого раздела

После каждого учебного раздела: минимум 5 базовых вопросов с эталонными критериями ответа отдельно, 2 сценария «почему не работает», один вопрос на оценку решений. Репетиция по одному вопросу за раз. Вопросы из публичных источников отмечать вместе с ссылками, самостоятельно составленные не выдавать за «топ реальных интервью».

Система прогресса должна опираться на **проверенные навыки**, а не на просмотр видео. Раз в 4 недели — смешанный ретест старых тем внутри бюджета часов. Допускай промежуточные пробные Junior-собеседования до конца 30 недель.

## 7. Выходные файлы и самопроверка

Создай `ROADMAP.md`, `curriculum/INDEX.md`, отдельные `curriculum/*/SYLLABUS.md`, `docs/source-roadmap-comparison.md`, `docs/learning-scope.md`, `docs/time-budget.md`, `resources/SOURCES.md`. В последнем указывай статус ссылок «проверено / не проверено» и даты там, где реально доступны.

**Не генерируй полнотекстовые уроки.** Сделай аудит: тематика покрыта, нет сломанных зависимостей, темы J0 не утонули в M/O, все недели 8 часов и суммарно 240 + 120, вопрос интервью есть на каждом участке. Показать подсчёт часов, пробелы, список следующего действия. Не коммить самостоятельно.
