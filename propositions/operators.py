# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2022
# File name: propositions/operators.py

"""Syntactic conversion of propositional formulas to use only specific sets of
operators."""

from propositions.semantics import *


def to_not_and_or(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'``, ``'&'``, and ``'|'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'``, ``'&'``, and
        ``'|'``.
    """
    # Task 3.5
    if is_variable(formula.root):
        return formula

    if is_constant(formula.root):
        if formula.root == "T":
            return Formula.parse("(p|~p)")

        return Formula.parse("(p&~p)")

    if is_unary(formula.root):
        return Formula("~", to_not_and_or(formula.first))

    new_first = to_not_and_or(formula.first)
    new_second = to_not_and_or(formula.second)

    op = formula.root
    if op == "&" or op == "|":
        return Formula(op, new_first, new_second)

    if op == "->":
        return Formula("|", Formula("~", new_first), new_second)

    if op == "+":
        return Formula("|",
                       Formula("&", new_first, Formula("~", new_second)),
                       Formula("&", Formula("~", new_first), new_second))

    if op == "<->":
        return Formula("|",
                       Formula("&", new_first, new_second),
                       Formula("&", Formula("~", new_first), Formula("~", new_second)))

    if op == "-&":
        return Formula("~", Formula("&", new_first, new_second))

    if op == "-|":
        return Formula("~", Formula("|", new_first, new_second))

    raise ValueError(f"Unknown operator: {op}")


def to_not_and(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'`` and ``'&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'`` and ``'&'``.
    """
    # Task 3.6a
    return to_not_and_or(formula).substitute_operators({"|": Formula.parse("~(~p&~q)")})


def to_nand(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'-&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'-&'``.
    """
    # Task 3.6b
    return to_not_and_or(formula).substitute_operators({
        "~": Formula.parse("(p-&p)"),
        "&": Formula.parse("((p-&q)-&(p-&q))"),
        "|": Formula.parse("((p-&p)-&(q-&q))")
    })


def to_implies_not(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'~'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'~'``.
    """
    # Task 3.6c
    return to_not_and_or(formula).substitute_operators({
        "|": Formula.parse("(~p->q)"),
        "&": Formula.parse("~(p->~q)")
    })


def to_implies_false(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'F'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'F'``.
    """
    # Task 3.6d
    return to_not_and_or(formula).substitute_operators({
        "~": Formula.parse("(p->F)"),
        "|": Formula.parse("((p->F)->q)"),
        "&": Formula.parse("((p->(q->F))->F)")
    })
