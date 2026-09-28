def light_spell_allowed_ingredients():
    return ["air", "earth", "water", "fire"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    from .light_validator import validate_ingredients

    result: str = validate_ingredients(ingredients)
    return f"Spell recorded: {spell_name} ({result})"
