import io
import tensorflow as tf
import model as m

MODEL, PREDICTION_MODEL = m.build_model()
MODEL.load_weights('my_model.hdf5')

def ocr():
    """OCR the captcha"""
    dataset = tf.data.Dataset.from_tensor_slices((['test.jpeg'], None))
    dataset = (
        dataset.map(m.encode_single_sample,
                    num_parallel_calls=tf.data.AUTOTUNE)
        .batch(16)  # batch size
        .prefetch(buffer_size=tf.data.AUTOTUNE)
    )

    out = PREDICTION_MODEL.predict(dataset)
    out = m.decode_batch_predictions(out, 6)  # max length = 6

    return out

a = open("test.jpeg", "rb")
captcha = io.BytesIO(open("test.jpeg", "rb").read())

print(ocr())
