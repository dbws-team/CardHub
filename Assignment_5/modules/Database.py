import functools

import mysql.connector
from mysql.connector import errorcode
import os
from typing import Callable, List, Type
from dataclasses import dataclass
import datetime

VERBOSE = True


class SqlException(Exception):
    def __init__(self, error: mysql.connector.Error, context: str):
        """
        Executes query and throws SqlException in case of exception
        :param error: mysql error with all needed data
        :param context: verbal representation of the context in which the exception occurred
        :return:
        """
        super().__init__(f'MYSQL EXCEPTION: f{str(error)}')
        self.error = error
        self.context = context


def query(verbal_context: str, return_type: Type = tuple):
    """
    Decorator for queries
    :param return_type:
    :param verbal_context: verbal representation of the context from which function is called
    :return:
    """

    def insertion_decorator(func: Callable[..., str]):
        """
        :param func: function that returns query to be executed
        :return:
        """

        @functools.wraps(func)
        def _wrapper(*args, **kwargs) -> List[return_type]:
            if VERBOSE:
                print(verbal_context)
            _query = func(*args, **kwargs)
            self = args[0]
            res = list(self.execute_query(_query, verbal_context))
            return [return_type(*r) for r in res] if return_type is not tuple else res

        return _wrapper

    return insertion_decorator


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    age: int
    rating: int


@dataclass
class Company:
    id: int
    name: str
    policy: str


@dataclass
class Chat:
    id: int
    client_first_name: str
    client_last_name: str
    employee_first_name: str
    employee_last_name: str
    opened_at: datetime.datetime
    closed_at: datetime.datetime


@dataclass
class Ride:
    id: int
    car_class: str
    point_a: str
    point_b: str
    booked_at: datetime.datetime
    price: float


@dataclass
class IssueTicket:
    id: int
    open_at: datetime.datetime
    point_a: str
    point_b: str
    booked_at: datetime.datetime
    issue_type: str


@dataclass
class Car:
    id: int
    owning_company_id: int
    model: str
    color: str
    capacity: int
    plate_number: str
    insurance_number: str
    car_class: int


