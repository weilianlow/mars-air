import unittest
from requests import Session
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
        response = self.session.post(self.url, data='&'.join([v for v in data]))
        soup = BeautifulSoup(response.text, features='html.parser')
        # assert
        self.assertEqual(200, response.status_code)
        actual_lst = soup.find('div', {'id': 'content'}).find_all('p')
        for i, actual in enumerate(actual_lst):
            exp, act = expected[i], actual.get_text().strip()
            self.assertEqual(exp, act, f'expected is "{exp}", but actual is "{act}"')


class TestBasicSearch(Case):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.precondition = ['promotional_code=']

    def test_basic_search_dep_ret_not_selected(self):
        self.execute(data=['departing=', 'returning='],
                     expected=['Departing or Returning field cannot be empty.', 'Back'])

    def test_basic_search_ret_not_selected(self):
        self.execute(data=['departing=0', 'returning='],
                     expected=['Departing or Returning field cannot be empty.', 'Back'])

    def test_basic_search_seat_unavailable(self):
        self.execute(data=['departing=0', 'returning=3'],
                     expected=['Sorry, there are no more seats available.', 'Back'])

    def test_basic_search_seat_available(self):
        self.execute(data=['departing=0', 'returning=5'],
                     expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'])


class TestPromo(Case):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.precondition = ['departing=0', 'returning=5']

    def test_invalid_promo_whitespace_input(self):
        self.execute(data=['promotional_code=  '],
                     expected=['Seats available!', 'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_invalid_promo_invalid_format(self):
        self.execute(data=['promotional_code=XYZ'],
                     expected=['Seats available!', 'Sorry, code XYZ is not valid',
                               'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_invalid_promo_invalid_checksum(self):
        self.execute(data=['promotional_code=XX9-XXX-999'],
                     expected=['Seats available!', 'Sorry, code XX9-XXX-999 is not valid',
                               'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_invalid_promo_00_percent_discount(self):
        self.execute(data=['promotional_code=XX0-XXX-000'],
                     expected=['Seats available!', 'Sorry, code XX0-XXX-000 is not valid',
                               'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_valid_promo_10_percent_discount(self):
        self.execute(data=['promotional_code=XX1-XXX-001'],
                     expected=['Seats available!', 'Promotional code XX1-XXX-001 used: 10% discount!',
                               'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_valid_promo_90_percent_discount(self):
        self.execute(data=['promotional_code=XX9-XXX-009'],
                     expected=['Seats available!', 'Promotional code XX9-XXX-009 used: 90% discount!',
                               'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_valid_promo_whitespace_padding(self):
        self.execute(data=['promotional_code=  XX5-XXX-005   '],
                     expected=['Seats available!', 'Promotional code XX5-XXX-005 used: 50% discount!',
                               'Call now on 0800 MARSAIR to book!', 'Back'])

    def test_valid_promo_non_alphanumeric_promo(self):
        self.execute(data=['promotional_code=$$5-@@@-005'],
                     expected=['Seats available!', 'Promotional code $$5-@@@-005 used: 50% discount!',
                               'Call now on 0800 MARSAIR to book!', 'Back'])


class TestMarsAirBookWithPromoCode(Case):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.precondition = ['promotional_code=']

    def test_invalid_returning_date_earlier_than_departing(self):
        self.execute(data=['departing=5', 'returning=0'],
                     expected=['Unfortunately, this schedule is not possible. Please try again.', 'Back'])

    def test_invalid_returning_date_same_as_departing(self):
        self.execute(data=['departing=0', 'returning=0'],
                     expected=['Unfortunately, this schedule is not possible. Please try again.', 'Back'])

    def test_invalid_returning_date_less_than_one_year(self):
        self.execute(data=['departing=0', 'returning=1'],
                     expected=['Unfortunately, this schedule is not possible. Please try again.', 'Back'])
