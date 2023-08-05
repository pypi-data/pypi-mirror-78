__version__ = "0.1.0"


def generate_dcostring(first_notation, second_notation, name):
    notations = {
        "F": "Future worth, value, or amount",
        "P": "Present worth, value, or amount",
        "A": "Uniform amount per interest period",
        "G": "Uniform gradient amount per interest period",
    }
    docstring = f"""
       Factor applies to {first_notation}/{second_notation} => to {first_notation} ({notations[first_notation]}) given {second_notation} ({notations[second_notation]})

       :param i: Interest rate per interest period

       :param n: Number of compounding periods

       :return: {name} factor
       """

    def dec(obj):
        obj.__doc__ = docstring
        return obj

    return dec
