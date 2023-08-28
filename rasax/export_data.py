# Export NLU data to csv file with question-answer

import pandas as pd
import yaml
# from ruamel import yaml
import re

default_responses = {
    # 'utter_greet': [{'text': 'Xin chào, tôi là bot'}],
    # 'utter_goodbye': [
    #     {'text': 'Tạm biệt, hẹn gặp lại bạn'},
    #     {'text': 'Tạm biệt :('}
    # ],
    'utter_iamabot': [{'text': 'Tôi là bot hỗ trợ việc làm'}],
    # 'utter_welcome': [{'text': 'Không có chi'}],
}

def create_nlu_data(df):
    data = []
    for intent, rows in df.groupby("intent"):
        examples = rows['question'].values.tolist()
        # examples = [f"- {x}" for x in examples]
        # examples = "\n".join(examples)
        data.append({
            'examples': examples,
            'intent': intent,
        })

    return data

def write_nlu_data(df):
    nlu_data = create_nlu_data(df)
    version = "2.0"

    # Get common nlu data

    path = 'data/nlu.yml'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"version: \"{version}\"\n\n")
        f.write(f"nlu:\n")
        for row in nlu_data:
            intent = row['intent']
            examples = row['examples']
            f.write(f"- intent: {intent}\n  examples: |\n")
            for example in examples:
                f.write(f"    - {example}\n")
            f.write("\n")

    print(f"{path} updated")

def clean_text(text):
    """
    Remove "-" at begin and strip
    """
    return re.sub(r"^\-", "", text).strip()


if __name__ == '__main__':
    # Read data
    with open('dataset/data.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    with open('domain.yml', 'r', encoding='utf-8') as f:
        domain = yaml.safe_load(f)

    data_df = []
    stories = []
    domain['intents'] = []
    domain['entities'] = []
    domain['responses'] = default_responses
    for d in data:
        intent = d['intent']
        # new intent
        domain['intents'].append(intent)
        examples = d['examples'].split('\n')

        for example in examples:
            question = clean_text(example)

            if question:
                if 'answer' in d:
                    ans = clean_text(d['answer'])
                    data_df.append([intent, question, ans])

                    action = f'utter_{intent}'
                    if action not in domain['responses']:
                        answers = []
                        for a in ans.split('\n'):
                            answers.append({'text': clean_text(a)})
                        domain['responses'][action] = answers

                        if intent not in ['goodbye', 'bot_challenge']:
                            stories.append([intent, action])

                # Find and update entities e.g : [lắp ráp ô tô](job_position)
                entities =  re.findall(u"\]\([A-Za-z_]+\)", question)
                if entities:
                    for e in entities:
                        e = e.split("](")[1][:-1]
                        domain['entities'].append(e)

    data_df = pd.DataFrame(data_df, columns=['intent', 'question', 'answer'])

    domain_path = 'domain.yml'
    domain['entities'] = list(set(domain['entities']))
    domain['intents'] = list(set(domain['intents']))
    with open(domain_path, 'w', encoding='utf-8') as f:
        # print(domain)
        yaml.dump(domain, f, allow_unicode=True)
        print(f"{domain_path} updated")

    group_df = []

    for intent, qa in data_df.groupby('intent'):
        questions = "\n".join("- " + x for x in qa['question'].values)
        answers = "\n".join("- " + x for x in list(set(qa['answer'].values)))
        group_df.append([intent, questions, answers])
    
    write_nlu_data(data_df)

    # Export data to excel
    writer = pd.ExcelWriter('dataset/data.xlsx', engine='xlsxwriter')
    pd.DataFrame(group_df,
        columns=['intent', 'questions', 'answers']).to_excel(writer, index=False)
    workbook=writer.book
    worksheet = writer.sheets['Sheet1']

    # Set width
    # intent col = 20
    worksheet.set_column('A:A', 35)
    # questions = 35
    worksheet.set_column(1, 1, 45)
    # answer = 35
    worksheet.set_column(2, 2, 50)

    fmt = workbook.add_format({'text_wrap': True, 'align': 'valign'})
    # Setting the format but not setting the column width.
    worksheet.set_column('A:C', None, fmt)
    writer.save()
    

    story_data = {
        'version': '2.0',
        'stories': [],
    }
    
    for st in stories:
        story_data['stories'].append({
            'story': st[0],
            'steps': [{'intent': st[0]}, {'action': st[1]}]
        })
    # print(data_df.head())

    with open('data/stories.yml', 'w', encoding='utf-8') as f:
        # stories = yaml.safe_load(f)
        yaml.dump(story_data, f, allow_unicode=True)
        print('data/stories.yml updated')