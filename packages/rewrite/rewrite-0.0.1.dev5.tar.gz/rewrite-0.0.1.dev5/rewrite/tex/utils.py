# Standard Library
import contextlib # For creating contextmanagers
from pathlib import Path # For directory management
import os # For changing the working directory
import shutil # For moving all PDFs to `original directory / PDF`

# Third Party
None

# Locals
None


LATEXMKRC = r"""#!/usr/bin/perl

my @extensions = ('pytxcode', 'pytxmcr', 'pytxpyg', 'pkl');
push @generated_exts, @extensions;

$clean_ext = 'pythontex_data.pkl';

add_cus_dep('sagetex.sage', 'sagetex.sout', 0, 'makesout');
$hash_calc_ignore_pattern{'sage'} = '^( _st_.goboom| ?_st_.current_tex_line|print .SageT)';
sub makesout {
    system("sage '$_[0].sagetex.sage'");
}

add_cus_dep('pytxcode', 'pytxmcr', 0, 'pythontex');
sub pythontex { return system("pythontex3 '$_[0]'"); }
"""

@contextlib.contextmanager
def latexmk_dir(path: str, copy_pdf: bool = True) -> None:
    """Changes working directory and then returns to the original directory on exit."""

    path = Path(path)
    original_directory = Path.cwd()
    if not path.is_dir():
        path.mkdir(parents=True)
    os.chdir(path)

    # Create the '.latexmkrc' file if necessary
    rcpath = path / '.latexmkrc'
    if not rcpath.is_file():
        with open('.latexmkrc', 'w', encoding='utf-8') as rcfile:
            rcfile.write(LATEXMKRC)

    try:
        yield
    finally:
        os.chdir(original_directory)

    if copy_pdf:
        # Move PDFs to the folder 'PDF' in the orginial directory
        pdf_path = original_directory / 'PDF'
        if not pdf_path.is_dir():
            pdf_path.mkdir(parents=True)

        files = path.glob('*.pdf')
        for file in files:
            if file.is_file():
                # To move files, shutil must have the full file name as a string
                src = str(file)
                dest = str(pdf_path / file.name)
                shutil.move(src, dest)