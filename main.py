from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from neo4j import GraphDatabase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from datetime import datetime, timedelta
from pymongo import MongoClient
import random
import string
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
def parse_date(date_string):

    try:
        return datetime.strptime(date_string, '%d-%m-%Y').date()
    except ValueError:
        return None


def parse_time(time_string):
    try:
        return datetime.strptime(time_string, '%H:%M').time()
    except ValueError:
        return None


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Przycisk do dodawania pociągu
        add_train_button = Button(text='Dodaj Pociąg')
        add_train_button.bind(on_press=self.go_to_add_train_screen)
        layout.add_widget(add_train_button)

        # Przycisk do usuwania pociągu
        delete_train_button = Button(text='Usuń Pociąg')
        delete_train_button.bind(on_press=self.go_to_delete_train_screen)
        layout.add_widget(delete_train_button)

        # Przycisk do wyszukiwania pociągu
        search_connections_button = Button(text='Wyszukaj Pociąg')
        search_connections_button.bind(on_press=self.go_to_search_connections_screen)
        layout.add_widget(search_connections_button)

        # Przycisk do zakupu biletów
        purchase_ticket_button = Button(text='Kup Bilety')
        purchase_ticket_button.bind(on_press=self.go_to_purchase_ticket_screen)
        layout.add_widget(purchase_ticket_button)

        view_tickets_button = Button(text='Przegląd biletów')
        view_tickets_button.bind(on_press=self.go_to_view_tickets_screen)
        layout.add_widget(view_tickets_button)
        self.add_widget(layout)

    def go_to_add_train_screen(self, instance):
        self.manager.current = 'add_train'

    def go_to_delete_train_screen(self, instance):
        self.manager.current = 'delete_train'

    def go_to_search_connections_screen(self, instance):
        self.manager.current = 'search_connections'
    def go_to_purchase_ticket_screen(self, instance):
        self.manager.current = 'purchase_ticket'
    def go_to_view_tickets_screen(self, instance):
         self.manager.current = 'view_tickets'
