import pomegranate as pg


def cal_prob(network, domain_list, predict_list):
    iter_count = 1
    for i in range(network.node_count()):
        if predict_list[i] is None:
            iter_count *= len(domain_list[i])

    result = 0
    for i in range(iter_count):
        temp_val = iter_count
        temp_list = []
        for j in range(network.node_count()):
            if predict_list[j] is not None:
                temp_list.append(predict_list[j])
            else:
                temp_val //= len(domain_list[j])
                temp_list.append(domain_list[j][(i // temp_val) % len(domain_list[j])])
        result += network.probability(temp_list)

    return result


def cal_cond_prob(network, domain_list, predict_list, condition_list):
    for i in range(len(predict_list)):
        if predict_list[i] is None and condition_list[i] is not None:
            predict_list[i] = condition_list[i]
    return cal_prob(network, domain_list, predict_list) / cal_prob(network, domain_list, condition_list)


if __name__ == "__main__":
    print("Monty Hall problem")
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
    print("P['A', 'C', 'B'] = ", model.probability(['A', 'B', 'C']))
    print("P['A', 'C', 'A'] = ", model.probability(['A', 'B', 'B']))

    print()

    print("Burglary")
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

    # Calculate the probability
    print("P(JohnCalls, MaryCalls) = ", cal_prob(model, [['T', 'F'] for _ in range(5)], [None, None, None, 'T', 'T']))
    print("P(Burglary, Earthquake, Alarm, JohnCalls, MaryCalls) = ", cal_prob(model, [['T', 'F'] for _ in range(5)], ['T', 'T', 'T', 'T', 'T']))
    print("P(Alarm | JohnCalls, MaryCalls) = ", cal_cond_prob(model, [['T', 'F'] for _ in range(5)], [None, None, 'T', None, None], [None, None, None, 'T', 'T']))
    print("P(JohnCalls, ￢MaryCalls | ￢Burglary) = ", cal_cond_prob(model, [['T', 'F'] for _ in range(5)], [None, None, None, 'T', 'F'], ['F', None, None, None, None]))

    print()

    print("Diagnosing")
    # Probability
    patientAge = pg.DiscreteDistribution({'0-30': 0.1, '31-65': 0.3, '65+': 0.6})
    ctScanResult = pg.DiscreteDistribution({'Ischemic Stroke': 0.7, 'Hemmorraghic Stroke': 0.3})
    mriScanResult = pg.DiscreteDistribution({'Ischemic Stroke': 0.7, 'Hemmorraghic Stroke': 0.3})
    anticoagulants = pg.DiscreteDistribution({'Used': 0.5, 'Not used': 0.5})
    strokeType = pg.ConditionalProbabilityTable(
        [['Ischemic Stroke', 'Ischemic Stroke', 'Ischemic Stroke', 0.8],
         ['Ischemic Stroke', 'Hemmorraghic Stroke', 'Ischemic Stroke', 0.5],
         ['Hemmorraghic Stroke', 'Ischemic Stroke', 'Ischemic Stroke', 0.5],
         ['Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Ischemic Stroke', 0],

         ['Ischemic Stroke', 'Ischemic Stroke', 'Hemmorraghic Stroke', 0],
         ['Ischemic Stroke', 'Hemmorraghic Stroke', 'Hemmorraghic Stroke', 0.4],
         ['Hemmorraghic Stroke', 'Ischemic Stroke', 'Hemmorraghic Stroke', 0.4],
         ['Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Hemmorraghic Stroke', 0.9],

         ['Ischemic Stroke', 'Ischemic Stroke', 'Stroke Mimic', 0.2],
         ['Ischemic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic', 0.1],
         ['Hemmorraghic Stroke', 'Ischemic Stroke', 'Stroke Mimic', 0.1],
         ['Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic', 0.1]], [ctScanResult, mriScanResult]
    )
    mortality = pg.ConditionalProbabilityTable(
        [['Ischemic Stroke', 'Used', 'False', 0.28],
         ['Hemmorraghic Stroke', 'Used', 'False', 0.99],
         ['Stroke Mimic', 'Used', 'False', 0.1],
         ['Ischemic Stroke', 'Not used', 'False', 0.56],
         ['Hemmorraghic Stroke', 'Not used', 'False', 0.58],
         ['Stroke Mimic', 'Not used', 'False', 0.05],

         ['Ischemic Stroke', 'Used', 'True', 0.72],
         ['Hemmorraghic Stroke', 'Used', 'True', 0.01],
         ['Stroke Mimic', 'Used', 'True', 0.9],
         ['Ischemic Stroke', 'Not used', 'True', 0.44],
         ['Hemmorraghic Stroke', 'Not used', 'True', 0.42],
         ['Stroke Mimic', 'Not used', 'True', 0.95]], [strokeType, anticoagulants]
    )
    disability = pg.ConditionalProbabilityTable(
        [['Ischemic Stroke', '0-30', 'Negligible', 0.8],
         ['Hemmorraghic Stroke', '0-30', 'Negligible', 0.7],
         ['Stroke Mimic', '0-30', 'Negligible', 0.9],
         ['Ischemic Stroke', '31-65', 'Negligible', 0.6],
         ['Hemmorraghic Stroke', '31-65', 'Negligible', 0.5],
         ['Stroke Mimic', '31-65', 'Negligible', 0.4],
         ['Ischemic Stroke', '65+', 'Negligible', 0.3],
         ['Hemmorraghic Stroke', '65+', 'Negligible', 0.2],
         ['Stroke Mimic', '65+', 'Negligible', 0.1],

         ['Ischemic Stroke', '0-30', 'Moderate', 0.1],
         ['Hemmorraghic Stroke', '0-30', 'Moderate', 0.2],
         ['Stroke Mimic', '0-30', 'Moderate', 0.05],
         ['Ischemic Stroke', '31-65', 'Moderate', 0.3],
         ['Hemmorraghic Stroke', '31-65', 'Moderate', 0.4],
         ['Stroke Mimic', '31-65', 'Moderate', 0.3],
         ['Ischemic Stroke', '65+', 'Moderate', 0.4],
         ['Hemmorraghic Stroke', '65+', 'Moderate', 0.2],
         ['Stroke Mimic', '65+', 'Moderate', 0.1],

         ['Ischemic Stroke', '0-30', 'Severe', 0.1],
         ['Hemmorraghic Stroke', '0-30', 'Severe', 0.1],
         ['Stroke Mimic', '0-30', 'Severe', 0.05],
         ['Ischemic Stroke', '31-65', 'Severe', 0.1],
         ['Hemmorraghic Stroke', '31-65', 'Severe', 0.1],
         ['Stroke Mimic', '31-65', 'Severe', 0.3],
         ['Ischemic Stroke', '65+', 'Severe', 0.3],
         ['Hemmorraghic Stroke', '65+', 'Severe', 0.6],
         ['Stroke Mimic', '65+', 'Severe', 0.8]], [strokeType, patientAge]
    )

    # Create nodes of guest, prize and monty
    s1 = pg.Node(patientAge, name="PatientAge")
    s2 = pg.Node(ctScanResult, name="CTScanResult")
    s3 = pg.Node(mriScanResult, name="MRIScanResult")
    s4 = pg.Node(anticoagulants, name="Anticoagulants")
    s5 = pg.Node(strokeType, name="StrokeType")
    s6 = pg.Node(disability, name="Disability")
    s7 = pg.Node(mortality, name="Mortality")

    # Build a bayes net
    model = pg.BayesianNetwork("Diagnosing")
    model.add_states(s1, s2, s3, s4, s5, s6, s7)
    model.add_edge(s1, s6)
    model.add_edge(s2, s5)
    model.add_edge(s3, s5)
    model.add_edge(s5, s6)
    model.add_edge(s5, s7)
    model.add_edge(s4, s7)
    model.bake()

    # Calculate the probability
    domainList = [['0-30', '31-65', '65+'],
                  ['Ischemic Stroke', 'Hemmorraghic Stroke'],
                  ['Ischemic Stroke', 'Hemmorraghic Stroke'],
                  ['Used', 'Not used'],
                  ['Ischemic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic'],
                  ['Negligible', 'Moderate', 'Severe'],
                  ['True', 'False']]
    print("P(Mortality='True' | PatientAge='0-30' , CTScanResult='Ischemic Stroke') = ",
          cal_cond_prob(model, domainList, [None, None, None, None, None, None, 'True'],
                        ['0-30', 'Ischemic Stroke', None, None, None, None, None]))
    print("P(Disability='Severe ' | PatientAge='65+' , MRIScanResult='Ischemic Stroke') = ",
          cal_cond_prob(model, domainList, [None, None, None, None, None, 'Severe', None],
                        ['65+', None, 'Ischemic Stroke', None, None, None, None]))
    print("P(StrokeType='Stroke Mimic' | PatientAge='65+', \
            \n\tCTScanResult='Hemmorraghic Stroke', MRIScanResult='Ischemic Stroke') = ",
          cal_cond_prob(model, domainList, [None, None, None, None, 'Stroke Mimic', None, None],
                        ['65+', 'Hemmorraghic Stroke', 'Ischemic Stroke', None, None, None, None]))
    print("P(Mortality='False' | PatientAge='0-30', \
            \n\tAnticoagulants=’Used’, StrokeType='Stroke Mimic') = ",
          cal_cond_prob(model, domainList, [None, None, None, None, None, None, 'False'],
                        ['0-30', None, None, 'Used', 'Stroke Mimic', None, None]))
    print("P(PatientAge='0-30', CTScanResult='Ischemic Stroke', \
            \n\tMRIScanResult='Hemmorraghic Stroke', Anticoagulants='Used', \
            \n\tStrokeType='Stroke Mimic', Disability='Severe', Mortality ='False') = ",
          cal_prob(model, domainList, ['0-30', 'Ischemic Stroke', 'Hemmorraghic Stroke', 'Used', 'Stroke Mimic', 'Severe', 'False']))
