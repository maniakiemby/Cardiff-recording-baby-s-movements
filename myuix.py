from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class TitleCurrentDateWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(TitleCurrentDateWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, .25)
        self.size = (400, 25)
        self.spacing = 30

class ButtonToday(Button):
    def __init__(self, **kwargs):
        super(ButtonToday, self).__init__(**kwargs)
        self.size_hint = (.4, .5)
        self.pos_hint = {'top': .75}
        self.text = 'Dziś'


class CancelButtonDate(Button):
    def __init__(self, **kwargs):
        super(CancelButtonDate, self).__init__(**kwargs)
        self.size_hint = (.4, .5)
        self.pos_hint = {'top': .75}
        self.text = 'Anuluj'


class SelectorMonthsWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(SelectorMonthsWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, .25)
        self.padding = 10
        self.spacing = 30

class SelectorMonthsLabel(Label):
    def __init__(self, **kwargs):
        super(SelectorMonthsLabel, self).__init__(**kwargs)
        self.font_size = 100
        self.pos = (1, 1)


class SelectorMonthsButtonPrevious(Button):
    def __init__(self, **kwargs):
        super(SelectorMonthsButtonPrevious, self).__init__(**kwargs)
        self.text = '<'
        self.size_hint = (.2, .5)
        self.pos_hint = {'top': .75}


class SelectorMonthsButtonNext(SelectorMonthsButtonPrevious):
    def __init__(self, **kwargs):
        super(SelectorMonthsButtonNext, self).__init__(**kwargs)
        self.text = '>'


class CalendarLayoutWidget(GridLayout):
    def __init__(self, **kwargs):
        super(CalendarLayoutWidget, self).__init__(**kwargs)
        # self.row_force_default = True
        # self.row_default_height = 100


class CalendarButtonDay(Button):
    def __init__(self, index: int, **kwargs):
        super(CalendarButtonDay, self).__init__(**kwargs)
        self.id = index
        # self.size_hint = (.15, .15)
        # self.size = (100,100)