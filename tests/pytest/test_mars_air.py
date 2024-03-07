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
        assert act == exp, f'expected is "{exp}", but actual is "{act}"'


def test_basic_search_dep_ret_not_selected(request, empty_promo_code):
    execute(data=['departing=', 'returning='],
            expected=['Departing and Returning field cannot be empty.', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_basic_search_ret_not_selected(request, empty_promo_code):
    execute(data=['departing=0', 'returning='],
            expected=['Departing and Returning field cannot be empty.', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_basic_search_seat_unavailable(request, empty_promo_code):
    execute(data=['departing=0', 'returning=3'],
            expected=['Sorry, there are no more seats available.', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_basic_search_seat_available(request, empty_promo_code):
    execute(data=['departing=0', 'returning=5'],
            expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_invalid_promo_whitespace_input(request, seat_available):
    execute(data=['promotional_code=  '],
            expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_invalid_promo_invalid_format(request, seat_available):
    execute(data=['promotional_code=XYZ'],
            expected=['Seats available!', 'Sorry, code XYZ is not valid',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_invalid_promo_invalid_checksum(request, seat_available):
    execute(data=['promotional_code=XX9-XXX-999'],
            expected=['Seats available!', 'Sorry, code XX9-XXX-999 is not valid',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_invalid_promo_00_percent_discount(request, seat_available):
    execute(data=['promotional_code=XX0-XXX-000'],
            expected=['Seats available!', 'Sorry, code XX0-XXX-000 is not valid',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_valid_promo_10_percent_discount(request, seat_available):
    execute(data=['promotional_code=XX1-XXX-001'],
            expected=['Seats available!', 'Promotional code XX1-XXX-001 used: 10% discount!',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_valid_promo_90_percent_discount(request, seat_available):
    execute(data=['promotional_code=XX9-XXX-009'],
            expected=['Seats available!', 'Promotional code XX9-XXX-009 used: 90% discount!',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_valid_promo_whitespace_padding(request, seat_available):
    execute(data=['promotional_code=  XX5-XXX-005   '],
            expected=['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_valid_promo_non_alphanumeric_promo(request, seat_available):
    execute(data=['promotional_code=$$5-@@@-005'],
            expected=['Seats available!', 'Promotional code $$5-@@@-005 used: 50% discount!',
                      'Call now on 0800 MARSAIR to book!', 'Back'],
            precondition=seat_available,
            request=request)


def test_invalid_returning_date_earlier_than_departing(request, empty_promo_code):
    execute(data=['departing=5', 'returning=0'],
            expected=['Unfortunately, this schedule is not possible. Please try again.', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_invalid_returning_date_same_as_departing(request, empty_promo_code):
    execute(data=['departing=0', 'returning=0'],
            expected=['Unfortunately, this schedule is not possible. Please try again.', 'Back'],
            precondition=empty_promo_code,
            request=request)


def test_invalid_returning_date_less_than_one_year(request, empty_promo_code):
    execute(data=['departing=0', 'returning=1'],
            expected=['Unfortunately, this schedule is not possible. Please try again.', 'Back'],
            precondition=empty_promo_code,
            request=request)
