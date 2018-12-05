import pomegranate as pg


def cal_prob(model, domain_list, predict_list):
    iter_count = 1
    for i in range(model.node_count()):
        if predict_list[i] is None:
            iter_count *= len(domain_list[i])

    top = 0
    for i in range(iter_count):
        temp_val = iter_count
        temp_list = []
        for j in range(model.node_count()):
            if predict_list[j] is not None:
                temp_list.append(predict_list[j])
            else:
                temp_val //= len(domain_list[j])
                temp_list.append(domain_list[j][(i // temp_val) % len(domain_list[j])])
        top += model.probability(temp_list)

    return top


def cal_cond_prob(model, domain_list, predict_list, condition_list):
    for i in range(len(predict_list)):
        if predict_list[i] is None and condition_list[i] is not None:
            predict_list[i] = condition_list[i]
    return cal_prob(model, domain_list, predict_list) / cal_prob(model, domain_list, condition_list)


if __name__ == "__main__":
    # The probability that guest choose a door
    guest = pg.DiscreteDistribution({'A': 1 / 3, 'B': 1 / 3, 'C': 1 / 3})
    # The probability that prize is behind a door
    prize = pg.DiscreteDistribution({'A': 1 / 3, 'B': 1 / 3, 'C': 1 / 3})
    # The probability that Monty open a door
    monty = pg.ConditionalProbabilityTable(
        [['A', 'A', 'A', 0.0],
         ['A', 'A', 'B', 0.5],
         ['A', 'A', 'C', 0.5],
         ['A', 'B', 'A', 0.0],
         ['A', 'B', 'B', 0.0],
         ['A', 'B', 'C', 1.0],
         ['A', 'C', 'A', 0.0],
         ['A', 'C', 'B', 1.0],
         ['A', 'C', 'C', 0.0],
         ['B', 'A', 'A', 0.0],
         ['B', 'A', 'B', 0.0],
         ['B', 'A', 'C', 1.0],
         ['B', 'B', 'A', 0.5],
         ['B', 'B', 'B', 0.0],
         ['B', 'B', 'C', 0.5],
         ['B', 'C', 'A', 1.0],
         ['B', 'C', 'B', 0.0],
         ['B', 'C', 'C', 0.0],
         ['C', 'A', 'A', 0.0],
         ['C', 'A', 'B', 1.0],
         ['C', 'A', 'C', 0.0],
         ['C', 'B', 'A', 1.0],
         ['C', 'B', 'B', 0.0],
         ['C', 'B', 'C', 0.0],
         ['C', 'C', 'A', 0.5],
         ['C', 'C', 'B', 0.5],
         ['C', 'C', 'C', 0.0]], [guest, prize])

    # Create nodes of guest, prize and monty
    s1 = pg.Node(guest, name="guest")
    s2 = pg.Node(prize, name="prize")
    s3 = pg.Node(monty, name="monty")

    # Build a bayes net
    model = pg.BayesianNetwork("Monty Hall Problem")
    model.add_states(s1, s2, s3)
    model.add_edge(s1, s3)
    model.add_edge(s2, s3)
    model.bake()

    # Calculate the probability
    print("P['A', 'C', 'B']:\t", model.probability(['A', 'B', 'C']))
    print("P['A', 'C', 'A']:\t", model.probability(['A', 'B', 'B']))

    # Probability
    burglary = pg.DiscreteDistribution({'T': 0.001, 'F': 0.999})
    earthquake = pg.DiscreteDistribution({'T': 0.002, 'F': 0.998})
    alarm = pg.ConditionalProbabilityTable(
        [['T', 'T', 'T', 0.95],
         ['T', 'T', 'F', 0.05],
         ['T', 'F', 'T', 0.94],
         ['T', 'F', 'F', 0.06],
         ['F', 'T', 'T', 0.29],
         ['F', 'T', 'F', 0.71],
         ['F', 'F', 'T', 0.001],
         ['F', 'F', 'F', 0.999]], [burglary, earthquake]
    )
    john = pg.ConditionalProbabilityTable(
        [['T', 'T', 0.9],
         ['T', 'F', 0.1],
         ['F', 'T', 0.05],
         ['F', 'F', 0.95]], [alarm]
    )
    mary = pg.ConditionalProbabilityTable(
        [['T', 'T', 0.7],
         ['T', 'F', 0.3],
         ['F', 'T', 0.01],
         ['F', 'F', 0.99]], [alarm]
    )

    # Create nodes
    s1 = pg.Node(burglary, name="Burglary")
    s2 = pg.Node(earthquake, name="Earthquake")
    s3 = pg.Node(alarm, name="Alarm")
    s4 = pg.Node(john, name="JohnCalls")
    s5 = pg.Node(mary, name="MaryCalls")

    # Build a bayes net
    model = pg.BayesianNetwork("Burglary")
    model.add_states(s1, s2, s3, s4, s5)
    model.add_edge(s1, s3)
    model.add_edge(s2, s3)
    model.add_edge(s3, s4)
    model.add_edge(s3, s5)
    model.bake()

    print(cal_prob(model, [['T', 'F'] for _ in range(5)], ['T', 'T', 'T', None, None]))
    print(cal_cond_prob(model, [['T', 'F'] for _ in range(5)], [None, None, 'T', None, None], [None, None, None, 'T', 'T']))
