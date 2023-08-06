from ai_training_utils.logging_helper import Logger
from tensorboard import program


def run_tensorboard(log_dir: str):
    tb = program.TensorBoard()
    tb.configure(argv=[None, '--logdir', log_dir])
    url = tb.launch()
    Logger().info('Started Tensorboard at %s' % url)
