import pytest

def test_file_not_empty(csv_data):
    assert len(csv_data) > 0, "CSV file is empty"

@pytest.mark.validate_csv
@pytest.mark.xfail(reason = "known duplicates")
def test_duplicates(csv_data):
    rows = []

    for row in csv_data:
        rows.append(tuple(row.values()))

    assert len(rows) == len(set(rows)), "Duplicate rows found"




@pytest.mark.validate_csv
def test_validate_schema(csv_data,schema_validate):
    actual_schema = csv_data[0].keys()
    expected_schema = ['id','name','age','email','is_active']
    assert schema_validate(expected_schema,actual_schema), "Schema mismatch"

@pytest.mark.validate_csv
@pytest.mark.skip(reason = "skip age validation")
def test_age_column_valid(csv_data):
    for row in csv_data:
        age = int(row["age"])
        assert 0 <= age <= 100, f"Invalid age: {age}"



@pytest.mark.validate_csv
def test_email_column_valid(csv_data):
    for row in csv_data:
        email = row["email"]
        assert "@" in email and "." in email and "com" in email, f"Invalid email: {email}"


@pytest.mark.parametrize("id,is_active",[("1","False"),("2","True")])
def test_active_players_parameter(csv_data,id,is_active):
    for row in csv_data:
        if row["id"] == id:
            assert row["is_active"] == is_active, f"id has wrong value: {id}"



def test_active_player(csv_data):
    for row in csv_data:
        id = row["id"]
        is_active = row["is_active"]
        if id == "2":
            assert is_active == "True", "should be True"
