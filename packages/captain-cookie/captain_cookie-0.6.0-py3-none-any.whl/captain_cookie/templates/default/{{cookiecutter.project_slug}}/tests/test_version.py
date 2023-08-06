""" A dummy test to demonstrate pytest fixture usage """


def test_current_version(version):
    """ Receive current version from fixture and check value.

    In a real test you might want to do some operation on the fixture value
    before asserting a condition.
    """
    assert version == "0.1.0"
