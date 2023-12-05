from attrs import define

@define
class Purchase:
    user_id: int
    flower_id: int
    
class PurchaseRepository:
    def __init__(self):
        self.purchases = []
        
    def save(self, purchase: Purchase):
        self.purchases.append(purchase)
        
    def get_by_user_id(self, user_id: int):
        purchases = []
        for purchase in self.purchases:
            if purchase.user_id == user_id:
                purchases.append(purchase.flower_id)
        return purchases