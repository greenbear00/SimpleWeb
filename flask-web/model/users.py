from sqlalchemy import Column, String, DateTime
from common.database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column('id', String(30), primary_key=True)  # 01073000217
    name = Column('name', String(30))  # greenbear
    passwd = Column('passwd', String(120))
    cret_dt = Column('cret_dt', DateTime)

    def __init__(self, user_id=None, user_name=None, passwd=None, cret_dt=None):
        self.id = user_id
        self.name = user_name
        self.passwd = passwd
        self.cret_dt = cret_dt

    def __repr__(self):
        return f"<Users({self.id}, {self.name})>"

if __name__ == "__main__":
    from common.database import session_scope

    tmp_user = Users(user_id='01073000219', user_name='greenbear')
    with session_scope() as db_session:
        db_session.add(tmp_user)
