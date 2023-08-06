from __future__ import absolute_import, division, print_function

import mesh_tensorflow as mtf
import tensorflow.compat.v1 as tf
from pydantic.dataclasses import dataclass


@dataclass
class OptimizerConfig:
    pass


def clip_by_global_norm(grads, clip_norm):
    """Clip the grads by global norm."""
    global_norm = mtf.sqrt(
        mtf.add_n([mtf.reduce_sum(mtf.square(t)) for t in grads if t is not None])
    )
    multiplier = clip_norm / mtf.maximum(global_norm, clip_norm)
    clipped_grads = [None if t is None else t * multiplier for t in grads]
    return clipped_grads, global_norm


def get_optimizer(loss, params, summary, inp_var_grads=None):
    """Creates and returns an optimizer training op."""

    global_step = tf.train.get_or_create_global_step()  # get global step
    mesh = loss.mesh  # get mesh info from loss
    graph = mesh.graph  # get graph info from mesh

    if inp_var_grads is None:
        var_grads = mtf.gradients(
            [loss], [v.outputs[0] for v in graph.trainable_variables]
        )
    else:
        var_grads = inp_var_grads

    learning_rate = tf.constant(
        value=params["lr"], shape=[], dtype=tf.float32
    )  # grab lr param

    if params["lr_decay"] == "linear":
        learning_rate = tf.train.polynomial_decay(
            learning_rate,
            global_step,
            params["train_steps"],
            end_learning_rate=params["lr"]
            * 0.1,  # decrease to 10% of initial LR according to GPT-3 paper
            power=1.0,
            cycle=False,
        )
    elif params["lr_decay"] == "cosine":
        learning_rate = tf.train.cosine_decay(
            learning_rate,
            global_step,
            params["train_steps"],
            alpha=0.1,  # alpha is min lr value as a fraction of init lr.
        )

    if params["warmup_steps"] > 0:
        global_steps_int = tf.cast(global_step, tf.int32)
        warmup_steps_int = tf.constant(params["warmup_steps"], dtype=tf.int32)

        global_steps_float = tf.cast(global_steps_int, tf.float32)
        warmup_steps_float = tf.cast(warmup_steps_int, tf.float32)

        warmup_percent_done = global_steps_float / warmup_steps_float
        warmup_learning_rate = learning_rate * warmup_percent_done

        is_warmup = tf.cast(global_steps_int < warmup_steps_int, tf.float32)
        learning_rate = (
            1.0 - is_warmup
        ) * learning_rate + is_warmup * warmup_learning_rate

    summary.scalar("lr", learning_rate)

    if params["opt_name"].lower() == "adam":
        optimizer = mtf.optimize.AdamWeightDecayOptimizer(
            learning_rate=learning_rate,
            weight_decay_rate=params["weight_decay"],
            beta_1=params["beta1"],
            beta_2=params["beta2"],
            epsilon=params["epsilon"],
            exclude_from_weight_decay=["norm", "bias"],
        )
    else:
        optimizer = mtf.optimize.AdafactorOptimizer(
            learning_rate=params["lr"],
            decay_rate=params["weight_decay"],
            beta1=params["beta1"],
            epsilon1=params["ada_epsilon1"],
            epsilon2=params["ada_epsilon2"],
        )

    if params["gradient_clipping"] is not None:
        clip_value = mtf.constant(mesh, params["gradient_clipping"], dtype=tf.float32)
        (var_grads, _) = clip_by_global_norm(var_grads, clip_norm=clip_value)

    update_ops = optimizer.apply_grads(var_grads, graph.trainable_variables)
    return learning_rate, update_ops
