from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase as TestCase
from django_gems.order.forms import CardDetailsForm


class CompleteTransactionViewTests(TestCase):
    def setUp(self):
        user_data = {
            'email': 'beatris@icloud.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'consent': True
        }

        self.client.post(
            reverse('register_user'),
            data=user_data
        )

        self.user = get_user_model(). \
            objects.get(email=user_data['email'])

        profile_data = {
            'first_name': 'Beatris',
            'last_name': 'Ilieve',
            'phone_number': '0000000000',
            'country': 'BG',
            'city': 'Sofia',
            'delivery_address': 'Some Address',
            'user': self.user

        }

        self.client.post(
            reverse(
                'complete_order', kwargs={'pk': self.user.pk}
            ),
            data={
                **profile_data
            }
        )

        self.current_date = \
            datetime.now()

        self.current_month = \
            self.current_date.month

        self.current_year = \
            self.current_date.year

        self.one_year_behind_date = \
            self.current_date - relativedelta(years=1)

        self.one_year_behind = \
            self.one_year_behind_date.year

        self.valid_card_data = {
            'card_number': int(
                '1' * CardDetailsForm.CARD_NUMBER_LENGTH
            ),

            'expiration_date':
                f'{self.current_month:02d}/{self.current_year % 100:02d}',

            'cvv_code': int(
                '1' * CardDetailsForm.CVV_CODE_LENGTH
            )
        }

        self.invalid_card_number_data = {
            'card_number': int(
                '1' * (CardDetailsForm.CARD_NUMBER_LENGTH - 1)
            ),

            'expiration_date':
                f'{self.current_month:02d}/{self.current_year % 100:02d}',

            'cvv_code': int(
                '1' * CardDetailsForm.CVV_CODE_LENGTH
            )
        }

        self.invalid_expiry_date_format_data = {
            'card_number': int(
                '1' * CardDetailsForm.CARD_NUMBER_LENGTH
            ),

            'expiration_date':
                f'{self.current_month:02d}.{self.current_year % 100:02d}',

            'cvv_code': int(
                '1' * CardDetailsForm.CVV_CODE_LENGTH
            )
        }

        self.invalid_expiry_date_data = {
            'card_number': int(
                '1' * CardDetailsForm.CARD_NUMBER_LENGTH
            ),

            'expiration_date':
                f'{self.current_month:02d}/{self.one_year_behind % 100:02d}',

            'cvv_code': int(
                '1' * CardDetailsForm.CVV_CODE_LENGTH
            )
        }

        self.invalid_cvv_code_data = {
            'card_number': int(
                '1' * CardDetailsForm.CARD_NUMBER_LENGTH
            ),

            'expiration_date':
                f'{self.current_month:02d}/{self.current_year % 100:02d}',

            'cvv_code': int(
                '1' * (CardDetailsForm.CVV_CODE_LENGTH - 1)
            )
        }

    def test_proceed_transaction__when_valid_card_details__expect__success(self):
        response = self.client.post(
            reverse(
                'complete_transaction', kwargs={'pk': self.user.pk}
            ),
            data={
                **self.valid_card_data
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            'order/proceed-transaction.html'
        )

    def test_proceed_transaction__when_invalid_card_number_data__expect__raises(self):
        form = CardDetailsForm(
            data=self.invalid_card_number_data
        )

        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors['card_number'][0],
            CardDetailsForm.CARD_NUMBER_ERROR_MESSAGE
        )

    def test_proceed_transaction__when_invalid_expiry_date_format_data__expect__raises(self):
        form = CardDetailsForm(
            data=self.invalid_expiry_date_format_data
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertEqual(
            form.errors['expiration_date'][0],
            CardDetailsForm.EXPIRATION_DATE_FORMAT_ERROR_MESSAGE
        )

    def test_proceed_transaction__when_card_has_expired__expect__raises(self):
        form = CardDetailsForm(
            data=self.invalid_expiry_date_data
        )

        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors['expiration_date'][0],
            CardDetailsForm.CARD_HAS_EXPIRED_ERROR_MESSAGE
        )

    def test_proceed_transaction__when__invalid_cvv_code__expect__raises(self):
        form = CardDetailsForm(
            data=self.invalid_cvv_code_data
        )

        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors['cvv_code'][0],
            CardDetailsForm.CVV_CODE_ERROR_MESSAGE
        )
