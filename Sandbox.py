import uuid
from datetime import date
import counter

class DBHandler:
    def __init__(self, db_path="app.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

class NoAlternate(Exception):
    pass

class UnassignedItem(Exception):
    pass

class PointsExhausted(Exception):
    pass

class InsufficientPoints(Exception):
    pass


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
        self.gathering_skills=details.gathering
        self.gathering_skills['cargo_ship']*=2
        self.rank=details.rank
        self.assigned_pulls={
            'mining':[],
            'hunting':[],
            'mercantile':[],
            'black_market':[],
            'cargo_ship':[]
        }

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
        self.status=None
        for item,amount in orders.items():
            for _ in range(amount):
                self.items.append(item)

    def create(self):
        self.status='Pending'

class Pull:
    def __init__(self,item):
        self.item=item
        dic_lookup=item_lookup[item]
        self.cost=dic_lookup['points']
        self.cat=dic_lookup['cat']
        if self.cost<=2 and self.cat=='mercantile':
            self.cargo_ship=True
        else:
            self.cargo_ship=False

    def alternate(self):
        if self.item in alternates:
            new_cat=alternates[self.item]
            logging.info(f'switching {self.item} from {self.cat} to {new_cat}')
            self.cat=new_cat
        else:
            logging.debug(f'{self.item} cannot be alternated. Skipping and raising NoAlternate')
            raise NoAlternate

class OrderManager:
    def __init__(self,orders):
        self.pulls={ 
            'mercantile':[],
            'black_market':[],
            'hunting':[],
            'mining':[],
            'cargo_ship':[]}  # this will mutate so be careful- it is used to pass whatever the given orders are needed into other contexts
        
        self.raw_pulls=[]

        for item in orders:
            for _ in range(orders[item]):
                pull_det=Pull(item)
                self.raw_pulls.append(pull_det)

        self.unassigned_pulls=[]
        
        self.eligible_alternates=[]
        self.cargo_pulls=[]
        self.overflow_pulls=[]

    def alternate_pulls(self):
        for pull in self.unassigned_pulls[:]:
            try:
                pull.alternate()
                self.eligible_alternates.append(pull)
                self.unassigned_pulls.remove(pull)
            except NoAlternate:
                continue
        self.build_dic(self.eligible_alternates)

    def set_sail(self):
        for pull in self.unassigned_pulls:
            if pull.cargo_ship is True:
                pull.cat='cargo_ship'
                self.cargo_pulls.append(pull)
            else:
                self.overflow_pulls.append(pull)
        self.build_dic(self.cargo_pulls)

    def build_dic(self,list_):
        self.pulls={ 
            'mercantile':[],
            'black_market':[],
            'hunting':[],
            'mining':[],
            'cargo_ship':[]}
        for pull in list_:
            self.pulls[pull.cat].append(pull)

    def call(self):
        return self.pulls

class AssignmentManager:
    def __init__(self,orders,employees_):
        self.employees_=employees_
        self.eligible_employees={
            'mercantile':employees_,
            'hunting':employees_,
            'black_market':employees_,
            'mining':employees_,
            'cargo_ship':employees_
        }


        self.order_list=OrderManager(orders)

        self.pull_cat()

        order_list.alternate_pulls()

        self.pull_cat()

        order_list.set_sail()

        self.pull_cat()

    def pull_cat(self):
        for cat in self.order_list.pulls:
            order_list_=self.order_list.pulls[cat]
            for pull in order_list_:
                employees=self.eligible_employees[cat]
                try:
                    self.assign_pull(pull,employees)
                except UnassignedItem:
                    self.order_list.unassigned_pulls.append(pull)

    def assign_pull(self,pull,employees):
        for employee in employees[:]:
            try:
                self.check_eligibility(pull,employee)
                break
            except InsufficientPoints:
                continue

            except PointsExhausted:
                self.eligible_employees[pull.cat].remove(employee)
                continue

        else:
            raise UnassignedItem    
    
    def check_eligibility(self,pull,employee):
        category=pull.cat
        current_score=employee.gathering_skills[category]
        if current_score>=pull.cost:
            self.assign_item(pull,employee)
        else:
            if current_score==0:
                raise PointsExhausted
            else:
                raise InsufficientPoints
    
    def assign_item(self,pull,employee):
        category=pull.cat
        current_score=employee.gathering_skills[category]
        new_score=current_score-pull.cost
        employee.gathering_skills[category]=new_score
        logging.debug(f'assigning {employee.character_name} {pull.item}.')
        employee.assigned_pulls[category].append(pull.item)

class Assignments:
    def __init__(self, manager):
        self.manager=manager
        self.unpulled_items=[pull.item for pull in self.manager.order_list.unassigned_pulls]
        self.no_pull_out=self.count_unassigned_items()
        self.all_pulls={emp.character_name: emp.assigned_pulls for emp in self.manager.employees_}

    def count_unassigned_items(self):
        self.unpulled_items=[pull.item for pull in self.manager.order_list.unassigned_pulls]
        return Counter(self.unpulled_items)
