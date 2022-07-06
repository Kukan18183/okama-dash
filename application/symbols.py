from flask_caching import Cache

import pandas as pd
import okama as ok


def get_symbols_names() -> dict:
    """
    Get a dictionary of long_name + symbol values.
    """
    namespaces = ["US", "LSE", "MOEX", "INDX", "COMM", "FX", "CC"]
    list_of_symbols = [
        ok.symbols_in_namespace(ns).loc[:, ["symbol", "name"]] for ns in namespaces
    ]
    classifier_df = pd.concat(
        list_of_symbols, axis=0, join="outer", copy="false", ignore_index=True
    )
    classifier_df["long_name"] = classifier_df.symbol + " : " + classifier_df.name
    return classifier_df.loc[:, ["long_name", "symbol"]].to_dict("records")
