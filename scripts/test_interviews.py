"""Все результаты в этих тестах синтетические; курс и прогресс не изменяются."""
import contextlib
from datetime import date, timedelta
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import interview as app


class InterviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for directory in ['questions/demo', 'answer-keys/demo', 'results']:
            (self.root / 'interviews' / directory).mkdir(parents=True)
        self.qid = 'Q-A-M02-S03-01'
        self.counter = 0
        self.question(self.qid)
        self.schedule([])

    def question(self, qid, level='J0', minutes=3):
        path = self.root / f'interviews/questions/demo/{qid}.md'
        path.write_text(f'''# Синтетический вопрос

- ID: {qid}
- Статус: проверено
- Назначение: пример
- Модуль: {qid[2:7]}
- Раздел: {qid[2:11]}
- Уроки: {qid[2:11]}-L01
- Уровень: {level}
- Тип: mechanism
- Проверяет: Синтетический навык
- Лаборатория: нет
- Минуты: {minutes}
- Происхождение: синтетическая fixture
- Источник: синтетическая fixture

## Вопрос

Какое безопасное наблюдение выберешь?

## Условия

Ничего не выполнять.
''')
        (self.root / f'interviews/answer-keys/demo/{qid}.md').write_text('SECRET_KEY_MARKER: не читать до ответа')
        return path

    def result(self, qid=None, day=date(2026, 1, 1), score=1, stage='initial', base=None):
        self.counter += 1
        qid = qid or self.qid
        rid = f'RES-{day.isoformat()}-{self.counter:03}'
        question = app.load_questions(self.root)[qid]
        (self.root / f'interviews/results/{rid}.md').write_text(f'''# Синтетическая fixture, не результат студента

- ID: {rid}
- Вопрос: {qid}
- Дата: {day.isoformat()}
- Уровень: {question.level}
- Этап: {stage}
- Базовая проверка: {base or '—'}
- Оценка: {score}
- Ответ: синтетическая fixture
- Обоснование: синтетическая fixture
- Ошибка: синтетическая fixture
- Подсказки: нет
- Следующее действие: синтетическая fixture
''')
        return rid

    def row(self, rid, day=date(2026, 1, 1), qid=None, done7='—', done30='—'):
        return f'| {rid} | {qid or self.qid} | {day} | {day+timedelta(days=7)} | {done7} | {day+timedelta(days=30)} | {done30} | — |'

    def schedule(self, rows):
        path = self.root / 'interviews/review-schedule.md'
        path.write_text('# Синтетическая fixture\n\n| Базовый результат | Вопрос | D | Срок +7 | Результат +7 | Срок +30 | Результат +30 | Перенос / причина |\n|---|---|---|---|---|---|---|---|\n'+'\n'.join(rows)+'\n')

    def queue(self, on=date(2026, 1, 8), **kwargs):
        return app.review(self.root, on, **kwargs)

    def test_empty_results_create_no_schedule(self):
        self.assertEqual(self.queue(), ([], 0, 0))

    def test_seven_day_boundary(self):
        rid = self.result(); self.schedule([self.row(rid)])
        self.assertFalse(self.queue(date(2026,1,7))[0])
        self.assertEqual(self.queue()[0][0].stage, 'review-7')

    def test_calendar_month_and_leap_year(self):
        day = date(2024,1,31); rid = self.result(day=day); self.schedule([self.row(rid,day)])
        questions = app.load_questions(self.root); results = app.load_results(self.root,questions)
        before = app.scheduled_candidates(self.root,questions,results,date(2024,2,29))
        after = app.scheduled_candidates(self.root,questions,results,date(2024,3,1))
        self.assertNotIn('review-30',[c.stage for c in before])
        self.assertIn('review-30',[c.stage for c in after])

    def test_completion_closes_only_one_stage(self):
        rid=self.result(); done=self.result(day=date(2026,1,8),stage='review-7',base=rid)
        self.schedule([self.row(rid,done7=done)])
        self.assertFalse(self.queue()[0])
        self.assertEqual(self.queue(date(2026,1,31))[0][0].stage,'review-30')

    def test_future_completion_does_not_change_past_queue(self):
        rid=self.result(); done=self.result(day=date(2026,1,9),stage='review-7',base=rid)
        self.schedule([self.row(rid,done7=done)])
        self.assertEqual(self.queue()[0][0].stage,'review-7')

    def test_early_retest_rejected(self):
        rid=self.result(); self.result(day=date(2026,1,7),stage='review-7',base=rid)
        with self.assertRaises(app.InvalidData): self.queue()

    def test_wrong_question_completion_rejected(self):
        other='Q-A-M02-S03-02'; self.question(other)
        rid=self.result(); other_rid=self.result(qid=other)
        done=self.result(qid=other,day=date(2026,1,8),stage='review-7',base=other_rid)
        self.schedule([self.row(rid,done7=done)])
        with self.assertRaises(app.InvalidData): self.queue()

    def test_wrong_stage_completion_rejected(self):
        rid=self.result(); done=self.result(day=date(2026,1,31),stage='review-30',base=rid)
        self.schedule([self.row(rid,done7=done)])
        with self.assertRaises(app.InvalidData): self.queue(date(2026,1,31))

    def test_changed_deadline_rejected(self):
        rid=self.result(); self.schedule([self.row(rid).replace('2026-01-08','2026-01-09')])
        with self.assertRaises(app.InvalidData): self.queue()

    def test_duplicate_schedule_rejected(self):
        rid=self.result(); self.schedule([self.row(rid),self.row(rid)])
        with self.assertRaises(app.InvalidData): self.queue()

    def test_weak_junior_first_and_budget_bounded(self):
        strong='Q-A-M02-S03-02'; extra='Q-A-M02-S03-03'
        self.question(strong); self.question(extra,level='J1')
        a=self.result(score=0); b=self.result(qid=strong,score=3); c=self.result(qid=extra,score=0)
        self.schedule([self.row(c,qid=extra),self.row(b,qid=strong),self.row(a)])
        chosen,used,deferred=self.queue(minutes=3)
        self.assertEqual([c.qid for c in chosen],[self.qid]); self.assertEqual(used,3); self.assertEqual(deferred,2)

    def test_middle_is_opt_in(self):
        qid='Q-B-M01-S01-01'; self.question(qid,level='M'); rid=self.result(qid=qid)
        self.schedule([self.row(rid,qid=qid)])
        self.assertFalse(self.queue()[0]); self.assertTrue(self.queue(include_m=True)[0])
        with self.assertRaises(app.InvalidData): app.show(self.root,qid)
        self.assertIn(qid,app.show(self.root,qid,True))

    def test_duplicate_due_question_is_shown_once(self):
        rid=self.result(); self.schedule([self.row(rid)])
        chosen,_,deferred=self.queue(date(2026,1,31))
        self.assertEqual(len(chosen),1); self.assertEqual(deferred,1)

    def test_mixed_only_every_four_weeks(self):
        rid=self.result(); self.schedule([self.row(rid)])
        self.assertFalse(self.queue(date(2026,1,2),week=3)[0]); self.assertEqual(self.queue(date(2026,1,2),week=4)[0][0].stage,'mixed')

    def test_mixed_does_not_repeat_todays_answer(self):
        day=date(2026,1,8); rid=self.result(day=day); self.schedule([self.row(rid,day)])
        self.assertFalse(self.queue(week=4)[0])

    def test_initial_without_schedule_is_reported(self):
        self.result()
        with self.assertRaises(app.InvalidData): self.queue()

    def test_mixed_does_not_close_interval(self):
        rid=self.result(); self.result(day=date(2026,1,8),stage='mixed'); self.schedule([self.row(rid)])
        self.assertEqual(self.queue(week=4)[0][0].stage,'review-7')

    def test_invalid_date_score_and_budget(self):
        for value in ['2026-02-30','2026-1-01','today']:
            with self.assertRaises(app.InvalidData): app.iso(value)
        self.result(score=4)
        with self.assertRaises(app.InvalidData): self.queue()
        for minutes in [0,61]:
            with self.assertRaises(app.InvalidData): self.queue(minutes=minutes)

    def test_repeated_metadata_field_rejected(self):
        p=self.root/f'interviews/questions/demo/{self.qid}.md'
        p.write_text(p.read_text()+'\n- Уровень: M\n')
        with self.assertRaises(app.InvalidData): app.show(self.root,self.qid)

    def test_wrong_id_and_answer_in_card_rejected(self):
        p=self.root/f'interviews/questions/demo/{self.qid}.md'
        original=p.read_text(); p.write_text(original.replace('- Раздел: A-M02-S03','- Раздел: A-M02-S02'))
        with self.assertRaises(app.InvalidData): app.show(self.root,self.qid)
        p.write_text(original+'\n## Тезисы хорошего ответа\n\nНельзя включать.\n')
        with self.assertRaises(app.InvalidData): app.show(self.root,self.qid)

    def test_show_one_question_reads_no_keys_and_writes_nothing(self):
        other='Q-A-M02-S03-02'; self.question(other)
        before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob('*') if p.is_file()}
        original=Path.read_text
        def guarded(path,*args,**kwargs):
            if 'answer-keys' in path.parts or path.name==other+'.md':
                raise AssertionError('show прочитал лишний вопрос/ключ')
            return original(path,*args,**kwargs)
        with patch.object(Path,'read_text',guarded):
            output=app.show(self.root,self.qid)
        self.assertNotIn('SECRET_KEY_MARKER',output); self.assertNotIn(other,output)
        def no_keys(path,*args,**kwargs):
            if 'answer-keys' in path.parts:
                raise AssertionError('review прочитал ключ')
            return original(path,*args,**kwargs)
        with patch.object(Path,'read_text',no_keys):
            self.queue()
        after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before,after)

    def test_cli_empty_queue_and_bad_question(self):
        with patch.object(app,'ROOT',self.root),contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(app.main(['review','--on','2026-01-08']),0)
        self.assertIn('Изменений нет',out.getvalue())
        with patch.object(app,'ROOT',self.root),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(app.main(['show','../../answer-keys']),2)


class RepositoryCardsTests(unittest.TestCase):
    def test_complete_examples_and_separate_keys(self):
        questions=app.load_questions(app.ROOT)
        examples={qid:q for qid,q in questions.items() if qid.startswith('Q-A-M02-S03-')}
        self.assertEqual(len(examples),8)
        self.assertEqual(sum(q.minutes for q in examples.values()),35)
        bank=(app.ROOT/'interviews/questions/INT-A-M02-S03.md').read_text()
        for qid,question in examples.items():
            self.assertIn(qid,bank)
            key=app.ROOT/f'interviews/answer-keys/networking/{qid}.md'
            content=key.read_text()
            self.assertEqual(app.fields(content)['ID'],qid)
            for heading in ['## Тезисы хорошего ответа','## Распространённые ошибки','## Необязательное уточнение','## Оценка 0–3']:
                self.assertIn(heading,content)
        app.load_results(app.ROOT,questions)


if __name__=='__main__':
    unittest.main()
