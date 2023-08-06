# Standard Library
from datetime import datetime # Try to replace this with Pandas
# For the Topics() class
from typing import Tuple, Union, List

# Third Party
## For the main document
from pylatex import Document, LongTable, MultiColumn
from pylatex.base_classes import Command
from pylatex.utils import bold
## For the header and footer
from pylatex import PageStyle, Head, Foot, LineBreak, FootnoteText
# For the Topics() class
from pylatex import Itemize, Package
from pylatex.base_classes import Options
import pandas as pd
## For creating the timestamp in the footer
from pytz import timezone # Try to replace this with Pandas
# The itemize environment inside of the longtable automatically
# inserts \parskip before and after the list. I cannot figure out
# how to suppress this behavior. My hacky solution is to overload
# the Topics.dumps() method to insert \vspace{-1em} before and after
# the list. UnsafeCammand and Arguments are required for negative
# lengths because pylatex escapes the '-' symbol.
from pylatex.base_classes import UnsafeCommand, Arguments

# Local
from rewrite import tex


def generate_schedules(
    term,
    course,
    sections,
    clean_tex=True
):
    """Generate schedules for sections of a course in PDF format."""

    for section in sections.values():
        filename = f'{term.name} {course.cid}-{section.sid} Schedule'
        print(f'Generating {filename}.pdf')

        # Create the pylatex.Document object
        geometry_options = {
            "left": "0.5in",
            "right": "0.5in",
            "top": "1.5in",
            "bottom": "1in",
            "headheight":"1in"
        }
        doc = Document(document_options='11pt', page_numbers=False, geometry_options=geometry_options)

        # Create the header and footer
        headfoot = get_headfoot(term, course, section)
        doc.preamble.append(headfoot)
        doc.change_document_style(headfoot.name)

        # Set the default values for all itemize environments
        doc.append(Command('setlist', f'wide, nolistsep, noitemsep, nosep'))
        # Generate schedule table
        with doc.create(LongTable("| l  p{4.9in}  r |", row_height=1.4, booktabs=False)) as schedule:
            # Create the table header
            schedule.add_hline()
            schedule.add_row([
                bold('Date'),
                bold('Topics'),
                bold('Highlights')
            ])
            schedule.add_hline()
            schedule.end_table_header()

            # Create the next-page footer
            schedule.add_hline()
            schedule.add_row((MultiColumn(3, align='c', data='Continued on Next Page'),))
            schedule.add_hline()
            schedule.end_table_footer()

            # Create the last-page footer
            schedule.add_hline()
            schedule.add_row((MultiColumn(3, align='r', data=''),))
            schedule.add_hline()
            schedule.end_table_last_footer()

            # Get the dates
            schedule_dates = term.dates(section.subterm, section.days)
            # Get the agenda
            agenda = course.agendas[len(schedule_dates)]
            # Format the topics, and highlights
            topics, highlights = format_agenda(agenda, course.highlight_types)

            # Insert no class messages
            if not term.no_classes.empty:
                for index, no_class in term.no_classes.iterrows():
                    date = no_class['date']
                    if date.weekday() in section.days:
                        for day in range(1, len(schedule_dates) - 1):
                            start = schedule_dates[day - 1]
                            end = schedule_dates[day]
                            if start < date and date <= end:
                                schedule_dates.insert(day, date)
                                message = no_class['message']
                                topics.insert(day, Command('centering', bold(message)))
                                highlights.insert(day, '')
                                break

            # Insert notices
            notices = course.notices.loc[course.notices['subterm']==section.subterm]
            if not notices.empty:
                for index, notice in notices.iterrows():
                    for day in range(1, len(schedule_dates) - 1):
                        start = schedule_dates[day - 1]
                        end = schedule_dates[day]
                        date = notice['date']
                        if start < date and date <= end:
                            schedule_dates.insert(day, date)
                            message = notice['message']
                            topics.insert(day, Command('centering', bold(message)))
                            highlights.insert(day, '')
                            break

            dates = format_dates(schedule_dates)
            for day in range(len(dates)):
                schedule.add_row(
                    dates[day],
                    topics[day],
                    highlights[day],
                )
                schedule.add_hline()

        # Temporarily switch to the subdirectory './Schedules' to run Latexmk
        with tex.utils.latexmk_dir('Schedules', copy_pdf=False):
            # Generate the PDFs
            doc.generate_pdf(filename, clean_tex=clean_tex)

    print('Done generating schedules')

