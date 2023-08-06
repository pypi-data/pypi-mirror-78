# Standard Library
from dataclasses import dataclass, field
from typing import Tuple, Union, List
import datetime as dt
import ast # For safely evaluating a string containing a Python literal

# Thrid Party
import pandas as pd

@dataclass(frozen=True)
class Course():
    cid: str
    title: str
    organization: str
    hw_code_name: str
    highlight_types: Tuple[str]
    agendas: dict = field(default_factory=dict)
    ####sections: dict = field(default_factory=dict)
    notices: pd.DataFrame = pd.DataFrame(columns=['subterm', 'date', 'message'])

    @classmethod
    def from_excel(cls, filename: str) -> object:
        """Constructs a course and its sections from an Excel workbook."""

        # Append '.xlsx' if necessary
        if isinstance(filename, str):
            if '.xlsx' not in filename:
                filename += '.xlsx'
        else:
            raise ValueError("The filename must be a string naming an Excel workbook.")

        # Load the data
        xls = pd.read_excel(filename, sheet_name=None)

        ##### Make a dictionary of sections keyed by sid
        ####sections = Sections.from_df(xls['sections'])

        # Read the course arguments
        cid, title, organization, hw_code_name, agenda_sheets, types_order, highlight_types = xls['course'].iloc[0]
        # Convert strings to tuples
        agenda_sheets = ast.literal_eval(agenda_sheets)
        types_order = ast.literal_eval(types_order)
        highlight_types = ast.literal_eval(highlight_types)
        # Make a dictionary of agendas keyed by the number of days in the agenda
        agendas = {}
        for agenda in agenda_sheets:
            data = xls[agenda]
            ######## 20200603 Trying to prevent the reording of the adgenda by section
            # Sort the rows by 'day' and 'types_order'
            ##if types_order is not None:
            ##    data['type'] = pd.Categorical(data['type'], types_order, ordered=True)
            ##    data.sort_values(['day', 'type'], inplace=True)
            ##else:
            ##    data.sort_values('day', inplace=True)
            num_of_days = data['day'].max()
            agendas[num_of_days] = data

        # Create the course
        course = cls(
            cid,
            title,
            organization,
            hw_code_name,
            highlight_types,
            agendas=agendas,
            ####sections = sections,
            notices=xls['notices'],
        )

        return course

