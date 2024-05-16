from flask import Blueprint, request
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher

from .schema import AssignmentSchema, AssignmentGradeSchema

principal_resources = Blueprint('principal_resources', __name__)


@principal_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """List all submitted and graded assignments"""
    assignments = Assignment.query.filter((Assignment.state == 'SUBMITTED') | (Assignment.state == 'GRADED')).all()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


@principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """List all the teachers"""
    teachers = Teacher.query.all()
    teachers_dump = [{'id': teacher.id, 'user_id': teacher.user_id,
    'created_at': teacher.created_at, 'updated_at': teacher.updated_at} for teacher in teachers]
    return APIResponse.respond(data=teachers_dump)


@principal_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p):
    """Grade or re-grade an assignment"""
    incoming_payload = request.json
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    assignment = Assignment.get_by_id(grade_assignment_payload.get('id'))
    if assignment is None:
        return APIResponse.respond(message='Assignment not found', status=404)

    assignment.grade = grade_assignment_payload.get('grade')
    assignment.state = 'GRADED'
    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=graded_assignment_dump)
