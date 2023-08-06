"""
File: email_template.py
Created: 2020-08-28
Author: Subhendu R Mishra
"""
from jinja2 import Environment, meta


class EmailTemplate:

    def __init__(self, template: str):
        self.template = template
        self.subject_template, self.body_template = split_template(template)
        env = Environment()
        ast = env.parse(self.template)
        self.required_variables = meta.find_undeclared_variables(ast)
        self.subject_t = env.from_string(self.subject_template)
        self.body_t = env.from_string(self.body_template)

    def get_subject(self, mapping):
        return self.subject_t.render(mapping)

    def get_body(self, mapping):
        return self.body_t.render(mapping)


def split_template(template: str) -> (str, str):
    lines = [line for line in template.split("\n")]
    subject, body = "", ""
    i = 0
    for line in lines:
        i += 1
        if len(line.strip()) != 0:
            subject = line.strip()
            break

    body = "\n".join(lines[i:])

    return subject, body