def get_headfoot(term, course, section):
    """Create the header and footer for the schedule."""

    headfoot = PageStyle('schedule')
    # Create left header
    with headfoot.create(Head('L')):
        headfoot.append(f"{course.organization}")
        headfoot.append(LineBreak())
        headfoot.append(f"{course.title}")
        headfoot.append(LineBreak())
        headfoot.append(f"{course.cid} - {section.sid} (CRN: {section.crn})")
        headfoot.append(LineBreak())
        headfoot.append(f"{course.hw_code_name}: {section.hw_code}")

    # Create right header
    with headfoot.create(Head('R')):
        headfoot.append("Tentative Course Schedule")
        headfoot.append(LineBreak())
        headfoot.append(f"{term.name}, {section.subterm}")
        headfoot.append(LineBreak())
        #headfoot.append(f"Room: {section.room}")
        headfoot.append(LineBreak())
        headfoot.append(f"{section.meeting_times}")

    # Create right footer
    with headfoot.create(Foot('R')):
        now = datetime.now(timezone('US/Eastern')).strftime('%Y%m%d%H%M')
        headfoot.append(FootnoteText(now))

    return headfoot

def format_agenda(agenda: object, highlight_types: Tuple[str] = None):
    """Convert the raw data into a list of Topics objects indexed by the day on which the topic will be covered.

    Topics() is a preformated subclass of pylatex.Itemize."""

    days = range(agenda['day'].max())
    topics = [Topics() for day in days]
    highlights = [''] * len(days)
    for day in days:
        # Filter by the day of the class meeting
        temp = agenda.loc[agenda['day'] == day + 1]
        for index, row in temp.iterrows():
            # Add the topic
            topics[day].add_item(row)
            # Add the highlights
            type_ = row['type']
            if type_ in highlight_types:
                highlight = row['type']
                highlights[day] = bold(highlight) #Command('textbf', arguments=highlight)

    return (topics, highlights)

def format_dates(dates: Union[List[object], object]) -> Union[List[str], str]:
    """Convert dates like '1/1/2001' to 'M, 1/1'"""

    # Abbreviations for days of the week
    day_names = {0:'M', 1:'T', 2:'W', 3:'R', 4:'F', 5:'S', 6:'Su'}
    formated_dates = []

    if isinstance(dates, list):
        for date in dates:
            string = day_names[date.weekday()] + ", " + date.strftime('%m/%d')
            formated_dates.append(string)
        return formated_dates
    else:
        return day_names[dates.weekday()] + ", " + dates.strftime('%m/%d')

class Topics(Itemize):
    """Compact bulleted list with the blanklines before and after the list removed"""

    packages = [Package('enumitem')]
    latex_name = 'itemize'

    def __init__(self):
        super().__init__()

    def dumps(self):
        removeline = UnsafeCommand('vspace', arguments=Arguments('-1em'))
        string = removeline.dumps()
        string += super().dumps()
        string += removeline.dumps()

        return string

    def add_item(self, row):
        topic = self.get_topic_tex(row)
        return super().add_item(topic)

    def get_topic_tex(self, row):
        if row['type'] == 'Lecture':
            topic = self.getlecture(row)
        elif row['type'] == 'Quiz':
            topic = self.getquiz(row)
        elif row['type'] == 'Review':
            topic = self.getreview(row)
        elif row['type'] == 'Midterm':
            topic = self.getexam(row)
        elif row['type'] == 'Final':
            topic = self.getexam(row)
        elif row['type'] == 'Exam':
            topic = self.getexam(row)
        else:
            topic = self.getdefault(row)
        return topic

    def getlecture(self, row):
        # Handle null values in the section and subtopic fields
        if pd.isnull(row['section']):
            if pd.isnull(row['subtopic']):
                return f"{row['topic']} ({row['minutes']} min.)"
            else:
                return f"{row['topic']} - {row['subtopic']} ({row['minutes']} min.)"
        else:
            if pd.isnull(row['subtopic']):
                return f"{row['section']} {row['topic']} ({row['minutes']} min.)"
            else:
                return f"{row['section']} {row['topic']} - {row['subtopic']} ({row['minutes']} min.)"

    def getquiz(self, row):
        quiz = f"{row['topic']} - Sections {row['subtopic']} ({row['minutes']} min.)"
        return bold(quiz) #Command('textbf', arguments=quiz)

    def getreview(self, row):
        return f"{row['topic']} ({row['minutes']} min.)"

    def getexam(self, row):
        exam = f"{row['topic']} - Sections {row['subtopic']} ({row['minutes']} min.)"
        return bold(exam) #Command('textbf', arguments=exam)

    def getdefault(self, row):
        if pd.isnull(row['subtopic']):
            return f"{row['topic']} ({row['minutes']} min.)"
        else:
            return f"{row['topic']} - {row['subtopic']} ({row['minutes']} min.)"