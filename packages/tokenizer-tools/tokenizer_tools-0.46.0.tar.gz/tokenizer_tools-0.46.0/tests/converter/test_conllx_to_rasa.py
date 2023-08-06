import json

import pytest
from jsoncomparison import Compare, NO_DIFF

from tokenizer_tools.converter.conllx_to_rasa import conllx_to_rasa


def test_conllx_to_rasa(datadir, tmpdir):
    expected_file = datadir / "output.json"
    result_file = tmpdir / "output.json"

    rs = conllx_to_rasa(datadir / "input.conllx", result_file)
    print(rs)

    with open(expected_file) as e_fd, open(result_file) as r_fd:
        expected = json.load(e_fd)
        result = json.load(r_fd)

        assert Compare().check(result, expected) == NO_DIFF

def test_conllx_with_role_and_group_to_rasa(datadir, tmpdir):
    expected_file = datadir / "output_with_role_and_group.json"
    result_file = tmpdir / "output_with_role_and_group.json"

    rs = conllx_to_rasa(datadir / "input_with_role_and_group.conllx", result_file)
    print(rs)

    with open(expected_file) as e_fd, open(result_file) as r_fd:
        expected = json.load(e_fd)
        result = json.load(r_fd)

        assert Compare().check(result, expected) == NO_DIFF
