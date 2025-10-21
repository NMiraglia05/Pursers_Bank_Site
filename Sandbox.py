import uuid
from datetime import date

class DBHandler:
    def __init__(self, db_path="app.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

class Transaction(ABC):
    @property
    @abstractmethod
    def ID(self):
        """Unique identifier for the transaction."""
        pass

    @abstractmethod
    def save(self):
        """Save transaction details."""
        pass

class Account(ABC):
    @abstractmethod
    def update(self):
        """Update the account."""
        pass

    @abstractmethod
    def create(self):
        """create the account."""
        pass

    @abstractmethod
    def save(self):
        """Save the account to the db."""
        pass

class Payment(Transaction):
    def __init__(self):
        pass

    def save(self):
        if self.value is None:
            raise InvalidPaymentDetails
        trans={'id':self.id,'type':self.type,'desc':self.desc,'value':self.value}
        return trans

class Credit(Payment):
    def __init__(self,amount):
        self.type='Credit'
        self.value=amount*-1 # because this is a credit transaction, this bills at a negative. The assumption being an account only pays with credit to cover a gap created by insufficient funds.
        self.desc='Future payment for goods/services received'

class Cash(Payment):
    def __init__(self,amount):
        self.type='Cash'
        self.value=amount
        self.desc='Direct Currency'

class Materials(Payment):
    def __init__(self,materials):
        self.type='Materials'
        self.value=0
        for mat,amount in materials.items():
            mat_value=item_lookup[mat]['points']
            trans_value=mat_value*amount
            self.value+=trans_value
        self.desc=materials

class Service(Payment):
    def __init__(self,value=None):
        self.type='Services'
        self.value=value # this is so that an adjustor can review the service provided and determine the value thereof. If a service payment is attempted without a value being set, it will not work.
        self.desc='Services provided for goods/services received.'

class Person(Account,DBHandler):
    def __init__(self,details):
        self.details=details
        self.character_name=details.character_name
        self.player_name=details.player_name
        self.discord=details.discord
    
    def create(self,category=None):
        if category is None:
            raise AttributeError('No category defined.')
        self.uuid=str(uuid.uuid4())
        sql=f"SELECT MAX(ID) FROM {category}"
        cursor.execute(sql)
        max_id = cursor.fetchone()[0] or 0
        self.id=max_id+1
        self.day_created=date.today()

    def save(self):
        self.save_data=[self.uuid,self.id,self.character_name,self.player_name,self.day_created]

    def format(self):
        read_dic={'ID':self.id,'Character':self.character_name}
        return read_dic


class Employee(Person):
    def __init__(self,details):
        super().__init__(details)
        self.rank=details.rank
    
    def save(self):
        super().save()
        self.save_data.append(self.rank)

    def format(self):
        read_dic=super().format()
        read_dic['Rank']=self.rank
        return read_dic

class Customer(Person):
    def __init__(self,details):
        super().__init__(details)
        self.log_message=f'Customer {self.character_name}'
        self.accounts=[]

class Savings_Account(Account):
    def __init__(self):
        self.id=none
        self.customer_id=none

    def Update_Balance(self):
        pass

class Order(Transaction):
    def __init__(self,order,customer):
        self.id=None
        self.Recipient=customer.character_name
        self.discord_id=customer.discord
        self.receipient_id=order.customer_id
        self.items=[]
        for item,amount in orders.items():
            for _ in range(amount):
                self.items.append(item)

class Process_Manager:
