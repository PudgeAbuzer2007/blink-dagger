import sqlalchemy
import sqlalchemy.ext.declarative as dec


class Jobs(dec.declarative_base()):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    job = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)
