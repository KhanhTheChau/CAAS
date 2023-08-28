"""
Show evaluation result from results/ folder
"""

import os
import json

template = "{0:20}|{1:10}|{2:15}|{3:7}"
print(template.format("Model", "Acc", "Precision", "Recall"))
print("-" * 60)

models = []
for model in os.listdir("results"):
    report_file = f"results/{model}/intent_report.json"
    
    with open(report_file, "r") as f:
        report_data = json.load(f)

    acc = report_data["accuracy"]
    precision = report_data["macro avg"]["precision"]
    recall = report_data["macro avg"]["recall"]

    models.append([model, acc, precision, recall])

models.sort(key = lambda k: k[1], reverse=True) # acc
for model, acc, precision, recall in models:
    print(template.format(model, round(acc, 3), round(precision, 3), round(recall, 3)))
