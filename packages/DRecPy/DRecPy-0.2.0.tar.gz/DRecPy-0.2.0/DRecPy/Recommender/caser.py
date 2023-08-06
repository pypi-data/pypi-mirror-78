from DRecPy.Recommender import RecommenderABC
from DRecPy.Sampler import ListSampler
import tensorflow as tf
from heapq import nlargest


class Caser(RecommenderABC):
    def __init__(self, L=0, T=0, d=0, n_v=0, n_h=0, act_h=tf.nn.relu, act_mlp=tf.nn.relu, dropout_rate=0.5,
                 sort_column='timestamp', **kwds):
        super(Caser, self).__init__(**kwds)

        self.L = L
        self.T = T
        self.d = d
        self.n_v = n_v
        self.n_h = n_h
        self.act_h = act_h
        self.act_mlp = act_mlp
        self.dropout_rate = dropout_rate
        self.sort_column = sort_column

        self._loss = tf.losses.BinaryCrossentropy()

    def _pre_fit(self, learning_rate, neg_ratio, reg_rate, **kwds):
        l2_reg = tf.keras.regularizers.l2(reg_rate)
        self.user_embeddings = tf.keras.layers.Embedding(self.n_users, self.d, embeddings_regularizer=l2_reg)
        self._register_trainable(self.user_embeddings)

        self.item_embeddings = tf.keras.layers.Embedding(self.n_items, self.d, embeddings_regularizer=l2_reg)
        self._register_trainable(self.item_embeddings)

        self.conv_v = tf.keras.layers.Conv1D(filters=self.n_v, kernel_size=self.L, kernel_regularizer=l2_reg)
        self._register_trainable(self.conv_v)

        self.convs_h = []
        for i in range(self.L):
            self.convs_h.append(tf.keras.layers.Conv1D(filters=self.n_h, kernel_size=i+1, kernel_regularizer=l2_reg))
        self._register_trainables(self.convs_h)

        self.dropout = tf.keras.layers.Dropout(self.dropout_rate)

        self.dense_0 = tf.keras.layers.Dense(self.d, activation=self.act_mlp, input_shape=(self.d * self.n_v + self.n_h,), kernel_regularizer=l2_reg)
        self._register_trainable(self.dense_0)

        self.dense_1_W = tf.keras.layers.Embedding(self.n_items, 2 * self.d, embeddings_regularizer=l2_reg)
        self._register_trainable(self.dense_1_W)

        self.dense_1_b = tf.keras.layers.Embedding(self.n_items, 1)
        self._register_trainable(self.dense_1_b)

        self._sampler = ListSampler(self.interaction_dataset, ['uid'], neg_ratio=neg_ratio, n_targets=self.T,
                                    interaction_threshold=self.interaction_threshold, negative_ids_col='iid',
                                    min_positive_records=self.L, max_positive_records=self.L,
                                    #sort_column=self.sort_column,
                                    seed=self.seed)

    def _sample_batch(self, batch_size, **kwds):
        return self._sampler.sample_group_records(batch_size)

    def _predict_batch(self, batch_samples, **kwds):
        predictions, desired_values = [], []

        for (positive_user_records, target_user_records, negative_iids) in batch_samples:
            iids_before = [record['iid'] for record in positive_user_records]
            iids_target = [record['iid'] for record in target_user_records] + negative_iids
            target_predictions = self._predict_batch_aux(positive_user_records[0]['uid'], iids_before, iids_target)

            #print('target_predictions', target_predictions)
            # add predictions and expected values
            predictions.append(target_predictions)
            desired_values.append(tf.convert_to_tensor([1.] * len(target_user_records) + [0.] * len(negative_iids)))

        return predictions, desired_values

    def _predict_batch_aux(self, uid, iids_before, iids_after):
        uid = int(uid)  # user_embeddings call does not support np.int64
        iids_before = tf.constant([int(iid) for iid in iids_before])  # item_embeddings call does not support np.int64
        iids_after = tf.constant([int(iid) for iid in iids_after])  # item_embeddings call does not support np.int64

        # compute embeddings
        items_embeddings = self.item_embeddings(iids_before)
        items_embeddings_3dim = tf.reshape(items_embeddings, [1, items_embeddings.shape[0], items_embeddings.shape[1]])

        # compute convolutions
        out_v = tf.reshape(self.conv_v(items_embeddings_3dim), [-1])

        out_h = []
        for conv_h in self.convs_h:
            conv_output = self.act_h(conv_h(items_embeddings_3dim))
            #print('conv_output', conv_output)
            #print('before', tf.reduce_max(conv_output, axis=-2))
            #print('new', tf.nn.max_pool1d(conv_output, conv_output.shape[1], conv_output.shape[1], 'SAME').squeeze(1))
            out_h.append(tf.squeeze(tf.nn.max_pool1d(conv_output, conv_output.shape[1], conv_output.shape[1], 'SAME'), 1))
            #out_h.append(tf.reduce_max(conv_output, axis=-2))

        out_h = tf.reshape(tf.convert_to_tensor(out_h), [-1])

        # compute feedforward
        concat_conv_out = tf.expand_dims(tf.concat([out_h, out_v], axis=-1), 0)
        out_dense = self.dense_0(self.dropout(concat_conv_out))
        user_embeddings = self.user_embeddings(uid)
        concat_dense_1_input = tf.concat([out_dense, [user_embeddings]], axis=-1)

        #print('self.dense_1_W(iids_after)', self.dense_1_W(iids_after))
        #print('concat_dense_1_input', concat_dense_1_input)
        #print('self.dense_1_b(iids_after)', self.dense_1_b(iids_after))
        #print('(self.dense_1_W(iids_after) * concat_dense_1_input)', self.dense_1_W(iids_after) * concat_dense_1_input)
        #print('(self.dense_1_W(iids_after) * concat_dense_1_input + self.dense_1_b(iids_after))', self.dense_1_W(iids_after) * concat_dense_1_input + self.dense_1_b(iids_after))
        #print('tf.reduce_sum(self.dense_1_W(iids_after) * concat_dense_1_input + self.dense_1_b(iids_after))', tf.reduce_sum(self.dense_1_W(iids_after) * concat_dense_1_input + self.dense_1_b(iids_after), 1))
        #print('tf.reduce_sum(self.dense_1_W(iids_after) * concat_dense_1_input)', tf.reduce_sum(self.dense_1_W(iids_after) * concat_dense_1_input, 1))
        #print('tf.nn.sigmoid(tf.reduce_sum(self.dense_1_W(iids_after) * concat_dense_1_input)', tf.nn.sigmoid(tf.reduce_sum(self.dense_1_W(iids_after) * concat_dense_1_input)))

        preds = tf.nn.sigmoid(tf.reduce_sum(self.dense_1_W(iids_after) * concat_dense_1_input + self.dense_1_b(iids_after), 1))
        #print('preds', preds)
        return preds

    def _compute_batch_loss(self, predictions, desired_values, **kwds):
        return self._loss(desired_values, predictions)

    def _compute_reg_loss(self, reg_rate, batch_size, non_layer_weights, **kwds):
        return 0  # automatically computed via layer l2 regularization defined in self._pre_fit

    def _predict(self, uid, iid, **kwds):
        return None

    def _rank(self, uid, iids, n, novelty):
        user_records = self.interaction_dataset.select(f'uid == {uid}').values_list()

        if self.sort_column in self.interaction_dataset.columns:
            user_records.sort(key=lambda x: x[self.sort_column])

        user_iids = [record['iid'] for record in user_records]

        if novelty:
            user_iids_set = set(user_iids)
            novel_user_iids = list(filter(lambda x: x not in user_iids_set, iids))
            predictions = self._predict_batch_aux(uid, user_iids[-self.L:], novel_user_iids)
            return nlargest(n, list(zip(predictions, novel_user_iids)))
        else:
            predictions = self._predict_batch_aux(uid, user_iids[-self.L:], iids)
            largetst = nlargest(n, list(zip(predictions, iids)))
            print('largetst', largetst)
            return nlargest(n, list(zip(predictions, iids)))
