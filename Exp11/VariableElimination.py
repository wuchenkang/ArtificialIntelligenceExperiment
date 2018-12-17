class VariableElimination:
    @staticmethod
    def inference(factor_list, query_variables,
                  ordered_list_of_hidden_variables, evidence_list):
        # 限制证据变量
        for ev in evidence_list:
            for i in range(len(factor_list)):
                if ev in factor_list[i].var_list:
                    factor_list[i] = factor_list[i].restrict(ev, evidence_list[ev])
        # 求和其他非查询变量
        for var in ordered_list_of_hidden_variables:
            new_factor = None
            deleted_list = []
            for factor in factor_list:
                if var in factor.var_list:
                    if new_factor == None:
                        new_factor = factor
                    else:
                        new_factor = new_factor.multiply(factor)
                    deleted_list.append(factor)
            for factor in deleted_list:
                factor_list.remove(factor)
            new_factor = new_factor.sum_out(var)
            factor_list.append(new_factor)
        print("RESULT: ")

        # 剩余因子相乘并归一化得到结果
        res = factor_list[0]
        for factor in factor_list[1:]:
            res = res.multiply(factor)
        total = sum(res.cpt.values())
        res.cpt = {k: v / total for k, v in res.cpt.items()}
        res.print_inf()

    @staticmethod
    def print_factors(factor_list):
        for factor in factor_list:
            factor.print_inf()


class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.var_list = var_list
        self.cpt = {}

    def set_cpt(self, cpt):
        self.cpt = cpt

    def print_inf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.var_list))
        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))
        print()

    def multiply(self, factor):
        """function that multiplies with another factor"""
        # 两因子变量列表求并集得到乘积的变量列表
        new_list = list(set(self.var_list).union(set(factor.var_list)))

        # 找到两个因子中变量在新因子变量列表中的索引
        self_map = {}
        for i in range(len(self.var_list)):
            self_map[i] = new_list.index(self.var_list[i])
        other_map = {}
        for i in range(len(factor.var_list)):
            other_map[i] = new_list.index(factor.var_list[i])

        # 新因子的CPT表项的值等于两因子中对应项的乘积
        new_cpt = {}
        for i in range(pow(2, len(new_list))):
            key = Util.to_binary(i, len(new_list))
            if len(new_list) == 0:
                key = ''
            self_key  = ''
            for i in range(len(self.var_list)):
                self_key += key[self_map[i]]
            other_key = ''
            for i in range(len(factor.var_list)):
                other_key += key[other_map[i]]
            new_cpt[key] = self.cpt[self_key] * factor.cpt[other_key]

        new_node = Node('f' + str(new_list), new_list)
        new_node.set_cpt(new_cpt)
        return new_node

    def sum_out(self, variable):
        """function that sums out a variable given a factor"""
        # 新因子变量列表为原因子变量列表减去被求和的变量
        sumed_variable = self.var_list.index(variable)
        new_var_list = self.var_list[:sumed_variable] + self.var_list[sumed_variable+1:]

        # 对于新因子CPT中的表项，其值等于原因子与新因子变量取值相同的几个表项的和
        new_cpt = {}
        if sumed_variable == 0:
            for j in range(pow(2, len(new_var_list) - sumed_variable)):
                postfix = Util.to_binary(j, len(new_var_list) - sumed_variable)
                if len(self.var_list) == 1:
                    postfix = ''
                new_cpt[postfix] = self.cpt['0' + postfix] + self.cpt['1' + postfix]
        elif sumed_variable == len(self.var_list) - 1:
            for i in range(pow(2, sumed_variable)):
                    prefix = Util.to_binary(i, sumed_variable)
                    new_cpt[prefix] = self.cpt[prefix + '0'] + self.cpt[prefix + '1']
        else:
            for i in range(pow(2, sumed_variable)):
                prefix = Util.to_binary(i, sumed_variable)
                for j in range(pow(2, len(new_var_list) - sumed_variable)):
                    postfix = Util.to_binary(j, len(new_var_list) - sumed_variable)
                    new_cpt[prefix + postfix] = self.cpt[prefix + '0' + postfix] + self.cpt[prefix + '1' + postfix]
        new_node = Node('f' + str(new_var_list), new_var_list)
        new_node.set_cpt(new_cpt)
        return new_node

    def restrict(self, variable, value):
        """function that restricts a variable to some value
        in a given factor"""
        # 新因子变量列表为原因子变量列表减去被求和的变量
        restricted_variable = self.var_list.index(variable)
        new_var_list = self.var_list[:restricted_variable] + self.var_list[restricted_variable + 1:]

        # 对于新因子CPT中的表项，其值为原因子中与新因子变量取值相同且限制变量取对应值的的单个表项的值
        new_cpt = {}
        if restricted_variable == 0:
            for j in range(pow(2, len(new_var_list) - restricted_variable)):
                postfix = Util.to_binary(j, len(new_var_list) - restricted_variable)
                if len(self.var_list) == 1:
                    postfix = ''
                new_cpt[postfix] = self.cpt[str(value) + postfix]
        elif restricted_variable == len(self.var_list) - 1:
            for i in range(pow(2, restricted_variable)):
                prefix = Util.to_binary(i, restricted_variable)
                new_cpt[prefix] = self.cpt[prefix + str(value)]
        else:
            for i in range(pow(2, restricted_variable)):
                prefix = Util.to_binary(i, restricted_variable)
                for j in range(pow(2, len(new_var_list) - restricted_variable)):
                    postfix = Util.to_binary(j, len(new_var_list) - restricted_variable)
                    new_cpt[prefix + postfix] = self.cpt[prefix + str(value) + postfix]
        new_node = Node('f' + str(new_var_list), new_var_list)
        new_node.set_cpt(new_cpt)
        return new_node


# Create nodes for Bayes Net
B = Node('B', ['B'])
E = Node('E', ['E'])
A = Node('A', ['A', 'B', 'E'])
J = Node('J', ['J', 'A'])
M = Node('M', ['M', 'A'])

# Generate cpt for each node
B.set_cpt({'0': 0.999, '1': 0.001})
E.set_cpt({'0': 0.998, '1': 0.002})
A.set_cpt({'111': 0.95, '011': 0.05, '110': 0.94, '010': 0.06,
           '101':0.29, '001': 0.71, '100': 0.001, '000': 0.999})
J.set_cpt({'11': 0.9, '01': 0.1, '10': 0.05, '00': 0.95})
M.set_cpt({'11': 0.7, '01': 0.3, '10': 0.01, '00': 0.99})

print("P(A) **********************")
VariableElimination.inference([B, E, A, J, M], ['A'], ['B', 'E', 'J', 'M'], {})

print("P(B | J, ~M) **********************")
VariableElimination.inference([B, E, A, J, M], ['B'], ['E', 'A'], {'J':1, 'M':0})