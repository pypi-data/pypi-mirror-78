# For the timestamp
from datetime import datetime

# Third Party
from pytz import timezone
from pylatex import NewLine, VerticalSpace
from pylatex import Document, Command
from pylatex.utils import NoEscape

# Local
from rewrite import tex


class Problem(Document):
    """The pylatex representation of rewrite.Problem."""

    content_separator = '\n'
    packages = tex.PACKAGES
    # Document aguments
    documentclass='standalone'
    document_options=[
        'class=article',
        'fontsize=12pt',
        'varwidth=false',
        'crop=false'
    ]
    geometry_options = {
        "left": "0in",
        "right": "0in",
        "top": "0in",
        "bottom": "0in",
        "headheight":"0pt"
    }
    indent = False

    def __init__(self, problem):
        self._problem = problem

        #### Create TeX objects that will be modified when generating PDFs
        # Create boolean flags that can be toggled by assigning a new truth value
        # Example: self.instructor_key = True
        self.instructor_key = tex.SetBool('instructorKey', False)
        self.student_key = tex.SetBool('studentKey', False)
        # Create the parameters iterator that can be modified with next(self.parameters)
        self.parameters = tex.Parameters(problem.Parameters())

        super().__init__(
            documentclass=self.documentclass,
            document_options=self.document_options,
            geometry_options=self.geometry_options,
            indent=self.indent,
        )

        #### Create the default preamble.
        #self.preamble.content_separator = self.content_separator
        # Set Pythontex's output directory to the same directory as the source TeX file
        # This is necessary because Latexmk is not recognizing the need to run pythontex
        pythontex_out = Command('setpythontexoutputdir', '.')
        self.preamble.append(pythontex_out)

        # Set the key flags in the preamble
        # The truth values of these TeX bools can be modified later by changing the
        # value attribute: `instructor_key.value = True`
        self.preamble.append(tex.ProvideBool('instructorKey'))
        self.preamble.append(self.instructor_key)
        self.preamble.append(tex.ProvideBool('studentKey'))
        self.preamble.append(self.student_key)

        self.append(self.content)

    @property
    def content(self):
        content = tex.TexList()

        #### Create the default document environment
        # Assign the point values in a pycode environment
        content.append(tex.Points(self.problem.points))
        # Assign the parameters in a pycode environment
        content.append(self.parameters)
        content.append(NoEscape(self.problem.body))

        return content

    @property
    def problem(self):
        return self._problem

    def generate_pdf(self, versions, timestamp=False, **kwargs):
        if timestamp:
            self.append('')
            self.append(VerticalSpace('.5in'))
            self.append('')
            self.append(datetime.now(timezone('US/Eastern')).strftime('%Y%m%d%H%M'))

        # Run Latexmk in the subdirectory './tex'
        with tex.utils.latexmk_dir('tex'):
            for version in versions:
                # Generate similar parameters
                next(self.parameters)
                #self.pyvars.vars_dict.update(vars(self.parameters))
                for show_key in [False, True]:
                    # Set the key flag in the preamble
                    self.instructor_key.value = show_key
                    self.student_key.value = show_key

                    # Set the output filename
                    filename = f'{self.problem.name} {version}'
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
        if 'clean' in kwargs.keys():
            if kwargs['clean'] and os.path.isfile('pythontex_data.pkl'):
                os.remove('pythontex_data.pkl')
        print('Done generating PDFs!')

    def __next__(self):
        next(self.parameters)