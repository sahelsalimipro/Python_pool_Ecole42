from .dark_validator import validate_ingredients


def dark_spell_allowed_ingredients():
    return ["air", "earth", "water", "fire"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    result: str = validate_ingredients(ingredients)
    return f"Spell recorded: {spell_name} ({result})"
