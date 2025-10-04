from entity import User
from sqlalchemy.orm import Session
from database import SessionLocal

class DbUserRepository:     
    def __init__(self):
        self.db = SessionLocal()

    def get_user_by_id(self, user_id: int):
#        return self.db.query(User).filter(User.id == user_id).first()
        query = self.db.query(User).filter(User.id == user_id)
       
#        sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
#        print(f"SQL: {sql}")
         
        return query.first()

    def get_all_users(self):
        return self.db.query(User).all()
    
    def close(self):
        """Close the database session."""
        self.db.close()