import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
import pickle
import gdown
import numpy as np
import pkg_resources
import tensorflow_datasets as tfds
from utils import utils
from nkia.ml.cnn_nlp_model import CNN


class ClassifyProducts(object):

    def load_model_to_memory(self, model_name):
        model_version = pkg_resources.get_distribution('nkia').version
        os.makedirs(model_name) if model_name not in os.listdir() else ...
        utils.get_model_files_by_version(model_name + '/', model_version)

        tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file(
            './'+model_name+'/'+model_version+'/token')

        nb_classes = 29 if model_name == 'category_model' else 2

        cnn = CNN(vocab_size=tokenizer.vocab_size, emb_dim=300, nb_filters=100,
                  ffn_units=256, nb_classes=nb_classes, dropout_rate=0.2)

        cnn.load_weights('./'+model_name+'/'+model_version +
                         '/model_checkpoint/cp.ckpt').expect_partial()
        return cnn

    def load_dictionary(self):
        if 'nlp_dictionary' not in os.listdir():
            os.makedirs('nlp_dictionary')
            gdown.download('https://project-elements-nk.s3.amazonaws.com/dictionary.pkl',
                           'nlp_dictionary/dictionary.pkl', quiet=False)

        return utils.instantiate_spelling_corrector('nlp_dictionary/dictionary.pkl')

    def inference_from_category_model(self, model, sym_spell, product_name=[''], description=['']):
        """
        This method is responsible to infer the product category based on your caracteristics. Pass just one product
        by time.

        Args:
            product_name (list):  ['energético sabor baunilha']
            description (list):  ['Esse produto é simplesmente fantástico']

        Returns:
            str: Category name. e.g: 'Bebidas não alcoolicas'

        """
        X = self.preprocessing_fn(
            sym_spell, product_name, description, 'category_model')

        product_category = model(np.array(X), training=False).numpy()[0]
        product_category_proba = product_category[product_category.argmax()]

        if product_category_proba < 0.6:
            return 'categoria desconhecida'

        return self.label_encoder.inverse_transform([product_category.argmax()])[0]

    def inference_from_food_model(self, model, sym_spell, product_name=[''], description=['']):
        """
        This method is responsible to infer if a product is a food or not. Pass just one product
        by time.

        Args:
            product_name (list):  ['energético sabor baunilha']

        Returns:
            str: food or not food.

        """
        X = self.preprocessing_fn(
            sym_spell, product_name, description, 'food_model')

        product_type = model(np.array(X), training=False).numpy()

        if product_type > 0.4 and product_type < 0.6:
            return 'sem certeza'

        product_type = 1 if product_type >= 0.6 else 0

        return self.label_encoder.inverse_transform([product_type])[0]

    def preprocessing_fn(self, sym_spell, product_name, description, model_name):
        model_version = pkg_resources.get_distribution('nkia').version
        tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file(
            './'+model_name+'/'+model_version+'/token')

        X = utils.get_cleaned_predictor(
            sym_spell, [description], [product_name], model_name)

        tokenized_predictor = [tokenizer.encode(sentence) for sentence in X]

        self.label_encoder = self.get_label_encoder(
            './'+model_name+'/'+model_version+'/label_encoder.pkl')

        return tokenized_predictor

    def get_label_encoder(self, encoder_path):
        pkl_encoder_file = open(encoder_path, 'rb')
        encoder = pickle.load(pkl_encoder_file)
        pkl_encoder_file.close()
        return encoder


ClassifyProducts()
