import questionary
from questionary import Style
from questionary import Validator, ValidationError, prompt

custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    # ('answer', 'fg:#f44336 bold'),      # submitted answer text behind the question
    ('answer', 'fg:#57a8ff bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#673ab7 bold'),     # pointer used in select and checkbox prompts
    # ('highlighted', 'fg:#673ab7 bold'), # pointed-at choice in select and checkbox prompts
    ('highlighted', 'fg:#7000A9 bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#cc5454'),         # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', 'fg:#808080 italic'),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])
custom_menu_style = Style([
    ('qmark', 'fg:#b28df2 bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#ff5757 bold'),      # submitted answer text behind the question
    # ('answer', 'fg:#039300 bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#b28df2 bold'),     # pointer used in select and checkbox prompts
    # ('highlighted', 'fg:#673ab7 bold'), # pointed-at choice in select and checkbox prompts
    ('highlighted', 'fg:#e69532 bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#cc5454'),         # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', 'fg:#808080 italic'),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])
	
def ask_select(message: str, choices: list, return_index: bool):

	answer = questionary.select(
    f"{message}",
    qmark="",
    instruction="use arrow keys and <enter> to select",
    style=custom_menu_style,
    choices=choices,
	).ask()

	if return_index:
		for i, choice in enumerate(choices):
			if answer == choice:
				return(i)
	else:
		return answer
	
def ask_checkbox(message: str, choices: list, return_index: bool):
	answer = questionary.checkbox(
	f"{message}",
	qmark="",
    style=custom_menu_style,
	choices=choices
	).ask()

	return_list = []

	if return_index:
		for option in answer:
			for i, choice in enumerate(choices):
				if option == choice:
					return_list.append(i)
		return return_list
	else:
		return answer

def ask_text(message: str):
	return questionary.text(message,qmark="",style=custom_style).ask()

def ask_name(message: str):
	return questionary.text(
	message,
	instruction="\ntype new name and press <enter>, or press <enter> to cancel\n",
	qmark="",
	style=custom_style
	).ask()

def print_error(message: str):
	return questionary.print(message, style="fg:#C00000 bold")

def print_hint(message: str):
	return questionary.print(message, style='fg:#808080 italic')

def print_return():
	return questionary.print("\nreturning to main menu", style="fg:#808080 italic")