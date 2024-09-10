from aqt import QAction, QFileDialog, mw
from aqt.utils import showWarning, tooltip, showInfo
from collections import Counter
from aqt.gui_hooks import browser_will_show_context_menu
import re

# Context to all tooltips
global header
header = "Listening generator: "

def testCardSelect(card_ids):
    try  :
        card_ids[0]
    except :
        tooltip(header + """please select at least one card.""")
        return True
    
def getUniqueCharacters(card_ids, chineseOnly = False):
    unique_characters = set()
    for cid in card_ids:
        note = mw.col.get_note(mw.col.get_card(cid).nid)
        if "Hanzi" in note:
            unique_characters.update(note["Hanzi"])
    if chineseOnly:
        chinese_characters = {char for char in unique_characters if re.match(r'[\u4e00-\u9fff]', char)}
        unique_characters = chinese_characters
    return unique_characters

def list_unique_characters(browser):

    # Get the selected notes
    selected_cards = browser.selectedCards()

    # Check if any cards are selected
    if testCardSelect(selected_cards): return

    unique_characters = getUniqueCharacters(selected_cards, chineseOnly=True)

    file_path, _ = QFileDialog.getSaveFileName(browser, "Save Unique Characters", "", "Text Files (*.txt);;All Files (*)")
    if not file_path:
        tooltip(header + "No file selected.")
        return
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(",".join(unique_characters))
        tooltip(header + f"{len(unique_characters)} unique Chinese characters saved to {file_path}")
    
# Create a new menu item
def on_context_menu(browser, menu):
    action = QAction("List and save unique characters", browser)
    action.triggered.connect(lambda _, b=browser: list_unique_characters(b))
    menu.addAction(action)

browser_will_show_context_menu.append(on_context_menu)