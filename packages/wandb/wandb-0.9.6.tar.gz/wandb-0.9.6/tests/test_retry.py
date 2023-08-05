import pytest
import datetime
import requests

from wandb import retry
from wandb import util
from wandb.apis import CommError


class FailException(Exception):
    pass


def fail_for_n_function(n):
    call_num = [0]  # use a list so we can modify in this scope

    def fn(an_arg):
        print(an_arg)
        try:
            if call_num[0] < n:
                raise retry.TransientException(
                    exc=FailException('Failed at call_num: %s' % call_num))
        finally:
            call_num[0] += 1
        return True
    return fn


def test_fail_for_n_function():
    failing_fn = fail_for_n_function(3)
    with pytest.raises(retry.TransientException):
        failing_fn('hello')
    with pytest.raises(retry.TransientException):
        failing_fn('hello')
    with pytest.raises(retry.TransientException):
        failing_fn('hello')
    assert failing_fn('hello')


def test_retry_with_success():
    failing_fn = fail_for_n_function(3)
    fn = retry.Retry(failing_fn)
    fn('hello', retry_timedelta=datetime.timedelta(days=1), retry_sleep_base=0.001)
    assert fn.num_iters == 3


def test_retry_with_timeout():
    failing_fn = fail_for_n_function(10000)
    fn = retry.Retry(failing_fn)
    with pytest.raises(retry.TransientException):
        fn('hello', retry_timedelta=datetime.timedelta(
            0, 0, 0, 50), retry_sleep_base=0.001)


def test_retry_with_noauth_401(capsys):
    def fail():
        res = requests.Response()
        res.status_code = 401
        raise retry.TransientException(exc=requests.HTTPError(response=res))
    fn = retry.Retry(fail, check_retry_fn=util.no_retry_auth)
    with pytest.raises(CommError) as excinfo:
        fn()
    assert excinfo.value.message == 'Invalid or missing api_key.  Run wandb login'


def test_retry_with_noauth_403(capsys):
    def fail():
        res = requests.Response()
        res.status_code = 403
        raise retry.TransientException(exc=requests.HTTPError(response=res))
    fn = retry.Retry(fail, check_retry_fn=util.no_retry_auth)
    with pytest.raises(CommError) as excinfo:
        fn()
    assert excinfo.value.message == 'Permission denied, ask the project owner to grant you access'
