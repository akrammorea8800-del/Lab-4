class Item:
    def __init__(self, symbol, weight, value):
        self.symbol, self.weight, self.value = symbol, weight, value


def knapsack(items, capacity):
    def node_bound_count(i, weight, value):
        if weight > capacity:
            return 0
        node_value = value
        j = i
        total_weight = weight
        while j < len(items) and total_weight + items[j].weight <= capacity:
            node_value += items[j].value
            total_weight += items[j].weight
            j += 1
        if j < len(items):
            node_value += (capacity - total_weight) * (items[j].value / items[j].weight)
        return node_value

    def branch_bound(i, weight, value, chosen):
        nonlocal max_value, best
        if weight <= capacity and value > max_value:
            max_value, best = value, chosen
        if i == len(items):
            return 0
        if node_bound_count(i, weight, value) > max_value:
            branch_bound(i + 1, weight, value, chosen)
        if value + (capacity - weight) * (items[i].value / items[i].weight) > max_value:
            branch_bound(i + 1, weight + items[i].weight, value + items[i].value, chosen + [items[i]])

    items = sorted(items, key=lambda x: x.value / x.weight, reverse=True)
    max_value, best = 0, []
    branch_bound(0, 0, 0, [])
    return max_value, best


if __name__ == '__main__':
    items = [Item('r', 3, 25), Item('p', 2, 15), Item('a', 2, 15),
             Item('m', 2, 20), Item('i', 1, 5), Item('k', 1, 15),
             Item('x', 3, 20), Item('t', 1, 25), Item('f', 1, 15),
             Item('d', 1, 10), Item('s', 2, 20), Item('c', 2, 20)]
    capacity = 8
    max_value, best = knapsack(items, capacity)
    cells = [item.symbol for item in best for _ in range(item.weight)]
    for i in range(0, 8, 4):
        print(','.join(f'[{s}]' for s in cells[i:i + 4]))
    score = 15 + 2 * max_value - sum(item.value for item in items)
    print('Итоговые очки выживания:', score)
    print('Условие выполнено' if score > 0 else 'Условие не выполнено')
