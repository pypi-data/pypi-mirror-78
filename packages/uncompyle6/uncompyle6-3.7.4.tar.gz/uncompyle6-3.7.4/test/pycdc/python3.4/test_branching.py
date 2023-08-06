from uncompyle6.test.basetestsblackbox.blackboxtestcase import BlackBoxTestCase


class TestBranching(BlackBoxTestCase):

    def test_if(self):
        infile = "branching/if.cpython-32.pyc"
        expected = "branching/if.py"
        self.assertProgramOutput(infile, expected)

    def test_ifelse(self):
        infile = "branching/ifelse.cpython-32.pyc"
        expected = "branching/ifelse.py"
        self.assertProgramOutput(infile, expected)
