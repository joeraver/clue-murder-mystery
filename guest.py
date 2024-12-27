from dataclasses import dataclass


@dataclass
class Card:
    name: str
    category: str
    value: str

    def format_text(self) -> str:
        return f"{self.name}'s {self.category} is {self.value}"