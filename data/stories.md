## talk to a human
* greet
- utter_greet
- utter_what_can_do
* speak_to_human
- utter_passing_to_human

## opening times happy
* greet
 - utter_greet
 - utter_what_can_do
* opening_times
 - opening_times_form
 - form{"library" : "opening_times_form"}
 - form{"library" : null}
* affirm
 - action_opening_times_lookup
* thanks
 - utter_your_welcome

## opening times one-shot
 * greet
  - utter_greet
  - utter_what_can_do
 * opening_times
  - action_opening_times_lookup
 * thanks
  - utter_your_welcome
