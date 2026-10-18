#!/usr/bin/env python3
"""Один вопрос или очередь повторений; только чтение Markdown, без сети/ключей."""
import argparse
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
QID = r'Q-[AB]-M\d{2}-S\d{2}-\d{2}'
RID = r'RES-\d{4}-\d{2}-\d{2}-\d{3}'
LEVELS = {'J0', 'J1', 'M'}
STAGES = {'initial', 'review-7', 'review-30', 'mixed'}


class InvalidData(ValueError):
    pass


def fields(text):
    values = {}
    for key, value in re.findall(r'^- ([^:\n]+): (.+)$', text, re.M):
        if key in values:
            raise InvalidData(f'Поле повторяется: {key}')
        values[key] = value.strip()
    return values


def require(values, names):
    missing = [name for name in names if not values.get(name) or '{{' in values[name]]
    if missing:
        raise InvalidData('Не заполнены поля: ' + ', '.join(missing))


def iso(value):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise InvalidData('Дата должна иметь формат YYYY-MM-DD')
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise InvalidData('Несуществующая календарная дата') from exc


def identifier(value, pattern):
    found = set(re.findall(pattern, value))
    if len(found) != 1:
        raise InvalidData('Неоднозначный или отсутствующий ID')
    return found.pop()


def read_inside(path, directory):
    if path.is_symlink() or not path.resolve().is_relative_to(directory.resolve()):
        raise InvalidData('Файл выходит за разрешённый каталог')
    return path.read_text(encoding='utf-8')


@dataclass(frozen=True)
class Question:
    qid: str
    level: str
    minutes: int
    prompt: str
    metadata: dict


