from allokation.utils import (calculate_amount, calculate_multiplier,
                              calculate_percentage_of_each_ticker,
                              calculate_total_for_each_ticker,
                              get_closing_price_from_yahoo, get_target_date,
                              map_columns_without_suffix, transpose_prices)


def allocate_money(available_money, tickers):
    # import ipdb; ipdb.set_trace()
    target_date = get_target_date()
    prices = get_closing_price_from_yahoo(tickers=tickers, date=target_date)
    renamed_columns = map_columns_without_suffix(tickers)
    prices.rename(columns=renamed_columns, inplace=True)
    df = transpose_prices(prices)
    multiplier = calculate_multiplier(df, number_of_tickers=len(tickers), available_money=available_money)

    df['amount'] = calculate_amount(df, multiplier)
    df['total'] = calculate_total_for_each_ticker(df)
    df['percentage'] = calculate_percentage_of_each_ticker(df)

    result = {}
    result['allocations'] = df.set_index('symbol').T.to_dict()
    result['total_value'] = df["total"].sum()

    return result
