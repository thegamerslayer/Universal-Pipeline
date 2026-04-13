# The "Converter" (Pydantic models)

import re
import json
from typing import Any, Dict, Optional, Union
from pydantic import create_model, field_validator, BeforeValidator
from typing_extensions import Annotated

def clean_data(v:Any):
    """
    THE CLEANER: This runs BEFORE validation. 
    It strips currency symbols, commas, and whitespace so '£ 52.35' becomes '52.35'.

    """
    if isinstance(v,str):
        # Remove anything that isn't a digit, a decimal point, or a letter

        cleaned=re.sub(r'[^\d\.]', '', v)
        return cleaned
    return v

def build_dynamic_model(schema_json:str):
    """
    THE ARCHITECT: This takes your JSON settings and builds a 
    Python Class (Model) out of thin air.

    """

    schema=json.loads(schema_json)
    fields={}

    for field_name,rules in schema.items():
        # 1. Determine the Python Type (int, float, or str)
        target_type=str
        if rules["type"]=="float":
            target_type=float
        elif rules["type"]=="int":
            target_type=int

        # 2. The 'Annotated' trick:
        # We tell Pydantic: "Try to make this a float, but RUN 'clean_data' first."

        if rules["type"] in ["float","int"]:
            field_type=Annotated[target_type,BeforeValidator(clean_data)]
        else:
            field_type=target_type

        # 3. Handle Optional vs Required
        # If 'required' isn't in JSON, we default to None (Optional)

        if not rules.get("required",False):
            field_type=Optional[field_type]
            default_value=None
        else:
            default_value=... # The '...' means 'No default, this is mandatory'

        # 4. Add to our field dictionary
        fields[field_name]=(field_type,default_value)

    # 5. Build the Class
    # This creates a class called 'ScrapedItem' using the fields we just defined
    return create_model("ScrapedItem",**fields)