# 创建初始候选集
def apriori(data_set):
    # 候选项1项集
    c1 = set()
    for items in data_set:
        for item in items:
            item_set = frozenset([item])
            c1.add(item_set)

# 从候选项集中选出频繁项集
def generate_freq_supports(data_set, item_set, min_support):
    freq_set = set()  # 保存频繁项集元素
    item_count = {}  # 保存元素频次，用于计算支持度
    supports = {}  # 保存支持度

    # 如果项集中元素在数据集中则计数
    for record in data_set: # data_set为初始的数据
        for item in item_set:
            if item.issubset(record): # 判断集合元素是否在record中
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1

    data_len = float(len(data_set))

    # 计算项集支持度
    for item in item_count:
        if (item_count[item] / data_len) >= min_support:
            freq_set.add(item)
            supports[item] = item_count[item] / data_len

    return freq_set, supports

# 生成新组合
def generate_new_combinations(freq_set, k):
    new_combinations = set()  # 保存新组合
    sets_len = len(freq_set)  # 集合含有元素个数，用于遍历求得组合
    freq_set_list = list(freq_set)  # 集合转为列表用于索引

    for i in range(sets_len):
        for j in range(i + 1, sets_len):
            l1 = list(freq_set_list[i])
            l2 = list(freq_set_list[j])
            l1.sort()
            l2.sort()
            # 项集若有相同的父集则合并项集
            if l1[0:k-1] == l2[0:k-1]:
                freq_item = freq_set_list[i] | freq_set_list[j]
                new_combinations.add(freq_item)

    return new_combinations

# 循环生成候选集集频繁集
def apriori(data_set, min_support, max_len=None):
    max_items = 1  # 初始项集元素个数
    freq_sets = []  # 保存所有频繁项集
    supports = {}  # 保存所有支持度

    # 候选项1项集
    c1 = set()
    for items in data_set:
        for item in items:
            item_set = frozenset([item])
            c1.add(item_set)

    # 频繁项1项集及其支持度
    l1, support1 = generate_freq_supports(data_set, c1, min_support)

    freq_sets.append(l1)
    supports.update(support1)

    if max_len is None:
        max_len = float('inf')

    while max_items and max_items <= max_len:
        ci = generate_new_combinations(freq_sets[-1], max_items)  # 生成候选集
        li, support = generate_freq_supports(data_set, ci, min_support)  # 生成频繁项集和支持度

        # 如果有频繁项集则进入下个循环
        if li:
            freq_sets.append(li)
            supports.update(support)
            max_items += 1
        else:
            max_items = 0

    return freq_sets, supports

# 生成关联规则
def association_rules(freq_sets, supports, min_conf):
    rules = []
    max_len = len(freq_sets)

    # 生成关联规则，筛选符合规则的频繁集计算置信度，满足最小置信度的关联规则添加到列表
    for k in range(max_len - 1): # 层数
        for freq_set in freq_sets[k]: #k层元素
            for index in range(k+1,max_len):# k层与后面的层都进行计算
                for sub_set in freq_sets[index]:
                    if freq_set.issubset(sub_set):
                        conf = supports[sub_set] / supports[freq_set]
                        rule = (freq_set, sub_set - freq_set, conf)
                        if conf >= min_conf:
                            rules.append(rule)


    return rules
if __name__ == '__main__':
     # data = [[1, 2, 4, 5], [2, 3, 4], [1, 2, 4, 5], [1, 3, 4, 5], [2, 3, 4, 5],
     #         [2, 4, 5], [3, 4], [1, 2, 3], [1, 4, 5], [2, 4]]
    data = [['a', 'b', 'd','e'],
            ['b', 'c', 'd'],
            ['a', 'b', 'd', 'e'],
            ['a', 'c', 'd', 'e'],
            ['b', 'c', 'd', 'e'],
            ['b', 'd', 'e'],
            ['c', 'd'],
            ['a', 'b', 'c'],
            ['a', 'd', 'e'],
            ['b', 'd']]
    L, support_data = apriori(data, min_support=0.3)

    print('='*50)
    print('频繁集 \t\t\t 支持度')
    print('='*50)
    index = 0
    for i in L:
        for j in i:
            index+=1
            print(set(j), '\t\t\t\t', support_data[j])
    print("一共%d"%index,"条数据")
    print()
    print('='*50)
    print('antecedent consequent \t\t\t置信度')
    print('='*50)
    rules = association_rules(L, support_data, min_conf=0.5)
    index=0
    for _rule in rules:
        print('{}  =>  {}\t\t\t\t{}'.format(set(_rule[0]), set(_rule[1]),_rule[2]))
        index += 1
    print("一共%d" % index, "条数据")

a = [i/10.0 for i in range(1, 10)]
acc=[]
import matplotlib.pyplot as plt
for min_suport in a:
    L, support_data = apriori(data, min_support=min_suport)
    length = len(L)
    x = 0
    for i in range(length):
        x+=len(L[i])
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.xlabel("min_support")
    plt.ylabel("频繁集个数")
    acc.append(x)
plt.plot(a, acc)
plt.show()
acc.clear()
for min_conf in a:
    L, support_data = apriori(data, min_support=0.2)
    rules = association_rules(L, support_data, min_conf=min_conf)
    length = len(rules)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.xlabel("min_conf")
    plt.ylabel("关联规则个数")
    acc.append(length)
plt.plot(a, acc)
plt.show()

