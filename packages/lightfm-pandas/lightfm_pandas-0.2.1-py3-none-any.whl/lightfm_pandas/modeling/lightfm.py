import logging

import lightfm

from lightfm_pandas.modeling import factorization_base
from lightfm_pandas.utils.instrumentation import log_errors
from lightfm_pandas.utils.config import N_CPUS

logger = logging.getLogger(__name__)

# monkey patch print function
@log_errors()
def _epoch_logger(s, print_each_n=20):
    if not int(s.replace('Epoch ', '')) % print_each_n:
        logger.info(s)

lightfm.lightfm.print = _epoch_logger


class LightFMRecommender(factorization_base.BaseFactorizationRecommender):

    default_model_params = {
        'loss': 'warp',
        'learning_schedule': 'adadelta',
        'no_components': 30,
        'max_sampled': 10,
        'item_alpha': 0,
        'user_alpha': 0,
    }

    default_fit_params = {
        'epochs': 100,
        'item_features': None,
        'num_threads': N_CPUS,
        'verbose': True,
    }

    default_external_features_params = dict(add_identity_mat=True)

    def __init__(self,
                 use_sample_weight=False,
                 external_features=None,
                 external_features_params=None,
                 **kwargs):
        self.use_sample_weight = use_sample_weight
        self.external_features = external_features
        self.external_features_params = external_features_params or \
                                        self.default_external_features_params.copy()
        super().__init__(**kwargs)

    def _prep_for_fit(self, train_obs, **fit_params):
        # self.toggle_mkl_blas_1_thread(True)
        # assign all observation data
        self._set_data(train_obs)
        fit_params['sample_weight'] = self.train_mat.tocoo() \
            if self.use_sample_weight else None
        self._set_fit_params(fit_params)
        self._add_external_features()
        # init model and set params
        self.model = lightfm.LightFM(**self.model_params)

    def _add_external_features(self):
        if self.external_features is not None:
            self.external_features_mat = self.external_features.\
                create_sparse_features_mat(
                    items_encoder=self.sparse_mat_builder.iid_encoder,
                    **self.external_features_params)
            logger.info('External item features matrix: %s' %
                            str(self.external_features_mat.shape))

        # add external features if specified
        self.fit_params['item_features'] = self.external_features_mat
        if self.external_features_mat is not None:
            logger.info('Fitting using external features mat: %s'
                               % str(self.external_features_mat.shape))

    def fit(self, train_obs, **fit_params):
        self._prep_for_fit(train_obs, **fit_params)
        self.model.fit_partial(self.train_mat, **self.fit_params)
        return self

    def fit_partial(self, train_obs, epochs=1):
        self.set_params(epochs=epochs)
        if self.model is None:
            self.fit(train_obs)
        else:
            self.model.fit_partial(self.train_mat)
        return self

    def set_params(self, **params):
        params = self._pop_set_params(
            params, ['use_sample_weight', 'external_features', 'external_features_params'])
        super().set_params(**params)

    def _get_item_factors(self, mode=None):

        n_items = len(self.sparse_mat_builder.iid_encoder.classes_)

        biases, representations = self.model.get_item_representations(self.fit_params['item_features'])

        if mode is None:
            pass  # default mode

        elif mode == 'external_features':
            external_features_mat = self.external_features_mat

            assert external_features_mat is not None, \
                'Must define and add a feature matrix for "external_features" similarity.'

            representations = external_features_mat

        elif (mode == 'no_features') and (self.fit_params['item_features'] is not None):

            logger.info('LightFM recommender: get_similar_items: "no_features" mode '
                               'assumes ID mat was added and is the last part of the feature matrix.')

            assert self.model.item_embeddings.shape[0] > n_items, \
                'Either no ID matrix was added, or no features added'

            representations = self.model.item_embeddings[-n_items:, :]

        else:
            raise ValueError('Uknown representation mode: %s' % mode)

        return biases, representations

    def _get_user_factors(self, mode=None):
        return self.model.get_user_representations()

    def _predict_on_inds(self, user_inds, item_inds):
        return self.model.predict(user_inds, item_inds,
                                  item_features=self.fit_params['item_features'],
                                  num_threads=N_CPUS)


    def _predict_rank(self, test_mat, train_mat=None):
        return self.model.predict_rank(
            test_interactions=test_mat,
            train_interactions=train_mat,
            item_features=self.fit_params['item_features'],
            num_threads=N_CPUS)

    def reduce_memory_for_serving(self):
        # would be best to set those to None, but than LightFM will complain, and more importantly
        # Cython code expects the right data format and will crash if its predict() will be used,
        # so I just point to the embeddings (which doesn't add memory).
        # the danger in this is that I don't know what will be the damage if someone calls one of the fit methods
        # for this reason it's in an explicit method "for_serving" and not in a __getstate__() method
        self.model.item_embedding_gradients = self.model.item_embeddings
        self.model.item_embedding_momentum= self.model.item_embeddings
        self.model.user_embedding_gradients = self.model.user_embeddings
        self.model.user_embedding_momentum = self.model.user_embeddings
        self.model.item_bias_gradients = self.model.item_biases
        self.model.item_bias_momentum= self.model.item_biases
        self.model.user_bias_gradients = self.model.user_biases
        self.model.user_bias_momentum = self.model.user_biases
        self.fit_params['sample_weight'] = None

