"""
    Phase 4 - Prompt Loader for XML Prompt Templates
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    In this file you will create a class that loads and parses
    XML prompt template files from the prompts/ folder.
    Each XML file contains a different prompting technique
    (minimal, structured, chain-of-thought, persona).
"""


# TODO:
# Phase 4 — Imports
#
# > Import xml.etree.ElementTree as ET for parsing XML files
# Reference: https://docs.python.org/3/library/xml.etree.elementtree.html
#
# > Import Path from pathlib for cross-platform file paths
# Reference: https://docs.python.org/3/library/pathlib.html
#
# > Import Optional from typing
# Reference: https://docs.python.org/3/library/typing.html#typing.Optional
#
# > Import PromptTemplate from models
# Reference: https://docs.python.org/3/tutorial/modules.html
# YOUR CODE STARTS HERE
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional
from models import PromptTemplate

# YOUR CODE ENDS HERE


# TODO:
# Task 1 — Create the PromptLoader class
#
# > Create a class called PromptLoader
# Reference: https://docs.python.org/3/tutorial/classes.html
#
# > Inside the class, create an __init__ method that takes an optional prompts_dir (str)
#   - If prompts_dir is None, set it to Path(__file__).parent / "prompts"
#     This automatically points to the prompts/ folder next to this file
#   - Store it as self.prompts_dir = Path(prompts_dir)
#   - Create an empty cache dictionary: self._cache: dict[str, PromptTemplate] = {}
# Reference: https://docs.python.org/3/library/pathlib.html#pathlib.Path
# Reference: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
#
# > Inside the class, create a method called list_prompts that returns list[str]
#   - Use self.prompts_dir.glob("prompt-*.xml") to find all prompt files
#   - For each file, extract the name by removing "prompt-" prefix and ".xml" suffix
#     using file.stem.replace("prompt-", "")
#   - Return a sorted list of prompt names
# Reference: https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
# Reference: https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.stem
#
# > Inside the class, create a method called load_prompt that takes name (str)
#   and returns a PromptTemplate
#   - First check if name is in self._cache, if so return the cached version
#   - Build the file path: self.prompts_dir / f"prompt-{name}.xml"
#   - If the file doesn't exist, raise FileNotFoundError
#   - Call self._parse_xml(file_path) to parse the template
#   - Cache the result and return it
# Reference: https://docs.python.org/3/library/pathlib.html#pathlib.Path.exists
# Reference: https://docs.python.org/3/library/exceptions.html#FileNotFoundError
#
# > Inside the class, create a private method called _parse_xml that takes
#   file_path (Path) and returns a PromptTemplate
#   - Parse the XML file using ET.parse(file_path)
#   - Get the root element with tree.getroot()
#   - Extract the name attribute: root.get('name', file_path.stem)
#   - Extract the version attribute: root.get('version', '1.0')
#   - Find the system_prompt element: root.find('system_prompt')
#   - Find the user_template element: root.find('user_template')
#   - If either is None, raise ValueError
#   - Extract and strip the text from each element
#   - Return a PromptTemplate with all extracted values
# Reference: https://docs.python.org/3/library/xml.etree.elementtree.html#parsing-xml
# Reference: https://docs.python.org/3/library/xml.etree.elementtree.html#finding-interesting-elements
#
# > Inside the class, create a method called load_all that returns dict[str, PromptTemplate]
#   - Iterate over list_prompts() and load each one
#   - Return a dictionary mapping name to template
# Reference: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
#
# > Inside the class, create a method called get_prompt_info that takes name (str)
#   and returns a dict with metadata about the prompt template
#   - Load the template and return a dict with name, version, file_path,
#     system_prompt_length, and user_template_length
# Reference: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
# YOUR CODE STARTS HERE
class PromptLoader:
    """Loads and manages XML prompt templates from the prompts/ directory."""

    def __init__(self, prompts_dir: Optional[str]=None):
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent/ "prompts"
        self.prompts_dir = Path(prompts_dir)
        self.cache: dict[str, PromptTemplate] = {}

    def list_prompts(self) -> list[str]:
        return sorted([file.stem.replace("prompt-","") for file in self.prompts_dir.glob("prompt-*.xml")])
       
    def _parse_xml(self, file_path: Path) -> PromptTemplate:
        tree = ET.parse(file_path)
        root = tree.getroot()
        name = root.get('name', file_path.stem)
        version = root.get('version', '1.0')
        system_prompt_elem = root.find('system_prompt')
        user_template_elem = root.find('user_template')
        if system_prompt_elem is None or user_template_elem is None:
            raise ValueError(f"Missing required elements in {file_path}")
        system_prompt = system_prompt_elem.text.strip()
        user_template = user_template_elem.text.strip()
        return PromptTemplate(name=name, version=version, system_prompt=system_prompt, user_template=user_template, file_path=str(file_path))

    def load_prompt(self, name: str) -> PromptTemplate:
        if name in self.cache:
            return self.cache[name]
        file_path = self.prompts_dir / f"prompt-{name}.xml"
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt template '{name}' not found.")
        template = self._parse_xml(file_path)
        self.cache[name] = template
        return template

    def load_all(self) -> dict[str, PromptTemplate]:
        return {name: self.load_prompt(name) for name in self.list_prompts()}
    
    def get_prompt_info(self, name: str) -> dict:
        template = self.load_prompt(name)
        return {
            "name": template.name,
            "version": template.version,
            "file_path": template.file_path,
            "system_prompt_length": len(template.system_prompt),
            "user_template_length": len(template.user_template),
        }
# YOUR CODE ENDS HERE


# TODO:
# Task 2 — Add a main block to test the prompt loader
#
# > Add an if __name__ == "__main__" block that:
#   - Creates a PromptLoader instance
#   - Prints all available prompt names
#   - For each prompt, prints its info (name, version, system_prompt length)
# Reference: https://docs.python.org/3/library/__main__.html
# YOUR CODE STARTS HERE
if __name__ == "__main__":
    loader = PromptLoader()
    print("Available prompts:")
    for name in loader.list_prompts():
        info = loader.get_prompt_info(name)
        print(f"  - {name} (v{info.get('version', '?')}, {info['system_prompt_length']} chars)")


# YOUR CODE ENDS HERE
