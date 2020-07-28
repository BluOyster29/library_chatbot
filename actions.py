from typing import Any, Text, Dict, List, Union
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset

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

        opening_times = {'majorna': 'Due to Covid, Majorna is closed until further notice',
                         'angered': 'Angered library is open 10-16 on Mondays, Wednesdays and Fridays,\n10-19 on Tuesdays and Thursdays,\n10-16 on Saturdays and closed on Sundays',
                         'stadsbiblioteket': 'Stadsbiblioteket is open 8-19.30 Monday to Friday,\nand 10-17 on Saturdays and Sundays'}

        if library not in libraries.keys():
            dispatcher.utter_message("We don't have oppening times for that or maybe you need to check your spelling")

        else:
            dispatcher.utter_message(opening_times[library.lower()])
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
        dispatcher.utter_message(template="utter_affirm_library", library=tracker.get_slot('library'))
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
