"""

"""

import os
from keras.models import load_model
from oap.deep.models import f1
from oap.utils import adjust_y, monochromatic, move_to_y, move_to_x


class ModelV1:

    def __init__(self):
        self.model_c = load_model(os.path.join("models", "final_column_mc_pre14_e11_acc0.98_fs0.98.hdf5"),
                                  custom_objects={'f1': f1})
        self.model_r = load_model(os.path.join("models", "final_rosette_mc_pre06_e05_acc0.97_fs0.97.hdf5"),
                                  custom_objects={'f1': f1})

    def predict(self, array):

        array = adjust_y(array, new_y=64, as_type="array")
        array = move_to_x(array, new_x=31)
        array = move_to_y(array, new_y=31)
        array = monochromatic(array)
        tensor = array.astype(float).reshape(1, 64, 64, 1)
        pred_c = self.model_c.predict(tensor)
        pred_r = self.model_r.predict(tensor)
        print(pred_c, pred_r)


if __name__ == "__main__":
    from tests.data import array01_original

    model = ModelV1()
    model.predict(array01_original)
