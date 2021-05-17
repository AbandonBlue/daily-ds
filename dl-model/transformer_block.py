import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# 實作multi head self attention as a keras layer
# multi head self attention: 超參數, 可以關注不同的地方

class MultiHeadSelfAttention(layers.Layer):
    """
        多頭注意力機制layer。
    """
    def __init__(self, embed_dim, num_heads=8):
        super(MultiHeadSelfAttention, self).__init__()
        self.embed_dim = embed_dim          # 輸入會先經過embed layer
        self.num_heads = num_heads          # 關注的點不一樣
        if embed_dim % num_heads != 0:      # why?
            raise ValueError(
                f"embedding dimension = {embed_dim} should be divisible by number of heads = {num_heads}"
            )
        self.projection_dim = embed_dim // num_heads
        self.query_dense = layers.Dense(embed_dim)      # Q, 透過layers.Dense來去學矩陣參數
        self.key_dense = layers.Dense(embed_dim)        # K, 同上!
        self.value_dense = layers.Dense(embed_dim)      # V, 同上!
        self.combine_heads = layers.Dense(embed_dim)    # 如果有多頭，將其combine，注意的地方不同，透過參數學習達成

    def attention(self, query, key, value):
        """
            注意力機制計算。
        """
        score = tf.matmul(query, key, transpose_b=True)     # inner product
        dim_key = tf.cast(tf.shape(key)[-1], tf.float32)    # 
        scaled_score = score / tf.math.sqrt(dim_key)        # 標準化
        weights = tf.nn.softmax(scaled_score, axis=-1)      # 算機率
        output = tf.matmul(weights, value)
        return output, weights
    
    def separate_heads(self, x, batch_size):
        """
            ??
        """
        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.projection_dim))
        return tf.transpose(x, perm=[0, 2, 1, 3])   # 維度轉換
    
    def call(self, inputs):
        """
            tf的前向傳遞呼叫。
        """
        # inputs.shape = (batch_size, seq_len, embedding_dim)
        batch_size = tf.shape(inputs)[0]
        query = self.query_dense(inputs)    # (batch_size, seq_len, embedding_dim)??, Dense可以3維?, yes: https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dense
        key = self.key_dense(inputs)        # 同上
        value = self.value_dense(inputs)    # 同上
        query = self.separate_heads(
            query, batch_size
        )   # (batch_size, num_heads, seq_len, project_dim)
        key = self.separate_heads(
            key, batch_size
        )
        value = self.separate_heads(
            value, batch_size
        )
        attention, weights = self.attention(query, key, value)
        attention = tf.transpose(
            attention, perm=[0, 2, 1, 3]
        )   # (batch_size, seq_len, num_heads, projection_dim)
        concat_attention = tf.reshape(
            attention, (batch_size, -1, self.embed_dim)
        )   # (batch_size, seq_len, embed_dim)
        output = self.combine_heads(
            concat_attention
        )   # (batch_size, seq_len, embed_dim)
        return output


# 實作Transformer block as a layer

class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = MultiHeadSelfAttention(embed_dim, num_heads)
        self.ffn = keras.Sequential(
            [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim),]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)
    
    def call(self, inputs, training):
        attn_output = self.att(inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)# 實作embedding layer


class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)  # why這也要?

    def call(self, x):
        maxlen = tf.shape(x)[-1]    # -1, ???
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions

if __name__ == '__main__':
    pass