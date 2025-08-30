import os

from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
)


def get_prompt_template(name: str, **kwargs):
    """
    Load and return prompt template with Jinja2

    :param name: Name of the prompt template file (without .md extension)
    :return: The template string
    """
    template = env.get_template(f"{name}.md")
    return template.render(kwargs)
