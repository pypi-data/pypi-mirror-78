import random

import tensorflow as tf
from absl import app, logging
from absl.flags import argparse_flags

import lm.config
import lm.encoders
import lm.examples
import lm.human


def parse_args(argv):
    parser = argparse_flags.ArgumentParser()
    parser.add_argument(
        "input",
        type=str,
        help="Path to where your files are located. Files ending in .zst are treated as \
                        archives, all others as raw text.",
    )
    parser.add_argument(
        "--encoder", type=str, required=True, help="Name or path of a tokenizer spec"
    )
    parser.add_argument(
        "--sample_size", type=int, default=10, help="the size of samples to inspect"
    )
    args = parser.parse_args(argv[1:])
    return args


# def load_tokenizer(location):
#     if tf.io.gfile.exists(os.path.join(location, "merges.txt")):
#         # use tf gfile in case the dictionary is remote
#         fastok = GPT2TokenizerFast.from_pretrained(location)
#         fastok.add_special_tokens(
#             {"eos_token": "[EOS]", "pad_token": "[PAD]", "unk_token": "[UNK]",}
#         )
#     else:
#         if location.startswith("/"):
#             raise ValueError("invalid location %s", location)
#         else:
#             fastok = GPT2TokenizerFast.from_pretrained(location)
#     return fastok


def read_example(example_proto, max_seq_len=1024) -> dict:
    features = {
        "id": tf.io.VarLenFeature(tf.int64),
        "content": tf.io.FixedLenFeature([], tf.string),
        "target": tf.io.VarLenFeature(tf.int64),
        "offset_start": tf.io.VarLenFeature(tf.int64),
        "offset_end": tf.io.VarLenFeature(tf.int64),
    }
    parsed_features = tf.io.parse_single_example(example_proto, features)
    return {
        "id": tf.cast(parsed_features["id"], tf.uint64),
        "content": parsed_features["content"],
        "target": tf.sparse.to_dense(tf.cast(parsed_features["target"], tf.int64)),
        "offset_start": tf.sparse.to_dense(
            tf.cast(parsed_features["offset_start"], tf.uint64)
        ),
        "offset_end": tf.sparse.to_dense(
            tf.cast(parsed_features["offset_end"], tf.uint64)
        ),
    }


def main(args):
    encfg = lm.config.load(args.encoder)
    tokenizer = lm.encoders.from_config(encfg)
    with tf.Session() as sess:
        files = lm.human.filepaths_from_user_input(args.input)
        if len(files) == 0:
            logging.error("no file found at %s", args.input)
            return

        sampled_files = random.choices(files, k=args.sample_size)

        ds = tf.data.Dataset.from_tensor_slices(sampled_files)
        ds = ds.interleave(lm.examples.from_file_list(sampled_files), cycle_length=4)
        ds = ds.map(read_example)
        ds = ds.shuffle(1024)
        ds = ds.take(args.sample_size)

        it = ds.make_one_shot_iterator()
        example = it.get_next()

        while True:
            try:
                result = sess.run(example)  # , max_id_tf, min_id_tf])
                pt = lm.examples.PreProcessedTextLine(
                    id=result["id"],
                    content=result["content"],
                    target=result["target"],
                    offset_start=result["offset_start"],
                    offset_end=result["offset_end"],
                )

                ids = tokenizer.decode(result["target"])

                logging.info("gold text:    %r", pt.content.decode("utf-8"))
                logging.info("decoded:       %r", ids)
                logging.info(
                    "tokenization: %s",
                    [
                        pt.content.decode("utf-8")[slice(int(start), int(end))]
                        for start, end in zip(pt.offset_start, pt.offset_end)
                    ],
                )
                logging.info("-" * 10)
            except tf.errors.OutOfRangeError:
                break


def apprun():
    app.run(main, flags_parser=parse_args)


if __name__ == "__main__":
    apprun()
