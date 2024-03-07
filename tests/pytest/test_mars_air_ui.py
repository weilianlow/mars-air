import pytest
from tests.models.home import Home


@pytest.fixture
def home_page(chrome):
    page = chrome.new_page()
    home = Home(page)
    home.navigate()
    yield home


def test_return_to_home_via_back_hyperlink(home_page):
    home_page.search("July", "December (two years from now)", None)
    assert home_page.search_title.text_content() == "Search Results"
    home_page.back_link.click()
    assert home_page.search_title.text_content() == "Welcome to MarsAir!"


def test_return_to_home_via_home_hyperlink(home_page):
    home_page.search("July", "December (two years from now)", None)
    assert home_page.search_title.text_content() == "Search Results"
    home_page.home_link.click()
    assert home_page.search_title.text_content() == "Welcome to MarsAir!"


"""
def test_basic_search_dep_ret_not_selected(home_page):
    home_page.search()
    expected = ['Departing or Returning field cannot be empty.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_basic_search_ret_not_selected(home_page):
    home_page.search(departing='July')
    expected = ['Departing or Returning field cannot be empty.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_basic_search_seat_unavailable(home_page):
    home_page.search(departing='July', returning='December (next year)')
    expected = ['Sorry, there are no more seats available.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_basic_search_seat_available(home_page):
    home_page.search(departing='July', returning='December (two years from now)')
    expected = ['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_invalid_promo_invalid_format(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='XYZ')
    expected = ['Seats available!', 'Sorry, code XYZ is not valid', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_invalid_promo_valid_format_invalid_checksum(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='XX9-XXX-999')
    expected = ['Seats available!', 'Sorry, code XX9-XXX-999 is not valid', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_invalid_promo_00_percent_discount(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='XX0-XXX-000')
    expected = ['Seats available!', 'Sorry, code XX0-XXX-000 is not valid', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_valid_promo_10_percent_discount(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='XX1-XXX-001')
    expected = ['Seats available!', 'Promotional code XX1-XXX-001 used: 10% discount!',
                'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_valid_promo_90_percent_discount(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='XX9-XXX-009')
    expected = ['Seats available!', 'Promotional code XX9-XXX-009 used: 90% discount!',
                'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_valid_promo_empty_input(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='')
    expected = ['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_valid_promo_whitespace_input(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='  ')
    expected = ['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_valid_promo_whitespace_padding(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='  XX9-XXX-009  ')
    expected = ['Seats available!', 'Promotional code XX9-XXX-009 used: 90% discount!',
                'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_valid_promo_non_alphanumeric_promo(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='$$5-@@@-005')
    expected = ['Seats available!', 'Promotional code $$5-@@@-005 used: 50% discount!',
                'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_invalid_returning_date_earlier_than_departing(home_page):
    home_page.search(departing='December (two years from now)', returning='July')
    expected = ['Unfortunately, this schedule is not possible. Please try again.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_invalid_returning_date_same_as_departing(home_page):
    home_page.search(departing='July', returning='July')
    expected = ['Unfortunately, this schedule is not possible. Please try again.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_invalid_returning_date_less_than_one_year(home_page):
    home_page.search(departing='July', returning='December')
    expected = ['Unfortunately, this schedule is not possible. Please try again.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]
"""
