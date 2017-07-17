import openpyxl
import os

os.chdir('file_manager/scripts/location_list/')
wb = openpyxl.load_workbook('country_list.xlsx')
sheet = wb.get_sheet_by_name('Sheet1')

continents = []
countries = []

CONTINENT_NAMES = {
    'AF':'Africa',
    'AS':'Asia',
    'EU':'Europe',
    'NA':'North America',
    'SA':'South America',
    'OC':'Oceania',
    'AN':'Antarctica',
}

# Edit this to handle models

# # ------------ Location Tags ------------#
#
# class ContinentTag(TagGroup):
#
# class CountryTag(Tag):
#     name = models.CharField(max_length=64)
#     group = models.ForeignKey(ContinentTag, on_delete=models.CASCADE)
# 

def create_continent_tag(code, name):
    continent_codes = [continent[0] for continent in continents]
    if code not in continent_codes:
        continents.append((code, name))
        print('Created continent tag for {}, code: {}'.format(name, code))

def create_country_tag(continent, code, name):
    # when dealing with models check country does not already exist
    countries.append((continent, code, name))
    print('Created country tag for {}, code: {}, in continent {}'.format(name, code, continent))

def evaluate_row(row):
    if sheet.cell(row=row, column=1).value is not None:
        continent_code = sheet.cell(row=row, column=1).value
        continent_name = CONTINENT_NAMES[continent_code]
        country_code = sheet.cell(row=row, column=3).value
        country_name = sheet.cell(row=row, column=5).value

        create_continent_tag(continent_code, continent_name)
        create_country_tag(continent_name, country_code, country_name)

        evaluate_row(row+1)

def run():
    print(os.getcwd())

    evaluate_row(2)
