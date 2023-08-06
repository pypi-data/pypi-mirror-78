import argparse
import importlib.metadata
import logging
import os
import re
import shutil
from pathlib import Path

from yaml import safe_load

from nbconvert import HTMLExporter
from nbconvert.preprocessors import tagremove
from traitlets.config import Config

from . import preprocessors, toc, utils

__version__ = importlib.metadata.version(__package__)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('directory', type=Path, help="The directory containing the notebooks")
    parser.add_argument('--no-prompt', action='store_true', dest="no_prompt")
    args = parser.parse_args()

    if not args.directory.exists() or not args.directory.is_dir():
        print("Error: Directory must exist")
        parser.print_help()
        exit(1)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("nbpretty")

    mod_dir = Path(os.path.abspath(os.path.dirname(__file__)))
    template_file = mod_dir / "course.tpl"
    css_file = mod_dir / "custom.css"

    config = Config()
    config.TagRemovePreprocessor.remove_cell_tags = {"remove_cell"}
    if args.no_prompt:
        config.TemplateExporter.exclude_input_prompt = True
        config.TemplateExporter.exclude_output_prompt = True

    chapters = sorted(f for f in args.directory.glob("*.ipynb") if re.match(r"\d\d.*", f.name))
    answers = sorted(f for f in args.directory.glob("answer_*.ipynb"))
    asides = sorted(f for f in args.directory.glob("aside_*.ipynb"))
    appendixes = sorted(f for f in args.directory.glob("appendix_*.ipynb"))

    with open("config.yaml") as f:
        nbpretty_config = safe_load(f)
        course_title = nbpretty_config["course_title"]
        custom_blocks = nbpretty_config.get("custom_blocks")

    logger.info("Constructing table of contents")
    toc_html = toc.construct_toc(chapters, config)

    html_exporter = HTMLExporter(template_file=str(template_file), config=config)
    html_exporter.register_preprocessor(tagremove.TagRemovePreprocessor, enabled=True)
    html_exporter.register_preprocessor(preprocessors.PageLinks(chapters), enabled=True)
    html_exporter.register_preprocessor(preprocessors.HighlightExercises, enabled=True)
    html_exporter.register_preprocessor(preprocessors.SetTitle(course_title), enabled=True)
    html_exporter.register_preprocessor(preprocessors.HideWriteFileMagic, enabled=True)
    html_exporter.register_preprocessor(preprocessors.FixLinkExtensions, enabled=True)
    html_exporter.register_preprocessor(preprocessors.CustomBlocks(custom_blocks), enabled=True)
    html_exporter.register_preprocessor(preprocessors.InsertTOC(toc_html), enabled=True)
    html_exporter.register_preprocessor(preprocessors.UninlineCss, enabled=True)

    extra_files = {}

    for filename in chapters + answers + asides + appendixes:
        body, resources = utils.ipynb_to_html(html_exporter, filename)
        extra_files.update(resources["files"])
        with open(f"{resources['output_stem']}.html", "w") as out:
            logger.info(f"Writing '{filename}' as '{out.name}'")
            out.write(body)

    for filename, contents in extra_files.items():
        with filename.open("w") as f:
            f.write(contents)

    shutil.copy(css_file, ".")
