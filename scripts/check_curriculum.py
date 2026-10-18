#!/usr/bin/env python3
"""Read-only аудит Markdown-программы. Python 3.9+, без сети и зависимостей."""
import argparse
from collections import Counter, defaultdict
from pathlib import Path
import re
import sys
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LESSON_ID = r'[AB]-M\d{2}-S\d{2}-L\d{2}'


def cells(line):
    return [part.strip() for part in line.strip().strip('|').split('|')]


def validate_plan(weeks, lessons, expected_weeks=45):
    errors = []
    numbers = [row['number'] for row in weeks]
    if sorted(numbers) != list(range(1, expected_weeks + 1)):
        errors.append('Номера недель пропущены или повторяются')
    for row in weeks:
        if row['minutes'] != [180, 60, 180, 60, 480]:
            errors.append(f"W{row['number']:02}: нарушен бюджет 3+1+3+1")
    ids = [row['id'] for row in lessons]
    if len(ids) != len(set(ids)):
        errors.append('Повторяется ID микрозанятия')
    position = {value: index for index, value in enumerate(ids)}
    counts = Counter(row['week'] for row in lessons)
    for number in numbers:
        if counts[number] != 3:
            errors.append(f'W{number:02}: нужно три теоретических микрозанятия')
    for row in lessons:
        if row['minutes'] != 60 or not 20 <= row['minutes'] <= 75:
            errors.append(f"{row['id']}: время урока не согласовано с неделей")
        if row['level'] not in {'J0', 'J1', 'M', 'O'}:
            errors.append(f"{row['id']}: неизвестный уровень")
        if row['id'].startswith('A-') and row['level'] == 'M':
            errors.append(f"{row['id']}: расширение M попало в обязательную A")
        prereq = row['prereq']
        if prereq and prereq not in position:
            errors.append(f"{row['id']}: prerequisite {prereq} отсутствует")
        elif prereq and position[prereq] >= position[row['id']]:
            errors.append(f"{row['id']}: prerequisite ведёт вперёд/образует цикл")
        if not row['concepts'] or not row['question']:
            errors.append(f"{row['id']}: нет конкретных понятий/вопроса")
        if not 1 <= len(row['sources']) <= 2:
            errors.append(f"{row['id']}: требуется 1–2 источника")
    return errors


