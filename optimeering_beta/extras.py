import functools
from importlib import import_module
from typing import Any, Callable, Optional

pd: Any = None
try:
    pd = import_module("pandas")
except ImportError:
    PANDAS_AVAILABLE = False
else:
    PANDAS_AVAILABLE = True


def require_pandas(fn: Callable):
    @functools.wraps(fn)
    def inner(cls, *args, **kwargs):
        if not PANDAS_AVAILABLE:
            raise ImportError("Pandas is not available.")
        return fn(cls, *args, **kwargs)

    return inner


ALLOWED_UNPACK_VALUE_METHODS = ("retain_original", "new_rows", "new_columns")
EXPLOSION_COLUMNS = {
    # predictions
    "events": "event",
    "predictions": "prediction",
    "value": "value",
}


def _merge_resolving_conflicting_columns(
    df_left: "pd.DataFrame", df_right: "pd.DataFrame", expanded_column_name: str
) -> "pd.DataFrame":
    """
    Joins 2 dataframe upon their indices.
    If there are any columns that are conflicting, the column on the left dataframe are prepended
    with a word depending on `expanded_column_name`.
    """
    # Expanded column is no longer required
    del df_left[expanded_column_name]

    conflicting_columns = set(df_left.columns).intersection(set(df_right.columns))
    if len(conflicting_columns):
        conflict_prepend = EXPLOSION_COLUMNS[expanded_column_name]
        df_left = df_left.rename(columns={i: f"{conflict_prepend}_{i}" for i in conflicting_columns})

    df = pd.merge(df_left, df_right, left_index=True, right_index=True).reset_index(drop=True)
    return df


def pydantic_to_pandas(obj, unpack_value_method: Optional[str] = None) -> "pd.DataFrane":  # type: ignore[name-defined]
    dict_repr = obj.to_dict()
    if "items" in dict_repr:
        dict_repr = dict_repr["items"]

    df = pd.DataFrame(dict_repr)

    while merge_columns := set(EXPLOSION_COLUMNS).intersection(set(df.columns)):
        for merge_column in merge_columns:
            column_type = type(df[merge_column].iloc[0])
            if column_type is list:
                df = df.explode(merge_column).reset_index(drop=True)
                break
            elif column_type is dict:
                if merge_column in ("value",):
                    match unpack_value_method:
                        case "retain_original":
                            continue
                        case "new_rows":
                            df = df.reset_index(drop=True)
                            df_value = (
                                pd.DataFrame(df[merge_column].to_list())
                                .melt(var_name="value_category", value_name="value", ignore_index=False)
                                .dropna(subset=["value"])
                            )
                            df = _merge_resolving_conflicting_columns(df, df_value, merge_column)
                            break
                        case "new_columns":
                            df = df.reset_index(drop=True)
                            df_value = pd.json_normalize(df["value"])
                            df_value = df_value.rename(columns={i: f"value_{i}" for i in df_value.columns})
                            df = _merge_resolving_conflicting_columns(df, df_value, merge_column)
                            break
                        case _:
                            raise ValueError(
                                f"`unpack_value_method` must be used, and be one of {','.join(ALLOWED_UNPACK_VALUE_METHODS)}"
                            )
                else:
                    # If columns are of type dict, make each record a new column
                    df = df.reset_index(drop=True)
                    df_value = pd.DataFrame.from_dict(df[merge_column].to_list())
                    df = _merge_resolving_conflicting_columns(df, df_value, merge_column)
                    break
        else:
            # All columns that needs to be operated on has been completed
            # Break the while loop.
            break
    return df
