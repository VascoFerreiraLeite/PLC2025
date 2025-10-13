import sys
import json
import re

def sanitize(expr: str) -> str:
    """Remove (?i) e transforma (?i:...) em (?:...)"""
    expr = expr.replace('(?i)', '')
    expr = expr.replace('(?i:', '(?:')
    return expr

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 TPC3.py <tokens.json>", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            tokens = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: File '{filename}' is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    parts = []
    for t in tokens:
        name = t['id']
        expr = sanitize(t['expreg'])
        parts.append(f"(?P<{name}>{expr})")

    tokens_regex = "|".join(parts)
    regex_literal = json.dumps(tokens_regex)

    code = f"""import re

TOKENS_RE = re.compile({regex_literal}, re.IGNORECASE)

def tokenize(line, lineno=1):
    tokens = []
    for m in TOKENS_RE.finditer(line):
        dic = m.groupdict()
        for name, value in dic.items():
            if value is not None:
                if name not in ("SKIP", "COMMENT"):
                    tokens.append((name, value, lineno, m.span()))
                break
    return tokens

if __name__ == "__main__":
    print("Escreve a tua query SPARQL (Enter para ver tokens, 'exit' para sair):")
    lineno = 1
    while True:
        line = input("> ")
        if line.strip().lower() == "exit":
            break
        toks = tokenize(line, lineno)
        for t in toks:
            print(t)
        lineno += 1
"""

    print(code)

if __name__ == "__main__":
    main()
