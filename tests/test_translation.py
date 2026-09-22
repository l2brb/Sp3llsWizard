import copy
import unittest
from pathlib import Path

from src.declare_translator.dec_translator import translate_to_DEC
from src.utils.petri_parser import parse_wn_from_pnml
from tests.behavior import accepts, assert_equivalent, make_net

ROOT = Path(__file__).resolve().parents[1]


class TranslationTests(unittest.TestCase):
    def fixtures(self):
        return {
            'single': make_net({'t1': (['i'], ['o'])}),
            'sequence_duplicate_names': make_net(
                {'t1': (['i'], ['p']), 't2': (['p'], ['o'])}, {'t1': 'A', 't2': 'A'}),
            'xor': make_net({'a': (['i'], ['p']), 'b': (['p'], ['q']),
                             'c': (['p'], ['q']), 'd': (['q'], ['o'])}),
            'and': make_net({'a': (['i'], ['p', 'q']), 'b': (['p'], ['r']),
                             'c': (['q'], ['s']), 'd': (['r', 's'], ['o'])}),
            'loop': make_net({'a': (['i'], ['p']), 'b': (['p'], ['q']),
                              'c': (['q'], ['p']), 'd': (['q'], ['o'])}),
            'self_loop': make_net({'a': (['i'], ['p']), 'b': (['p'], ['p']),
                                   'c': (['p'], ['o'])}),
            'boundary_choices': make_net({'a': (['i'], ['p']), 'b': (['i'], ['p']),
                                          'c': (['p'], ['o']), 'd': (['p'], ['o'])}),
        }

    def test_full_language_equivalence_on_small_nets(self):
        for name, net in self.fixtures().items():
            with self.subTest(net=name):
                assert_equivalent(self, net, translate_to_DEC(net, name))

    def test_repository_models_full_language_equivalence(self):
        paths = sorted((ROOT / 'evaluation/bisimulation/test/wn_collection/wn').glob('*.pnml'))
        self.assertEqual(len(paths), 5)
        for path in paths:
            with self.subTest(net=path.name):
                net = parse_wn_from_pnml(path)
                assert_equivalent(self, net, translate_to_DEC(net, path.name))

    def test_exact_sequence_specification_uses_ids(self):
        net = self.fixtures()['sequence_duplicate_names']
        self.assertEqual(translate_to_DEC(net, 'sequence'), {
            'name': 'sequence', 'tasks': ['t1', 't2'], 'constraints': [
                {'template': 'End', 'parameters': [['t2']]},
                {'template': 'Atmost1', 'parameters': [['t1']]},
                {'template': 'AlternatePrecedence', 'parameters': [['t1'], ['t2']]},
            ]})

    def test_names_and_invisibility_metadata_do_not_change_specification(self):
        net = self.fixtures()['loop']
        expected = translate_to_DEC(net, 'same')
        for transition in net['transitions']:
            transition['name'] = 'tau'
            transition['is_tau'] = True
        self.assertEqual(translate_to_DEC(net, 'same'), expected)
        for transition in net['transitions']:
            del transition['name']
        self.assertEqual(translate_to_DEC(net, 'same'), expected)

    def test_branches_preserve_choice_and_synchronization(self):
        xor = translate_to_DEC(self.fixtures()['xor'], 'xor')
        parallel = translate_to_DEC(self.fixtures()['and'], 'and')
        self.assertTrue(accepts(xor, 'abd'))
        self.assertTrue(accepts(xor, 'acd'))
        self.assertFalse(accepts(xor, 'abcd'))
        self.assertTrue(accepts(parallel, 'abcd'))
        self.assertTrue(accepts(parallel, 'acbd'))
        self.assertFalse(accepts(parallel, 'abd'))

    def test_translation_does_not_mutate_input(self):
        net = self.fixtures()['and']
        original = copy.deepcopy(net)
        translate_to_DEC(net, 'and')
        self.assertEqual(net, original)

    def test_oracle_detects_a_missing_constraint(self):
        net = self.fixtures()['sequence_duplicate_names']
        spec = translate_to_DEC(net, 'broken')
        spec['constraints'].pop()
        with self.assertRaisesRegex(AssertionError, 'Distinguishing transition trace'):
            assert_equivalent(self, net, spec)


if __name__ == '__main__':
    unittest.main()
