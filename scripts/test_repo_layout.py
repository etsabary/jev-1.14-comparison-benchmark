"""Regressions for current-source resolution and explicit historical audits."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import shlex
import tempfile
import unittest
from unittest.mock import patch

import repo_layout as layout


class RepositoryLayout(unittest.TestCase):
    def test_complete_source_only_migration(self):
        from validate_repository_layout import validate
        validate()

    def test_workflow_unittest_targets_resolve_after_relocation(self):
        commands = 0
        for workflow in (layout.ROOT / '.github/workflows').glob('*.yml'):
            for line in workflow.read_text().splitlines():
                if '- run: python3 -m unittest ' not in line:
                    continue
                arguments = shlex.split(line.split('- run: ', 1)[1])[3:]
                if 'discover' in arguments:
                    continue
                commands += 1
                for target in arguments:
                    if target.startswith('-'):
                        continue
                    with self.subTest(workflow=workflow.name, target=target):
                        if target.endswith('.py'):
                            self.assertTrue((layout.ROOT / target).is_file())
                        else:
                            self.assertIsNotNone(importlib.util.find_spec(target))
        self.assertGreater(commands, 0)

    def test_current_sources_are_not_the_archived_implementation(self):
        active = layout.source_file('frontier_reference.py')
        old = layout.frozen_file('frontier_reference.py')
        self.assertEqual(active, layout.SCRIPTS / 'frontier_reference.py')
        self.assertNotEqual(active, old)
        self.assertNotEqual(active.read_bytes(), old.read_bytes())
        self.assertEqual(layout.frozen_file(active), old)

    def test_data_paths_are_not_redirected(self):
        path = layout.ROOT / 'consolidated_2026-10-19/questions_1342.jsonl'
        self.assertEqual(layout.source_file(path), path)
        self.assertEqual(layout.frozen_file(path), path)

    def test_report_renderers_still_build_all_current_rows_and_categories(self):
        import publish_october21_additions as report
        from validate_direct_release import Page
        statistics = json.loads((report.DEST / 'statistics.json').read_text())
        guide = json.loads((report.DEST / 'category_guide.json').read_text())
        page = Page()
        page.feed(report.summary_html(statistics))
        page.feed(report.readable.clarity_section(statistics, guide))
        self.assertEqual(page.summary, statistics['ranked_model_ids'])
        self.assertEqual(len(page.cells), 29 * 31)
        for cell in page.cells:
            score = statistics['models'][cell['data-model']]['families'][cell['data-category']]
            self.assertEqual((int(cell['data-correct']), int(cell['data-n'])),
                             (score['correct'], score['n']))

    def test_live_tev_controller_pin_matches_executed_source(self):
        import tev_screening_2026_10_18 as wrapper
        controller = layout.source_file('llm_screening_2026_10_18.py')
        self.assertEqual(wrapper.CONTROL_SHA256, sha256(controller.read_bytes()).hexdigest())
        self.assertEqual(Path(wrapper.control.__file__), Path(wrapper.__file__))

    def test_live_resume_rejects_old_software_by_default(self):
        name = 'frontier_reference.py'
        previous = {name: sha256(layout.frozen_file(name).read_bytes()).hexdigest()}
        current = {name: sha256(layout.source_file(name).read_bytes()).hexdigest()}
        with self.assertRaisesRegex(AssertionError, 'Frozen execution software changed'):
            layout.verify_software(previous, current)
        layout.verify_software(previous, current, historical=True)
        layout.verify_software(current, current)

    def test_historical_audits_reject_wrong_hash_or_missing_dependency(self):
        current = {'frontier_reference.py': 'current'}
        with self.assertRaises(AssertionError):
            layout.verify_software({'frontier_reference.py': 'wrong'}, current, historical=True)
        with self.assertRaisesRegex(AssertionError, 'dependency set'):
            layout.verify_software({}, current, historical=True)

    def test_archive_bytes_cannot_be_silently_changed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / 'scripts/legacy_layout'
            archive.mkdir(parents=True)
            saved = archive / 'example.py.snapshot'
            saved.write_text('original')
            manifest = root / 'scripts/layout_manifest.json'
            manifest.write_text(json.dumps({'moved_sources': {'example.py': 'scripts/example.py'},
                'preserved_sources': {'example.py': {'archive_path': 'scripts/legacy_layout/example.py.snapshot',
                    'sha256': sha256(saved.read_bytes()).hexdigest()}}}))
            with patch.multiple(layout, ROOT=root, ARCHIVE=archive, MANIFEST=manifest):
                self.assertEqual(layout.frozen_file('example.py'), saved)
                saved.write_text('changed')
                with self.assertRaises(AssertionError):
                    layout.frozen_file('example.py')


if __name__ == '__main__':
    unittest.main()