class AddTrainScreen(Screen):
    def __init__(self, neo4j_driver, **kwargs):
        super(AddTrainScreen, self).__init__(**kwargs)
        self.neo4j_driver = neo4j_driver

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Tabela 3x3 dla podstawowych informacji o pociągu
        grid_3x3 = GridLayout(cols=3, spacing=[5, 10])
        self.train_number_input = TextInput(hint_text='Numer pociągu', font_size=20)
        self.seats_input = TextInput(hint_text='Ilość miejsc', font_size=20)
        self.occupied_seats_input = TextInput(hint_text='Ilość zajętych miejsc', font_size=20)
        self.departure_city_input = TextInput(hint_text='Miasto odjazdu', font_size=20)
        self.departure_station_input = TextInput(hint_text='Stacja odjazdu', font_size=20)
        self.departure_track_input = TextInput(hint_text='Tor odjazdu', font_size=20)
        self.arrival_city_input = TextInput(hint_text='Miasto docelowe', font_size=20)
        self.arrival_station_input = TextInput(hint_text='Stacja docelowa', font_size=20)
        self.arrival_track_input = TextInput(hint_text='Tor docelowy', font_size=20)

        grid_3x3.add_widget(self.train_number_input)
        grid_3x3.add_widget(self.seats_input)
        grid_3x3.add_widget(self.occupied_seats_input)
        grid_3x3.add_widget(self.departure_city_input)
        grid_3x3.add_widget(self.departure_station_input)
        grid_3x3.add_widget(self.departure_track_input)
        grid_3x3.add_widget(self.arrival_city_input)
        grid_3x3.add_widget(self.arrival_station_input)
        grid_3x3.add_widget(self.arrival_track_input)

        main_layout.add_widget(grid_3x3)

        # Tabela 4x1 dla dat i godzin
        grid_4x1 = GridLayout(cols=4, size_hint_y=None, height=40)
        self.departure_date_input = TextInput(hint_text='Data odjazdu (DD-MM-YYYY)', font_size=18)
        self.departure_time_input = TextInput(hint_text='Godzina odjazdu (HH:MM)', font_size=18)
        self.arrival_date_input = TextInput(hint_text='Data przyjazdu', font_size=18)
        self.arrival_time_input = TextInput(hint_text='Godzina przyjazdu', font_size=18)

        grid_4x1.add_widget(self.departure_date_input)
        grid_4x1.add_widget(self.departure_time_input)
        grid_4x1.add_widget(self.arrival_date_input)
        grid_4x1.add_widget(self.arrival_time_input)

        main_layout.add_widget(grid_4x1)

        # Tabela 3x1 dla przycisków i informacji
        grid_3x1 = GridLayout(cols=1)
        submit_button = Button(text='Dodaj do bazy', font_size=32)
        submit_button.bind(on_press=self.submit_to_db)
        grid_3x1.add_widget(submit_button)

        self.message_label = Label(text='', font_size=32)
        grid_3x1.add_widget(self.message_label)

        back_button = Button(text='Powrót do głównego ekranu', font_size=32)
        back_button.bind(on_press=self.go_to_main_screen)
        grid_3x1.add_widget(back_button)

        main_layout.add_widget(grid_3x1)

        self.add_widget(main_layout)

    def go_to_main_screen(self, instance):
        self.manager.current = 'main'

    def submit_to_db(self, instance):
        print("submit_to_db is called")
        train_number = self.train_number_input.text
        seats = self.seats_input.text
        occupied_seats = self.occupied_seats_input.text
        departure_city = self.departure_city_input.text
        departure_station = self.departure_station_input.text
        departure_track = self.departure_track_input.text
        departure_date = parse_date(self.departure_date_input.text)
        departure_time = parse_time(self.departure_time_input.text)
        arrival_city = self.arrival_city_input.text
        arrival_station = self.arrival_station_input.text
        arrival_track = self.arrival_track_input.text
        arrival_date = parse_date(self.arrival_date_input.text)
        arrival_time = parse_time(self.arrival_time_input.text)

        if None in [departure_date, arrival_date, departure_time, arrival_time]:
            self.message_label.text = 'Nieprawidłowy format daty lub czasu'
            return
        departure_datetime = datetime.combine(departure_date, departure_time)
        arrival_datetime = datetime.combine(arrival_date, arrival_time)
        duration = arrival_datetime - departure_datetime
        if duration.days < 0:
            self.message_label.text = 'Godzina przyjazdu jest przed godziną odjazdu'
            return

        if not all([train_number, seats, occupied_seats, departure_city, departure_station,
                    departure_track, departure_date, departure_time, arrival_city,
                    arrival_station, arrival_track, arrival_date, arrival_time]):
            self.message_label.text = 'Nie wszystkie pola są wypełnione'
            return

        data = {
            "train_number": train_number,
            "seats": seats,
            "occupied_seats": occupied_seats,
            "departure_city": departure_city,
            "departure_station": departure_station,
            "departure_track": departure_track,
            "departure_date": departure_date,
            "departure_time": departure_time,
            "arrival_city": arrival_city,
            "arrival_station": arrival_station,
            "arrival_track": arrival_track,
            "arrival_date": arrival_date,
            "arrival_time": arrival_time
        }

        insert_data_into_neo4j(self.neo4j_driver, **data)
        self.message_label.text = 'Dodano pomyślnie'


class DeleteTrainScreen(Screen):
    def __init__(self, neo4j_driver, **kwargs):
        super(DeleteTrainScreen, self).__init__(**kwargs)
        self.neo4j_driver = neo4j_driver
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Pola do wprowadzania danych
        self.train_number_input = TextInput(hint_text='Numer pociągu', multiline=False)

        grid_2x2 = GridLayout(cols=2, spacing=[250, 10])
        self.departure_date_input = TextInput(hint_text='Data odjazdu (opcjonalnie)', multiline=False)
        self.departure_time_input = TextInput(hint_text='Godzina odjazdu (opcjonalnie)', multiline=False)
        self.city_input = TextInput(hint_text='Miasto (opcjonalnie)', multiline=False)
        self.station_input = TextInput(hint_text='Nazwa stacji (opcjonalnie)', multiline=False)

        grid_2x2.add_widget(self.departure_date_input)
        grid_2x2.add_widget(self.city_input)
        grid_2x2.add_widget(self.departure_time_input)
        grid_2x2.add_widget(self.station_input)
        layout.add_widget(self.train_number_input)
        layout.add_widget(grid_2x2)

        delete_button = Button(text='Usuń z bazy')
        delete_button.bind(on_press=self.delete_from_db)

        # Label do wyświetlania komunikatów
        self.message_label = Label(text='')

        layout.add_widget(delete_button)
        layout.add_widget(self.message_label)

        # Przycisk powrotu do głównego ekranu
        back_button = Button(text='Powrót do głównego ekranu')
        back_button.bind(on_press=self.go_to_main_screen)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to_main_screen(self, instance):
        self.manager.current = 'main'

    def delete_from_db(self, instance):
        train_number = self.train_number_input.text
        departure_date = self.departure_date_input.text
        departure_time = self.departure_time_input.text
        city = self.city_input.text
        station = self.station_input.text

        with self.neo4j_driver.session() as session:
            if train_number and not any([departure_date, departure_time, city, station]):
                session.run("MATCH (t:Train {number: $number}) DETACH DELETE t", number=train_number)
                self.message_label.text = f'Usunięto wszystkie dane o pociągu {train_number}'
            elif train_number and departure_date and departure_time:
                session.run("MATCH (t:Train {number: $number})-[r:DEPARTS_FROM|ARRIVES_AT]->() "
                            "WHERE r.date = $date AND r.time = $time "
                            "DELETE r", number=train_number, date=departure_date, time=departure_time)
                self.message_label.text = f'Usunięto pociąg {train_number} odjeżdżający {departure_date} o {departure_time} oraz powiązane przyjazdy'
            elif train_number and city and station:
                session.run(
                    "MATCH (t:Train {number: $number})-[r:DEPARTS_FROM]->(s:Station {city: $city, name: $name}) "
                    "OPTIONAL MATCH (t)-[r2:ARRIVES_AT]->() "
                    "DELETE r, r2", number=train_number, city=city, name=station)
                self.message_label.text = f'Usunięto pociąg {train_number} z peronu w {city}, stacja {station} oraz powiązane przyjazdy'
            else:
                self.message_label.text = 'Niepoprawne dane lub brakujące informacje'


