try:
    from ..utils.data_loader import read_mat_file
except:
    from utils.data_loader import read_mat_file

from .preprocess import normalize_data
from .io_helper import save_windowed_dataset_hdf5
import numpy as np
import os
import re
import json
from tqdm import tqdm


def get_file_list(root, ext=""):
    f_list = []

    for r, d, f in os.walk(root):
        for fname in f:
            if fname.endswith(ext):
                f_list.append("{}/{}".format(r, fname))
    return f_list


def prepare_data(root, full_length=False, accelerometer=True, gyroscope=True, orientation=False,
                 stroke=False, dataset_type="Drill", merge_clap_null=True, verbose=1):
    csv_list = []
    segment_data_list = []
    segment_timestamp_list = []
    labels_list = []
    subjects_list = []

    label_info = dict()
    unique_subjects = set()
    file_list = get_file_list(root, ext=".mat")

    pbar = tqdm(file_list, desc="Reading mat files ...")
    dataset_type = dataset_type.lower()
    for i, fpath in enumerate(pbar):
        subject_name = re.search("(S[0-9]+_|[sS]troke[0-9]+)", fpath).group().replace("_", "").lower()
        data_collection_type = re.search("_((D|d)rill|(I|i)ndi|(L|l)ong)", fpath).group().replace("_", "").lower()
        if dataset_type != "all" and data_collection_type != dataset_type:
            continue

        if (stroke and not subject_name.startswith("stroke")) or \
                (not stroke and subject_name.startswith("stroke")):
            continue

        pbar.set_description("Reading {} ...".format(fpath))

        unique_subjects.add(subject_name)

        try:
            segment_data = []
            segment_tstamp = []
            labels = []
            subjects = []

            csv, video, segment = read_mat_file(fpath)
            for segment_x, segment_sensor_data, label, name in zip(segment['segment_x'], segment['segment_sensor_data'], segment['segment_label'], segment['segment_name']):
                name = name.replace(" ", "").lower().replace("pck", "pick")

                # Fix wrong label START
                erratas = {
                        'clapnull': 'clap',
                        'openrefrigv': 'openrefrig',
                        '청소기밀기': 'vacuum',
                        'clapl': 'clap'
                    }

                if name in erratas.keys():
                    name = erratas[name]
                # Fix wrong label END

                if merge_clap_null:
                    name = name.replace("clap", "null")

                if name not in label_info.keys():
                    label_info[name] = len(label_info)

                segment_data.append(segment_sensor_data)
                segment_tstamp.append(segment_x)
                subjects.append(subject_name)
                labels.append(label_info[name])

            csv_list.append(csv)
            segment_data_list.append(segment_data)
            segment_timestamp_list.append(segment_tstamp)
            labels_list.append(labels)
            subjects_list.append(subjects)

        except ValueError:
            print("Read Error! {}".format(fpath))

    unique_subjects = sorted(unique_subjects)

    if verbose > 0:
        print("Label information")
        inv_label = {v: k for k, v in label_info.items()}
        flatten_labels = [lab for label in labels_list for lab in label]
        label_hist = np.histogram(flatten_labels, bins=len(label_info) - 1)

        for hist, label in zip(label_hist[0], label_hist[1]):
            print("{}: {}, ".format(inv_label[label], hist), end="")
        print("")

    sensor_idx = []
    if accelerometer:
        sensor_idx += [0, 1, 2]
    if gyroscope:
        sensor_idx += [3, 4, 5]
    if orientation:
        sensor_idx += [6, 7, 8]

    if not full_length:
        segment_data = [segment for segments in segment_data_list for segment in segments]
        labels = [lab for label in labels_list for lab in label]
        subjects = [sub for subject in subjects_list for sub in subject]

        for i in range(len(segment_data)):
            segment_data[i] = segment_data[i][:, sensor_idx, :]

        return segment_data, labels, subjects, label_info, unique_subjects
    else:
        for i in range(len(segment_data_list)):
            for j in range(len(segment_data_list[i])):
                segment_data_list[i][j] = segment_data_list[i][j][:, sensor_idx, :]

            csv_list[i]["sensor_data"] = csv_list[i]["sensor_data"][:, sensor_idx, :]

        return csv_list, segment_data_list, segment_timestamp_list, labels_list, subjects_list, label_info, unique_subjects


