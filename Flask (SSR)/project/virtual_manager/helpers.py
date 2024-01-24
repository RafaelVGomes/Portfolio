from pprint import pprint
from flask import Request
from virtual_manager.db import get_db


def usd(value):
  """Format value as USD."""
  if value == None:
    return '-'
  else:
    return f"${float(value):.2f}"
  

def percent_diff(current_value, previous_value):
  """Formats difference between values to [-]0.00%"""
  return round(float((current_value / previous_value - 1) * 100), 2)


def updated_columns(old_values:dict, new_values:dict) -> dict:
  """Returns column names that have their values changed"""
  cols = {}
  for col in new_values.keys():
    if col in old_values.keys() and new_values[col] != old_values[col]:
      cols[col] = {'new': new_values[col], 'old': old_values[col]}
  return cols


def format_field_name(name:str) -> str:
  name = name.replace('_', ' ').title()
  return name



def form_factory(request: Request, table_name: str, custom_fields: dict | list, exclude: list = ['id'], validate: True|False = False) -> dict:
  """
  Generates form field data from database, accepts custom fields and returns
  'form.get()' values. If validate: True, returns "'Field_name' is required"
  message on NOT NULL database columns without DEFAULT values.
  
  custom_fields dict format:
    >>> custom_fields_sample = [
    >>>  {'name': 'field_1_name', 'data_type': str|int|float, ['required': True|(False)]},
    >>>  {'name': 'field_2_name', 'data_type': str|int|float, ['required': True|(False)]},
    >>>  {...},
    >>>  {...}
    >>> ]
  """
  data = {'errors': []}
  form = request.form
  fields = []
  rows = get_db().execute(f"PRAGMA table_info({table_name});").fetchall()

  if not rows:
   print("No data returned")
   return
  # TODO: find a way to work only with template's fields
  for row in rows:
    row = dict(row)
    # print(f"{row=}")
    
    if row['name'] not in exclude:
      name = row['name']
      data_type = None
      required = (False, True)[row['notnull'] == 1 and row['dflt_value'] == None]

      match row['type']:
        case 'NUMERIC' | 'REAL':
          data_type = float
        case 'INTEGER': 
          data_type = int
        case _:
          data_type = str
      
      fields.append({'name': name, 'data_type': data_type, 'required': required})
      
  if type(custom_fields) == list:
    for row in custom_fields:
      if 'required' not in row.keys():
        row['required'] = False

      fields.append({'name': row['name'], 'data_type': row['data_type'], 'required': row['required']})
  elif type(custom_fields) == dict:
    if 'required' not in custom_fields.keys():
      custom_fields['required'] = False

    fields.append({'name': custom_fields['name'], 'data_type': custom_fields['data_type'], 'required': custom_fields['required']})
  else:
    print("Invalid input")

  for field in fields:
    if validate:
      if field['required'] and not form.get(field['name'], '', type=field['data_type']):
        data['errors'].append({field['name']: f"{field['name'].title()} is required."})
        data[field['name']] = form.get(field['name'], '', type=field['data_type'])
    else:
      data[field['name']] = form.get(field['name'], '', type=field['data_type'])

  # pprint(data)
  return data
