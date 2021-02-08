import base64
from os import listdir
import joblib
from skimage.io import imread
from skimage.transform import resize, rescale
import matplotlib.pyplot as plt
import pandas as pd
from python.Transformer import RGB2GrayTransformer, HogTransformer


def get_data(src, includes, w, h):
    data = {'label': [], 'filename': [], 'rgb': [], 'description': []}

    for current_dir in includes:
        images = [_ for _ in listdir(src + current_dir)]
        for image in images:
            file_path = src + current_dir + "/" + image
            label = file_path.split("/")[2]
            filename = file_path.split("/")[-1]
            rgb = get_image_resized(get_image(file_path), w, h)

            if rgb.shape[-1] != 3:
                continue

            description = "Image d'un {0} redimensionnée ({1}x{2}) en RGB".format(label, int(w), int(h))

            data["label"].append(label)
            data["filename"].append(filename)
            data["rgb"].append(rgb.astype(int))
            data["description"].append(description)

    return pd.DataFrame(data)


def decode(base64_string):
    if isinstance(base64_string, bytes):
        base64_string = base64_string.decode("utf-8")

    imgdata = base64.b64decode(base64_string)
    img = imread(imgdata, plugin='imageio')
    return img


def get_image(file_path):
    return imread(file_path)


def get_image_resized(source, w, h):
    X = resize(source, (w, h), preserve_range=True, anti_aliasing=False)
    return X  # rescale(X, .85, preserve_range=True, multichannel=True)


def save(data, location):
    with open(location, "wb") as f:
        joblib.dump(data, f)


def load(location):
    return joblib.load(location)


def debug_df(df_, idx=0):
    df = df_.groupby("label").nth(idx).reset_index()
    fig, axes = plt.subplots(nrows=1, ncols=9, figsize=(15, 5))
    axes = axes.ravel()
    for i, row in df.iterrows():
        axes[i].imshow(row.rgb)
        axes[i].set_title(row.label)
        axes[i].axis('off')
    return fig


def debug_pipeline_steps(X):
    gray_transformer = RGB2GrayTransformer()
    hog_transformer = HogTransformer()

    gt = gray_transformer.transform(X)

    ht = hog_transformer.transform(gt, visualize=True)

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(20, 20))
    axes = axes.ravel()

    axes[0].set_title("Image redimensionnée (90,90)", fontsize=15)
    axes[0].imshow(X[-1])

    axes[1].set_title("Image au format noir et blanc", fontsize=15)
    axes[1].imshow(gt[-1], cmap="gray")

    axes[2].set_title("Image au format HOG", fontsize=15)
    axes[2].imshow(ht[-1][1], cmap="gray")

    fig.subplots_adjust(wspace=1.5)