class SearchConnectionsScreen(Screen):
    def __init__(self, neo4j_driver, **kwargs):
        super(SearchConnectionsScreen, self).__init__(**kwargs)
        self.neo4j_driver = neo4j_driver

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input fields for date, departure city, and arrival city
        self.departure_city_input = TextInput(hint_text='Miasto początkowe', font_size=20)
        self.arrival_city_input = TextInput(hint_text='Miasto docelowe', font_size=20)
        self.date_input = TextInput(hint_text='Data (DD-MM-YYYY)', font_size=20)

        # Button for searching connections
        search_button = Button(text='Szukaj połączeń', font_size=20)
        search_button.bind(on_press=self.search_connections)

        # Adding widgets to layout
        main_layout.add_widget(self.departure_city_input)
        main_layout.add_widget(self.arrival_city_input)
        main_layout.add_widget(self.date_input)
        main_layout.add_widget(search_button)

        # Label to display results
        self.results_label = Label(text='', font_size=20)
        main_layout.add_widget(self.results_label)

        back_button = Button(text='Powrót do głównego ekranu')
        back_button.bind(on_press=self.go_to_main_screen)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def go_to_main_screen(self, instance):
        self.manager.current = 'main'

    def search_connections(self, instance):
        # Retrieve input values
        departure_city = self.departure_city_input.text
        arrival_city = self.arrival_city_input.text
        date_str = self.date_input.text

        # Parse the date
        try:
            date = datetime.strptime(date_str, '%d-%m-%Y').date()
        except ValueError:
            self.results_label.text = 'Nieprawidłowy format daty'
            return

        # Retrieve connections from the database
        results = self.find_connections(departure_city, arrival_city, date)

        # Display the results
        self.display_results(results)

    def find_connections(self, departure_city, arrival_city, date):
        query = """
            MATCH (dep:Station {city: $departure_city})<-[train_from_A:DEPARTS_FROM]-(train:Train)-[train_to_C:ARRIVES_AT]->(arr:Station {city: $arrival_city})
            WHERE train_from_A.date = $date
            RETURN dep.city as departure_city, arr.city as arrival_city, train_from_A.date as date, train_from_A.time as departure_time, train_to_C.date as arrival_date, train_to_C.time as arrival_time, train.number as train_number
            ORDER BY train_from_A.time
            LIMIT 3
        """

        with self.neo4j_driver.session() as session:
            results = list(session.run(query, departure_city=departure_city, arrival_city=arrival_city, date=date))
        return results

    def display_results(self, connections):
        if not connections:
            self.results_label.text = 'Brak wyników'
            return

        output = ""
        for record in connections:
            departure_date_str = record["date"].iso_format()
            departure_time_str = f"{record['departure_time'].hour:02d}:{record['departure_time'].minute:02d}"
            arrival_date_str = record["arrival_date"].iso_format()
            arrival_time_str = f"{record['arrival_time'].hour:02d}:{record['arrival_time'].minute:02d}"
            train_name = record["train_number"]

            output += f"Odjazd: {record['departure_city']}, Przyjazd: {record['arrival_city']}, " \
                      f"Data odjazdu: {departure_date_str}, Godzina odjazdu: {departure_time_str}, " \
                      f"Data przyjazdu: {arrival_date_str}, Godzina przyjazdu: {arrival_time_str}, " \
                      f"Nazwa pociągu: {train_name}\n"

        self.results_label.text = output
