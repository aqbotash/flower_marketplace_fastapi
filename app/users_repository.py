from attrs import define
from pydantic import BaseModel, Field

class User(BaseModel):
    email: str
    full_name: str = Field()
    password: str = Field()
    id: int = 0

class UserLogin(BaseModel):
    email: str
    password: str
    
    
class UsersRepository:
    def __init__(self):
        self.users = [
            User(email = 'aqbotamaratqyzy@gmail.com', full_name = 'Akbota Kurmangazhyyeva', password = '12345', id = 1)
        ]
    def save(self, user: User):
        user.id = len(self.users)+1
        self.users.append(user)
        
    def get_by_email(self, email)->User:
        for user in self.users:
            if user.email == email:
                return user
        return None
    def get_all(self):
        return self.users
        
    
