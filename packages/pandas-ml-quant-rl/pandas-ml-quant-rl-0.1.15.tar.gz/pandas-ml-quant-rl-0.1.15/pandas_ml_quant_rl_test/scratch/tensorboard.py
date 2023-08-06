from tensorboardX import SummaryWriter
import time

from pandas_ml_quant_rl.wrapper.tensorboardX import EasySummaryWriter

log_file_context = 'lala'
log_file = f'/tmp/{log_file_context}/{int(time.time() / 60) - int(time.time() / 60 / 100000) * 100000}'
print(f"tensorboard --logdir {log_file_context}")

#sw = SummaryWriter(log_file)
sw = EasySummaryWriter("test")

for i in range(100):
    sw.add_scalars("lala", {"a": i, "b": -i}, i)

#sw.add_histogram()