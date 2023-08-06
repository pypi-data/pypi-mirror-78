from DRecPy.Recommender import RecommenderABC
from DRecPy.Sampler import PointSampler
import tensorflow as tf
import numpy as np


class NeuMF(RecommenderABC):
    def __init__(self, gmf_embedding_dim, mlp_embedding_dim, layer_dims=None, pre_train=True, **kwds):
        super(NeuMF, self).__init__(**kwds)

        assert gmf_embedding_dim > 0, 'The "gmf_embedding_dim" argument should be a positive number.'
        assert mlp_embedding_dim > 0, 'The "mlp_embedding_dim" argument should be a positive number.'  # todo: remove by using layer_dims[0] / 2

        self.gmf_embedding_dim = gmf_embedding_dim
        self.mlp_embedding_dim = mlp_embedding_dim
        self.layer_dims = layer_dims
        if self.layer_dims is None:
            self.layer_dims = [64, 32]  # TODO change

        assert isinstance(layer_dims, list), 'The "layer_dims" argument must be of type list (ex: [64, 32]).'
        assert len(layer_dims) > 0, 'The "layer_dims" argument must have at least 1 element.'

        self.pre_train = pre_train
        self._loss = tf.losses.BinaryCrossentropy()  # TODo add support for more loss functions(?? check paper if is possible)

    def _pre_fit(self, learning_rate, neg_ratio, reg_rate, **kwds):
        assert 0 <= self.max_interaction <= 1 and 0 <= self.min_interaction <= 1, \
            'NeuCF only supports binary interaction values. ' \
            'Consider converting all interaction values to the [0, 1] range.'

        weight_initializer = tf.initializers.GlorotUniform()
        #weight_initializer = tf.initializers.RandomNormal(mean=0, stddev=0.01)
        self.user_embeddings_mlp = tf.Variable(weight_initializer(shape=[self.n_users, self.mlp_embedding_dim]))
        self.item_embeddings_mlp = tf.Variable(weight_initializer(shape=[self.n_items, self.mlp_embedding_dim]))
        self.user_embeddings_gmf = tf.Variable(weight_initializer(shape=[self.n_users, self.gmf_embedding_dim]))
        self.item_embeddings_gmf = tf.Variable(weight_initializer(shape=[self.n_items, self.gmf_embedding_dim]))

        self.mlp = tf.keras.Sequential()
        self.mlp.add(
            tf.keras.layers.Dense(self.layer_dims[0], activation=tf.nn.relu,  # TODO add support for other activations
                                  input_shape=(self.mlp_embedding_dim * 2,),
                                  kernel_regularizer=tf.keras.regularizers.l2(reg_rate), autocast=False))

        for dim in self.layer_dims[1:]:
            self.mlp.add(tf.keras.layers.Dense(dim, activation=tf.nn.relu,
                                               kernel_regularizer=tf.keras.regularizers.l2(
                                                   reg_rate)))  # TODO add support for other activations

        # self.mlp.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid,
        #                                   kernel_regularizer=tf.keras.regularizers.l2(reg_rate)))  # TODO ad support for probit or sigmoid

        # self.h = tf.Variable(weight_initializer(shape=[2, 2]))  # last layer that concatenates both predictions
        self.h = tf.Variable(weight_initializer(
            shape=[self.layer_dims[-1] + self.gmf_embedding_dim]))  # last layer that concatenates both predictions

        self._optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        self._sampler = PointSampler(self.interaction_dataset, neg_ratio, self.interaction_threshold, self.seed)

        if self.pre_train:
            self._optimizer_pre_train = tf.keras.optimizers.SGD(learning_rate=learning_rate)
            for e in range(50):
                print('pretrain epoch', e)
                for b in range(256):
                    self._do_pretrain_batch()

    def _do_pretrain_batch(self):
        pass
        """pairs = []
        for i in range(256):
            sampled_uid, sampled_iid = self._sampler.sample_one()
            des = self.interaction_dataset.select_one(
                f'uid == {sampled_uid}, iid == {sampled_iid}', 'interaction', to_list=True)
            if des is None: des = 0

            pairs.append((sampled_uid, sampled_iid, des))

        with tf.GradientTape() as tape:
            tape.watch(self.user_embeddings_mlp), tape.watch(self.item_embeddings_mlp)
            tape.watch(self.user_embeddings_gmf), tape.watch(self.item_embeddings_gmf)
            tape.watch(self.h)

            preds = []
            for uid, iid, des in pairs:
                mlp_embeddings = self._compute_embeddings(uid, iid, True)
                pred_vec_mlp = self.mlp(mlp_embeddings)
                pred_tensor_mlp = tf.sigmoid(tf.reduce_sum(tf.multiply(pred_vec_mlp[0], self.h[:self.layer_dims[-1]])))

            loss = self._loss([des], [pred_tensor_mlp])  # TODO: Regularizer?? check paper

        grads = tape.gradient(loss, [self.user_embeddings_mlp, self.item_embeddings_mlp,
                                     self.h, self.mlp.trainable_variables])
        self._optimizer_pre_train.apply_gradients(zip(grads[:-1],
                                                      [self.user_embeddings_mlp, self.item_embeddings_mlp, self.h]))
        self._optimizer_pre_train.apply_gradients(zip(grads[-1], self.mlp.trainable_variables))

        with tf.GradientTape() as tape:
            tape.watch(self.user_embeddings_gmf), tape.watch(self.item_embeddings_gmf)
            tape.watch(self.h)

            gmf_user_embeddings, gmf_item_embeddings = self._compute_embeddings(sampled_uid, sampled_iid, False)
            pred_vec_gmf = tf.multiply(gmf_user_embeddings, gmf_item_embeddings)
            pred_tensor_gmf = tf.sigmoid(tf.reduce_sum(tf.multiply(pred_vec_gmf, self.h[self.layer_dims[-1]:])))

            loss = self._loss([des], [pred_tensor_gmf])  # TODO: Regularizer?? check paper

        grads = tape.gradient(loss, [self.user_embeddings_gmf, self.item_embeddings_gmf, self.h])
        self._optimizer_pre_train.apply_gradients(zip(grads,
                                                      [self.user_embeddings_gmf, self.item_embeddings_gmf, self.h]))"""

    def _do_batch(self, batch_size, **kwds):
        sampled_triples = self._sampler.sample(batch_size)

        uids, iids, labels = [], [], []
        for uid, iid, desired in sampled_triples:
            uids.append(uid)
            iids.append(iid)
            labels.append(desired)

        with tf.GradientTape() as tape:
            tape.watch(self.user_embeddings_mlp), tape.watch(self.item_embeddings_mlp)
            tape.watch(self.user_embeddings_gmf), tape.watch(self.item_embeddings_gmf)
            tape.watch(self.h)

            #print('pred', pred, 'vs des', des)
            preds = [self._predict(uid, iid, tensor=True) for uid, iid in zip(uids, iids)]
            loss = self._loss(labels, preds)  # TODO: Regularizer?? check paper
        print('labels', labels, '\npred', [p.numpy() for p in preds], '\nloss', loss)
        grads = tape.gradient(loss, [self.user_embeddings_mlp, self.item_embeddings_mlp,
                                     self.user_embeddings_gmf, self.item_embeddings_gmf,
                                     self.h, self.mlp.trainable_variables])
        self._optimizer.apply_gradients(zip(grads[:-1], [self.user_embeddings_mlp, self.item_embeddings_mlp,
                                                         self.user_embeddings_gmf, self.item_embeddings_gmf, self.h]))
        self._optimizer.apply_gradients(zip(grads[-1], self.mlp.trainable_variables))

        return loss

    def _compute_embeddings(self, uid, iid, is_mlp_embeddings):
        if is_mlp_embeddings:
            user_embeddings = tf.nn.embedding_lookup(self.user_embeddings_mlp, uid)
            item_embeddings = tf.nn.embedding_lookup(self.item_embeddings_mlp, iid)
            concat_embeddings = tf.concat([user_embeddings, item_embeddings], axis=0)
            return tf.reshape(concat_embeddings, [1, self.mlp_embedding_dim * 2])

        user_embeddings = tf.nn.embedding_lookup(self.user_embeddings_gmf, uid)
        item_embeddings = tf.nn.embedding_lookup(self.item_embeddings_gmf, iid)
        return user_embeddings, item_embeddings

    def _predict(self, uid, iid, **kwds):
        mlp_embeddings = self._compute_embeddings(uid, iid, True)
        gmf_user_embeddings, gmf_item_embeddings = self._compute_embeddings(uid, iid, False)

        pred_vec_mlp = self.mlp(mlp_embeddings)
        pred_vec_gmf = tf.multiply(gmf_user_embeddings, gmf_item_embeddings)
        concat_preds = tf.concat([pred_vec_mlp[0], pred_vec_gmf], axis=0)

        pred_tensor = tf.sigmoid(tf.reduce_sum(tf.multiply(concat_preds, self.h)))
        if kwds.get('tensor', False): return pred_tensor
        return pred_tensor.numpy()
        #return self.model.predict([np.array(uid), np.array(iid)])