class Database:
    """
    Mysql connector wrapper
    """

    def __init__(self, user: str, password: str, host: str = 'localhost', port: int = 3306, database='dbws'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def execute_query(self, _query: str, context: str):
        """
        Executes query and throws SqlException in case of exception
        :param _query:
        :param context: verbal representation of the context from which function is called
        :return:
        """
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password, autocommit=True, database=self.database)
            cursor = connection.cursor()

            _query = f'{_query}'
            cursor.execute(_query)
            res = cursor.fetchall()

            cursor.close()
            connection.close()
            return res
        except mysql.connector.Error as err:
            raise SqlException(error=err, context=context)

    @query("Start transaction")
    def start_transaction(self):
        return "START TRANSACTION;"

    @query("Commit")
    def commit(self):
        return "COMMIT;"

    @query('Select all')
    def select_all(self, table):
        """
        Should be used only for debug
        """
        return f'select * from {table};'

    @query('Select chat ids', int)
    def select_chat_ids(self):
        return f'select id from chats;'

    @query("Select users", User)
    def select_users(self):
        return 'select * from users'

    @query("Select cars", Car)
    def select_cars(self):
        return 'select * from cars'

    @query('Select companies', Company)
    def select_companies(self):
        return f'select * from companies'

    @query("Get client chats", Chat)
    def select_client_chats(self, client_email: str, limit: int = 5):
        return f'''\
                   select c.id, client.first_name as client_first_name, client.last_name as client_last_name,
                    employee.first_name as employee_first_name, employee.last_name as employee_last_name,
                    c.opened_at, c.closed_at from chats c
                        inner join users client on client.id = c.client_id
                        inner join users employee on employee.id = c.employee_id 
                        where c.client_id=(select id from users where email="{client_email}")
                        order by c.opened_at desc limit {limit}
                   '''

    @query("Get driver-client chats", Chat)
    def select_client_driver_chats(self, client_email: str, limit: int = 5):
        return f'''\
               select c.id, client.first_name as client_first_name, client.last_name as client_last_name,
                employee.first_name as employee_first_name, employee.last_name as employee_last_name,
                c.opened_at, c.closed_at from driver_client_chats dcc
                    inner join chats c on c.id = dcc.id
                    inner join users client on client.id = c.client_id
                    inner join users employee on employee.id = c.employee_id 
                    where c.client_id=(select id from users where email="{client_email}")
                    order by c.opened_at desc limit {limit}
               '''

    @query("Get assistant-client chats", Chat)
    def select_client_assistant_chats(self, client_email: str, limit: int = 5):
        return f'''\
                   select c.id, client.first_name as client_first_name, client.last_name as client_last_name,
                    employee.first_name as employee_first_name, employee.last_name as employee_last_name,
                    c.opened_at, c.closed_at from assistant_client_chats acc
                        inner join chats c on c.id = acc.id
                        inner join users client on client.id = c.client_id
                        inner join users employee on employee.id = c.employee_id 
                        where c.client_id=(select id from users where email="{client_email}")
                        order by c.opened_at desc limit {limit}
                   '''

    @query("Get rides", Ride)
    def select_client_rides(self, client_email: str, limit=5):
        return f'''\
        select id, class, point_a, point_b, booked_at, price from rides
        where client_id=(select id from users where email="{client_email}")
        order by id desc limit {limit}
        '''

    @query("Get tickets", IssueTicket)
    def select_client_issue_tickets(self, client_email: str, limit=5):
        return f'''\
            select it.id, open_at, r.point_a, r.point_b, r.booked_at, issue_type from issue_tickets it
            join rides r on it.ride_id = r.id
            where r.client_id=(select id from users where email="{client_email}")
            order by id desc limit {limit}
            '''

    @query('Add company')
    def insert_company(self, name: str, policy: str):
        return f'insert into companies(name, policy) values("{name}", "{policy}");'

    @query('Insert car')
    def insert_car(self, company_name: str, model: str, color: str, capacity: int, plate_number: str,
                   insurance_number: str, car_class: str):
        return f'''\
        insert into cars(owning_company_id, model, color, capacity, plate_number, insurance_number, class) \
        values((select id from companies where name="{company_name}"), "{model}", "{color}", {capacity},\
        "{plate_number}", "{insurance_number}", {car_class});
        '''

    @query("Add user")
    def insert_user(self, first_name: str, last_name: str, email: str, phone_number: str, age: int):
        return f'''\
        insert into users(first_name, last_name, email, phone_number, age)
	    values("{first_name}", "{last_name}", "{email}", "{phone_number}", {age});
        '''

    @query("Add client")
    def insert_client(self, email: str, has_subscription: bool = False):
        return f'''\
        insert into clients(id, has_subscription)
	    values((select id from users where email="{email}"), false);
        '''

    @query("Add employee")
    def insert_employee(self, email: str, company_name: str):
        return f'''\
        insert into employees(id, employer_id)
	    values((select id from users where email="{email}"), (select id from companies where name="{company_name}"));
        '''

    @query("Add assistant")
    def insert_assistant(self, email: str):
        return f'''\
        insert into assistants(id)
        values((select id from users where email="{email}"));
        '''

    @query("Add assistant language")
    def insert_assistants_language(self, email: str, language: str):
        return f'''\
        insert into assistants_languages(assistant_id, language_speaking)
	    values((select id from users where email="{email}"), "{language}");
        '''

    @query("Add driver")
    def insert_driver(self, email: str, license_number: str, driving_experience_since: datetime.date,
                      car_plate_number: str,
                      is_child_qualified: bool,
                      is_vip_qualified: bool):
        return f'''\
        insert into drivers(id, license_number, driving_experience_since, car_id, is_child_qualified, is_vip_qualified)
	    values((select id from users where email="{email}"), "{license_number}", '{driving_experience_since}',
		(select id from cars where plate_number="{car_plate_number}"), {is_child_qualified}, {is_vip_qualified});
        '''

    @query("Add chat")
    def insert_chat(self, client_email: str, employee_email: str):
        return f'''\
        insert into chats(client_id, employee_id)
	    values((select id from users where email="{client_email}"), (select id from users where email="{employee_email}"));
        '''

    @query("Add driver-client chat")
    def insert_driver_client_chat(self, chat_id: int):
        return f'''\
        insert into driver_client_chats(id)
        values({chat_id});
        '''

    @query("Add ride")
    def insert_ride(self, car_class: str, driver_email: str, client_email: str, point_a: str, point_b: str,
                    price: float, chat_id: int):
        return f'''\
        insert into rides(class, driver_id, client_id, point_a, point_b, price, driver_client_chat_id)
	    values ("{car_class}", (select id from users where email="{driver_email}"),
		(select id from users where email="{client_email}"),
		"{point_a}", "{point_b}",
		{price}, {chat_id});
        '''

    @query("Add message")
    def insert_message(self, chat_id: int, message: str, sender_email: str):
        return f'''\
        insert into messages(chat_id, message, sender_id)
        values({chat_id},
            "{message}",
            (select id from users where email="{sender_email}")
        );
        '''

    @query("Add issue ticket")
    def insert_issue_ticket(self, ride_id: int, issue_type: str = 'OTHER'):
        """
        :param: issue_type: enum ('FORGOTTEN_ITEM', 'ACCIDENT', 'DRIVER_ISSUE', 'REFUND', 'OTHER')
        :param: ride_id: You should specify ride id. You can access it via select_client_rides()
        :return:
        """
        return f'''\
        insert into issue_tickets(issue_type, ride_id)
	    values('{issue_type}', {ride_id}); # the last ride
        '''

    @query("Add assistant-client chat")
    def insert_assistant_client_chat(self, chat_id: int, ticket_id: int):
        """
        :param: chat_id: You should specify ticket id. You can access it via select_client_chats()
        :param: ticket_id: You should specify ticket id. You can access it via select_client_issue_tickets()
        """
        return f'''\
        insert into assistant_client_chats(id, ticket_id)
        values({chat_id}, {ticket_id});
        '''

    def create_client(self, first_name: str, last_name: str, email: str, phone_number: str, age: int,
                      has_subscription: bool = False):
        """
        Creates user and saves him as client
        """
        self.insert_user(first_name, last_name, email, phone_number, age)
        self.insert_client(email, has_subscription)

    def create_assistant(self, first_name: str, last_name: str, email: str, phone_number: str, age: int,
                         company_name: str, languages: List[str]):
        """
        Creates user and saves him as employee and assistant with list of languages
        """
        self.insert_user(first_name, last_name, email, phone_number, age)
        self.insert_employee(email, company_name)
        self.insert_assistant(email)
        for lang in languages:
            self.insert_assistants_language(email, lang)

    def create_driver(self, first_name: str, last_name: str, email: str, phone_number: str, age: int, company_name: str,
                      license_number: str, driving_experience_since: datetime.date, car_plate_number: str,
                      is_child_qualified: bool,
                      is_vip_qualified: bool):
        """
        Creates user and saves him as employee and driver
        """
        self.insert_user(first_name, last_name, email, phone_number, age)
        self.insert_employee(email, company_name)
        self.insert_driver(email, license_number, driving_experience_since, car_plate_number, is_child_qualified,
                           is_vip_qualified)

    def create_driver_client_chat(self, client_email: str, employee_email: str):
        """
        Creates chat and saves it as client-driver chat
        """
        self.start_transaction()
        self.insert_chat(client_email, employee_email)
        chat_id = self.select_client_chats(client_email, 1)[0].id
        self.insert_driver_client_chat(chat_id)
        self.commit()

    def create_assistant_client_chat(self, client_email: str, employee_email: str, ticket_id: int):
        """
        Creates chat and saves it as assistant-client chat
        """
        self.insert_chat(client_email, employee_email)
        chat_id = self.select_client_chats(client_email, 1)[0].id
        self.insert_assistant_client_chat(chat_id, ticket_id)


