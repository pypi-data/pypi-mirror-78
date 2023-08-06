# For the header and footer
from pylatex import PageStyle, Head, Foot, LineBreak, VerticalSpace, simple_page_number, SmallText, FootnoteText
from pylatex.utils import bold

# For the timestamp in the footer
from datetime import datetime
from pytz import timezone

# For the boolean flags
from rewrite.subclasses_of_pylatex import IfBool

def get_assessment_headfoot(term_name, subterm_name, course, assessment, version, padding='1pt'):
    """Create the header and footer for the schedule."""

    headfoot = PageStyle('assessment')
    # Create left header
    with headfoot.create(Head('L')):
        headfoot.append(f"{course.cid}, {course.title}")
        headfoot.append(LineBreak())
        assessment_info = f"{assessment.kind} {assessment.number}.{version} for {assessment.fullpoints} Points"
        headfoot.append(SmallText(assessment_info))
        headfoot.append(VerticalSpace(padding))
    with headfoot.create(Head('C')):
        if_instructorKey = [
            SmallText(bold("FOR INSTRUCTORS ONLY")),
            LineBreak(),
            SmallText(bold(f"(Max. of {assessment.maxpoints} points)"))
        ]
        headfoot.append(IfBool('instructorKey', if_instructorKey))
        headfoot.append(VerticalSpace(padding))
    # Create right header
    with headfoot.create(Head('R')):
        headfoot.append(f"{term_name}, {subterm_name}")
        headfoot.append(LineBreak())
        headfoot.append(SmallText(f"Assessing Period: {assessment.period}"))
        headfoot.append(VerticalSpace(padding))

    # Create left footer
    with headfoot.create(Foot('L')):
        now = datetime.now(timezone('US/Eastern')).strftime('%Y%m%d%H%M')
        headfoot.append(FootnoteText(now))
    # Create center footer
    with headfoot.create(Foot('C')):
        headfoot.append('')
    # Create right footer
    with headfoot.create(Foot('R')):
        headfoot.append(simple_page_number())

    return headfoot