def read_question(path, directory):
    text = read_inside(path, directory)
    meta = fields(text)
    require(meta, ['ID', 'Статус', 'Назначение', 'Модуль', 'Раздел', 'Уроки', 'Уровень', 'Тип', 'Проверяет', 'Лаборатория', 'Минуты', 'Происхождение', 'Источник'])
    qid = meta['ID']
    if not re.fullmatch(QID, qid) or path.stem != qid:
        raise InvalidData('ID вопроса не совпадает с именем файла')
    if meta['Модуль'] != qid[2:7] or meta['Раздел'] != qid[2:11]:
        raise InvalidData('Модуль/раздел не совпадает с Q-ID')
    if meta['Уровень'] not in LEVELS or meta['Тип'] not in {'definition', 'mechanism', 'troubleshooting', 'tradeoff'}:
        raise InvalidData('Неизвестный уровень или тип вопроса')
    if meta['Статус'] not in {'черновик', 'проверено', 'готово'}:
        raise InvalidData('Неизвестный статус карточки')
    if not re.search(re.escape(meta['Раздел']) + r'-L\d{2}', meta['Уроки']):
        raise InvalidData('Не указан конкретный урок раздела')
    try:
        minutes = int(meta['Минуты'])
    except ValueError as exc:
        raise InvalidData('Минуты должны быть целым числом') from exc
    if not 1 <= minutes <= 15:
        raise InvalidData('Карточка должна занимать 1–15 минут')
    match = re.search(r'^## Вопрос\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    prompt = match.group(1).strip() if match else ''
    if not prompt or any(marker in text for marker in ['## Тезисы хорошего ответа', '## Распространённые ошибки', '## Оценка 0–3']):
        raise InvalidData('Нет вопроса либо в карточку попали критерии ответа')
    return Question(qid, meta['Уровень'], minutes, prompt, meta)


def load_questions(root):
    directory = root / 'interviews/questions'
    questions = {}
    for path in sorted(directory.rglob('Q-*.md')):
        question = read_question(path, directory)
        if question.qid in questions:
            raise InvalidData('Дублируется рабочая карточка: ' + question.qid)
        questions[question.qid] = question
    return questions


def show(root, qid, include_m=False):
    if not re.fullmatch(QID, qid):
        raise InvalidData('Некорректный Q-ID')
    directory = root / 'interviews/questions'
    paths = list(directory.rglob(qid + '.md'))
    if len(paths) != 1:
        raise InvalidData('Нужна одна полная карточка; строка планового INT-банка её не заменяет')
    question = read_question(paths[0], directory)
    if question.level == 'M' and not include_m:
        raise InvalidData('M — дополнительное расширение: нужен явный --include-m')
    return f'{question.qid} [{question.level}; {question.metadata["Назначение"]}; {question.metadata["Статус"]}]\n\n{question.prompt}\n\nМентор ждёт фактического ответа; результат и сроки не создаются.'


@dataclass(frozen=True)
class Result:
    rid: str
    qid: str
    day: date
    level: str
    stage: str
    base: str
    score: int


def load_results(root, questions):
    directory = root / 'interviews/results'
    results = {}
    for path in sorted(directory.glob('RES-*.md')):
        meta = fields(read_inside(path, directory))
        require(meta, ['ID', 'Вопрос', 'Дата', 'Уровень', 'Этап', 'Базовая проверка', 'Оценка', 'Ответ', 'Обоснование', 'Ошибка', 'Подсказки', 'Следующее действие'])
        rid = meta['ID']
        if not re.fullmatch(RID, rid) or path.stem != rid or rid in results:
            raise InvalidData('Некорректный или повторяющийся ID результата')
        qid = meta['Вопрос']
        if qid not in questions or meta['Уровень'] != questions[qid].level or meta['Этап'] not in STAGES:
            raise InvalidData('Результат не связан с рабочей карточкой/уровнем/этапом')
        try:
            score = int(meta['Оценка'])
        except ValueError as exc:
            raise InvalidData('Балл должен быть целым числом 0–3') from exc
        if score not in range(4):
            raise InvalidData('Балл вне 0–3')
        base = meta['Базовая проверка']
        if base == '—':
            base = None
        stage = meta['Этап']
        if stage.startswith('review-') != bool(base):
            raise InvalidData('Только review-7/review-30 требуют базовый initial')
        results[rid] = Result(rid, qid, iso(meta['Дата']), meta['Уровень'], stage, base, score)
    for result in results.values():
        if result.base:
            base = results.get(result.base)
            if not base or base.stage != 'initial' or base.qid != result.qid:
                raise InvalidData('Ретест ссылается не на свой initial')
            delay = int(result.stage.split('-')[1])
            if result.day < base.day + timedelta(days=delay):
                raise InvalidData('Ретест раньше своего интервального срока')
    return results


@dataclass(frozen=True)
class Candidate:
    qid: str
    level: str
    score: int
    due: date
    stage: str
    base: str
    minutes: int


def scheduled_candidates(root, questions, results, on):
    path = root / 'interviews/review-schedule.md'
    text = read_inside(path, root / 'interviews')
    candidates = []
    seen = set()
    for line in text.splitlines():
        if not line.startswith('|'):
            continue
        row = [cell.strip() for cell in line.strip('|').split('|')]
        if row[0] == 'Базовый результат' or all(re.fullmatch(r'[:\- ]+', cell) for cell in row):
            continue
        if len(row) != 8:
            raise InvalidData('Строка реестра должна содержать 8 полей')
        base_id, qid = identifier(row[0], RID), identifier(row[1], QID)
        base = results.get(base_id)
        if not base or base.stage != 'initial' or base.qid != qid or base_id in seen:
            raise InvalidData('Реестр не согласован с уникальным фактическим initial')
        seen.add(base_id)
        if iso(row[2]) != base.day:
            raise InvalidData('D в реестре не совпадает с фактической датой initial')
        for delay, due_cell, done_cell in [(7, row[3], row[4]), (30, row[5], row[6])]:
            due = iso(due_cell)
            stage = f'review-{delay}'
            if due != base.day + timedelta(days=delay):
                raise InvalidData('Срок не равен D+7/D+30; перенос не меняет исходный срок')
            done = None
            if done_cell not in {'', '—', '-'}:
                done = results.get(identifier(done_cell, RID))
                if not done or done.base != base_id or done.qid != qid or done.stage != stage:
                    raise InvalidData('Срок закрыт не своим фактическим ретестом')
            if base.day <= on and due <= on and not (done and done.day <= on):
                history = [r for r in results.values() if r.qid == qid and r.day <= on]
                latest = max(history, key=lambda r: (r.day, r.rid))
                candidates.append(Candidate(qid, base.level, latest.score, due, stage, base_id, questions[qid].minutes))
    missing = [r.rid for r in results.values() if r.stage == 'initial' and r.day <= on and r.rid not in seen]
    if missing:
        raise InvalidData('Для фактических initial нет строки реестра: ' + ', '.join(sorted(missing)))
    return candidates


def priority(candidate):
    weak = candidate.score <= 1
    tier = (0 if weak else 1) if candidate.level == 'J0' else (2 if weak else 3) if candidate.level == 'J1' else 4
    return tier, candidate.due or date.max, candidate.score, candidate.qid, candidate.stage, candidate.base or ''


def review(root, on, minutes=10, week=None, include_m=False):
    if not 1 <= minutes <= 60 or (week is not None and week < 1):
        raise InvalidData('Бюджет: 1–60 минут; учебная неделя положительная')
    questions = load_questions(root)
    results = load_results(root, questions)
    candidates = scheduled_candidates(root, questions, results, on)
    if week is not None and week % 4 == 0:
        latest = {}
        for result in sorted(results.values(), key=lambda r: (r.day, r.rid)):
            if result.day <= on:
                latest[result.qid] = result
        candidates += [Candidate(r.qid, r.level, r.score, None, 'mixed', None, questions[r.qid].minutes) for r in latest.values() if r.day < on]
    candidates = [c for c in candidates if include_m or c.level != 'M']
    chosen, used, seen = [], 0, set()
    for candidate in sorted(candidates, key=priority):
        if candidate.qid in seen or used + candidate.minutes > minutes:
            continue
        chosen.append(candidate)
        seen.add(candidate.qid)
        used += candidate.minutes
    return chosen, used, len(candidates) - len(chosen)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    display = sub.add_parser('show', help='показать ровно одну карточку без ключа')
    display.add_argument('qid')
    display.add_argument('--include-m', action='store_true')
    queue = sub.add_parser('review', help='показать очередь; ничего не записывать')
    queue.add_argument('--on', required=True, help='локальная дата YYYY-MM-DD, явно')
    queue.add_argument('--minutes', type=int, default=10, help='лимит вопросов; по умолчанию 10 из 15 минут, ещё 5 на обратную связь')
    queue.add_argument('--week', type=int, help='фактическая учебная неделя; каждая четвёртая добавляет mixed')
    queue.add_argument('--include-m', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'show':
            print(show(ROOT, args.qid, args.include_m))
        else:
            chosen, used, deferred = review(ROOT, iso(args.on), args.minutes, args.week, args.include_m)
            if not chosen:
                print('Нет подходящих повторений в заданном бюджете; результаты и даты не создаются.')
            for item in chosen:
                print(f'{item.qid} | {item.level} | балл {item.score} | {item.stage} | срок {item.due or "выборка старой темы"} | база {item.base or "—"} | {item.minutes} мин')
            print(f'Время: {used}/{args.minutes} мин. Осталось элементов очереди: {deferred}. Изменений нет.')
        return 0
    except (InvalidData, OSError, UnicodeError) as exc:
        print(f'Ошибка данных: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
