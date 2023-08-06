import json

import click
from bavard_nlu.data_preprocessing.prediction_input import PredictionInput

from bavard_nlu.model import NLUModel


@click.command()
@click.option('--agent-data-file', type=click.Path(exists=True), required=True)
@click.option('--model-dir', type=click.Path(exists=True), required=True)
@click.option('--text', type=str, required=True)
def predict(agent_data_file: str, model_dir: str, text: str):
    with open(agent_data_file) as f:
        agent_data = json.load(f)
    intents = []
    for x in agent_data['intents']:
        intents.append(x['intent'])
    tag_types = agent_data['tagTypes']

    model = NLUModel(intents=intents,
                     tag_types=tag_types,
                     max_seq_len=200,
                     saved_model_dir=model_dir,
                     load_model=True)
    tokenizer = model.get_tokenizer()
    raw_prediction = model.predict(text=text, tokenizer=tokenizer)
    raw_intent_pred = raw_prediction[0]
    raw_tags_pred = raw_prediction[1]
    pred_input = PredictionInput(text, 200, tokenizer)
    intent = model.decode_intent(raw_intent_pred)
    tags = model.decode_tags(raw_tags_pred, text, pred_input.word_start_mask)
    print('intent: ', intent)
    print('tags: ', tags)
