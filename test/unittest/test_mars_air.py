import unittest
from collections import namedtuple
from requests import post, Session
from bs4 import BeautifulSoup


class Case(unittest.TestCase):
    url = "https://marsair.recruiting.thoughtworks.net/WeiLianLow"
    session = None

    @classmethod
    def setUpClass(cls):
        cls.session = Session()
        cls.session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})

    def execute(self, data: list, expected: list):
        precondition = getattr(self, 'precondition', None)
        if precondition:
            data.extend(precondition)
        # act
        response = post(self.url, data='&'.join([v for v in data]))
        soup = BeautifulSoup(response.text, features='html.parser')
        # assert
        self.assertEqual(200, response.status_code)
        actual_lst = soup.find('div', {'id': 'content'}).find_all('p')
        for i, actual in enumerate(actual_lst):
            exp, act = expected[i], actual.get_text().strip()
            self.assertEqual(exp, act, f'expected is "{exp}", but actual is "{act}"')


class TestMarsAirMandateFields(Case):
    @classmethod
    def setUpClass(cls):
        cls.precondition = ['promotional_code=']

    def test_without_departing_without_returning(self):
        self.execute(data=['departing=', 'returning='],
                     expected=['Departing or Returning field cannot be empty.', 'Back'])

    def test_with_departing_without_returning(self):
        self.execute(data=['departing=0', 'returning='],
                     expected=['Departing or Returning field cannot be empty.', 'Back'])

    def test_with_departing_with_returning(self):
        self.execute(data=['departing=0', 'returning=5'],
                     expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'])


class TestMarsAirBookWithoutPromoCode(Case):
    @classmethod
    def setUpClass(cls):
        cls.precondition = ['promotional_code=']

    def test_returning_earlier_than_departing(self):
        self.execute(data=['departing=5', 'returning=0'],
                     expected=['Returning date cannot be earlier or same as departing.', 'Back'])

    def test_returning_same_as_departing(self):
        self.execute(data=['departing=5', 'returning=0'],
                     expected=['Returning date cannot be earlier or same as departing.', 'Back'])

    def test_returning_less_than_1year(self):
        self.execute(data=['departing=0', 'returning=1'],
                     expected=['Unfortunately, this schedule is not possible. Please try again.', 'Back'])

    def test_returning_more_than_1year_AND_seat_unavailable(self):
        self.execute(data=['departing=0', 'returning=3'],
                     expected=['Sorry, there are no more seats available.', 'Back'])

    def test_returning_more_than_1year_AND_seat_available(self):
        self.execute(data=['departing=0', 'returning=5'],
                     expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'])


class TestMarsAirBookWithPromoCode(Case):
    @classmethod
    def setUpClass(cls):
        cls.precondition = ['departing=0', 'returning=5']

    def test_empty_promo(self):
        self.execute(data=['promotional_code='],
                     expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_whitespaces_only(self):
        self.execute(data=['promotional_code=  '],
                     expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_correct_format_AND_wrong_checksum(self):
        self.execute(data=['promotional_code=XX9-XXX-999'],
                     expected=['Seats available!', 'Sorry, code XX9-XXX-999 is not valid',
                               'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_valid_promo_AND_00_percent_discount(self):
        self.execute(data=['promotional_code=XX0-XXX-000'],
                     expected=['Seats available!', 'Sorry, code XX0-XXX-000 is not valid',
                               'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_valid_promo_AND_50_percent_discount(self):
        self.execute(data=['promotional_code=XX5-XXX-005'],
                     expected=['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                               'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_valid_promo_AND_50_percent_discount_AND_left_whitespace(self):
        self.execute(data=['promotional_code=  XX5-XXX-005'],
                     expected=['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                               'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_valid_promo_AND_50_percent_discount_AND_right_whitespace(self):
        self.execute(data=['promotional_code=XX5-XXX-005  '],
                     expected=['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                               'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_valid_promo_AND_50_percent_discount_AND_left_right_whitespace(self):
        self.execute(data=['promotional_code=  XX5-XXX-005   '],
                     expected=['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                               'Call now on 0800 MARSAIR to book!', 'Back'])