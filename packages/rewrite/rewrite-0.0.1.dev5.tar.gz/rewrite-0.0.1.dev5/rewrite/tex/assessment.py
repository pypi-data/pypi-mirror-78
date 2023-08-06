# Standard Library
from datetime import datetime # For the timestamp in the footer

# Third Party
from pylatex import Document, PageStyle, Command
## For creating a TeX representation of the header and footer
from pylatex import PageStyle, Head, Foot, LineBreak, VerticalSpace, simple_page_number, SmallText, FootnoteText
from pylatex.base_classes import Container
## For the timestamp in the footer
from pytz import timezone

# Local
## For the boolean flags, IfBool, and Bold
from rewrite import tex


class Assessment(Document):
    """The pylatex representation of rewrite Assessment."""

    # The default separator, '%\n' causes problems with the vspace
    content_separator = ' %\n'
    # Append the LaTeX packages required for all assessment
    packages = tex.PACKAGES
    # Document aguments
    documentclass='article'
    document_options='12pt'
    geometry_options = {
        "left": "0.5in",
        "right": "0.5in",
        "top": "1in",
        "bottom": "1in",
        "headheight":"33pt"
    }
    indent = False

    def __init__(self, assessment):
        self._assessment = assessment

        #### Create the mutable TeX objects that will be modified when generating PDFs
        #    Create boolean flags that can be toggled by assigning a new truth value
        #    Example: self.instructor_key = True
        self.instructor_key = tex.SetBool('instructorKey', False)
        self.student_key = tex.SetBool('studentKey', False)
        #    Create the parameters iterator that can be modified with next(self.parameters)
        self.problemset = tex.ProblemSet(self.assessment.problemset.cells)
        #    Create an empty header and footer
        self.headfoot = PageStyle(name='assessment')

        #### Initialize the document object
        super().__init__(
            documentclass=self.documentclass,
            document_options=self.document_options,
            geometry_options=self.geometry_options,
            indent=self.indent,
        )

        #### Create the default preamble.
        ############self.preamble.content_separator = self.content_separator
        # Set Pythontex's output directory to the same directory as the source TeX file
        # This is necessary because Latexmk is not recognizing the need to run pythontex
        pythontex_out = Command('setpythontexoutputdir', '.')
        self.preamble.append(pythontex_out)
        # Set the key flags in the preamble
        #    The truth values of these TeX bools can be modified later by changing the
        #    value attribute: `instructor_key.value = True`
        self.preamble.append(tex.ProvideBool('instructorKey'))
        self.preamble.append(self.instructor_key)
        self.preamble.append(tex.ProvideBool('studentKey'))
        self.preamble.append(self.student_key)
        # Create an blank header and footer object but populate it later
        self.preamble.append(self.headfoot)
        self.preamble.append(Command("pagestyle", arguments=self.headfoot.name))
        #    doc.change_document_style(headfoot.name) <- doc.clear() will delete this command

        #### Create the default document environment
        ##### Add the name line
        ####self.append(tex.NameLine())
        ##### Add the instructions
        ####if self.assessment.instructions:
        ####    # Convert the insturctions to a pylatex.sections.Subsubsection object
        ####    instructions = tex.AssessmentSection('Instructions')
        ####    instructions.append(self.assessment.instructions)
        ####    self.append(instructions)
        # Add the hints
        ####if self.assessment.hints:
        ####    # Convert the hints to a pylatex.sections.Subsubsection object
        ####    hints = tex.AssessmentSection('Reference Formulas')
        ####    hints.append(self.assessment.hints)
        ####    self.append(hints)
        # Use a horizontal line to separate the problems from the instructions/hints
        ####self.append(Command('hrulefill')) ############################################################################
        # Add the problem set
        self.append(self.problemset)

    @property
    def assessment(self):
        return self._assessment

    def generate_pdf(self, course_cid, course_title, term_name, subterm_name, period, versions, timestamp=False, **kwargs):

        # Temporarily switch to the subdirectory './tex' to run Latexmk
        with tex.utils.latexmk_dir('tex', copy_pdf=True):

            for version in versions:
                # Update the the header and footer
                self.headfoot.clear()
                new_headfoot = self.HeadFoot(self.assessment, course_cid, course_title, term_name, subterm_name, period, version)
                self.headfoot.extend(new_headfoot)

                # Generate similar parameters for each problem in assessment
                next(self.problemset)

                # Generate the assessment and its key
                for show_key in [False, True]:
                    # Set the key flag in the preamble
                    self.instructor_key.value = show_key
                    self.student_key.value = show_key

                    # Set the output filename
                    filename = f'{course_cid} {term_name} {subterm_name} - {self.assessment.kind} {self.assessment.number}-{version}'
                    if show_key:
                        filename += ' - KEY'
                    # Pythontex fails when there is white space in the filename
                    filename = filename.replace(' ', '_')

                    # Generate the PDF
                    print(f'Generating {filename}.pdf')
                    super().generate_pdf(filename, **kwargs)

        #### Clean up after running Latexmk
        # Latexmk does not delete 'pythontex_data.pkl' <----------------------- FIX THIS
        import os
        if kwargs['clean'] and os.path.isfile('pythontex_data.pkl'):
            os.remove('pythontex_data.pkl')

    @staticmethod
    def HeadFoot(assessment, course_cid, course_title, term_name, subterm_name, period, version, padding='1pt'):
        """Create the header and footer for the assessment."""

        headfoot = PageStyle('assessment')
        # Create left header
        with headfoot.create(Head('L')):
            headfoot.append(f"{course_cid}, {course_title}")
            headfoot.append(LineBreak())
            assessment_info = f"{assessment.kind} {assessment.number}.{version} for {assessment.fullpoints} Points"
            headfoot.append(SmallText(assessment_info))
            headfoot.append(VerticalSpace(padding))
        with headfoot.create(Head('C')):
            if_instructorKey = [
                SmallText(tex.Bold("FOR INSTRUCTORS ONLY")),
                LineBreak(),
                SmallText(tex.Bold(f"(Max. of {assessment.maxpoints} points)"))
            ]
            headfoot.append(tex.IfBool('instructorKey', if_instructorKey))
            headfoot.append(VerticalSpace(padding))
        # Create right header
        with headfoot.create(Head('R')):
            headfoot.append(f"{term_name}, {subterm_name}")
            headfoot.append(LineBreak())
            headfoot.append(SmallText(f"Assessing Period: {period}"))
            headfoot.append(VerticalSpace(padding))

        # Create left footer
        with headfoot.create(Foot('L')):
            now = datetime.now(timezone('US/Eastern')).strftime('%Y%m%d%H%M')
            headfoot.append(FootnoteText(now))
        ### Create center footer
        ##with headfoot.create(Foot('C')):
        ##    newpage_message = SmallText(tex.Bold(assessment.newpage_message))
        ##    headfoot.append(newpage_message)
        # Create right footer
        with headfoot.create(Foot('R')):
            headfoot.append(simple_page_number())

        return headfoot