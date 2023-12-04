from normalize import normalize
from benchmark import run_benchark
from model_maker import make_model
import sys
sys.path.insert(1, './dataset')
from make_dataset_function import make_dataset
import os
from make_charts import make_charts


make_dataset()
normalize()
if not os.path.exists("./cnn/model.keras"):
    make_model()
    run_benchark()

make_charts()