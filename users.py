from openpyxl import Workbook
from openpyxl.styles import Font
import time
from queryAPI import queryAPI
from config import *
import argparse


def users(ORG, API_TOKEN):
    book = Workbook()
    sheet = book.active

    sheet['A1'] = 'User Login'
    sheet['B1'] = 'User Name'
    sheet['C1'] = 'Role'

    sheet['A1'].font = Font(bold=True)
    sheet['B1'].font = Font(bold=True)
    sheet['C1'].font = Font(bold=True)

    MEMBERS_URL = BASE_URL + '/orgs/{0}/members'.format(ORG)
    row_num = 1

    while (MEMBERS_URL != ''):
        PARAMS = {'per_page': '100'}
        users_json, MEMBERS_URL = queryAPI(API_TOKEN, MEMBERS_URL, PARAMS)

        for j in range(0, len(users_json)):
            URL = users_json[j]['url']
            user_json, next_page = queryAPI(API_TOKEN, URL)
            URL = BASE_URL + \
                '/orgs/{0}/memberships/{1}'.format(ORG, user_json['login'])
            membership_json, next_page = queryAPI(API_TOKEN, URL)

            row_num += 1
            sheet[f'A{row_num}'] = user_json['login']
            sheet[f'B{row_num}'] = user_json['name']
            sheet[f'C{row_num}'] = membership_json['role']

    fecha = time.strftime("%d%m%Y")
    file_name = 'users_rpt_{0}.xlsx'.format(fecha)
    book.save(file_name)
    return file_name
