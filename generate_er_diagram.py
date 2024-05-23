import pydot
from django.apps import apps
from django.db import models
import os
import django

# Django settingsの設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # 'your_project_name'を実際のプロジェクト名に置き換えてください
django.setup()

def generate_er_diagram(app_label):
    app = apps.get_app_config(app_label)
    graph = pydot.Dot(graph_type='digraph')

    for model in app.get_models():
        model_name = model.__name__
        fields = [f"{field.name}: {field.get_internal_type()}" for field in model._meta.fields]
        label = f"{model_name}\n" + "\n".join(fields)
        node = pydot.Node(model_name, label=label, shape='record')
        graph.add_node(node)

        for field in model._meta.fields:
            if isinstance(field, models.ForeignKey):
                target_model = field.related_model.__name__
                edge = pydot.Edge(model_name, target_model)
                graph.add_edge(edge)

    return graph

app_label = 'render'  # 'your_app_name' を適切なDjangoアプリ名に置き換えてください
graph = generate_er_diagram(app_label)
graph.write_png('er_diagram.png')
