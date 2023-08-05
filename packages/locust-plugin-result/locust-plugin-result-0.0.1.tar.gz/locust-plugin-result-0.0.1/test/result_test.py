# -*- coding: utf-8 -*-


from locust_plugin_result.result import set_result, RESULT_PASS, RESULT_WARN, RESULT_FAIL


class _MockRunner():
    pass


def test_set_first_result():
    mr = _MockRunner()
    set_result(mr, RESULT_PASS, "Nice")
    assert mr.result.value == RESULT_PASS
    assert mr.result.reason == "Nice"


def test_set_result_again_warn_to_fail():
    mr = _MockRunner()

    set_result(mr, RESULT_WARN, "Up there")
    assert mr.result.value == RESULT_WARN
    assert mr.result.reason == "Up there"

    set_result(mr, RESULT_FAIL, "Out of bounds!")
    assert mr.result.value == RESULT_FAIL
    assert mr.result.reason == "Out of bounds!"


def test_set_result_again_fail_to_warn_ignored(caplog):
    mr = _MockRunner()

    set_result(mr, RESULT_FAIL, "Out of bounds!")
    assert mr.result.value == RESULT_FAIL
    assert mr.result.reason == "Out of bounds!"

    set_result(mr, RESULT_WARN, "Up there")  # This will not change result as we do no go from worse to better
    assert mr.result.value == RESULT_FAIL
    assert mr.result.reason == "Out of bounds!"

    exp_log_record = "NOT changing result from 'fail' to 'warning': 'Up there', we will not go from worse to better!"
    for record in caplog.records:
        if exp_log_record in record.message:
            break
    else:
        assert False, "Did not find: \"NOT changing result from 'fail' to 'warning': 'Up there', we will not go from worse to better!\" in log records"