def get_full_length_label_data(root, accelerometer=True, gyroscope=True, orientation=False, stroke=False,
                               dataset_type="Drill", merge_clap_null=True, verbose=1):

    csv_list, segment_data_list, segment_timestamp_list, labels_list, subjects_list, label_info, unique_subjects = prepare_data(
        root, full_length=True, accelerometer=accelerometer, gyroscope=gyroscope, orientation=orientation, stroke=stroke,
        merge_clap_null=merge_clap_null, verbose=verbose, dataset_type=dataset_type)

    data_list = []
    label_list = []
    subject_list = []

    for data_idx in range(len(segment_timestamp_list)):
        ground_truth = np.zeros(csv_list[data_idx]['x'].shape)
        for segment_idx in range(len(segment_timestamp_list[data_idx])):
            label = labels_list[data_idx][segment_idx]
            if label == 0:
                continue

            ts, te = segment_timestamp_list[data_idx][segment_idx][[0, -1]]
            mask = np.argwhere(np.logical_and(csv_list[data_idx]['x'] >= ts, csv_list[data_idx]['x'] <= te)).flatten()
            ground_truth[mask] = label

        subject = subjects_list[data_idx][0]

        data_list.append(csv_list[data_idx]['sensor_data'])
        label_list.append(ground_truth)
        subject_list.append(subject)

    return data_list, label_list, subject_list, label_info, unique_subjects


def generate_training_test_data(data, label, subjects, subject_list, training_portion=0.7, shuffle=False, cv=-1, n_cv=1, verbose=0):

    training_size = int(len(subject_list)*training_portion)

    sub_list = list(subject_list.copy())
    if shuffle:
        np.random.shuffle(sub_list)

    if cv > 0:
        test_size = int(len(subject_list) * 1/cv)

        idx1 = int(len(subject_list) * (1-(n_cv/cv)))
        idx2 = min(idx1+test_size, len(subject_list))

        training_subjects = sub_list[0:idx1] + sub_list[idx2:]
    else:
        training_subjects = sub_list[:training_size]

    if verbose > 0:
        for sub in subject_list:
            if sub in training_subjects:
                print(" {} , ".format(sub), end="")
            else:
                print("|{}|, ".format(sub), end="")
        print("")

    training_data = []
    training_label = []
    training_subject = []
    test_data = []
    test_label = []
    test_subject = []

    for i in range(len(data)):
        if subjects[i] in training_subjects:
            training_data.append(data[i])
            training_label.append(label[i])
            training_subject.append(subjects[i])
        else:
            test_data.append(data[i])
            test_label.append(label[i])
            test_subject.append(subjects[i])

    return training_data, training_label, training_subject, test_data, test_label, test_subject


def make_training_data(data_root: str, save_root: str = None, window_size: int = 300,
                       stride: int = 1, chunk_size: int = 50,
                       normalize_axis: bool = True, dataset_type: str = "Drill", stroke: bool =  False,
                       merge_clap_null: bool = True, training_portion: float =0.8, shuffle: bool = True,
                       verbose: int = 1):
    """

    Args:
        data_root (): Root directory of dataset
        save_root (): Root directory of generated data. None if window_size < 1
        window_size (): Less than 1 will return without sliding windowed data as (training_data, training_label, training_subject, test_data, test_label, test_subject)
        stride (): Size of stride
        chunk_size ():
        normalize_axis (): Normalize each sensors by (x-mu)/sigma
        dataset_type (str):
        merge_clap_null (): Treats clap label as null
        training_portion (): Percentage of subjects included in training data from entire dataset
        shuffle (): Shuffle subjects order.
        verbose ():

    Returns:

    """
    assert (save_root is not None and window_size > 0) or window_size < 1

    if window_size < 1:
        data, label, subjects, label_info, unique_subjects = get_full_length_label_data(data_root,
                                                                                        accelerometer=True,
                                                                                        gyroscope=True,
                                                                                        orientation=False,
                                                                                        stroke=stroke,
                                                                                        dataset_type=dataset_type,
                                                                                        merge_clap_null=merge_clap_null,
                                                                                        verbose=verbose)
    else:
        data, label, subjects, label_info, unique_subjects = prepare_data(data_root,
                                                                          stroke=stroke,
                                                                          dataset_type=dataset_type,
                                                                          merge_clap_null=merge_clap_null)

    data = [data[i] for i in range(len(data)) if np.argwhere(np.isnan(data[i])).shape[0] == 0]

    if normalize_axis:
        data, std_v, mean_v = normalize_data(data)

    training_data, training_label, training_subject, test_data, test_label, test_subject = \
        generate_training_test_data(data, label, subjects, unique_subjects, training_portion=training_portion,
                                    shuffle=shuffle, verbose=verbose)

    if window_size < 1:
        return training_data, training_label, training_subject, test_data, test_label, test_subject, label_info

    os.makedirs(save_root, exist_ok=True)
    save_windowed_dataset_hdf5(training_data, training_label, test_data, test_label,
                               window_size=window_size, stride=stride, save_root=save_root,
                               chunk_size=chunk_size)

    with open("{}label_info.json".format(save_root), "w") as f:
        json.dump(label_info, f)


if __name__ == "__main__":
    pass
