#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import enum
from datetime import datetime
from typing import Tuple

from hypothesis import strategies as st
from hypothesis.strategies import composite

from xotless.ranges import Range
from xotless.tests.strategies.domains import (
    float_ranges,
    numbers,
    many_float_ranges,
    many_date_ranges,
)

from ...types import Result, Undefined, TypedAttribute, SimpleType
from ...predicates import (
    ValidityPredicate,
    ExecutionPredicate,
    QuantityPredicate,
    MatchesAttributePredicate,
    AttributeInRangePredicate,
)
from ...procedures import (
    ConstantProcedure,
    GetAttributeProcedure,
    UndefinedProcedure,
    VarnameProcedure,
    CeilRoundingProcedure,
    FloorRoundingProcedure,
    RoundProcedure,
)
from ...aggregators import (
    SumAggregator,
    MultAggregator,
    DivideAggregator,
    MaxAggregator,
    MinAggregator,
    CountAggregator,
    TakeFirstAggregator,
    TakeLastAggregator,
    ModeAggregator,
    AverageAggregator,
)
from ...splitters import (
    UnitSplitter,
    UnitRequestSplitter,
    RequestSplitter,
    IdentitySplitter,
)

st.register_type_strategy(type(Undefined), st.just(Undefined))
st.register_type_strategy(Result, numbers | st.just(Undefined))  # type: ignore

nonnumerical_attributes = st.sampled_from(["code", "place"])
numerical_attributes = st.sampled_from(["pax_count"])
attributes = numerical_attributes | nonnumerical_attributes
variables = st.integers(min_value=0, max_value=100).map(lambda n: f"var{n}")
margins = st.floats(allow_infinity=False, allow_nan=False, min_value=0, max_value=1.0)
ratios = st.floats(
    allow_infinity=False, allow_nan=False, min_value=1 / 100, max_value=1.0
)


class OCCUPATION(enum.Enum):
    SGL = "SGL"
    DBL = "DBL"
    TPL = "TPL"
    SGL_Enf = "SGL + 1 Enf"
    SGL_2Enf = "SGL + 2 Enf"
    DBL_Enf = "DBL + 1 Enf"


OCCUPATIONS = st.sampled_from(OCCUPATION)
ATTR_OCCUPATION = TypedAttribute("occupation", SimpleType.from_python_enum(OCCUPATION))
occupation_attr_predicates = OCCUPATIONS.map(
    lambda val: MatchesAttributePredicate(ATTR_OCCUPATION, val)
)

other_attribute_match_predicates = st.tuples(numerical_attributes, numbers).map(
    lambda args: MatchesAttributePredicate(
        TypedAttribute(args[0], SimpleType.from_python_type(float)), args[1]
    )
)
attribute_range_predicates = st.tuples(numerical_attributes, float_ranges()).map(
    lambda args: AttributeInRangePredicate(
        TypedAttribute(args[0], SimpleType.from_python_type(float)), *args[1]
    )
)

constant_procs = numbers.map(lambda n: ConstantProcedure(n))
undefined_procs = st.just(UndefinedProcedure())
getattr_procs = numerical_attributes.map(
    lambda attr: GetAttributeProcedure(
        TypedAttribute(attr, SimpleType.from_python_type(float))
    )
)
getvar_procs = st.tuples(variables, numbers).map(
    lambda args: VarnameProcedure(args[0], default=args[1])
)
basic_procedures = constant_procs | undefined_procs | getattr_procs | getvar_procs
aggregator_classes = st.sampled_from(
    [
        SumAggregator,
        MultAggregator,
        DivideAggregator,
        MaxAggregator,
        MinAggregator,
        CountAggregator,
        TakeFirstAggregator,
        TakeLastAggregator,
        ModeAggregator,
        AverageAggregator,
    ]
)
aggregators = aggregator_classes.map(lambda cls: cls())
splitter_classes = st.sampled_from(
    [IdentitySplitter, UnitSplitter, UnitRequestSplitter, RequestSplitter]
)
splitters = splitter_classes.map(lambda cls: cls())
round_procedure_types = st.sampled_from(
    [CeilRoundingProcedure, FloorRoundingProcedure, RoundProcedure]
)


@composite
def validity_preds(draw, many=4, outer=None) -> Tuple[ValidityPredicate, ...]:
    if outer is None:
        outer = FIVE_YEARS_RANGE
    ranges = draw(many_date_ranges(many, outer=outer))
    return tuple(ValidityPredicate(*r) for r in ranges)


@composite
def execution_preds(draw, many=4, outer=None):
    if outer is None:
        outer = FIVE_YEARS_RANGE
    ranges = draw(many_date_ranges(many, outer=outer))
    return tuple(ExecutionPredicate(*r) for r in ranges)


@composite
def quantity_preds(draw, many=4, outer=None):
    if outer is None:
        outer = Range.new_open_right(0, 100)
    ranges = draw(many_float_ranges(many, outer=outer))
    return tuple(
        QuantityPredicate(safe_int(r.lowerbound), safe_int(r.upperbound)) for r in ranges
    )


def safe_int(val):
    from xotl.tools.infinity import Infinity

    if val is Infinity or val is -Infinity:
        return val
    else:
        return int(val)


TODAY = datetime.now()
FIVE_YEARS_RANGE = Range.new_open_right(
    TODAY.replace(year=TODAY.year - 1), TODAY.replace(year=TODAY.year + 4)
)
