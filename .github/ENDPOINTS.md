# GET - /users/<int:user_id>
Get a user by ID

#### RETURNS
```
{
  id,
    username,
      clients: {
        [
          {
            id,
            full_name
          },
        ],
      }
}
```

# PUT - /users/<int:user_id>
Update a user by ID

#### OPTIONAL PARAMS

```
full_name - String
phone - VARCHAR(12)
email - String
sex - String
race - String
dob - String
address_line_1 - String
address_line_2 - String
city - String
state - String
zip_code - VARCHAR(10)
license_number - String
license_issuing_state - VARCHAR(2))
license_expiration_date - Date
status - String
active - Boolean
convictions - ConvictionType
notes - Text
filing_court - String
judicial_circuit_number - String
county_of_prosecutor - String
judge_name - String
division_name - String
petitioner_name - String
division_number - String
city_name_here - String
county_name - String
arresting_county - String
prosecuting_county - String
arresting_municipality - String
other_agencies_name - Text
created_by - Integer
modified_by - Integer
purged_by - Integer
```

#### RETURNS
client_id

# POST - /clients
Create a client

#### OPTIONAL PARAMS

```
full_name - String
phone - VARCHAR(12)
email - String
sex - String
race - String
dob - String
address_line_1 - String
address_line_2 - String
city - String
state - String
zip_code - VARCHAR(10)
license_number - String
license_issuing_state - VARCHAR(2))
license_expiration_date - Date
status - String
active - Boolean
convictions - ConvictionType
notes - Text
filing_court - String
judicial_circuit_number - String
county_of_prosecutor - String
judge_name - String
division_name - String
petitioner_name - String
division_number - String
city_name_here - String
county_name - String
arresting_county - String
prosecuting_county - String
arresting_municipality - String
other_agencies_name - Text
created_by - Integer
modified_by - Integer
purged_by - Integer
```

#### RETURNS

200 - client_id

# '/clients', methods=['GET'])
Return all clients

#### RETURNS
```
[
  {
      'id',
      'full_name',
      'phone',
      'email',
      'sex',
      'race',
      'dob',
      'address_line_1',
      'address_line_2',
      'city',
      'state',
      'zip_code',
      'license_number',
      'license_issuing_state',
      'license_expiration_date',
      'status',
      'active',
      'user_id',
      'notes',
      'filing_court',
      'judicial_circuit_number',
      'county_of_prosecutor',
      'judge_name',
      'division_name',
      'division_name',
      'petitioner_name',
      'division_number',
      'city_name_here',
      'county_name',
      'arresting_county',
      'arresting_municipality',
      'other_agencies_name',
   },
]
```

# - GET - /clients/<int:client_id>
Get a client by ID

#### RETURNS
```
{
  'id',
  'full_name',
  'phone',
  'email',
  'sex',
  'race',
  'dob',
  'address_line_1',
  'address_line_2',
  'city',
  'state',
  'zip_code',
  'license_number',
  'license_issuing_state',
  'license_expiration_date',
  'status',
  'active',
  'user_id',
  'notes',
  'filing_court',
  'judicial_circuit_number',
  'county_of_prosecutor',
  'judge_name',
  'division_name',
  'petitioner_name',
  'division_number',
  'city_name_here',
  'county_name',
  'arresting_county',
  'arresting_municipality',
  'other_agencies_name',
}
```

# PUT - /clients/<int:client_id>
Update a client by ID

#### OPTIONAL PARAMS

```
full_name - String
phone - VARCHAR(12)
email - String
sex - String
race - String
dob - String
address_line_1 - String
address_line_2 - String
city - String
state - String
zip_code - VARCHAR(10)
license_number - String
license_issuing_state - VARCHAR(2))
license_expiration_date - Date
status - String
active - Boolean
notes - Text
filing_court - String
judicial_circuit_number - String
county_of_prosecutor - String
judge_name - String
division_name - String
petitioner_name - String
division_number - String
city_name_here - String
county_name - String
arresting_county - String
prosecuting_county - String
arresting_municipality - String
other_agencies_name - Text
created_by - Integer
modified_by - Integer
purged_by - Integer
```

#### RETURNS
200 - client_id

# DELETE - /clients/<int:client_id>
Undefined

# GET - /clients/<int:client_id>/convictions
Get a list of client convictions

#### RETURNS
```
[
  {
    'id',
    'client_id',
    'case_number',
    'agency',
    'court_name',
    'court_city_county',
    'judge',
    'record_name',
    'release_status',
    'release_date',
    'notes',
    'name',
    'arrest_date',
  },
]
```

# POST - /clients/<int:client_id>/convictions
Create a client conviction

#### OPTIONAL PARAMS
```
case_number - String
agency - String
court_name- String
court_city_county - String
judge - String
record_name - String
release_status - String
release_date - Date
notes - Text
name - String
arrest_date - Date
created_by - String
```

#### RETURNS
conviction_id

# GET - /convictions/<int:conviction_id>
Get a conviction by ID

#### RETURNS
```
{
  'id',
  'client_id',
  'case_number',
  'agency',
  'court_name',
  'court_city_county',
  'judge',
  'record_name',
  'release_status',
  'release_date',
  'notes',
  'name',
  'arrest_date',
}
```

# PUT - /convictions/<int:conviction_id>
Update a conviction by ID

#### OPTIONAL PARAMS
```
case_number - String
agency - String
court_name- String
court_city_county - String
judge - String
record_name - String
release_status - String
release_date - Date
notes - Text
name - String
arrest_date - Date
created_by - String
```


#### RETURNS
conviction_id

# DELETE - /convictions/<int:conviction_id>
Undefined

# GET - '/clients/<int:client_id>/convictions/<int:conviction_id>/charges', methods=['GET'])
Get a list of a client's conviction charges

#### RETURNS
```
[
  {
    'id',
    'conviction_id',
    'charge',
    'citation',
    'sentence',
    'eligible',
    'conviction_charge_type',
    'conviction_class_type',
    'eligible',
    'please_expunge',
    'notes',
    'conviction_description'
  }
]
```

# POST - /clients/<int:client_id>/convictions/<int:conviction_id>/charges
Create a new charge

#### OPTIONAL PARAMS
```
charge - String
citation - String)
sentence - String)
conviction_class_type - String
  ONE OF [A,B,C,D,E,UNDEFINED']
conviction_charge_type - String
  ONE OF [felony, misdemeanor]
eligible - Boolean
please_expunge - Boolean
notes - Text
conviction_description - String
```

#### RETURNS
charge_id

# GET - /charges/<int:charge_id>
Get a charge by ID

#### RETURNS
```
{
  'id',
  'conviction_id',
  'charge',
  'citation',
  'sentence',
  'eligible',
  'conviction_charge_type',
  'conviction_class_type',
  'eligible',
  'please_expunge',
  'notes',
  'conviction_description'
}
```

# PUT - '/charges/<int:charge_id>
Update a charge by ID

#### OPTIONAL PARAMS
```
charge - String
citation - String
sentence - String
conviction_class_type - String
  ONE OF [A,B,C,D,E,UNDEFINED']
conviction_charge_type - String
  ONE OF [felony, misdemeanor]
eligible - Boolean
please_expunge - Boolean
notes - Text
conviction_description - String
```

#### RETURNS
charge_id

# '/charges/<int:charge_id>', methods=['DELETE'])
Undefined
