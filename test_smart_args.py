from smart_args import smart_args, Isolated, Evaluated
import random
import pytest

# An example of applying the decorator to a function with the 'isolated' default argument
@smart_args
def check_isolation(*, d=Isolated()):
    d['a'] = 1
    return d


no_mutable = {'a': 10}
print('Testing isolated')
print(check_isolation(d=no_mutable))
print(no_mutable)

print(15 * '-')


# An example of applying the decorator to a function with the 'evaluated' default argument
def get_random_number():
    return random.randint(0, 100)


@smart_args
def check_evaluation(*, x=get_random_number(), y=Evaluated(get_random_number)):
    print(x, y)


print('Testing evaluated')
check_evaluation()
check_evaluation()
check_evaluation(y=146)


#Some tests for pytest
def test_mixed_types():
    with pytest.raises(ValueError):
        Evaluated(Isolated())

def test_positional_args():
    with pytest.raises(TypeError):

        @smart_args
        def dummy_func(*args):
            pass

        dummy_func(Isolated())

def test_evaluation():
    @smart_args
    def dummy_func2(a=Evaluated(get_random_number)):
        return a

    assert 0 <= dummy_func2() <= 100





