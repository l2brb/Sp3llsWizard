import copy
import unittest

from src.declare_translator.dec_translator import translate_to_DEC
from src.declare_translator.output import format_specification
from tests.behavior import assert_equivalent, make_net


class OutputTests(unittest.TestCase):
    def test_ids_preserve_constraints_and_include_mapping(self):
        net = make_net({'t1': (['i'], ['p']), 't2': (['p'], ['o'])},
                       {'t1': 'Approve', 't2': 'Approve'})
        specification = translate_to_DEC(net, 'sequence')
        original = copy.deepcopy(specification)
        output = format_specification(specification, net, "ids")
        self.assertEqual(output['transitionsMap'], {'Approve': ['t1', 't2']})
        self.assertEqual(output['tasks'], ['t1', 't2'])
        self.assertEqual(output['constraints'], specification['constraints'])
        output['constraints'][0]['parameters'][0].append('modified')
        self.assertEqual(specification, original)

    def test_duplicate_labels_are_substituted_only_after_synthesis(self):
        net = make_net({'t1': (['i'], ['p']), 't2': (['p'], ['o'])},
                       {'t1': 'Approve', 't2': 'Approve'})
        original_net = copy.deepcopy(net)
        specification = translate_to_DEC(net, 'sequence')
        output = format_specification(specification, net)
        self.assertEqual(output['tasks'], ['Approve'])
        self.assertEqual(output['constraints'], [
            {'template': 'End', 'parameters': [['Approve']]},
            {'template': 'Atmost1', 'parameters': [['Approve']]},
            {'template': 'AlternatePrecedence', 'parameters': [['Approve'], ['Approve']]},
        ])
        self.assertEqual(output['transitionsMap'], {'Approve': ['t1', 't2']})
        self.assertEqual(specification['tasks'], ['t1', 't2'])
        self.assertEqual(net, original_net)

    def test_unique_labels_preserve_language_under_renaming(self):
        # A label can equal another transition's ID; substitution is simultaneous.
        net = make_net({'t1': (['i'], ['p']), 't2': (['p'], ['o'])},
                       {'t1': 't2', 't2': 'Finish'})
        output = format_specification(translate_to_DEC(net, 'sequence'), net, 'labels')
        renamed_net = make_net({'t2': (['i'], ['p']), 'Finish': (['p'], ['o'])})
        assert_equivalent(self, renamed_net, output)

    def test_missing_labels_fall_back_to_ids_and_keep_transitions(self):
        net = make_net({'t1': (['i'], ['p']), 't2': (['p'], ['o'])})
        net['transitions'][0]['name'] = None
        net['transitions'][1]['name'] = ' '
        net['transitions'][1]['is_tau'] = True
        output = format_specification(translate_to_DEC(net, 'sequence'), net, 'labels')
        self.assertEqual(output['tasks'], ['t1', 't2'])
        self.assertEqual(output['transitionsMap'], {'t1': ['t1'], 't2': ['t2']})

    def test_invalid_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            format_specification({}, {}, 'unknown')
