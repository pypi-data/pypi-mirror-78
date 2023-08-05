from eng_econ import generate_dcostring


@generate_dcostring("F", "P", "Single payment compound amount")
def single_payment_compound_amount_factor(i, n):
    return (1 + i) ** n


@generate_dcostring("P", "F", "Single payment present worth")
def single_payment_present_worth_factor(i, n):
    return (1 + i) ** (-n)


@generate_dcostring("A", "F", "Uniform series sinking fund")
def uniform_series_sinking_fund_factor(i, n):
    return i / ((1 + i) ** n - 1)


@generate_dcostring("A", "P", "Capital recovery")
def capital_recovery_factor(i, n):
    temporary = (1 + i) ** n
    return i * temporary / (temporary - 1)


@generate_dcostring("F", "A", "Uniform series compound amount")
def uniform_series_compound_amount_factor(i, n):
    return ((1 + i) ** n - 1) / i


@generate_dcostring("P", "A", "Uniform series present worth")
def uniform_series_present_wortht_factor(i, n):
    temporary = (1 + i) ** n
    return (temporary - 1) / (i * temporary)


@generate_dcostring("P", "G", "uniform gradient present worth")
def uniform_gradient_present_worth_factor(i, n):
    temporary = (1 + i) ** n
    return (temporary - 1) / (i ** 2 * temporary) - (n / (i * temporary))


@generate_dcostring("F", "G", "uniform gradient future worth")
def uniform_gradient_future_worth_factor(i, n):
    return ((1 + i) ** n - 1) / (i ** 2) - (n / i)


@generate_dcostring("A", "G", "Uniform gradient uniform series")
def uniform_gradient_uniform_series_factor(i, n):
    return 1 / i - (n / ((1 + i) ** n - 1))
