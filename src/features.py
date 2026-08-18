import re
import pandas as pd

DANGEROUS_KEYWORDS = ['UNION', 'OR', 'DROP', 'SELECT', 'SLEEP']

def extract_features(query: str) -> dict:
    return {
        'length': len(query),
        'n_quote': query.count("'"),
        'n_dash_comment': len(re.findall(r'--', query)),
        'n_semicolon': query.count(';'),
        'n_equal': query.count('='),
        'n_paren': query.count('(') + query.count(')'),
        'has_union': int(bool(re.search(r'\bUNION\b', query, re.IGNORECASE))),
        'has_or': int(bool(re.search(r'\bOR\b', query, re.IGNORECASE))),
        'has_drop': int(bool(re.search(r'\bDROP\b', query, re.IGNORECASE))),
        'has_select_from': int(bool(re.search(r'\bSELECT\b.*\bFROM\b', query, re.IGNORECASE))),
        'has_sleep': int(bool(re.search(r'\bSLEEP\s*\(', query, re.IGNORECASE))),
        'uppercase_ratio': sum(1 for c in query if c.isupper()) / max(len(query), 1),
        'n_whitespace': query.count(' '),
        'n_digit': sum(c.isdigit() for c in query),
        'keyword_repeat_count': sum(len(re.findall(re.escape(kw), query, re.IGNORECASE)) for kw in DANGEROUS_KEYWORDS),
    }

def build_feature_dataframe(df: pd.DataFrame, query_col='Query') -> pd.DataFrame:
    features = df[query_col].apply(extract_features).apply(pd.Series)
    return pd.concat([df, features], axis=1)