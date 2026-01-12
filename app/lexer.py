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
    redirector: bool

redirect = False

def set_redirect():
    global redirect
    redirect = True

def read_redirect() -> bool:
    global redirect
    if redirect:
        redirect = False
        return True
    else:
        return False

def command_lexer(usrinput:str) -> List[SemanticToken]:
        tokens = []
        current_word = ""
        in_quotes = False
        token_has_quotes = QuoteState.NONE
        escaped = False
        escape_conditional = False

        for char in usrinput:
            if char == "\\" and not escaped:
                if in_quotes and token_has_quotes == QuoteState.SINGLE:
                    current_word = current_word + char
                elif in_quotes and token_has_quotes == QuoteState.DOUBLE:
                    escaped = True
                    escape_conditional = True
                else:
                    escaped = True
            elif escaped:
                if escape_conditional:
                    conditions = ['"', "\\", "$", "`", "\n"]
                    if char in conditions:
                        current_word = current_word + char
                    else:
                        current_word = current_word + "\\" + char
                    escaped = False
                    escape_conditional = False
                else:
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
                        semantic_token = SemanticToken(current_word, token_has_quotes, read_redirect())
                        tokens.append(semantic_token)
                        token_has_quotes = QuoteState.NONE
                    else:
                        if current_word:
                            semantic_token = SemanticToken(current_word, QuoteState.NONE, read_redirect())
                            tokens.append(semantic_token)
                    current_word = ""
            elif char == ">":
                current_word = current_word + char
                set_redirect()
            else:
                current_word = current_word + char
        
        if current_word and token_has_quotes is not QuoteState.NONE:
            semantic_token = SemanticToken(current_word, token_has_quotes, read_redirect())
            tokens.append(semantic_token)
        elif token_has_quotes is not QuoteState.NONE:
            semantic_token = SemanticToken(current_word, token_has_quotes, read_redirect())
            tokens.append(semantic_token)
        elif current_word and token_has_quotes is QuoteState.NONE:
            semantic_token = SemanticToken(current_word, QuoteState.NONE, read_redirect())
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


def redirect_output_tokens(semantic_tokens:List[SemanticToken]) -> tuple[List[SemanticToken], List[SemanticToken]]:
    redirect_state = False
    command_tokens = []
    redirect_tokens = []

    for token in semantic_tokens:
        if redirect_state:
            redirect_tokens.append(token)
        else:
            if token.redirector:
                redirect_state = True
                token_contents = token.value
                split_token = token_contents.split('>')
                if split_token[0][-1] == "1":
                    split_token[0] = split_token[0][0:-1]
                command_semantic_token = SemanticToken(split_token[0], token.state, False)
                redirect_semantic_token = SemanticToken(split_token[1], token.state, False)
                command_tokens.append(command_semantic_token)
                redirect_tokens.append(redirect_semantic_token)
            else:
                command_tokens.append(token)
    return command_tokens, redirect_tokens