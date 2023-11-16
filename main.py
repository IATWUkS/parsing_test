import json
import os
import zipfile
from tqdm import tqdm
import wget

from db import insert_company_data, create_table


# Обработка json
def handle_json(json_payload, file_path):
    try:
        # Цикл проходит по всем компаниям в json файле
        for company_info in json_payload:
            try:
                # В случае нахождения ОКВЭД 62, записывает в базу данных информацию по компании
                if company_info['data']['СвОКВЭД']['СвОКВЭДОсн']['КодОКВЭД'] == '62':
                    sv_address_legal = company_info['data']['СвАдресЮЛ']['АдресРФ']
                    # Формирования адреса в виде удобной строки для чтения
                    place_registration = f"{sv_address_legal['Индекс']}, {sv_address_legal['Регион']['НаимРегион']} " \
                                         f"{sv_address_legal['Регион']['ТипРегион']}, {sv_address_legal['Город']['ТипГород']}" \
                                         f"{sv_address_legal['Город']['НаимГород']}, {sv_address_legal['Улица']['ТипУлица']}" \
                                         f"{sv_address_legal['Улица']['НаимУлица']}, {sv_address_legal['Дом']}, " \
                                         f"{sv_address_legal['Кварт']}"
                    insert_company_data(company_info['name'], company_info['data']['СвОКВЭД']['СвОКВЭДОсн']['КодОКВЭД'],
                                        int(company_info['inn']), int(company_info['kpp']), place_registration)
            except KeyError:
                pass
    except UnicodeDecodeError:
        print(f'Не удалось десериализовать файл: {file_path}')


# Обработка всех файлов в zip архиве
def handle_zip_file(path):
    with zipfile.ZipFile(path, mode="r") as archive:
        for filename in tqdm(archive.namelist()):
            templates = archive.open(filename, 'r')
            json_payload = json.load(templates)
            handle_json(json_payload, filename)

# test test
if __name__ == '__main__':
    # Создает таблицу в базе, если её нет
    create_table()

    if os.path.exists('egrul.json.zip'):
        handle_zip_file('egrul.json.zip')
    else:
        print('Скачивания файла...')
        wget.download('https://ofdata.ru/open-data/download/egrul.json.zip', 'egrul.json.zip')

        handle_zip_file('egrul.json.zip')