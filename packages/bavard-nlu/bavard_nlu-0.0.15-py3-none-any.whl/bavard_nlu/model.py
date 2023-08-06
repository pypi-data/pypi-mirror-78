import logging
from datetime import datetime
from typing import List, Optional

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from official.nlp.bert.tokenization import FullSentencePieceTokenizer
from sklearn.preprocessing import LabelEncoder
from tensorflow.python.keras.layers import Input, Dense, TimeDistributed, Dropout, Lambda
from tensorflow.python.keras.models import Model

from bavard_nlu.data_preprocessing.data_preprocessor import decode_tf_record
from bavard_nlu.data_preprocessing.prediction_input import PredictionInput

logging.getLogger().setLevel(logging.DEBUG)


class NLUModel:
    def __init__(self,
                 intents: List[str],
                 tag_types: List[str],
                 max_seq_len: int,
                 saved_model_dir: Optional[str] = None,
                 load_model: bool = False,
                 verbose: bool = False):

        self.intents = sorted(intents)
        self.tag_types = sorted(tag_types)
        self.max_seq_len = max_seq_len
        self.save_model_dir = saved_model_dir
        self.verbose = verbose

        # intents encoder
        self.intents_encoder = LabelEncoder()
        self.intents_encoder.fit(self.intents)

        # tags encoder
        tag_set = {'[CLS]', '[SEP]', 'O'}
        for tag_type in tag_types:
            tag_set.add(f'B-{tag_type}')
            tag_set.add(f'I-{tag_type}')
        self.tag_encoder = LabelEncoder()
        self.tag_encoder.fit(list(tag_set))

        # tag and intent sizes
        self.n_tags = len(tag_set)
        self.n_intents = len(intents)

        self.model = None
        self.tokenizer = None

        if load_model:
            self.model = tf.keras.models.load_model(saved_model_dir)
            self._compile_model()

    def get_tokenizer(self) -> FullSentencePieceTokenizer:
        if not self.tokenizer:
            albert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/albert_en_base/1", trainable=False)
            sp_model_file = albert_layer.resolved_object.sp_model_file.asset_path.numpy()
            tokenizer = FullSentencePieceTokenizer(sp_model_file)
            self.tokenizer = tokenizer
        return self.tokenizer

    def build_and_compile_model(self):
        albert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/albert_en_base/1", trainable=True)
        sp_model_file = albert_layer.resolved_object.sp_model_file.asset_path.numpy()
        tokenizer = FullSentencePieceTokenizer(sp_model_file)
        self.tokenizer = tokenizer

        in_id = Input(shape=(self.max_seq_len,), name='input_ids', dtype=tf.int32)
        in_mask = Input(shape=(self.max_seq_len,), name='input_mask', dtype=tf.int32)
        in_segment = Input(shape=(self.max_seq_len,), name='segment_ids', dtype=tf.int32)
        word_start_mask = Input(shape=(self.max_seq_len,), name='word_start_mask', dtype=tf.float32)
        bert_inputs = [in_id, in_mask, in_segment]
        all_inputs = [in_id, in_mask, in_segment, word_start_mask]

        # the output of trained Bert
        pooled_output, sequence_output, = albert_layer(bert_inputs)

        # add the additional layer for intent classification and slot filling
        intents_drop = Dropout(rate=0.1)(pooled_output)
        intents_out = Dense(self.n_intents, activation='softmax', name='intent')(intents_drop)

        tags_drop = Dropout(rate=0.1)(sequence_output)
        tags_out = TimeDistributed(Dense(self.n_tags, activation='softmax'))(tags_drop)
        tags_out = Lambda(lambda x: x, name='tags')(tags_out)
        # tags_out = Multiply(name='tagger')([tags_out, word_start_mask])

        self.model = Model(inputs=all_inputs, outputs=[intents_out, tags_out])
        self._compile_model()

    def _compile_model(self):
        optimizer = tf.keras.optimizers.Adam(lr=5e-5)
        losses = {
            'tags': 'sparse_categorical_crossentropy',
            'intent': 'categorical_crossentropy'
        }
        loss_weights = {'tags': 3.0, 'intent': 1.0 }
        metrics = {'intent': 'acc'}
        self.model.compile(optimizer=optimizer, loss=losses, loss_weights=loss_weights, metrics=metrics)
        if self.verbose:
            self.model.summary()

    def get_tags_output_mask(self, word_start_mask):
        word_start_mask = np.expand_dims(word_start_mask, axis=2)  # n x seq_len x 1
        tags_output_mask = np.tile(word_start_mask, (1, 1, self.n_tags))  # n x seq_len x n_tags
        return tags_output_mask

    def train(self, training_path: str, batch_size: int, epochs: int):
        train_dataset = tf.data.TFRecordDataset([training_path])
        example_count = sum(1 for _ in train_dataset)
        if example_count < 5:
            raise Exception('Too few examples to train')
        valid_count = min(int(example_count * 0.2), 200)
        if example_count < 100:
            valid_count = 0
            epochs = 1

        train_count = example_count - valid_count
        logging.info(f'Training example count: {train_count}')
        logging.info(f'Validation example count: {valid_count}')

        def split_x_y(item):
            x = {
                'input_ids': item['input_ids'],
                'input_mask': item['input_mask'],
                'segment_ids': item['segment_ids'],
                'word_start_mask': item['word_start_mask'],
            }
            y = {
                'tags': item['tags'],
                'intent': item['intent'],
            }
            return x, y

        ds = train_dataset \
            .shuffle(buffer_size=1000) \
            .map(map_func=lambda x: decode_tf_record(x, self.max_seq_len, n_intents=self.n_intents, is_training=True)) \
            .map(split_x_y)

        test_ds = ds.take(valid_count).batch(batch_size=batch_size) if valid_count else None
        train_ds = ds.skip(valid_count).take(1000).batch(batch_size=batch_size)

        if not valid_count:
            train_ds = train_ds.repeat(30)
            steps_per_epoch = sum(1 for _ in train_ds)
        else:
            steps_per_epoch = sum(1 for _ in train_ds)
            train_ds = train_ds.repeat()


        # checkpoints
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.save_model_dir,
                                                         save_best_only=True if valid_count else False,
                                                         save_weights_only=False,
                                                         verbose=1)

        # tensorboard
        logdir = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        tb_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

        # train
        self.model.fit(train_ds,
                       epochs=epochs,
                       steps_per_epoch=steps_per_epoch,
                       validation_data=test_ds,
                       use_multiprocessing=True,
                       callbacks=[cp_callback, tb_callback])

    def predict(self, text: str, tokenizer: FullSentencePieceTokenizer):
        text = text.lower()
        raw_input = PredictionInput(text=text, max_seq_len=self.max_seq_len, tokenizer=tokenizer)
        x = raw_input.to_model_input()
        prediction = self.model.predict(x=x)
        return prediction

    def decode_intent(self, raw_intent_prediction: np.ndarray):
        intent_max = np.argmax(raw_intent_prediction)
        decoded_intent = self.intents_encoder.inverse_transform([intent_max])[0]
        return decoded_intent

    def decode_tags(self, raw_tag_predictions: np.ndarray, text: str, word_start_mask: List[int]):
        raw_tag_predictions = np.squeeze(raw_tag_predictions)
        assert raw_tag_predictions.shape[0] == len(word_start_mask)
        decoded_tags = []
        for i, e in enumerate(word_start_mask):
            if e == 1:
                predicted_tag_idx = np.argmax(raw_tag_predictions[i])
                predicted_tag = self.tag_encoder.inverse_transform([predicted_tag_idx])[0]
                decoded_tags.append(predicted_tag)

        words = text.split()

        result = []
        current_tag_words = []
        current_tag_type = None
        for i, tag in enumerate(decoded_tags):
            if tag == 'O':
                if current_tag_words and current_tag_type:
                    result.append({
                        'tag_type': current_tag_type,
                        'value': ' '.join(current_tag_words),
                    })

                current_tag_type = None
                current_tag_words = []
                continue

            if tag.startswith('B-'):
                if current_tag_words and current_tag_type:
                    result.append({
                        'tag_type': current_tag_type,
                        'value': ' '.join(current_tag_words),
                    })

                current_tag_words = [words[i]]
                current_tag_type = tag[2:]
            elif tag.startswith('I-'):
                current_tag_words.append(words[i])

        if current_tag_words and current_tag_type:
            result.append({
                'tag_type': current_tag_type,
                'value': ' '.join(current_tag_words),
            })

        return result

