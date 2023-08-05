from abc import ABC, abstractmethod
from builtins import bool
from typing import Any, Dict, List, Tuple

from qpd.dataframe import Column, DataFrame
from qpd.specs import (
    AggFunctionSpec,
    ArgumentSpec,
    IsValueSpec,
    OrderBySpec,
    WindowFunctionSpec,
)
from triad.utils.assertion import assert_or_throw


class QPDEngine(ABC):
    def __call__(self, func_name: str, *args: Any, **kwargs: Any) -> Any:
        return getattr(self, func_name)(*args, **kwargs)

    def rename(self, col: Column, name: str) -> Column:
        return col.rename(name)

    def extract_col(self, df: DataFrame, name: str) -> Column:
        return df[name]

    def assemble_df(self, *args: Any) -> DataFrame:
        return DataFrame(*args)

    @abstractmethod
    def to_df(self, obj: Any) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def to_col(self, value: Any, name: str = "") -> Column:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def to_native(self, df: DataFrame) -> Any:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def is_series(self, obj: Any) -> bool:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def case_when(self, *cols: Column) -> Column:  # pragma: no cover
        """`cols` must be in the format of
        `when1`, `value1`, ... ,`default`, and length must be >= 3.
        The reason to design the interface in this way is to simplify the translation
        from SQL to engine APIs.

        :return: [description]
        :rtype: Column
        """
        raise NotImplementedError

    @abstractmethod
    def order_by_limit(
        self, df: DataFrame, order_by: OrderBySpec, limit: int
    ) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def group_agg(
        self,
        df: DataFrame,
        keys: List[str],
        agg_map: Dict[str, Tuple[str, AggFunctionSpec]],
    ) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def window(  # noqa: C901
        self,
        df: DataFrame,
        func: WindowFunctionSpec,
        args: List[ArgumentSpec],
        dest_col_name: str,
    ) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    def basic_unary_arithmetic_op(self, col: Column, op: str) -> Column:
        if op == "+":
            return col
        if op == "-":
            return Column(0 - col.native)
        raise NotImplementedError(f"{op} is not supported")  # pragma: no cover

    def binary_arithmetic_op(self, col1: Column, col2: Column, op: str) -> Column:
        if op == "+":
            return Column(col1.native + col2.native)
        if op == "-":
            return Column(col1.native - col2.native)
        if op == "*":
            return Column(col1.native * col2.native)
        if op == "/":
            return Column(col1.native / col2.native)
        raise NotImplementedError(f"{op} is not supported")  # pragma: no cover

    def comparison_op(self, col1: Column, col2: Column, op: str) -> Column:
        if op == "==":
            s: Any = col1.native == col2.native
        elif op == "!=":
            s = col1.native != col2.native
        elif op == "<":
            s = col1.native < col2.native
        elif op == "<=":
            s = col1.native <= col2.native
        elif op == ">":
            s = col1.native > col2.native
        elif op == ">=":
            s = col1.native >= col2.native
        else:  # pragma: no cover
            raise NotImplementedError(f"{op} is not supported")
        return self._set_op_result_to_none(s, col1.native, col2.native)

    def binary_logical_op(self, col1: Column, col2: Column, op: str) -> Column:
        c1 = self._safe_bool(col1)
        c2 = self._safe_bool(col2)
        if op == "and":
            s: Any = c1 * c2
            # in sql, FALSE AND anything is False
            if self.is_series(s):
                s = s.mask((c1 == 0) | (c2 == 0), 0)
            elif (c1 == 0) | (c2 == 0):
                s = 0.0
        elif op == "or":
            s = c1 + c2
            # in sql, True OR anything is True
            if self.is_series(s):
                s = s.mask((c1 > 0) | (c2 > 0), 1)
            elif (c1 > 0) | (c2 > 0):
                s = 1.0
        else:  # pragma: no cover
            raise NotImplementedError(f"{op} is not supported")
        return Column(s)

    def logical_not(self, col: Column) -> Column:
        s = self._safe_bool(col.native)
        if self.is_series(s):
            nulls = s.isnull()
            s = s == 0
            s = s.mask(nulls, None)
            return Column(s)
        return Column(1.0 - s)

    def filter_df(self, df: DataFrame, cond: Column) -> DataFrame:
        c = self._safe_bool(cond)
        if self.is_series(c):
            ndf = self.to_native(df)[c > 0]
            return self.to_df(ndf)
        elif c > 0:
            return df
        else:
            ndf = self.to_native(df).head(0)
            return self.to_df(ndf)

    def is_value(self, col: Column, is_value: IsValueSpec) -> Column:
        v = is_value.value_expr
        if v == "null":
            if is_value.positive:
                return Column(col.native.isnull())
            else:
                return Column(~col.native.isnull())
        if v == "true":
            if is_value.positive:
                return Column(col.native == True)  # noqa:
            else:
                return Column(col.native != True)  # noqa:
        if v == "false":
            if is_value.positive:
                return Column(col.native == False)  # noqa:
            else:
                return Column(col.native != False)  # noqa:
        raise NotImplementedError(v)  # pragma: no cover

    def is_in(self, col: Column, *values: Any, positive: bool) -> Column:
        cols = [x for x in values if isinstance(x, Column)]
        others = [x for x in values if not isinstance(x, Column)]
        if positive:
            o: Any = col.native.isin(others)
            for c in cols:
                o = o | col.native == c.native
        else:
            o = ~col.native.isin(others)
            for c in cols:
                o = o & col.native != c.native
        if self.is_series(o) and self.is_series(col.native):
            o = o.mask(col.native.isnull(), None)
        return Column(o)

    def is_between(
        self, col: Column, lower: Column, upper: Column, positive: bool
    ) -> Column:
        ln = lower.native
        cn = col.native
        un = upper.native
        if positive:
            s: Any = (ln <= cn) & (cn <= un)
        else:
            s = (ln > cn) | (cn > un)
        if self.is_series(col.native):
            s = s.mask(col.native.isnull(), None)
        if self.is_series(lower.native):
            s = s.mask(lower.native.isnull(), None)
        if self.is_series(upper.native):
            s = s.mask(upper.native.isnull(), None)
        return Column(s)

    def drop_duplicates(self, df: DataFrame) -> DataFrame:
        ndf = self.to_native(df)
        return self.to_df(self._drop_duplicates(ndf))

    def union(self, df1: DataFrame, df2: DataFrame, unique: bool) -> DataFrame:
        ndf1, ndf2 = self._preprocess_set_op(df1, df2)
        ndf = ndf1.append(ndf2)
        if unique:
            ndf = self._drop_duplicates(ndf)
        return self.to_df(ndf)

    def intersect(self, df1: DataFrame, df2: DataFrame, unique: bool) -> DataFrame:
        ndf1, ndf2 = self._preprocess_set_op(df1, df2)
        ndf = ndf1.merge(self._drop_duplicates(ndf2))
        if unique:
            ndf = self._drop_duplicates(ndf)
        return self.to_df(ndf)

    def except_df(self, df1: DataFrame, df2: DataFrame, unique: bool) -> DataFrame:
        ndf1, ndf2 = self._preprocess_set_op(df1, df2)
        ndf2["__anti_indicator__"] = 1
        ndf = ndf1.merge(ndf2, how="left", on=list(ndf1.columns))
        ndf = ndf[ndf["__anti_indicator__"].isnull()].drop(
            ["__anti_indicator__"], axis=1
        )
        if unique:
            ndf = self._drop_duplicates(ndf)
        return self.to_df(ndf)

    def join(
        self, df1: DataFrame, df2: DataFrame, join_type: str, on: List[str]
    ) -> DataFrame:
        ndf1 = self.to_native(df1)
        ndf2 = self.to_native(df2)
        if join_type == "inner":
            ndf1 = ndf1.dropna(subset=on)
            ndf2 = ndf2.dropna(subset=on)
            joined = ndf1.merge(ndf2, how=join_type, on=on)
        elif join_type == "left_semi":
            ndf1 = ndf1.dropna(subset=on)
            ndf2 = self._drop_duplicates(ndf2[on].dropna())
            joined = ndf1.merge(ndf2, how="inner", on=on)
        elif join_type == "left_anti":
            ndf2 = self._drop_duplicates(ndf2[on].dropna())
            ndf2["__anti_indicator__"] = 1
            joined = ndf1.merge(ndf2, how="left", on=on)
            joined = joined[joined["__anti_indicator__"].isnull()].drop(
                ["__anti_indicator__"], axis=1
            )
        elif join_type == "left_outer":
            ndf2 = ndf2.dropna(subset=on)
            joined = ndf1.merge(ndf2, how="left", on=on)
        elif join_type == "right_outer":
            ndf1 = ndf1.dropna(subset=on)
            joined = ndf1.merge(ndf2, how="right", on=on)
        elif join_type == "full_outer":
            add: List[str] = []
            for f in on:
                name = f + "_null"
                s1 = ndf1[f].isnull().astype(int)
                ndf1[name] = s1
                s2 = ndf2[f].isnull().astype(int) * 2
                ndf2[name] = s2
                add.append(name)
            joined = ndf1.merge(ndf2, how="outer", on=on + add).drop(add, axis=1)
        elif join_type == "cross":
            assert_or_throw(
                len(on) == 0, ValueError(f"cross join can't have join keys {on}")
            )
            ndf1["__cross_indicator__"] = 1
            ndf2["__cross_indicator__"] = 1
            joined = ndf1.merge(ndf2, how="inner", on=["__cross_indicator__"]).drop(
                ["__cross_indicator__"], axis=1
            )
        else:  # pragma: no cover
            raise NotImplementedError(join_type)
        return self.to_df(joined)

    def _set_op_result_to_none(self, series: Any, s1: Any, s2: Any) -> Column:
        if not self.is_series(series):
            if s1 is None or s2 is None:
                return Column(None)
            return Column(series)
        if self.is_series(s1):
            series = series.mask(s1.isnull(), None)
        if self.is_series(s2):
            series = series.mask(s2.isnull(), None)
        return Column(series)

    def _preprocess_set_op(self, df1: DataFrame, df2: DataFrame) -> Tuple[Any, Any]:
        assert_or_throw(
            len(df1) == len(df2),
            ValueError("two dataframes have different number of columns"),
        )
        ndf1 = self.to_native(df1)
        ndf2 = self.to_native(df2)
        ndf2.columns = ndf1.columns  # this is SQL behavior
        return ndf1, ndf2

    def _safe_bool(self, col: Any) -> Any:
        if self.is_series(col):
            return col.astype("f8")
        if self.is_series(col.native):
            return col.native.astype("f8")
        elif col is None:
            return float("nan")
        else:
            return float(col.native > 0)

    def _drop_duplicates(self, ndf: Any) -> Any:
        return ndf.drop_duplicates()
