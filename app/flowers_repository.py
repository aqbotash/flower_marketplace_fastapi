from attrs import define
from pydantic import BaseModel

class Flower(BaseModel):
    name: str
    count: int
    cost: int
    id: int = 0 
    
class FlowersRepository:
    def __init__(self):
        self.flowers = [
        ]
        
    def save(self, flower: Flower):
        flower.id = len(self.flowers)+1
        self.flowers.append(flower)
        
    def get_all(self)-> list:
        return self.flowers
    
    def get_by_ids(self, id_list: list)->list:
        flowers = []
        for id in id_list:
            flowers.append(self.flowers[id-1])
        return flowers
            
        