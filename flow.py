from graphviz import Digraph

# フローチャートのインスタンスを作成
dot = Digraph()

# ノードを追加
dot.node('1', '朝日焼ランク判定(お手本なし)')
dot.node('2', '朝日焼ランク判定(お手本あり)')
dot.node('3', '中川木工芸ランク判定(お手本なし)')
dot.node('4', '中川木工芸ランク判定(お手本あり)')
dot.node('5', '朝日焼正面画像判定(お手本なし)')
dot.node('6', '朝日焼正面画像判定(お手本あり)')

# 矢印でノードをつなぐ
dot.edge('1', '2')
dot.edge('2', '3')
dot.edge('3', '4')
dot.edge('4', '5')
dot.edge('5', '6')

# フローチャートを表示
dot.render('evaluation_flowchart', format='png', cleanup=False)
