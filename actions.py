from typing import Any, Text, Dict, List, Union
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset, SlotSet
from scripts.google_books_api import main as gb

book_database = {
    'olga tokarczuk'        : ['flights', 
                                'plow over the bones of the dead'],
    'stephen king'          : ['the shining', 'the dome', 'it'],
    'george orwell'         : ['animal farm', '1984'],
    'hunter s thompson'     : ['fear and loving in las vegas'],
    'patty smith'           : ['just kids'],
    'oliver rey'            : ['when the world became figures']           
}

def check_library(library):

    libraries = ['majorna','angered','Stadsbiblioteket']
    if library not in libraries:
        return False
    else:
        return True

class ActionOpeningTimesLookup(Action):

    def name(self) -> Text:
        return "action_opening_times_lookup"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["library"]

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        libraries = {'majorna' : 'Majorna','angered' : 'Angered','stadsbiblioteket' : 'Stadsbiblioteket'}

        print(tracker.get_slot('library'))
        library = tracker.get_slot("library")
        library = library.lower()

        opening_times = {'majorna': 'Due to Covid, Majorna is closed until further notice',
                         'angered': 'Angered library is open 10-16 on Mondays, Wednesdays and Fridays,\n10-19 on Tuesdays and Thursdays,\n10-16 on Saturdays and closed on Sundays',
                         'stadsbiblioteket': 'Stadsbiblioteket is open 8-19.30 Monday to Friday,\nand 10-17 on Saturdays and Sundays'}

        if library not in libraries.keys():
            dispatcher.utter_message("We don't have oppening times {} for that or maybe you need to check your spelling".format(library.capitalize()))

        else:
            dispatcher.utter_message(opening_times[library])
            return [AllSlotsReset()]

class OpeningTimesForm(FormAction):

    def name(self) -> Text:
        return 'opening_times_form'

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["library"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            'library' : self.from_entity(entity='library', intent='inform_library')
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain : Dict[Text, Any],
            ) -> List[Dict]:
        dispatcher.utter_message(template="utter_affirm_library", library=tracker.get_slot('library').capitalize())
        return []

class BorrowEbooksForm(FormAction):

    def name(self) -> Text:
        return "borrow_ebooks_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["has_card", "operating_system"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"has_card" : [self.from_intent(intent="affirm", value=True),
                              self.from_intent(intent="negative", value=False)],

                "operating_system" : [self.from_intent(intent="read_mobile", value=True),
                                      self.from_intent(intent="read_pc", value=False)]}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        '''
        check if registered and has library library card
        if has_card == True:
            different options depending on operating system

        '''
        print(tracker.get_slot("has_card"))
        print(tracker.get_slot("operating_system"))

        if tracker.get_slot("has_card") == True:

            ''' user has a card'''

            if tracker.get_slot("operating_system") == True:
                #True = mobile
                dispatcher.utter_message("You can download the app Libby from Overdrive to download ebooks")

            elif tracker.get_slot("operating_system") == False:
                dispatcher.utter_message("You will have to download the app Libby on a mobile device")

        else:
            dispatcher.utter_message("If you are registered you can login with your Personummer and Pin code\nOtherwise you will have to come to the library with ID to register")
        return [AllSlotsReset()]

class BookLookupForm(FormAction):

    def name(self) -> Text:
        return "book_lookup_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["book_author", "book_title"]

    def slot_mappings(self):


        return {"book_author": [self.from_entity(entity="book_author"),
                             self.from_text()],
                "book_title": [self.from_entity(entity="book_title"),
                             self.from_text()]}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        print(tracker.get_slot("book_author"))
        print(tracker.get_slot("book_title"))

        return []

class ActionCheckQuery(Action):

    def name(self) -> Text:
        return "action_check_query"

   
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        book_author = False
        book_title = False

        slots = []

        prediction = tracker.latest_message

        entities = [(i['entity'], i['value']) for i in prediction['entities']]

        for entity in entities:

            if entity[0] == 'book_author':
                book_author = entity

            if entity[0] == 'book_title':
                book_title =entity

        if book_author and not book_title:
            dispatcher.utter_message("You are looking for books by {}".format(book_author[1]))
            slots.append(SlotSet('book_author',book_author[1]))

        elif book_author and book_title:
            dispatcher.utter_message("You are looking for {} by {}?".format(book_title[1],book_author[1]))
            slots.append(SlotSet('book_title',book_title[1]))

        elif book_title and not book_author:
            dispatcher.utter_message("You are looking for {}?".format(book_title[1]))
            slots.append(SlotSet('book_title',book_title[1]))

        elif not book_author and not book_title:
            dispatcher.utter_message("What??!")
            return [AllSlotsReset()]

        return slots

class ActionBookLookup(Action):

    def name(self) -> Text:
        return "action_book_lookup"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slot_values = tracker.current_slot_values()
        print(slot_values)

        slots = {}

        for key, value in slot_values.items():

            try:
                if value != None:
                    slots[key] = value
            except:
                continue
        
        print(slots)
        results, book_db = gb(slots)
        print(book_db)
        print(len(results))
        if len(results) < 1:
            dispatcher.utter_message("Hmm I don't think we have any results for that, Sorry :(")

        else:
            print("Running Book Lookup with slots {}".format(slots))
            dispatcher.utter_message("Here are a few results from our database")
            for i in results:
                dispatcher.utter_message('\nBook Title: {}\nBook Author: {}\nISBN: {}'.format(i[0], i[1], i[2]))
        
                #dispatcher.utter_message("Here are a few results from our database\n{}".format(results))

            dispatcher.utter_message("If you would like to know more about a book type in the ISBN number :)")

            return [SlotSet("mini_bookdb", book_db)]

        '''

        then informing the user 

        '''


class BookDescription(Action):

    def name(self) -> Text:
        return "action_book_description"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('Description Lookup')
        book_db = tracker.get_slot('mini_bookdb')

        isbn = tracker.latest_message['entities'][0]['value']
        print(isbn)
        dispatcher.utter_message("Description of the book from Google: {}".format(book_db[isbn]['description']))


        return [AllSlotsReset()]