def check_links(root):
    errors = []
    count = 0
    texts = {path: path.read_text(encoding='utf-8') for path in root.rglob('*.md') if '.git' not in path.parts}
    anchors = {}
    for path, content in texts.items():
        explicit = set(re.findall(r'<a id="([^"]+)"', content))
        headings = set()
        for heading in re.findall(r'^#{1,6} (.+)$', content, re.M):
            headings.add(re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-'))
        anchors[path] = explicit | headings
    for path, content in texts.items():
        body = re.sub(r'```.*?```', '', content, flags=re.S)
        body = re.sub(r'`[^`\n]*`', '', body)
        for href in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', body):
            parsed = urlsplit(href.strip().strip('<>'))
            if parsed.scheme:
                continue
            count += 1
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not target.is_relative_to(root):
                errors.append(f'{path.relative_to(root)}: ссылка вне репозитория {href}')
            elif not target.is_file():
                errors.append(f'{path.relative_to(root)}: отсутствует цель {href}')
            elif parsed.fragment and unquote(parsed.fragment) not in anchors.get(target, set()):
                errors.append(f'{path.relative_to(root)}: отсутствует якорь {href}')
    return count, errors


def audit(root):
    errors = []
    modules = []
    for line in (root / 'curriculum/INDEX.md').read_text().splitlines():
        if re.match(r'^\| \[[AB]-M\d{2} —', line):
            row = cells(line)
            mid = re.search(r'[AB]-M\d{2}', row[0]).group()
            start, end = map(int, row[1].split('–'))
            hours = list(map(int, row[4:9]))
            n = end - start + 1
            if hours != [3*n, n, 3*n, n, 8*n]:
                errors.append(f'{mid}: часы модуля не совпадают с неделями')
            modules.append((mid, start, end, hours[-1]))
    if len(modules) != len({row[0] for row in modules}):
        errors.append('ID модуля повторяется')
    totals = {stage: sum(row[3] for row in modules if row[0].startswith(stage)) for stage in ('A', 'B')}
    if totals != {'A': 240, 'B': 120}:
        errors.append(f'Итоги ступеней неверны: {totals}')
    weeks = []
    for line in (root / 'docs/time-budget.md').read_text().splitlines():
        if re.match(r'^\| W\d{2} \|', line):
            row = cells(line)
            weeks.append({'number': int(row[0][1:]), 'module': re.search(r'[AB]-M\d{2}', row[1]).group(), 'minutes': list(map(int, row[3:8]))})
    week_module = {row['number']: row['module'] for row in weeks}
    for mid, start, end, _ in modules:
        for number in range(start, end+1):
            if week_module.get(number) != mid:
                errors.append(f'W{number:02}: модуль недельной сетки не совпадает с индексом')
    lessons = []
    sections = set()
    labs = set()
    for path in sorted((root / 'curriculum').glob('*/SYLLABUS.md')):
        content = path.read_text()
        sections.update(value.upper() for value in re.findall(r'<a id="([ab]-m\d{2}-s\d{2})"', content))
        labs.update(value.upper() for value in re.findall(r'<a id="(lab-[ab]-m\d{2}-s\d{2}-\d{2})"', content))
        for line in content.splitlines():
            if line.startswith('| <a id=') and re.search(LESSON_ID, line):
                row = cells(line)
                prereq = re.search(LESSON_ID, row[5])
                lessons.append({'id': re.search(LESSON_ID, row[0]).group(), 'week': int(row[1][1:]), 'level': row[2], 'concepts': row[3], 'minutes': int(row[4]), 'prereq': prereq.group() if prereq else None, 'question': row[6], 'sources': re.findall(r'\[(D\d{2})\]', row[7])})
        for label in ['Артефакт:', 'Негативный кейс:', 'Критерий готовности навыка:']:
            if content.count(label) != len([w for w in weeks if w['module'] == path.parent.name[:5]]):
                errors.append(f'{path.relative_to(root)}: не у каждого недельного lab есть {label}')
    errors += validate_plan(weeks, lessons)
    if len(labs) != len(weeks):
        errors.append('Не каждой неделе соответствует отдельный lab-ID')
    all_questions = []
    for section in sorted(sections):
        question_path = root / f'interviews/questions/INT-{section}.md'
        key_path = root / f'interviews/answer-keys/INT-{section}.md'
        if not question_path.is_file() or not key_path.is_file():
            errors.append(f'{section}: отсутствует банк или отдельный ключ')
            continue
        question = question_path.read_text()
        answer = key_path.read_text()
        qids = re.findall(r'`(Q-[AB]-M\d{2}-S\d{2}-\d{2})`', question)
        kids = re.findall(r'^\| (Q-[AB]-M\d{2}-S\d{2}-\d{2}) \|', answer, re.M)
        if len(qids) != 8 or qids != kids:
            errors.append(f'{section}: нужно 5 базовых + 2 сценария + 1 tradeoff с отдельными критериями')
        if question.count('| troubleshooting |') != 2 or question.count('| tradeoff |') != 1:
            errors.append(f'{section}: неверное распределение сценариев')
        if 'Минимальные тезисы' in question or 'Общая рубрика:' in question:
            errors.append(f'{section}: критерии ответа попали в вопрос')
        all_questions.extend(qids)
    if len(all_questions) != len(set(all_questions)):
        errors.append('ID вопроса повторяется')
    link_count, link_errors = check_links(root)
    errors += link_errors
    for path in root.rglob('*.md'):
        if '.git' in path.parts:
            continue
        content = path.read_text()
        if not content.endswith('\n'):
            errors.append(f'{path.relative_to(root)}: нет завершающего перевода строки')
        if any(line != line.rstrip() for line in content.splitlines()):
            errors.append(f'{path.relative_to(root)}: пробел в конце строки')
    summary = {'modules': len(modules), 'sections': len(sections), 'lessons_planned': len(lessons), 'labs_planned': len(labs), 'questions': len(all_questions), 'weeks': len(weeks), 'A_hours': totals['A'], 'B_hours': totals['B'], 'local_links': link_count}
    return summary, errors


class ModelTests(unittest.TestCase):
    def fixture(self):
        weeks = [{'number': 1, 'minutes': [180,60,180,60,480]}]
        lessons = []
        for i in range(1,4):
            lessons.append({'id': f'A-M01-S01-L{i:02}', 'week':1, 'minutes':60, 'level':'J0', 'concepts':'Конкретная тема', 'question':'Как проверить?', 'sources':['D01'], 'prereq': f'A-M01-S01-L{i-1:02}' if i>1 else None})
        return weeks, lessons

    def test_valid(self):
        self.assertEqual(validate_plan(*self.fixture(), expected_weeks=1), [])

    def test_bad_time(self):
        w,l = self.fixture(); w[0]['minutes'][0] = 181
        self.assertTrue(validate_plan(w,l,1))

    def test_missing_prerequisite(self):
        w,l = self.fixture(); l[1]['prereq'] = 'A-M99-S01-L01'
        self.assertTrue(validate_plan(w,l,1))

    def test_forward_and_cycle(self):
        w,l = self.fixture(); l[0]['prereq'] = l[-1]['id']
        self.assertTrue(validate_plan(w,l,1))

    def test_duplicate_id(self):
        w,l = self.fixture(); l[-1]['id'] = l[0]['id']
        self.assertTrue(validate_plan(w,l,1))

    def test_middle_in_A(self):
        w,l = self.fixture(); l[0]['level'] = 'M'
        self.assertTrue(validate_plan(w,l,1))

    def test_missing_week_lesson(self):
        w,l = self.fixture(); l.pop()
        self.assertTrue(validate_plan(w,l,1))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true', help='проверить валидатор на синтетических ошибках, не менять курс')
    args = parser.parse_args()
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(ModelTests))
        return 0 if result.wasSuccessful() else 1
    summary, errors = audit(ROOT)
    for key, value in summary.items():
        print(f'{key}: {value}')
    for error in errors:
        print(f'ERROR: {error}', file=sys.stderr)
    print('PASS' if not errors else 'FAIL')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
