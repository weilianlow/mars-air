import pytest
from tests.models.home import Home


@pytest.fixture
def home_page(chrome):
    page = chrome.new_page()
    home = Home(page)
    home.navigate()
    yield home


def test_without_departing_without_returning(home_page):
    home_page.search()
    expected = ['Departing or Returning field cannot be empty.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_with_departing_without_returning(home_page):
    home_page.search(departing='July')
    expected = ['Departing or Returning field cannot be empty.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_with_departing_with_returning(home_page):
    home_page.search(departing='July', returning='December (two years from now)')
    expected = ['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_returning_earlier_than_departing(home_page):
    home_page.search(departing='December (two years from now)', returning='July')
    expected = ['Returning date cannot be earlier or same as departing.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_returning_same_as_departing(home_page):
    home_page.search(departing='July', returning='July')
    expected = ['Returning date cannot be earlier or same as departing.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_returning_less_than_1year(home_page):
    home_page.search(departing='July', returning='December')
    expected = ['Unfortunately, this schedule is not possible. Please try again.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_returning_more_than_1year_and_seat_unavailable(home_page):
    home_page.search(departing='July', returning='December (next year)')
    expected = ['Sorry, there are no more seats available.', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_returning_more_than_1year_and_seat_available(home_page):
    home_page.search(departing='July', returning='December (two years from now)')
    expected = ['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_empty_promo(home_page):
    home_page.search(departing='July', returning='December (two years from now)')
    expected = ['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_whitespaces_only(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='  ')
    expected = ['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_correct_format_and_wrong_checksum(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='XX9-XXX-999')
    expected = ['Seats available!', 'Sorry, code XX9-XXX-999 is not valid', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_valid_promo_and_00_percent_discount(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='XX0-XXX-000')
    expected = ['Seats available!', 'Sorry, code XX0-XXX-000 is not valid', 'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_valid_promo_and_50_percent_discount(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='XX5-XXX-005')
    expected = ['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_valid_promo_and_50_percent_discount_and_left_whitespace(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='  XX5-XXX-005')
    expected = ['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_valid_promo_and_50_percent_discount_and_right_whitespace(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='XX5-XXX-005  ')
    expected = ['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_valid_promo_and_50_percent_discount_and_left_right_whitespace(home_page):
    home_page.search(departing='July', returning='December (two years from now)', promo_code='  XX5-XXX-005  ')
    expected = ['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                'Call now on 0800 MARSAIR to book!', 'Back']
    for i, element in enumerate(home_page.form_content.all()):
        assert element.text_content().strip() == expected[i]


def test_ui_navigation(home_page):
    home_page.search("July", "December (two years from now)", None)
    assert home_page.search_title.text_content() == "Search Results"
    home_page.back_link.click()
    assert home_page.search_title.text_content() == "Welcome to MarsAir!"
