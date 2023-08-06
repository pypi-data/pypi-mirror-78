import numpy as np


def normalize_data(data):
    concat_data = np.concatenate([np.swapaxes(d, 1, 2).reshape(-1, d.shape[1]) for d in data])
    concat_data = np.split(concat_data, concat_data.shape[1] // 3, axis=1)

    std_v = [c_data.std() for c_data in concat_data]
    mean_v = [m_data.mean() for m_data in concat_data]

    for d in data:
        for i in range(d.shape[1]//3):
            s_idx = i * 3
            e_idx = i * 3 + 3

            d[:, s_idx:e_idx, :] = (d[:, s_idx:e_idx, :] - mean_v[i]) / std_v[i]

    return data, std_v, mean_v


def reshape_data(data, rotate=True):
    data = data.reshape(data.shape[0], data.shape[1], data.shape[2]*data.shape[3])
    if rotate:
        data = np.rot90(data, axes=(1,2))

    return data


def generate_sliding_window_data(data, label, window_size=300, stride=1):
    n_data = 0
    for d, l in zip(data, label):
        if d.shape[0] < window_size:
            continue

        for i in range(0, d.shape[0] - window_size, stride):
            n_data += 1

    w_data = np.zeros((n_data, window_size, data[0].shape[1], data[0].shape[2]))
    w_label = np.zeros((n_data, ))
    idx = 0
    for d, l in zip(data, label):
        if d.shape[0] < window_size:
            continue

        for i in range(0, d.shape[0]-window_size, stride):
            w_data[idx] = d[i:(i+window_size)]
            w_label[idx] = l
            idx += 1

    return w_data, w_label
