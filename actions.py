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

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain : Dict[Text, Any],
            ) -> List[Dict]:
        dispatcher.utter_message(template="utter_affirm_library", library=tracker.get_slot('library'))
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            'library' : self.from_entity(entity='library', intent='inform_library')
        }