if __name__ == '__main__':
    db = Database(host=os.environ.get('DBWS_HOST'), user=os.environ.get('DBWS_USER'),
                  password=os.environ.get('DBWS_PASSWORD'))
    try:
        db.insert_company(name="Uber", policy='Economy price — 0.5$/minute \
                                            Vip price — 1.5$/minute')
        db.insert_company(name="Gett", policy='Economy price — 0.6$/minute \
                                                    Vip price — 1.4$/minute')

        db.insert_car('Uber', "Toyota", "Red", 4, "HB-12-BH", "xbc-12345", 3)
        db.insert_car('Uber', "BMW", "White", 4, "HB-92-KD", "aji-92875", 1)
        db.insert_car('Uber', "Toyota", "Black", 4, "HB-12-RD", "rdf-28562", 3)

        db.insert_car("Gett", "Volkswagen", "Red", 3, "HB-45-BH", "aop-19476", 1)
        db.insert_car("Gett", "Volkswagen", "White", 3, "HB-52-KD", "fdl-40385", 1)
        db.insert_car("Gett", "Volkswagen", "Black", 4, "HB-91-LK", "qwe-18465", 2)

        db.create_client("John", "Smith", "JS@gmail.com", "909-204-3604", 22, False)
        db.create_client("Robert", "Right", "RR@gmail.com", "540-206-1301", 20, True)

        db.create_assistant("Peter", "Baumann", "PB@gmail.com", "240-320-7741", 27, "Uber", ['english', 'german'])
        db.create_assistant("Patrick", "Bateman", "Batman@gmail.com", "303-382-6393", 25, "Gett", ['english', 'french'])

        db.create_driver("Egor", "Lebedev", "Gigachad@gmail.com", "505-859-0347", 24, "Uber",
                         "PN-19203", datetime.date(2004, 1, 22), "HB-92-KD", True, True)
        db.create_driver("Rayan", "Gosling", "LiterallyMe@gmail.com", "702-933-8695", 42, "Gett",
                         "PN-21345", datetime.date(2007, 1, 22), "HB-52-KD", False, False)

        db.create_driver_client_chat("JS@gmail.com", "Gigachad@gmail.com")
        db.create_driver_client_chat("RR@gmail.com", "LiterallyMe@gmail.com")

        # ride 1
        cid = db.select_client_driver_chats("JS@gmail.com", limit=1)[0].id
        db.insert_ride("VIP", "Gigachad@gmail.com", "JS@gmail.com", "Jacobs University Bremen", "Bremen HBF", 17, cid)
        db.insert_message(cid, "hey, where are you?", "JS@gmail.com")
        db.insert_message(cid, "am parking, just a sec", "Gigachad@gmail.com")
        db.insert_message(cid, "waiting for ya!", "JS@gmail.com")
        # end of ride 1

        # ride 2
        cid = db.select_client_driver_chats("RR@gmail.com", limit=1)[0].id
        db.insert_ride("STANDARD", "LiterallyMe@gmail.com", "RR@gmail.com", "Plan B bar", "Jacobs University Bremen",
                       10, cid)
        db.insert_message(cid, "hello, that's your driver, i'm waiting for you", "LiterallyMe@gmail.com")
        db.insert_message(cid, "be there in 3 minutes!", "RR@gmail.com")
        db.insert_message(cid, "ok.", "LiterallyMe@gmail.com")
        # end of ride 2

        ride_id = db.select_client_rides("RR@gmail.com", limit=1)[0].id
        db.insert_issue_ticket(ride_id, 'FORGOTTEN_ITEM')
        ticket_id = db.select_client_issue_tickets("RR@gmail.com", limit=1)[0].id
        db.create_assistant_client_chat("RR@gmail.com", "Batman@gmail.com", ticket_id)

        cid = db.select_client_assistant_chats("RR@gmail.com", limit=1)[0].id
        db.insert_message(cid, "hello, it seems I forgot my airpods in the car, can you help me?", "RR@gmail.com")
        db.insert_message(cid, "sure, I'll call the driver for you", "Batman@gmail.com")
        db.insert_message(cid, "Thx.", "RR@gmail.com")
        db.insert_message(cid,
                          "Yep, he found your airpods, you can grab it at our lost and fund center in Bremen, "
                          "starting from tommorow morning.",
                          "Batman@gmail.com")
        db.insert_message(cid, "Awesome!", "RR@gmail.com")

        print(db.select_companies())
    except SqlException as e:
        print(e)
        print(e.error.errno)
        print(e.context)
