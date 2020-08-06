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
 - form{"name" : "opening_times_form"}
 - form{"name" : null}
* affirm
 - action_opening_times_lookup
* thanks
 - utter_your_welcome
 - utter_more_help
* deny
 - utter_goodbye

## borrow ebooks
* greet
 - utter_greet
 - utter_what_can_do
* borrow_ebooks
 -utter_download_ebook
* affirm
 - borrow_ebooks_form
 - form{"name" : "borrow_ebooks_form"}
 - form{"name": null}

## how many ebooks
* greet
  - utter_greet
  - utter_what_can_do
* how_many
 - utter_how_many_ebooks
* thanks
 - utter_your_welcome

## how switch libby language
* greet
 - utter_greet
 - utter_what_can_do
* change_libby_language
 - utter_instructions_in_english

## book lookup happy
* greet
 - utter_greet
 - utter_what_can_do
* open_request
 - action_check_query
* affirm
 - action_book_lookup
* inform_isbn
 - action_book_description
 