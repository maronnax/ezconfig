from datetime import datetime
import os

import copy
import pdb
import ezconfig.config
import testdata
from nose.tools import assert_raises


def test_config_composion_interleaving():
    comp1_fn = testdata.get_comp1_test_config_filename()
    comp2_fn = testdata.get_comp2_test_config_filename()
    comp3_fn = testdata.get_comp3_test_config_filename()

    def make_permutation_generator(*filenames):
        def instantiation_permutation(*args):
            if len(args) == 0: # Set the default case as the identity permutation.
                return ezconfig.config.Configuration(*filenames)
            args = [(x-1) for x in args] # Make zero indexed
            return ezconfig.config.Configuration(*[filenames[ndx] for ndx in args])
        return instantiation_permutation

    def make_answer_key_generator(answers, *values):
        def generate_answer_key(*args):
            values = values[:] # Make a local copy, b/c we want to shuffle it.
            if len(args):
                values = [v[ndx] for ndx in args]

            # What I am going to do here is decompose the args
            # permutation into a set of cycles: e.g. (3 2 1) -> I (3
            # 2) (2 1) (1 3).  Then I'll make a dict of (1 2), (1 3),
            # (2 3) pairs that map to values which are pairs of key
            # swaps.  So (x y) == (y x) (updating the answer key by
            # swapping two variables around is undone by swapping it
            # back)

            # So any permutation can be obtained by decomposing it
            # into cycles, taking the Identity answer key, sorting the
            # cycles, looking up that function (list of key swaps),
            # and applying the swaps in order.

            answers = copy.copy(answers)

            if not len(args):
                return answers_identity_perm

            swap_var_map = {(1,2): [("common", "conf2_value"), ("1and2", "conf2_value")],
                            (2,1): [("common", "conf1_value"), ("1and2", "conf1_value")],
                            (1,3): [("common", "conf3_value"), ("1and3", "conf1_value")],
                            (3,1): [("common", "conf1_value"), ("1and3", "conf3_value")],
                            (2,3): [("common", "conf3_value"), ("2and3", "conf2_value")],
                            (3,2): [("common", "conf2_value"), ("2and3", "conf2_value")],
                            }

            cycles = [(ndx, ndx+1) for ndx in range(len(args_file))] + [ (args_file[-1], args_file[0]) ]

            for cycle in cycles:
                answers.update(dict(swap_var_map[cycle]))

            return swap_var_map

    conf_filenames = (comp1_fn, comp2_fn, comp3_fn)
    config = make_permutation_generator(*conf_filenames)

    perm1 = (1,2,3)
    perm2 = (2,3,1)

    assert len(config(*perm1).sections()) == len(set(config(*perm1).sections())) == len(config(*perm2).sections())
    assert set(config(*perm1).sections()) == set(config(*perm2).sections())

    assert config(1,2,3).sections() == \
        ["only1", "1and2", "1and3", "common", "only2", "2and3", "only3"]

    assert config(2,3,1).sections() == \
        ["only2", "1and2", "2and3", "common", "only3", "1and3", "only1"]

    MISSING_KEY="a missing key"
    with assert_raises(KeyError):
        config().get("conversions", MISSING_KEY, mandatory=True)


    with assert_raises(ValueError):
        config().get("conversions", MISSING_KEY,
                 default="Mandatory is mandatory dude.",
                 mandatory=True)

    MISSING_SECTION="this bit isn't in the documentation!"
    MISSING_KEY="where was that scrap of paper I wrote the keys on"

    assert config().get("common", "value", mandatory=True) == "conf1_val"
    assert config().get("2and3", "value", mandatory=True) == "conf2_val"
    with assert_raises(KeyError):
        config().get("conversions", MISSING_KEY, mandatory=True)

    with assert_raises(KeyError):
        config().get(MISSING_SECTION, MISSING_KEY, mandatory=True)

    with assert_raises(ValueError):
        config().get(MISSING_SECTION, MISSING_KEY, mandatory=True, default="a thing")

    answers = {
        "only1": "conf1_val",
        "1and2": "conf1_val",
        "1and3": "conf1_val",
        "common": "conf1_val",
        "only2": "conf2_val",
        "2and3": "conf2_val",
        "only3": "conf3_val"
    }

    # for (key, val) in answers.items():
    #     assert config().get(key, "value") == val

    # answer_key = make_answer_key_generator(answers, conf_filenames)
    # perm_set = [(2,1,3), (3,2,1), (3,1,2)]
    # for perm in perm_set:
    #     for (key, val) in answers.items():
    #         print "perm={}, key={}, val={}, ret={}".format(perm, key, val, config(*perm).get(key, "value"))
    #         assert config(*perm).get(key, "value") == val


    perms = [(1,2,3), (2,3,1), (3,1,2), (2,1,3), (3,1,2)]

    for p in perms:
        assert config(*p).get_key_help("1and2", "value") == "A long and great help message"
        assert config(*p).get_key_help("2and3", "value") == "A different help message only found once"
