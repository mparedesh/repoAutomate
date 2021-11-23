from openpyxl import Workbook
from openpyxl.styles import Font
import time
from queryAPI import queryAPI
from config import *


def repos(ORG, API_TOKEN):
    book = Workbook()
    sheet = book.active

    sheet['A1'] = 'Repo Name'
    sheet['B1'] = 'User Login'
    sheet['C1'] = 'User Name'
    sheet['D1'] = 'Triage'
    sheet['E1'] = 'Push'
    sheet['F1'] = 'Pull'
    sheet['G1'] = 'Maintain'
    sheet['H1'] = 'Admin'

    sheet['A1'].font = Font(bold=True)
    sheet['B1'].font = Font(bold=True)
    sheet['C1'].font = Font(bold=True)
    sheet['D1'].font = Font(bold=True)
    sheet['E1'].font = Font(bold=True)
    sheet['F1'].font = Font(bold=True)
    sheet['G1'].font = Font(bold=True)
    sheet['H1'].font = Font(bold=True)

    REPOS_URL = BASE_URL + '/orgs/{0}/repos'.format(ORG)
    row_num = 1

    while (REPOS_URL != ''):
        PARAMS = {'per_page': '100'}
        repos_json, REPOS_URL = queryAPI(API_TOKEN, REPOS_URL, PARAMS)

        for i in range(0, len(repos_json)):
            COLABORATORS_URL = str(repos_json[i]['collaborators_url']).replace(
                '{/collaborator}', '')
            while (COLABORATORS_URL != ''):
                users_json, COLABORATORS_URL = queryAPI(
                    API_TOKEN, COLABORATORS_URL, PARAMS)

                for j in range(0, len(users_json)):
                    USER_URL = users_json[j]['url']
                    user_json, USER_URL = queryAPI(API_TOKEN, USER_URL)
                    row_num += 1
                    sheet[f'A{row_num}'] = repos_json[i]['name']
                    sheet[f'B{row_num}'] = users_json[j]['login']
                    sheet[f'C{row_num}'] = user_json['name']
                    sheet[f'D{row_num}'] = str(
                        users_json[j]['permissions']['triage'])
                    sheet[f'E{row_num}'] = str(
                        users_json[j]['permissions']['push'])
                    sheet[f'F{row_num}'] = str(
                        users_json[j]['permissions']['pull'])
                    sheet[f'G{row_num}'] = str(
                        users_json[j]['permissions']['maintain'])
                    sheet[f'H{row_num}'] = str(
                        users_json[j]['permissions']['admin'])

    fecha = time.strftime("%d%m%Y")
    file_name = 'repos_rpt_{0}.xlsx'.format(fecha)
    book.save(file_name)
    return file_name
