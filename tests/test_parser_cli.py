import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.utils.petri_parser import parse_wn_from_pnml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/sequence.pnml'


class ParserTests(unittest.TestCase):
    def parse_text(self, text):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'net.pnml'
            path.write_text(text, encoding='utf-8')
            return parse_wn_from_pnml(path)

    def test_namespaced_pnml_with_unnamed_places(self):
        net = parse_wn_from_pnml(EXAMPLE)
        self.assertEqual([p['id'] for p in net['places']], ['start', 'middle', 'end'])
        self.assertEqual([t['id'] for t in net['transitions']], ['t1', 't2'])
        self.assertEqual([t['name'] for t in net['transitions']], ['Approve', 'Approve'])
        self.assertEqual(net['places'][0]['initialMarking'], '1')
        self.assertEqual(net['places'][-1]['finalMarking'], '1')

    def test_no_namespace_or_explicit_markings(self):
        text = EXAMPLE.read_text().replace(' xmlns="http://www.pnml.org/version-2009/grammar/pnml"', '')
        text = text.replace('<initialMarking><text>1</text></initialMarking>', '')
        text = text.replace('<finalmarkings><marking><place idref="end"><text>1</text></place></marking></finalmarkings>', '')
        net = self.parse_text(text)
        self.assertEqual(net['places'][0]['initialMarking'], '1')
        self.assertEqual(net['places'][-1]['finalMarking'], '1')

    def test_invisible_and_unnamed_transitions_remain_distinct(self):
        text = EXAMPLE.read_text().replace('<name><text>Approve</text></name>',
                                          '<toolspecific activity="$invisible$"/>')
        net = self.parse_text(text)
        self.assertEqual(net['transitions'], [{'id': 't1', 'name': 't1'}, {'id': 't2', 'name': 't2'}])

    def test_reject_unsupported_or_malformed_nets(self):
        text = EXAMPLE.read_text()
        variants = {
            'duplicate node': text.replace('transition id="t2"', 'transition id="t1"'),
            'dangling arc': text.replace('target="t2"', 'target="missing"'),
            'weighted arc': text.replace('<arc id="a1" source="start" target="t1"/>',
                '<arc id="a1" source="start" target="t1"><inscription><text>2</text></inscription></arc>'),
            'bad initial marking': text.replace('<initialMarking><text>1', '<initialMarking><text>2'),
            'bad final marking': text.replace('idref="end"><text>1', 'idref="end"><text>2'),
            'disconnected place': text.replace('</page>', '<place id="disconnected"/></page>'),
            'empty net': '<pnml><net id="empty"/></pnml>',
            'multiple nets': text.replace('</pnml>', '<net id="second"/></pnml>'),
        }
        for description, variant in variants.items():
            with self.subTest(case=description), self.assertRaises(ValueError):
                self.parse_text(variant)


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / 'main.py'), *map(str, args)],
                              cwd=ROOT, capture_output=True, text=True)

    def test_json_and_csv_translation(self):
        with tempfile.TemporaryDirectory() as folder:
            for output_format in ('json', 'csv'):
                with self.subTest(format=output_format):
                    path = Path(folder) / f'model.{output_format}'
                    result = self.run_cli('declare-synth', '--pnml-file', EXAMPLE,
                                          '--output-path', path, '--output-format', output_format)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    if output_format == 'json':
                        self.assertEqual(json.loads(path.read_text())['tasks'], ['t1', 't2'])
                    else:
                        with path.open() as file:
                            self.assertEqual([row[0] for row in csv.reader(file)], ['name', 'tasks', 'constraints'])

    def test_export_wn(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'net.json'
            result = self.run_cli('export-wn', '--pnml-file', EXAMPLE, '--output-path', path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(path.read_text())['transitions']), 2)

    def test_invalid_input_and_format_fail_without_output(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'output.json'
            broken = Path(folder) / 'broken.pnml'
            broken.write_text('<pnml><net id="empty"/></pnml>')
            for source, fmt in ((EXAMPLE, 'invalid'), (Path(folder) / 'missing.pnml', 'json'), (broken, 'json')):
                with self.subTest(source=source, format=fmt):
                    result = self.run_cli('declare-synth', '--pnml-file', source,
                                          '--output-path', path, '--output-format', fmt)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse(path.exists())
                    self.assertNotIn('Traceback', result.stderr)

    def test_experimental_commands_are_not_exposed(self):
        result = self.run_cli('--help')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('declare-synth', result.stdout)
        self.assertNotIn('declare-silent-synth', result.stdout)
        self.assertNotIn('conformance', result.stdout)


if __name__ == '__main__':
    unittest.main()
