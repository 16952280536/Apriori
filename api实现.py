import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

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

te = TransactionEncoder()
te_ary = te.fit(data).transform(data)
df = pd.DataFrame(te_ary, columns=te.columns_)
frequent_itemsets = apriori(df, min_support=0.3, use_colnames=True)
rules = association_rules(frequent_itemsets, min_threshold=0.5)
print(te_ary)
print(frequent_itemsets)
print(rules)