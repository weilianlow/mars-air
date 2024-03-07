import pytest
from bs4 import BeautifulSoup


@pytest.fixture(scope='module')
def empty_promo_code():
    return ['promotional_code=']


@pytest.fixture(scope='module')
def seat_available():
    return ['departing=0', 'returning=5']


def execute(data: list, expected: list, precondition=None, request=None):
    # act
    session, url = request.getfixturevalue('session')
    if precondition:
        data.extend(precondition)
    response = session.post(url, data='&'.join([v for v in data]))
    soup = BeautifulSoup(response.text, features='html.parser')
    # assert
    assert 200 == response.status_code
    actual_lst = soup.find('div', {'id': 'content'}).find_all('p')
    for i, actual in enumerate(actual_lst):
        exp, act = expected[i], actual.get_text().strip()
        assert exp == act, f'expected is "{exp}", but actual is "{act}"'


def test_without_departing_without_returning(request, empty_promo_code):
    execute(data=['departing=', 'returning='],
            expected=['Departing or Returning field cannot be empty.', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_with_departing_without_returning(request, empty_promo_code):
    execute(data=['departing=0', 'returning='],
            expected=['Departing or Returning field cannot be empty.', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_with_departing_with_returning(request, empty_promo_code):
    execute(data=['departing=0', 'returning=5'],
            expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_returning_earlier_than_departing(request, empty_promo_code):
    execute(data=['departing=5', 'returning=0'],
            expected=['Returning date cannot be earlier or same as departing.', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_returning_same_as_departing(request, empty_promo_code):
    execute(data=['departing=0', 'returning=0'],
            expected=['Returning date cannot be earlier or same as departing.', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_returning_less_than_1year(request, empty_promo_code):
    execute(data=['departing=0', 'returning=1'],
            expected=['Unfortunately, this schedule is not possible. Please try again.', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_returning_more_than_1year_and_seat_unavailable(request, empty_promo_code):
    execute(data=['departing=0', 'returning=3'],
            expected=['Sorry, there are no more seats available.', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_returning_more_than_1year_and_seat_available(request, empty_promo_code):
    execute(data=['departing=0', 'returning=5'],
            expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_empty_promo(request, seat_available):
    execute(data=['promotional_code='],
            expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_whitespaces_only(request, seat_available):
    execute(data=['promotional_code=  '],
            expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_correct_format_and_wrong_checksum(request, seat_available):
    execute(data=['promotional_code=XX9-XXX-999'],
            expected=['Seats available!', 'Sorry, code XX9-XXX-999 is not valid',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_valid_promo_and_00_percent_discount(request, seat_available):
    execute(data=['promotional_code=XX0-XXX-000'],
            expected=['Seats available!', 'Sorry, code XX0-XXX-000 is not valid',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_valid_promo_and_50_percent_discount(request, seat_available):
    execute(data=['promotional_code=XX5-XXX-005'],
            expected=['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_valid_promo_and_50_percent_discount_and_left_whitespace(request, seat_available):
    execute(data=['promotional_code=  XX5-XXX-005'],
            expected=['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_valid_promo_and_50_percent_discount_and_right_whitespace(request, seat_available):
    execute(data=['promotional_code=XX5-XXX-005  '],
            expected=['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_valid_promo_and_50_percent_discount_and_left_right_whitespace(request, seat_available):
    execute(data=['promotional_code=  XX5-XXX-005   '],
            expected=['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)
