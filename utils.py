#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Docstring."""

import smtplib


def send_email(from_addr, to_addr, subject, body):
    conn = smtplib.SMTP('localhost')
    msg = 'To: %s\nFrom: %s\nSubject: %s\n\n%s' % (
        to_addr, from_addr, subject, body)
    conn.sendmail(from_addr, [to_addr], msg)
    conn.quit()
