# Границы сложности и доказательства

Статус: **черновик решения об объёме программы 02**. Уровни относятся к отдельным темам; A готовит к пробным Junior-задачам, B даёт Junior+/фундамент Middle. Грейд и трудоустройство не гарантируются; Middle требует реальной эксплуатационной ответственности.

| Метка | Обязательная глубина | Доказательство |
|---|---|---|
| J0 | Понять, самостоятельно сделать и диагностировать обычную неисправность | Независимая lab, объяснение механизма и негативный кейс |
| J1 | Базовая практика/знакомство, простой пример | Правильное объяснение, ограниченный пример и понимание границ |
| M | Углублённые изменения, устойчивость, компромиссы | Интеграционный сценарий и восстановление с обоснованием |
| O | Необязательно позже; не входит в обязательные 360 ч | Отдельное решение по реальной потребности |

## Глубина по областям

| Область | A: обязательная часть | B: расширение | За пределами обязательного пути |
|---|---|---|---|
| Linux | J0: FHS, inode/links, права, users/groups/sudo, процессы/signals, systemd/journald, apt/SSH, Bash, storage/ресурсы; J1: ACL/timers | M: применение в recovery/интеграции | O: kernel development, deep tuning, HA storage |
| Сети/защита | J0: Ethernet/MAC/ARP, IPv4/CIDR, gateway/routing/NAT/DHCP, TCP/UDP/ports, DNS, HTTP/TLS/proxy/firewall и диагностика | M: сетевые границы workload/cloud и инциденты | O: BGP/STP/MPLS, Cisco lab, корпоративный PKI |
| Приложение | J0: JSON/YAML/config, health/ready/version, 12-Factor основы; J1: graceful shutdown/SQL/migrations обзор | M: связь наблюдений и совместимость восстановления | O: полноценный backend, auth/billing/microservices |
| Контейнеры | J0: layers/cache/multi-stage, Compose, volumes/networks, lifecycle/logs/digest; J1: runtime/изоляция/ARM64/scan | M: происхождение артефакта и интеграция | O: собственный runtime, контейнер вручную |
| PostgreSQL | J1: table/SELECT/transaction и schema; J0: отдельный синтетический dump/restore с проверкой | M: согласованность/время восстановления и rollback совместимость | O: DBA performance, HA replication/PITR production |
| Наблюдаемость | J0: host/API metrics, logs, node_exporter, Prometheus, простая панель/alert и короткий runbook | M: Kubernetes/Loki/OTel основы, SLI/SLO/error budget/alert quality | O: HA observability, все сигналы для всех компонентов |
| CI/CD | J0: Jenkins, triggers/PR checks, agents/cache/artifacts, версия, smoke/rollback/права; J1: другая CI, SBOM/mobile обзор | M: provenance/supply chain/GitOps boundaries | O: все CI, реальный signing/publication, enterprise Jenkins |
| Автоматизация | J0: два Ansible target, inventory/modules/playbooks/roles/templates/handlers/variables/check/diff/idempotence; J1: Python CLI | M: интеграция и контроль результата | O: большая универсальная платформа автоматизации, Go глубоко |
| Kubernetes | J0: components, Pod/Deployment/Service/Namespace, ConfigMap/Secret/probes/scale/rollout/DNS/Ingress и диагностика, resources/PVC основы; J1: RBAC/CNI/CSI назначение | M: RBAC, ограничения, CNI/CSI overview, storage/rollout failures, Helm | O: Kubespray, HA control plane, разработка CNI/CSI, Service Mesh |
| Cloud/Terraform | J1: один provider как модель VM/network/IAM, HCL/init/plan/state и локальный lifecycle | M: modules/environments/drift/locking, проект remote state и IAM/network | O: Terragrunt глубоко, несколько облаков, реальные платные ресурсы без отдельного задания |
| Reliability/platform | J0: incident/runbook, безопасный recovery и проверка backup; без SLO-платформы | M: RPO/RTO, инциденты, SLI/SLO; J1: DORA/platform overview | O: Backstage, собственная IDP, MLOps, production ownership «за курс» |

У каждой строки микрозанятия в syllabus указан конкретный уровень. A не зависит от прохождения Helm/Argo/Vault/SLI-SLO: эти темы находятся в B. Наличие обзорного термина в A не означает обязанность развернуть расширение.

## Практические границы бесплатного маршрута

Обязательна локальная Linux-практика и существующий маленький TS API; не нужен полный backend. Компоненты включаются последовательно по ресурсам, а не все одновременно. Конкретные версии/инструменты среды выбираются автором lab после проверки ARM64 и доступной памяти, ничего сейчас не установлено.

Terraform A использует terraform_data без cloud credentials/provisioner-команд. B проверяет локальную модель/state/locking и проектирует remote backend/IAM/network; это **не подтверждение реального cloud apply, remote backend, remote lock или production IAM**. Чтение/разбор наблюдений даёт знакомство, но не закрывает самостоятельный runtime-навык. Не записывать непроверенное в PROGRESS.

Один пример провайдера для чтения — Yandex Cloud; документация доступна бесплатно, ресурсы бесплатными не объявляются. Аккаунт, trial/карта, публичные IP/домены и внешние платные сервисы не обязательны. При отдельном запросе на облачную ветку сначала пересчитать время/расходы и получить соответствующее разрешение.

Git основы не повторять. Rebase/cherry-pick/reset/reflog — точечная диагностика пробела; мутирующие операции только по явному заданию в безопасном учебном репозитории. Сертификаты не обязательны; не нужно учить несколько облаков или несколько языков заново.

## Выходные проверки

A: объяснить обязательный J0, самостоятельно выполнить типовую задачу и локализовать отказ; показать собственный ход мысли, допустимые артефакты и объём подсказок. Пробные Junior-интервью разрешены раньше W30. Незакрытый J0 переносит срок A, не скрывается средним баллом и не перекладывается в B.

B: интегрировать ранее изученное, выбрать безопасное изменение/восстановление и обосновать компромисс. Учебные инциденты не моделируют полностью дежурства, ответственность и ограничения реального сервиса. По завершении составить план рабочей практики под наблюдением.

Навигация: [индекс](../curriculum/INDEX.md) · [бюджет](time-budget.md) · [методика](learning-method.md) · [сравнение исходников](source-roadmap-comparison.md).
