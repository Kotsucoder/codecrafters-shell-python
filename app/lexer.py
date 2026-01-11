import os
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

class QuoteState(Enum):
    NONE = auto()
    SINGLE = auto()
    DOUBLE = auto()

@dataclass(frozen=True)
class SemanticToken:
    value: str
    state: QuoteState

def command_lexer(usrinput:str) -> List[SemanticToken]:
        tokens = []
        current_word = ""
        in_quotes = False
        token_has_quotes = QuoteState.NONE
        escaped = False

        for char in usrinput:
            if char == "\\" and not in_quotes and token_has_quotes != QuoteState.SINGLE:
                escaped = True
            elif escaped:
                current_word = current_word + char
                escaped = False
            elif char == "'":
                if in_quotes:
                    if token_has_quotes == QuoteState.SINGLE:
                        in_quotes = False
                    else:
                        current_word = current_word + char
                else:
                    in_quotes = True
                    token_has_quotes = QuoteState.SINGLE
            elif char == '"':
                if in_quotes:
                    if token_has_quotes == QuoteState.DOUBLE:
                        in_quotes = False
                    else:
                        current_word = current_word + char
                else:
                    in_quotes = True
                    token_has_quotes = QuoteState.DOUBLE
            elif char == " ":
                if in_quotes:
                    current_word = current_word + char
                else:
                    if token_has_quotes is not QuoteState.NONE:
                        semantic_token = SemanticToken(current_word, token_has_quotes)
                        tokens.append(semantic_token)
                        token_has_quotes = QuoteState.NONE
                    else:
                        if current_word:
                            semantic_token = SemanticToken(current_word, QuoteState.NONE)
                            tokens.append(semantic_token)
                    current_word = ""
            else:
                current_word = current_word + char
        
        if current_word and token_has_quotes is not QuoteState.NONE:
            semantic_token = SemanticToken(current_word, token_has_quotes)
            tokens.append(semantic_token)
        elif token_has_quotes is not QuoteState.NONE:
            semantic_token = SemanticToken(current_word, token_has_quotes)
            tokens.append(semantic_token)
        elif current_word and token_has_quotes is QuoteState.NONE:
            semantic_token = SemanticToken(current_word, QuoteState.NONE)
            tokens.append(semantic_token)

        return tokens



def expander(object_set:List[SemanticToken]) -> List[str]:
    str_list = []
    for object in object_set:
        token = object.value
        state = object.state

        if state == QuoteState.SINGLE:
            str_list.append(token)

        elif state == QuoteState.NONE:
            try:
                if token[0] == "$":
                    variable_name = token[1:]
                    token = os.environ[variable_name]
                    str_list.append(token)
                elif token[0] == "~":
                    homedir = os.path.expanduser('~')
                    token = homedir + token[1:]
                    str_list.append(token)
                else:
                    str_list.append(token)
            except IndexError:
                continue

        elif state == QuoteState.DOUBLE:
            expanded_value = token
            for key, val in os.environ.items():
                expanded_value = expanded_value.replace(f"{key}", val)
            str_list.append(expanded_value)

    return str_list