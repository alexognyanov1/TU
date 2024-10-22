from collections import defaultdict


def find_most_valuable_currency(rates):
    graph = defaultdict(list)

    for rate in rates:
        graph[rate['from']].append((rate['to'], rate['multiplier']))
        graph[rate['to']].append((rate['from'], 1 / rate['multiplier']))

    base_currency = rates[0]['from']
    relative_values = {base_currency: 1}

    def dfs(currency, value):
        for neighbor, multiplier in graph[currency]:
            if neighbor not in relative_values:
                relative_values[neighbor] = value * multiplier
                dfs(neighbor, relative_values[neighbor])

    dfs(base_currency, 1)

    most_valuable = min(relative_values, key=relative_values.get)
    return most_valuable, relative_values[most_valuable]


rates = [
    {'from': 'USD', 'to': 'EUR', 'multiplier': 0.85},
    {'from': 'EUR', 'to': 'GBP', 'multiplier': 0.9},
    {'from': 'GBP', 'to': 'JPY', 'multiplier': 150},
    {'from': 'USD', 'to': 'JPY', 'multiplier': 110}
]

most_valuable_currency, value = find_most_valuable_currency(rates)
print(
    f"The most valuable currency is {most_valuable_currency} with a relative value of {value}")
