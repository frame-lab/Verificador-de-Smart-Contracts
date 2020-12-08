class MyJsonRules(object):

    def __init__(self, options):
        self.options = options
        self.err = False

    reserved = {
        'standard': 'STANDARD',
        'input_type': 'INPUT_TYPE',
        'pubkey_list': 'PUBKEY_LIST',
        'pubkey': 'PUBKEY',
        'pubkeys': 'PUBKEYS',
        'rule': 'RULE',
        'rules': 'RULES',
        'default_rule': 'DEFAULT_RULE',
        'inline_last': 'INLINE_LAST',
        'single': 'SINGLE',
        'signatures': 'SIGNATURES',
        'array': 'ARRAY',
        'smacco': 'SMACCO',
        'disabled': 'DISABLED',
        'ALLOW_ALL': 'ALLOW_ALL',
        'ALLOW_IF': 'ALLOW_IF',
        'DENY_ALL': 'DENY_ALL',
        'DENY_IF': 'DENY_IF',
        'rule_type': 'RULE_TYPE',
        'minimum_required': 'MINIMUM_REQUIRED',
        'timestamp': 'TIMESTAMP',
        'utc': 'UTC',
        'condition': 'CONDITION',
        'conditions': 'CONDITIONS',
        'condition_name': 'CONDITION_NAME',
        'condition_type': 'CONDITION_TYPE',
    }

    tokens = [
        'ID',
        'LBRACKET',
        'RBRACKET',
        'LBRACE',
        'RBRACE',
        'COMMA',
        'COLON',
        'QUOT',
    ] + list(reserved.values())

    t_ignore = ' \t\n'

    def t_ID(self, t):
        r'[a-zA-Z_0-9\-\/]+'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COMMA = r'\,'
    t_COLON = r'\:'
    t_QUOT = r'\"'

    def t_error(self, t):
        print("Illegal character '%s'" % t.value)
        self.err = True
