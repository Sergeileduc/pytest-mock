#!/usr/bin/python3
# -*-coding:utf-8 -*-

import smtplib
import pytest

from utils import send_email


# Please `pip install pytest-mock` to use mocker fixture
def test_send_mail(mocker):

    # We monkeypatch smtplib.SMTP class
    mocksmtpcls = mocker.patch("smtplib.SMTP")

    # Expected result
    from_addr = "toto@toto.fr"
    to_addr = "tata@tata.fr"
    subject = "coucou"
    body = "comment ça va ?\nbisous"

    msg = 'To: %s\nFrom: %s\nSubject: %s\n\n%s' % (to_addr, from_addr, subject, body)  # noqa: E501

    # Test happens here :
    send_email(from_addr, to_addr, subject, body)  # noqa: E501

    # Asserts:
    # As mocksmtpcls is a class, mockstpcls.return_value is the result
    # of creating an instance of this class, eg. the object smtp
    # We can assert the methode sendmail of this instance has been called once

    # assert_called without arguments :
    mocksmtpcls.return_value.sendmail.assert_called_once()

    # assert_called with arguments :
    mocksmtpcls.return_value.sendmail.assert_called_once_with(from_addr,
                                                              [to_addr],
                                                              msg)


def test_send_mail_error_420(mocker):

    # We monkeypatch smtplib.SMTP class
    mocksmtpcls = mocker.patch("smtplib.SMTP")
    # sendmail raises SMTPResponseException
    mocksmtpcls.return_value.sendmail.side_effect = smtplib.SMTPResponseException(420, "Timeout connection problem")

    # We check that send_email will raise SMTP exception 420
    with pytest.raises(smtplib.SMTPResponseException, match=r".*420.*Timeout.*") as e:  # noqa: E501
        send_email("toto@toto.fr", "tata@tata.fr", "coucou", "comment ça va ?\nbisous")  # noqa: E501

    mocksmtpcls.return_value.sendmail.assert_called_once()
    # print(e.value.smtp_code)
    # print(e.value.smtp_error)
