from openpyxl import Workbook
from openpyxl.styles import Font
import time
from queryAPI import queryAPI
from config import *


def teams(ORG, API_TOKEN):
    book = Workbook()
    sheet = book.active

    sheet['A1'] = 'Team Name'
    sheet['B1'] = 'Role Name'
    sheet['C1'] = 'Repo'
    sheet['D1'] = 'Triage'
    sheet['E1'] = 'Push'
    sheet['F1'] = 'Pull'
    sheet['G1'] = 'Maintain'
    sheet['H1'] = 'Admin'
    sheet['I1'] = 'Members'

    sheet['A1'].font = Font(bold=True)
    sheet['B1'].font = Font(bold=True)
    sheet['C1'].font = Font(bold=True)
    sheet['D1'].font = Font(bold=True)
    sheet['E1'].font = Font(bold=True)
    sheet['F1'].font = Font(bold=True)
    sheet['G1'].font = Font(bold=True)
    sheet['H1'].font = Font(bold=True)
    sheet['I1'].font = Font(bold=True)

    TEAMS_URL = BASE_URL + '/orgs/{0}/teams'.format(ORG)
    row_num = 1

    while (TEAMS_URL != ''):
        PARAMS = {'per_page': '100'}
        teams_json, TEAMS_URL = queryAPI(API_TOKEN, TEAMS_URL, PARAMS)

        for i in range(0, len(teams_json)):
            members = ''
            MEMBERS_URL = str(teams_json[i]['members_url']).replace(
                '{/member}', '')
            while (MEMBERS_URL != ''):
                members_json, MEMBERS_URL = queryAPI(
                    API_TOKEN, MEMBERS_URL, PARAMS)
                for j in range(0, len(members_json)):
                    members = members + members_json[j]['login'] + '; '

            REPOS_URL = teams_json[i]['repositories_url']

            while (REPOS_URL != ''):
                repos_json, REPOS_URL = queryAPI(API_TOKEN, REPOS_URL, PARAMS)

                if(len(repos_json) == 0):
                    row_num += 1
                    sheet[f'A{row_num}'] = teams_json[i]['name']
                    sheet[f'I{row_num}'] = members

                for j in range(0, len(repos_json)):
                    row_num += 1
                    sheet[f'A{row_num}'] = teams_json[i]['name']
                    sheet[f'B{row_num}'] = repos_json[j]['role_name']
                    sheet[f'C{row_num}'] = repos_json[j]['name']
                    sheet[f'D{row_num}'] = str(
                        repos_json[j]['permissions']['triage'])
                    sheet[f'E{row_num}'] = str(
                        repos_json[j]['permissions']['push'])
                    sheet[f'F{row_num}'] = str(
                        repos_json[j]['permissions']['pull'])
                    sheet[f'G{row_num}'] = str(
                        repos_json[j]['permissions']['maintain'])
                    sheet[f'H{row_num}'] = str(
                        repos_json[j]['permissions']['admin'])
                    sheet[f'I{row_num}'] = members

    fecha = time.strftime("%d%m%Y")
    file_name = 'teams_rpt_{0}.xlsx'.format(fecha)
    book.save(file_name)
    return file_name
