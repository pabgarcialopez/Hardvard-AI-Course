from logic import *

# Symbols for A, B, and C
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# A new symbol to capture what A said:
# ASaidKnave is True if A said "I am a Knave", and False if A said "I am a Knight".
ASaidKnave = Symbol("A said 'I am a Knave'")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a knight or a knave, but not both.
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # A's statement is: "I am both a knight and a knave."
    # The biconditional enforces that if A is a knight then his statement is true, and if A is a knave then his statement is false.
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A and B are both either a Knight ot a Knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    # But not both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A and B are both either a Knight ot a Knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    # But not both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # They are of the same kind
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # They are of diiferent kinds
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

knowledge3 = And(
    # Each person is either a Knight or a Knave (but not both).
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A's statement:
    # If ASaidKnave is true, then A said "I am a Knave" (i.e., his statement is AKnave).
    # If ASaidKnave is false, then A said "I am a Knight" (i.e., his statement is AKnight).
    Biconditional(AKnight, Or(And(ASaidKnave, AKnave),
                                And(Not(ASaidKnave), AKnight))),

    # B says: "A said 'I am a Knave'." 
    # (If B is a Knight, then it must be true that ASaidKnave is true.)
    Biconditional(BKnight, ASaidKnave),

    # B says: "C is a Knave."
    Biconditional(BKnight, CKnave),

    # C says: "A is a Knight."
    Biconditional(CKnight, AKnight)
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
