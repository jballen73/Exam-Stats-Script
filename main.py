import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
import re
import converter

class FloatInput(TextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)

class IntInput(TextInput):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat

        s = re.sub(pat, '', substring)
        return super(IntInput, self).insert_text(s, from_undo=from_undo)

class NamePopupView(GridLayout):
    def __init__(self, **kwargs):
        super(NamePopupView, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Section Name:"))
        self.section_name = TextInput(multiline=False, halign='center')
        self.add_widget(self.section_name)
        self.add_widget(Label(text="Number of People in Section:"))
        self.section_size = IntInput(multiline=False, halign='center')
        self.add_widget(self.section_size)
        self.create_button = Button(text="Create")
        self.add_widget(self.create_button)
        self.dismiss_button = Button(text="Cancel")
        self.add_widget(self.dismiss_button)

    def bind_buttons(self, self_popup, main_popup, main_popup_view):
        self.self_popup = self_popup
        self.main_popup = main_popup
        self.main_popup_view = main_popup_view
        self.dismiss_button.bind(on_press=self.dismiss_and_clear)
        self.create_button.bind(on_press=self.dismiss_and_create)

    def dismiss_and_create(self, *args):
        # self.self_popup.bind(on_dismiss=self.main_popup.open)
        self.main_popup_view.set_name_and_size(self.section_name.text, self.section_size.text)
        self.section_name.text = ''
        self.section_size.text = ''
        self.self_popup.dismiss()
        self.main_popup.open()

    def dismiss_and_clear(self, *args):
        self.section_name.text = ''
        self.section_size.text = ''
        self.self_popup.dismiss()

class FileNamePopupView(GridLayout):
    def __init__(self, **kwargs):
        super(FileNamePopupView, self).__init__()
        self.cols = 1
        self.add_widget(Label(text="Enter file name (no extension)"))
        self.filename = TextInput(multiline=False)
        self.add_widget(self.filename)
        self.eval_button = Button(text="Evaluate")
        self.add_widget(self.eval_button)
        self.cancel_button = Button(text="Cancel")
        self.add_widget(self.cancel_button)

        self.popup = None
        self.comps_view = None

        self.eval_button.bind(on_press=self.run_eval)
        self.cancel_button.bind(on_press=self.close)

    def bind_comps_view(self, view):
        self.comps_view = view

    def bind_popup(self, popup):
        self.popup = popup

    def run_eval(self, *args):
        if self.filename.text != "":
            self.comps_view.set_name(self.filename.text + ".txt")
            self.filename.text = ''
            self.popup.dismiss()
            self.comps_view.publish_comps()

    def close(self, *args):
        self.filename.text = ''
        self.popup.dismiss()



class CompsPopupView(GridLayout):
    def __init__(self, **kwargs):
        super(CompsPopupView, self).__init__()
        self.versions = kwargs['versions']
        self.cols = len(self.versions)
        self.create_label("Group 1")
        self.create_button_labels()


        self.group1_buttons = []
        for version in self.versions:
            checkbox = CheckBox()
            self.group1_buttons.append(checkbox)
            self.add_widget(checkbox)
        self.create_label("Group 2")
        self.create_button_labels()
        self.group2_buttons = []
        for version in self.versions:
            checkbox = CheckBox()
            self.group2_buttons.append(checkbox)
            self.add_widget(checkbox)

        self.add_button = Button(text="Add Comparison")
        self.add_widget(self.add_button)

        self.eval_button = Button(text="Evaluate")
        self.add_widget(self.eval_button)

        self.close_button = Button(text="Close")
        self.add_widget(self.close_button)

        self.comps = []
        self.main_view = None
        self.popup = None
        self.filename = "default.txt"

    def create_label(self, text):
        for i in range(self.cols):
            if i == self.cols // 2:
                self.add_widget(Label(text=text))
            else:
                self.add_widget(Label())

    def create_button_labels(self):
        for version in self.versions:
            self.add_widget(Label(text=version))

    def bind_buttons(self, popup):
        self.close_button.bind(on_press=popup.dismiss)
        self.eval_button.bind(on_press=self.create_filename_popup)
        self.add_button.bind(on_press=self.add_comp)

    def bind_main_view(self, view):
        self.main_view = view

    def bind_popup(self, popup):
        self.popup = popup

    def extract_comps(self):
        comp_1 = ""
        comp_2 = ""
        for i in range(len(self.versions)):
            version_name = self.versions[i]
            if self.group1_buttons[i].active:
                comp_1 += version_name + "+"
            if self.group2_buttons[i].active:
                comp_2 += version_name + "+"
        return (comp_1[:-1], comp_2[:-1])

    def add_comp(self, *args):
        comp = self.extract_comps()
        self.comps.append(comp)
        for button in self.group1_buttons:
            button.active = False
        for button in self.group2_buttons:
            button.active = False

    def publish_comps(self, *args):
        self.main_view.set_comps(self.comps)
        self.main_view.set_name(self.filename)
        self.popup.dismiss()
        self.main_view.run_evaluation()

    def set_name(self, name):
        self.filename = name

    def create_filename_popup(self, *args):
        filename_popup_view = FileNamePopupView()
        filename_popup = Popup(title="Enter Filename", content=filename_popup_view, size_hint=(.4,.3))
        filename_popup_view.bind_popup(filename_popup)
        filename_popup_view.bind_comps_view(self)
        filename_popup.open()

    def print_comp(self, *args):
        print(self.comps)

class AppView(GridLayout):
    def __init__(self, **kwargs):
        super(AppView, self).__init__(**kwargs)
        self.cols = 1
        self.popup_button = Button(text="Add New Version")
        self.add_widget(self.popup_button)
        self.print_button = Button(text="Evaluate")
        # self.print_button.bind(on_press=self.print_contents)
        self.print_button.bind(on_press=self.run_evaluation)
        # self.add_widget(self.print_button)
        self.questions = []
        self.scores = {}
        self.versions = []
        self.comps = []
        self.filename = "default.txt"

        self.comps_button = Button(text="Select Comparisons")
        self.add_widget(self.comps_button)
        self.comps_button.bind(on_press=self.create_and_open_comps)



    def bind_popup(self, popup):
        self.popup_button.bind(on_press=popup.open)

    def print_contents(self, *args):
        print(self.scores)
        print(self.questions)

    def run_evaluation(self, *args):
        converter.convert_gui_output_to_fullstatistics(self.scores, self.questions, self.comps, self.filename)

    def update_data(self, dict, list, name, size):
        self.scores[(name, size)] = dict
        self.questions = list
        self.versions.append(name)

    def create_and_open_comps(self, *args):
        versions_kwargs = {'versions': self.versions}
        comps_view = CompsPopupView(**versions_kwargs)
        comps_popup = Popup(title="Select Comparisons", content=comps_view, size_hint=(.75, .75))
        comps_view.bind_buttons(comps_popup)
        comps_view.bind_main_view(self)
        comps_view.bind_popup(comps_popup)
        comps_popup.open()

    def set_comps(self, comps):
        for comp in comps:
            if comp not in self.comps:
                self.comps.append(comp)

    def set_name(self, name):
        self.filename = name


class PopupView(GridLayout):

    def __init__(self, **kwargs):
        super(PopupView, self).__init__(**kwargs)
        self.cols = 3
        self.add_widget(Label(text="Question Name"))
        self.add_widget(Label(text="Mean"))
        self.add_widget(Label(text="Standard Deviation"))
        self.add_line_button = Button(text="Add Question")
        self.add_widget(self.add_line_button)
        self.add_line_button.bind(on_press=self.add_line)
        self.submit_button = Button(text="Submit")
        self.add_widget(self.submit_button)
        self.close_button = Button(text="Close")
        self.add_widget(self.close_button)


    def bind_buttons(self, popup):
        self.popup = popup
        self.close_button.bind(on_press=self.clear_scores_and_close)
        self.submit_button.bind(on_press=self.dump_and_submit)




    def add_line(self, *args):
        self.add_widget(TextInput(multiline=False, readonly=False), index=3)
        self.add_widget(FloatInput(multiline=False), index=3)
        self.add_widget(FloatInput(multiline=False), index=3)

    def configure_storage(self, view):
        self.view = view

    def dump_text(self, *args):
        text_views = self.children[:-3]

        dict = {}
        list = []
        for i in range(len(text_views) - 1, 3, -3):
            question_view = text_views[i]
            score_view = text_views[i - 1]
            std_view = text_views[i - 2]
            if question_view.text == '':
                continue
            elif score_view.text == '':
                list.append(question_view.text)
                continue
            else:
                dict[question_view.text] = (score_view.text,std_view.text)
                list.append(question_view.text)
                question_view.readonly = True
                score_view.text = ''
                std_view.text = ''
        self.view.update_data(dict, list, self.name, self.section_size)

    def dump_and_submit(self, *args):
        self.dump_text()
        self.popup.dismiss()

    def clear_scores_and_close(self, *args):
        text_views = self.children[:-6]
        for i in range(len(text_views) - 1, 0, -3):
            question_view = text_views[i]
            score_view = text_views[i-1]
            std_view = text_views[i-2]
            score_view.text = ''
            std_view.text = ''
        self.popup.dismiss()

    def set_name_and_size(self, name, size):
        self.name = name
        self.section_size = size

class StatsApp(App):
    '''
    def build_config(self, config):
        config.setdefaults('section1', {"key":"hello"})


    def build_settings(self, settings):
        jsondata = """[
                    {"type": "title",
                    "title":"Test Application"},
                    {"type": "options",
                    "title": "My first key",
                    "desc":"Key description",
                    "section":"section1",
                    "key":"key",
                    "options": ["value1", "value2", "value3"]}
        ]"""
        settings.add_json_panel('Test Application', self.config, data=jsondata)
'''




    def build(self):
        # config = self.config
        # self.title = config.get('section1', 'key2')
        popup_content = PopupView()
        popup = Popup(title="Version Submission", content=popup_content)
        main_view = AppView()


        popup_content.bind_buttons(popup)



        popup_content.configure_storage(main_view)

        name_popup_view = NamePopupView()
        name_popup = Popup(title="Enter version name", content=name_popup_view, size_hint=(.5,.5))
        name_popup_view.bind_buttons(name_popup, popup, popup_content)
        main_view.bind_popup(name_popup)
        return main_view

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            if token == ("section1", "key"):
                self.title = value
                print("Key has been changed to ", value)



if __name__ == '__main__':
    StatsApp().run()