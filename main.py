import os
# import platform
from subprocess import Popen
import webbrowser
from datetime import datetime, date, time, timedelta
import threading
from dateutil.relativedelta import relativedelta
import calendar

import kivy
from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.utils import platform
import openpyxl

from myuix import (TitleCurrentDateWidget, ButtonToday, CancelButtonDate, SelectorMonthsWidget, SelectorMonthsLabel,
    SelectorMonthsButtonPrevious, SelectorMonthsButtonNext, CalendarLayoutWidget, CalendarButtonDay
                   )


kivy.require('2.1.0')
__version__ = '0.1'


class Cardiff(GridLayout):
    def __init__(self, **kwargs):
        super(Cardiff, self).__init__(**kwargs)
        self.work_notebook = WorkNotebook()


class WorkNotebook:
    def __init__(self):
        self.path = 'CardiffWorkNotebook.xlsx'
        self.wb_obj = openpyxl.load_workbook(self.path)
        self.sheet_obj = self.wb_obj.active

        self._start_date = None  # pierwsze okienko C4
        self.last_cell = None  # for recovering

    @property
    def _start_date(self):
        return self.__start_date

    @_start_date.setter
    def _start_date(self, value):
        cell_obj = self.sheet_obj.cell(row=30, column=14)
        self.__start_date = cell_obj.value

    def print_cardiff_notebook(self):
        # date_picker = DatePicker()
        # current_app = App.get_running_app()
        # current_app.popup = ModalView(size_hint=(None, None),
        #                       size=(Window.width - 25, Window.height / 1.2),
        #                       auto_dismiss=True,
        #                       on_dismiss=self.grab_date
        #                       )
        # current_app.popup.add_widget(date_picker)
        # current_app.save_data = True
        # current_app.popup.open()

        if platform == 'windows':
            os.startfile(self.path)

        if platform == 'linux':
            # f = os.path.join('temp', self.path)
            Popen(['localc', self.path])

        if platform == 'android':
            filepath = os.path.join(os.getcwd(), self.path)
            print(filepath)
            webbrowser.open_new(f"ms-excel:ofv|u|{filepath}")

        else:
            pass
            # otwórz powiadomienie, bądź znajdź jeszcze inne roziwązanie. (np. wyślij plik emailem)

    # https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
    # https://stackoverflow.com/questions/49856502/kivy-listview-excel-file
    # otwiera excel: https://www.reddit.com/r/kivy/comments/rvq15j/how_to_launch_an_excel_file_in_android_using/

    def grab_date(self, *args):
        current_app = App.get_running_app()
        if current_app.save_data:
            # dodaj funkcjonalność pobierającą datę
            # self.task_date_of_performance.text = app.popup.date_picker.selected_date
            pass

    def change_value_in_cell(self, row: int, column: int, value: str):
        self.sheet_obj.cell(row=row, column=column, value=value)
        self.wb_obj.save(self.path)

    def which_column(self) -> int:
        delta = datetime.today() - self._start_date

        return delta.days

    @staticmethod
    def which_row() -> int:
        time_now = datetime.now().time()
        delta_time_now = timedelta(hours=time_now.hour, minutes=time_now.minute)
        # the time we start each day
        time_at_begin = time().fromisoformat('09:00')
        delta_time_at_begin = timedelta(hours=time_at_begin.hour, minutes=time_at_begin.minute)
        delta_time_from_begin = delta_time_now - delta_time_at_begin

        # change seconds to minutes and how many half-hour intervals occurred
        return int(delta_time_from_begin.seconds / 60 // 30) + 1

    def get_cell(self, *args):
        row = self.which_row()
        column = self.which_column()
        # table position correction
        row += 3
        column = column + 3
        print(row, column)
        return row, column

    def add_move(self, *args):
        cell = self.get_cell()
        self.last_cell = cell
        row, column = cell
        self.change_value_in_cell(row=row, column=column, value='x')

    def add_move_with_another_hour(self, *args):
        pass

    def remove_move(self, *args):
        if self.last_cell:
            row, column = self.last_cell
            self.change_value_in_cell(row=row, column=column, value='')


class DatePicker(GridLayout):
    def __init__(self, date_value=date.today(), **kwargs):
        super(DatePicker, self).__init__(**kwargs)
        self.selected_date = date_value

        self.head = TitleCurrentDateWidget()
        head_date = self.head_date_format()
        self.head_label = Label(text=head_date, font_size=100)
        self.head.add_widget(self.head_label)
        self.today = ButtonToday(on_release=self.set_today)
        self.head.add_widget(self.today)
        self.cancel_button = CancelButtonDate(on_release=self.cancel)
        self.head.add_widget(self.cancel_button)
        self.add_widget(self.head)

        self.selector_months_widget = SelectorMonthsWidget()
        selected_month_str = self.month_format()
        self.selector_months_label = SelectorMonthsLabel(text=selected_month_str)
        self.selector_months_widget.add_widget(self.selector_months_label)
        self.selector_months_widget.add_widget(
            SelectorMonthsButtonPrevious(on_press=self.go_previous_month)
        )
        self.selector_months_widget.add_widget(
            SelectorMonthsButtonNext(on_press=self.go_next_month)
        )
        self.add_widget(self.selector_months_widget)

        self.calendar_days = self.display_calendar()
        self.add_widget(self.calendar_days)

    def cancel(self, *args):
        pass

    def head_date_format(self):
        return self.selected_date.strftime('%d/%m/%Y')

    def set_today(self, *args):
        self.clear_widgets()
        self.__init__()

    def month_format(self):
        month_names = ['Styczeń',
                       'Luty',
                       'Marzec',
                       'Kwiecień',
                       'Maj',
                       'Czerwiec',
                       'Lipiec',
                       'Sierpień',
                       'Wrzesień',
                       'Październik',
                       'Listopad',
                       'Grudzień'
                       ]
        _format = '{} {}'.format(month_names[self.selected_date.month - 1], self.selected_date.year)

        return _format

    def display_calendar(self):
        calendar_days = CalendarLayoutWidget()
        days = ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'So', 'Nd']
        for day in days:
            name_of_the_day = Label(text=day)
            calendar_days.add_widget(name_of_the_day)

        monthrange = calendar.monthrange(self.selected_date.year, self.selected_date.month)
        first_day_month = monthrange[0]
        days_in_month = monthrange[1]

        _id = 0
        for number in range(days_in_month):
            while first_day_month > _id:
                day = Label(text='')
                calendar_days.add_widget(day)
                _id += 1
            day = CalendarButtonDay(text=str(number + 1), index=(number + 1))
            day.bind(on_release=self.change_date)
            calendar_days.add_widget(day)

        return calendar_days

    def go_previous_month(self, *args):
        self.selected_date = self.selected_date + relativedelta(months=-1)
        self.refresh_month()

    def go_next_month(self, *args):
        self.selected_date = self.selected_date + relativedelta(months=+1)
        self.refresh_month()

    def change_date(self, *args):
        day = args[0].id
        self.selected_date = self.selected_date + relativedelta(day=day)

        head_date = self.head_date_format()
        self.head_label.text = head_date

    def refresh_month(self):
        selected_month_str = self.month_format()
        self.selector_months_label.text = selected_month_str

        self.remove_widget(self.calendar_days)
        self.calendar_days = self.display_calendar()
        self.add_widget(self.calendar_days)


class MyApp(App):
    def build(self):
        Window.clearcolor = (151 / 255, 152 / 255, 164 / 255)
        return Cardiff()


if __name__ == '__main__':
    app = MyApp()
    app.run()
