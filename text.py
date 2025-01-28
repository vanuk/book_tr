from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from googletrans import Translator
import PyPDF2
from plyer import filechooser

# Клас екрану
class MainScreen(Screen):
    pass

KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:  # Використовуємо MDTopAppBar замість MDToolbar
            title: "Book Translator"
            elevation: 10
            pos_hint: {"top": 1}

        MDRectangleFlatButton:
            text: "Load PDF"
            pos_hint: {"center_x": 0.5}
            on_release: app.load_pdf()

        ScrollView:
            MDTextField:
                id: text_box  # Це ID для доступу до текстового поля
                hint_text: "Text from PDF will appear here..."
                multiline: True
                size_hint_y: None
                height: 400
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                on_selection_text: app.on_text_selected(args[1])

        MDLabel:
            id: translation_label
            text: ""
            halign: "center"
'''

class BookTranslatorApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def load_pdf(self):
        """Load PDF and display text."""
        file_path = filechooser.open_file(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            with open(file_path[0], "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = "".join(page.extract_text() for page in reader.pages)
            # Оновлений доступ до text_box через self.root.get_screen('main').ids
            text_box = self.root.get_screen('main').ids.text_box  # Оновлений доступ
            text_box.text = text

    def on_text_selected(self, selection):
        """Функція для обробки вибору тексту."""
        if selection:
            self.translate_selected_word(selection)

    def translate_selected_word(self, word):
        """Translate selected word using Google Translate."""
        if word:
            translator = Translator()
            translation = translator.translate(word, src='en', dest='uk')
            # Оновлений доступ до translation_label
            self.root.get_screen('main').ids.translation_label.text = f"Переклад: {translation.text}"
        else:
            self.root.get_screen('main').ids.translation_label.text = "Please select a word."

if __name__ == '__main__':
    BookTranslatorApp().run()
