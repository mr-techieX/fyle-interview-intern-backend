import json
from core.models.assignments import AssignmentStateEnum, GradeEnum
from core import db


def test_list_assignments(client, principal_headers):
    response = client.get('/principal/assignments', headers=principal_headers)
    assert response.status_code == 200

    data = response.json['data']
    assert isinstance(data, list)

def test_list_teachers(client, principal_headers):
    # Ensure that the endpoint responds with a 200 status code
    response = client.get('/principal/teachers', headers=principal_headers)
    assert response.status_code == 200

    # Ensure that the response contains a list of teachers
    data = response.json['data']
    assert isinstance(data, list)
    
    

def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    payload = {
        'id': 5,
        'grade': GradeEnum.A.value
    }
    response = client.post(
        '/principal/assignments/grade',
        json=payload,
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B
    
def test_list_assignments_no_data(client, principal_headers):
    # Ensure that the endpoint handles the case when there are no assignments
    response = client.get('/principal/assignments', headers=principal_headers)
    assert response.status_code == 200
    assert response.json['data'] == []

def test_list_teachers_no_data(client, principal_headers):
    # Ensure that the endpoint handles the case when there are no teachers
    response = client.get('/principal/teachers', headers=principal_headers)
    assert response.status_code == 200
    assert response.json['data'] == []