@dataclass(frozen=True)
class Section():
    """Container for information about a section of a course."""

    sid: str
    crn: str
    hw_code: str
    room: str
    subterm: str
    days: Tuple[int] # 0 is 'Monday', 6 is 'Sunday'
    start_time: object
    end_time: object
    break_minutes: int
    instructor: str

    @property
    def meeting_minutes(self):
        """The total mintutes available during each meeting."""

        start = dt.datetime.combine(dt.date(2000, 1, 1), self.start_time)
        end = dt.datetime.combine(dt.date(2000, 1, 1), self.end_time)
        duration = pd.Timedelta(end - start - self.break_minutes)
        temp = duration.total_seconds()/60
        minutes = int(temp)
        return minutes

    @property
    def meeting_times(self):
        """The weekdays and times of meetings."""

        day_names = {
            0:'Monday',
            1:'Tuesday',
            2:'Wednesday',
            3:'Thursday',
            4:'Friday',
            5:'Saturday',
            6:'Sunday'
        }
        days = ' and '.join([day_names[i] for i in self.days])
        start_time = self.start_time.strftime("%I:%M %p")
        end_time = self.end_time.strftime("%I:%M %p")
        return f'{days} from {start_time} to {end_time}'

    @staticmethod
    def get_xls(filename: str) -> object:
        """Returns an Excel workbook as a dictionary of Pandas dataframes."""

        # Append '.xlsx' if necessary
        if isinstance(filename, str):
            if '.xlsx' not in filename:
                filename += '.xlsx'
        else:
            raise ValueError("The filename must be a string naming an Excel workbook.")

        # Load the data
        xls = pd.read_excel(filename, sheet_name=None)

        return xls

    @classmethod
    def from_excel(cls, filename: str) -> dict:
        """Constructs a dictionary of sections, keyed by the section.ids, from an Excel workbook."""

        # Load the data
        xls = cls.get_xls(filename)

        # Make a dictionary of sections keyed by sid
        sections = cls.from_df(xls['sections'])

        return sections

    @classmethod
    def from_ivy(cls, filename: str) -> dict:
        """Constructs a dictionary of sections, keyed by the section.ids, from an Ivy Tech formatted Excel workbook."""

        # Load the data
        xls = cls.get_xls(filename)
        old_df = xls['sections']

        old_names = ['Section ID', 'CRN', 'hw_code', 'Sub Academic Period', 'Days', 'Time', 'break_minutes', 'Building', 'Room', 'Instructor Name']
        new_df = pd.DataFrame(columns=['sid', 'crn', 'hw_code', 'subterm', 'days', 'start_time', 'end_time', 'break_minutes', 'room', 'instructor'])
        for i, row in old_df[old_names].iterrows():
            # Get the row values
            [sid, crn, hw_code, subterm, days, start_end_time, break_minutes, building, room, instructor] = row.to_list()

            # Translate the subterm names
            rewrite_ivyterm = {
                '1st 8wk Monday': '1st 8-Weeks',
                '1st 8wk Tuesday': '1st 8-Weeks',
                '2nd 8wk Monday': '2nd 8-Weeks',
                '2nd 8wk Tuesday': '2nd 8-Weeks',
                'Standard Term' : '16-Weeks',
            }
            subterm = rewrite_ivyterm[subterm]

            # Get the start and end times
            start_end = start_end_time.split('-')
            start_time, end_time = pd.to_datetime(start_end)

            # Translate the building names to room prefixes
            rewrite_ivybuilding = {
                'Greencastle Campus' : '',
                'Noblesville/Hamilton County' : 'NOBLE',
                'Avon' : 'AVON',
                'North Meridian Center' : 'NMC',
                'Illinois Fall Creek Center' : 'IFC',
                'R M Fairbanks Cntr for Hlth Pr' : ''
            }
            # Format the room names
            building = rewrite_ivybuilding[building]
            room = building + ' ' + str(room)

            # Replace missing instructors names with 'TBD'
            if pd.isnull(instructor):
                instructor = 'TBD'

            # Add the properly formated row
            new_df.loc[i] = [sid, crn, hw_code, subterm, days, start_time, end_time, break_minutes, room, instructor]

        # Make a dictionary of sections keyed by sid
        sections = cls.from_df(new_df)

        return sections

    @classmethod
    def from_df(cls, df: object) -> dict:
        """Constructs a dictionary of sections keyed by the section.ids from a Pandas dataframe."""

        sections = {}
        for index, section_series in df.iterrows():
            sid = section_series['sid']
            sections[sid] = cls.from_series(section_series)

        return sections

    @classmethod
    def from_series(cls, series: object) -> object:
        """Constructs a section from a Pandas series."""

        # Convert strings like 'MW' to (0, 2)
        day_index = {
            'M':0,
            'T':1,
            'W':2,
            'R':3,
            'F':4,
            'S':5,
            'Su':6
        }
        day_indices = [day_index[char] for char in series['days']]
        days = tuple(day_indices)

        # Convert break_minutes to a Timedelta object
        break_minutes = pd.Timedelta(series['break_minutes'], unit='m')

        section = cls(
            sid = series['sid'],
            crn = series['crn'],
            hw_code = series['hw_code'],
            room = series['room'],
            subterm = series['subterm'],
            days = days,
            start_time = series['start_time'],
            end_time = series['end_time'],
            break_minutes = break_minutes,
            instructor = series['instructor'],
        )

        return section