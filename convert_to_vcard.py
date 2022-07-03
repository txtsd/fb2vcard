#!/usr/bin/env python

import csv
import phonenumbers

with open('../../Documents/Contacts/contacts.csv') as f:
    reader = csv.DictReader(f)

    for row in reader:
        # print(row['Given Name'])
        contents = 'BEGIN:VCARD\r\n'
        contents += 'VERSION:4.0\r\n'

        # Name
        if not row['Given Name'] == '':
            # print(row['Given Name'])
            contents += 'KIND:individual\r\n'


            contents += 'FN:{}\r\n'.format(row['Name'])
            contents += 'N:{};{};{};{};{}\r\n'.format(
                row['Family Name'],
                row['Given Name'],
                row['Additional Name'],
                row['Name Prefix'],
                row['Name Suffix'],
            )
        else:
            contents += 'KIND:org\r\n'
            contents += 'FN:{}\r\n'.format(row['Organization 1 - Name'])

        # Phone number
        numbers = []
        if len(row['Phone 1 - Value']) == 3:
            contents += 'TEL;VALUE=uri;TYPE=voice:tel:{}\r\n'.format(row['Phone 1 - Value'])
        elif row['Phone 1 - Value'][:4] == '1800' or row['Phone 1 - Value'][:4] == '1855':
            contents += 'TEL:VALUE=uri;TYPE=voice:tel:{}\r\n'.format(row['Phone 1 - Value'].replace(' ', '').replace('-', ''))
        elif row['Phone 1 - Value'][:1] == '*' and row['Phone 1 - Value'][-1:] == '#':
            contents += 'TEL:VALUE=uri;TYPE=ussd:tel:{}\r\n'.format(row['Phone 1 - Value'])
        else:
            for number in row['Phone 1 - Value'].split(' ::: '):
                if not number == '':
                    number_parsed = phonenumbers.parse(number)
                    number_rfc3966 = phonenumbers.format_number(number_parsed, phonenumbers.PhoneNumberFormat.RFC3966)
                    number_type = False
                    if row['Phone 1 - Type'] == 'Mobile':
                        number_type = 'cell'
                    elif row['Phone 1 - Type'] == 'Work' or row['Phone 1 - Type'] == 'workFax' or row['Phone 1 - Type'] == 'Pager' or row['Phone 1 - Type'] == 'homeFax':
                        number_type = 'voice,work'
                    elif row['Phone 1 - Type'] == 'Voicemail':
                        number_type = 'voice,voicemail'
                    elif row['Phone 1 - Type'] == 'Main' or row['Phone 1 - Type'] == 'Other':
                        number_type = 'voice'
                    elif row['Phone 1 - Type'] == 'Home':
                        number_type = 'voice,landline'
                    if number_type:
                        if ',' in number_type:
                            contents += 'TEL;VALUE=uri;TYPE="{teltype}":{tel}\r\n'.format(tel=number_rfc3966, teltype=number_type)
                        else:
                            contents += 'TEL;VALUE=uri;TYPE={teltype}:{tel}\r\n'.format(tel=number_rfc3966, teltype=number_type)
                    else:
                        contents += 'TEL;VALUE=uri;TYPE=voice:{}\r\n'.format(number_rfc3966)
        if len(row['Phone 2 - Value']) == 3:
            contents += 'TEL;VALUE=uri;TYPE=voice:tel:{}\r\n'.format(row['Phone 2 - Value'])
        elif row['Phone 2 - Value'][:4] == '1800' or row['Phone 2 - Value'][:4] == '1855':
            contents += 'TEL:VALUE=uri;TYPE=voice:tel:{}\r\n'.format(row['Phone 2 - Value'].replace(' ', '').replace('-', ''))
        elif row['Phone 2 - Value'][:1] == '*' and row['Phone 2 - Value'][-1:] == '#':
            contents += 'TEL:VALUE=uri;TYPE=ussd:tel:{}\r\n'.format(row['Phone 2 - Value'])
        else:
            for number in row['Phone 2 - Value'].split(' ::: '):
                if not number == '':
                    number_parsed = phonenumbers.parse(number)
                    number_rfc3966 = phonenumbers.format_number(number_parsed, phonenumbers.PhoneNumberFormat.RFC3966)
                    number_type = False
                    if row['Phone 2 - Type'] == 'Mobile':
                        number_type = 'cell'
                    elif row['Phone 2 - Type'] == 'Work' or row['Phone 2 - Type'] == 'workFax' or row['Phone 2 - Type'] == 'Pager' or row['Phone 2 - Type'] == 'homeFax':
                        number_type = 'voice,work'
                    elif row['Phone 2 - Type'] == 'Voicemail':
                        number_type = 'voice,voicemail'
                    elif row['Phone 2 - Type'] == 'Main' or row['Phone 2 - Type'] == 'Other':
                        number_type = 'voice'
                    elif row['Phone 2 - Type'] == 'Home':
                        number_type = 'voice,landline'
                    if number_type:
                        if ',' in number_type:
                            contents += 'TEL;VALUE=uri;TYPE="{teltype}":{tel}\r\n'.format(tel=number_rfc3966, teltype=number_type)
                        else:
                            contents += 'TEL;VALUE=uri;TYPE={teltype}:{tel}\r\n'.format(tel=number_rfc3966, teltype=number_type)
                    else:
                        contents += 'TEL;VALUE=uri;TYPE=voice:{}\r\n'.format(number_rfc3966)
        if len(row['Phone 3 - Value']) == 3:
            contents += 'TEL;VALUE=uri;TYPE=voice:tel:{}\r\n'.format(row['Phone 3 - Value'])
        elif row['Phone 3 - Value'][:4] == '1800' or row['Phone 3 - Value'][:4] == '1855':
            contents += 'TEL:VALUE=uri;TYPE=voice:tel:{}\r\n'.format(row['Phone 3 - Value'].replace(' ', '').replace('-', ''))
        elif row['Phone 3 - Value'][:1] == '*' and row['Phone 3 - Value'][-1:] == '#':
            contents += 'TEL:VALUE=uri;TYPE=ussd:tel:{}\r\n'.format(row['Phone 3 - Value'])
        else:
            for number in row['Phone 3 - Value'].split(' ::: '):
                if not number == '':
                    number_parsed = phonenumbers.parse(number)
                    number_rfc3966 = phonenumbers.format_number(number_parsed, phonenumbers.PhoneNumberFormat.RFC3966)
                    number_type = False
                    if row['Phone 3 - Type'] == 'Mobile':
                        number_type = 'cell'
                    elif row['Phone 3 - Type'] == 'Work' or row['Phone 3 - Type'] == 'workFax' or row['Phone 3 - Type'] == 'Pager' or row['Phone 3 - Type'] == 'homeFax':
                        number_type = 'voice,work'
                    elif row['Phone 3 - Type'] == 'Voicemail':
                        number_type = 'voice,voicemail'
                    elif row['Phone 3 - Type'] == 'Main' or row['Phone 3 - Type'] == 'Other':
                        number_type = 'voice'
                    elif row['Phone 3 - Type'] == 'Home':
                        number_type = 'voice,landline'
                    if number_type:
                        if ',' in number_type:
                            contents += 'TEL;VALUE=uri;TYPE="{teltype}":{tel}\r\n'.format(tel=number_rfc3966, teltype=number_type)
                        else:
                            contents += 'TEL;VALUE=uri;TYPE={teltype}:{tel}\r\n'.format(tel=number_rfc3966, teltype=number_type)
                    else:
                        contents += 'TEL;VALUE=uri;TYPE=voice:{}\r\n'.format(number_rfc3966)
        if len(row['Phone 4 - Value']) == 3:
            contents += 'TEL;VALUE=uri;TYPE=voice:tel:{}\r\n'.format(row['Phone 4 - Value'])
        elif row['Phone 4 - Value'][:4] == '1800' or row['Phone 4 - Value'][:4] == '1855':
            contents += 'TEL:VALUE=uri;TYPE=voice:tel:{}\r\n'.format(row['Phone 4 - Value'].replace(' ', '').replace('-', ''))
        elif row['Phone 4 - Value'][:1] == '*' and row['Phone 4 - Value'][-1:] == '#':
            contents += 'TEL:VALUE=uri;TYPE=ussd:tel:{}\r\n'.format(row['Phone 4 - Value'])
        else:
            for number in row['Phone 4 - Value'].split(' ::: '):
                if not number == '':
                    number_parsed = phonenumbers.parse(number)
                    number_rfc3966 = phonenumbers.format_number(number_parsed, phonenumbers.PhoneNumberFormat.RFC3966)
                    number_type = False
                    if row['Phone 4 - Type'] == 'Mobile':
                        number_type = 'cell'
                    elif row['Phone 4 - Type'] == 'Work' or row['Phone 4 - Type'] == 'workFax' or row['Phone 4 - Type'] == 'Pager' or row['Phone 4 - Type'] == 'homeFax':
                        number_type = 'voice,work'
                    elif row['Phone 4 - Type'] == 'Voicemail':
                        number_type = 'voice,voicemail'
                    elif row['Phone 4 - Type'] == 'Main' or row['Phone 4 - Type'] == 'Other':
                        number_type = 'voice'
                    elif row['Phone 4 - Type'] == 'Home':
                        number_type = 'voice,landline'
                    if number_type:
                        if ',' in number_type:
                            contents += 'TEL;VALUE=uri;TYPE="{teltype}":{tel}\r\n'.format(tel=number_rfc3966, teltype=number_type)
                        else:
                            contents += 'TEL;VALUE=uri;TYPE={teltype}:{tel}\r\n'.format(tel=number_rfc3966, teltype=number_type)
                    else:
                        contents += 'TEL;VALUE=uri;TYPE=voice:{}\r\n'.format(number_rfc3966)

        contents += 'END:VCARD'

        print(contents)
        print()