class PurchaseTicketScreen(Screen):
    def __init__(self, neo4j_driver, mongo_uri, mongo_db, mongo_collection, **kwargs):
        super(PurchaseTicketScreen, self).__init__(**kwargs)
        self.neo4j_driver = neo4j_driver
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[mongo_db]
        self.mongo_collection = self.mongo_db[mongo_collection]

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input fields for ticket purchase
        self.train_number_input = TextInput(hint_text='Numer pociągu', font_size=20)
        self.departure_date_input = TextInput(hint_text='Data odjazdu (DD-MM-YYYY)', font_size=20)
        self.departure_time_input = TextInput(hint_text='Godzina odjazdu (HH:MM)', font_size=20)
        self.num_tickets_input = TextInput(hint_text='Liczba biletów', font_size=20)
        self.first_name_input = TextInput(hint_text='Imię', font_size=20)
        self.last_name_input = TextInput(hint_text='Nazwisko', font_size=20)

        # Button for purchasing tickets
        purchase_button = Button(text='Kup bilet', font_size=20)
        purchase_button.bind(on_press=self.purchase_ticket)

        # Adding widgets to layout
        main_layout.add_widget(self.train_number_input)
        main_layout.add_widget(self.departure_date_input)
        main_layout.add_widget(self.departure_time_input)
        main_layout.add_widget(self.num_tickets_input)
        main_layout.add_widget(self.first_name_input)
        main_layout.add_widget(self.last_name_input)
        main_layout.add_widget(purchase_button)

        # Label to display purchase results
        self.purchase_result_label = Label(text='', font_size=20)
        main_layout.add_widget(self.purchase_result_label)

        back_button = Button(text='Powrót do głównego ekranu')
        back_button.bind(on_press=self.go_to_main_screen)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def go_to_main_screen(self, instance):
        self.manager.current = 'main'

    def generate_ticket_number(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def generate_ticket(self, train_number, departure_date, departure_time, first_name, last_name):
        ticket_number = self.generate_ticket_number()
        ticket_data = {
            "ticket_number": ticket_number,
            "train_number": train_number,
            "departure_date": departure_date,
            "departure_time": departure_time,
            "first_name": first_name,
            "last_name": last_name
        }
        return ticket_data

    def purchase_ticket(self, instance):
        train_number = self.train_number_input.text
        departure_date = self.departure_date_input.text
        departure_time = self.departure_time_input.text
        num_tickets = int(self.num_tickets_input.text)
        first_name = self.first_name_input.text
        last_name = self.last_name_input.text

        for _ in range(num_tickets):
            ticket_data = self.generate_ticket(train_number, departure_date, departure_time, first_name, last_name)

            # Здесь вы можете выбрать подходящий метод для вставки данных в вашу коллекцию MongoDB
            # Например, для вставки одного документа вы можете использовать insert_one:
            self.mongo_collection.insert_one(ticket_data)

        # Отобразите результат покупки
        self.purchase_result_label.text = f'Kupiono {num_tickets} miejsc na pociąg № {train_number}, wyjazd: {departure_date} o {departure_time}'

        # Очистите поля ввода после покупки
        self.train_number_input.text = ''
        self.departure_date_input.text = ''
        self.departure_time_input.text = ''
        self.num_tickets_input.text = ''
        self.first_name_input.text = ''
        self.last_name_input.text = ''

    def on_leave(self, *args, **kwargs):
        # Закрывайте соединение с MongoDB при выходе из экрана
        self.mongo_client.close()

class ViewTicketsScreen(Screen):
    def __init__(self, mongo_uri, mongo_db, mongo_collection, **kwargs):
        super(ViewTicketsScreen, self).__init__(**kwargs)
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[mongo_db]
        self.mongo_collection = self.mongo_db[mongo_collection]

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input fields for name and last name
        self.first_name_input = TextInput(hint_text='Imię', font_size=20)
        self.last_name_input = TextInput(hint_text='Nazwisko', font_size=20)

        # Button for searching tickets
        search_button = Button(text='Szukaj Biletów', font_size=20)
        search_button.bind(on_press=self.search_tickets)

        # Adding widgets to layout
        main_layout.add_widget(self.first_name_input)
        main_layout.add_widget(self.last_name_input)
        main_layout.add_widget(search_button)

        # ScrollView to display the ticket results
        self.scroll_view = ScrollView()
        main_layout.add_widget(self.scroll_view)

        # Label to display results
        self.results_label = Label(text='', font_size=20)
        self.scroll_view.add_widget(self.results_label)

        back_button = Button(text='Powrót do głównego ekranu')
        back_button.bind(on_press=self.go_to_main_screen)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def go_to_main_screen(self, instance):
        self.manager.current = 'main'

    def search_tickets(self, instance):
        first_name = self.first_name_input.text
        last_name = self.last_name_input.text

        # Retrieve tickets from the database
        results = self.find_tickets(first_name, last_name)

        # Display the results
        self.display_results(results)

    def find_tickets(self, first_name, last_name):
        query = {
            "first_name": first_name,
            "last_name": last_name
        }

        results = list(self.mongo_collection.find(query))
        return results

    def display_results(self, tickets):
        if not tickets:
            self.results_label.text = 'Brak wyników'
            return

        output = ""
        for ticket in tickets:
            output += f"Numer biletu: {ticket['ticket_number']}, Pociąg: {ticket['train_number']}, " \
                      f"Wyjazd: {ticket['departure_date']} o {ticket['departure_time']}, " \
                      f"Imię: {ticket['first_name']}, Nazwisko: {ticket['last_name']}\n"

        self.results_label.text = output

    def on_leave(self, *args, **kwargs):
        # Закрывайте соединение с MongoDB при выходе из экрана
        self.mongo_client.close()
class Neo4jApp(App):
    def build(self):
        # Подключение к Neo4j
        self.driver = connect_to_neo4j("bolt://localhost:7687", "neo4j", "12121212")

        # Подключение к MongoDB Atlas
        # Замените "your_mongo_uri", "your_database_name" и "your_collection_name" на свои реальные значения
        mongo_uri = "mongodb+srv://diplom:diplom@diplom.hbexvph.mongodb.net/diplom?retryWrites=true&w=majority"
        mongo_db = "bazy"
        mongo_collection = "tickets"

        # Создание менеджера экранов
        self.screen_manager = ScreenManager()

        # Добавление экранов в менеджер
        self.screen_manager.add_widget(MainScreen(name='main'))
        self.screen_manager.add_widget(AddTrainScreen(self.driver, name='add_train'))
        self.screen_manager.add_widget(DeleteTrainScreen(self.driver, name='delete_train'))
        self.screen_manager.add_widget(SearchConnectionsScreen(self.driver, name='search_connections'))
        self.screen_manager.add_widget(ViewTicketsScreen(mongo_uri, mongo_db, mongo_collection, name='view_tickets'))
        # Вставьте данные подключения к MongoDB Atlas здесь
        self.screen_manager.add_widget(
            PurchaseTicketScreen(self.driver, mongo_uri, mongo_db, mongo_collection, name='purchase_ticket'))

        return self.screen_manager

# Funkcje Neo4j
def connect_to_neo4j(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver


def insert_data_into_neo4j(driver, **data):
    with driver.session() as session:
        session.run("""
            CREATE (t:Train {number: $train_number, seats: $seats, occupied_seats: $occupied_seats})
            CREATE (ds:Station {name: $departure_station, city: $departure_city, track: $departure_track})
            CREATE (as:Station {name: $arrival_station, city: $arrival_city, track: $arrival_track})
            MERGE (t)-[:DEPARTS_FROM {date: $departure_date, time: $departure_time}]->(ds)
            MERGE (t)-[:ARRIVES_AT {date: $arrival_date, time: $arrival_time}]->(as)
            """, data)
        print("Данные были добавлены в базу данных.")


def delete_train(driver, train_number, departure_station, platform_number):
    with driver.session() as session:
        if departure_station and platform_number:
            # Usuwanie pociągu z konkretnego peronu na określonej stacji
            query = """
                MATCH (t:Train {number: $train_number})-[:DEPARTS_FROM]->(p:Platform {number: $platform_number})-[:LOCATED_IN]->(s:Station {name: $departure_station})
                DETACH DELETE t
                RETURN count(t) as deletedCount
            """
        else:
            # Usuwanie wszystkich danych o pociągu
            query = """
                MATCH (t:Train {number: $train_number})
                DETACH DELETE t
                RETURN count(t) as deletedCount
            """

        result = session.run(query, train_number=train_number, departure_station=departure_station,
                             platform_number=platform_number).single()

        if result and result["deletedCount"] > 0:
            return True  # Zwraca True, jeśli pociąg został usunięty
        else:
            return False  # Zwraca False, jeśli żaden pociąg nie został usunięty


# Główna funkcja
if __name__ == '__main__':
    Neo4jApp().run()
