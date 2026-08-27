# Parser fix requirements

The parser must reject trailing non-whitespace input after a complete value.
The change is accepted when focused parser tests cover valid whitespace and
invalid trailing tokens without changing other parsing behavior.
