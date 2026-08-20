import logging

import click
import inquirer

from .custom_types import Email

logger = logging.getLogger(__name__)


class SelectChoice:
    def __init__(self, value: str, label: str):
        self.value = value
        self.label = label


class Prompt:
    @staticmethod
    def select(message: str, choices: list[SelectChoice]):
        answer = inquirer.prompt([
            inquirer.List(
                'value',
                message=message,
                choices=[choice.label for choice in choices],
                carousel=True
            )
        ])

        label_selected = answer['value']

        choice_selected = next(choice for choice in choices if choice.label == label_selected)

        return choice_selected.value

    @staticmethod
    def checkbox(message: str, choices: list[SelectChoice]) -> list[str]:
        answer = inquirer.prompt([
            inquirer.Checkbox(
                'values',
                message=message,
                choices=[choice.label for choice in choices],
                carousel=True
            )
        ])

        labels_selected = answer['values']

        choices_selected = [
            choice for choice in choices if choice.label in labels_selected
        ]

        return choices_selected

    @staticmethod
    def string(message: str) -> str:
        value = click.prompt(message, type=str)

        return value

    @staticmethod
    def email(message: str) -> str:
        value = click.prompt(message, type=Email)

        return value

    @staticmethod
    def money(message: str) -> float:
        value = click.prompt(message, type=str)
        value = value.removeprefix('$')

        if ',' in value:
            value = value.replace(',', '')

        try:
            return float(value)
        except ValueError:
            logger.error(f"Invalid amount format: {value}")

            return Prompt.money(message)

    @staticmethod
    def echo(message: str):
        click.echo(message)

    @staticmethod
    def confirm(message: str) -> bool:
        return click.confirm(message)
