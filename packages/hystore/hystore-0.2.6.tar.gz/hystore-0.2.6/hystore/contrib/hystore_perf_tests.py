import time
import numpy as np
import pandas as pd

import h5py

from hystore.core.session import Session
from hystore.core import operations as ops
from hystore.core.operations import ordered_map_to_right_left_unique
from hystore.core import fields as flds
from hystore.core import utils as utils


def generate_a_ids(length, id_base):
    a_ids = np.arange(length, dtype=np.int64) + id_base
    return a_ids


def generate_b_ids(length, id_base, mapping):
    b_ids = np.zeros(length * sum(mapping) // len(mapping), dtype=np.int64)
    cur = 0
    for i in range(length):
        count = mapping[i % 4]
        for c in range(count):
            b_ids[cur] = i + id_base
            cur += 1
    return b_ids


def generate_a_vals(length, min_val, max_val, rng):
    a_vals = rng.randint(min_val, max_val, size=length)
    return a_vals


def generate_dataset_1(length, rng):
    mapping = [0, 1, 2, 1]
    a_id_base = 100000000
    a_ids = np.arange(length, dtype=np.int64) + a_id_base
    a_vals = rng.randint(0, 100, size=length)
    b_ids = np.zeros(length * sum(mapping) // len(mapping), dtype=np.int64)
    cur = 0
    for i in range(length):
        count = mapping[i % 4]
        for c in range(count):
            b_ids[cur] = a_ids[i]
            cur += 1
    return a_ids, a_vals, b_ids


def pd_test_1(length, val_column_count):
    # a_ids, a_vals, b_ids = generate_dataset_1(length, rng)
    rng = np.random.RandomState(12345678)
    id_base = 1000000000
    mapping = [0, 1, 2, 1]
    a_ids = generate_a_ids(length, id_base)
    b_ids = generate_b_ids(length, id_base, mapping)
    a_vals = dict({'id': a_ids})
    for v in range(val_column_count):
        a_vals["vals_{}".format(v)] = generate_a_vals(length, 0, 100, rng)
    a_df = pd.DataFrame(a_vals)
    a_df.set_index('id')
    b_df = pd.DataFrame({'a_id': b_ids})
    b_df.set_index('a_id')
    t0 = time.time()
    r_df = pd.merge(left=b_df, right=a_df, left_on='a_id', right_on='id', how='left')
    # r_df = pd.merge(left=a_df, right=b_df, left_on='id', right_on='a_id', how='right')
    # r_df = b_df.join(a_df, on='a_id')
    msg = "{} elements merged with {} elements in {}s"
    print(msg.format(a_ids.size, b_ids.size, time.time() - t0))
    # for k in a_vals:
    #     if k != 'id':
    #         with utils.Timer("get data and sum"):
    #             vals = r_df[k][:]
    #             print(sum(r_df[k]))
    #         with utils.Timer("repeat get data and sum"):
    #             print(sum(vals))

def hs_test_1(length, val_column_count):
    # a_ids, a_vals, b_ids = generate_dataset_1(length)
    rng = np.random.RandomState(12345678)
    id_base = 1000000000
    mapping = [0, 1, 2, 1]
    s = Session()
    with h5py.File('/home/ben/covid/benchmarking.hdf5', 'w') as hf:
        print('creating a_ids')
        a_ids = generate_a_ids(length, id_base)
        a_ids_f = s.create_numeric(hf, 'a_ids', 'int64')
        a_ids_f.data.write(a_ids)
        del a_ids

        print('creating a_vals')
        # all_a_val_fields = list()
        for v in range(val_column_count):
            a_vals = generate_a_vals(length, 0, 100, rng)
            a_vals_f = s.create_numeric(hf, 'a_vals_{}'.format(v), 'int64')
            a_vals_f.data.write(a_vals)
            # all_a_val_fields.append(a_vals_f)
            del a_vals

        print('creating b_ids')
        b_ids = generate_b_ids(length, id_base, mapping)
        b_ids_f = s.create_numeric(hf, 'b_ids', 'int64')
        b_ids_f.data.write(b_ids)
        del b_ids

        all_b_val_fields = list()
        for v in range(val_column_count):
            b_vals_f = s.create_numeric(hf, 'b_vals_{}'.format(v), 'int32')
            all_b_val_fields.append(b_vals_f)

        a_to_b = s.create_numeric(hf, 'a_to_b', 'int64')

        all_a_val_fields = list()
        for v in range(val_column_count):
            a_vals_f = s.get(hf['a_vals_{}'.format(v)])
            all_a_val_fields.append(a_vals_f)

        print("running test")
        t0 = time.time()
        # s.ordered_left_merge(a_ids, b_ids, a_to_b, left_unique=True,
        #                      left_field_sources=(a_vals_f,), left_field_sinks=(b_vals_f,))
        s.ordered_left_merge(a_ids_f, b_ids_f, a_to_b, left_unique=True,
                             left_field_sources=tuple(all_a_val_fields),
                             left_field_sinks=tuple(all_b_val_fields))
        elapsed = time.time() - t0
        print(elapsed)
        print(all_b_val_fields[0].data[:100])

# from numba import njit
# @njit
def fast_sum(d_it):
    dsum = np.int64(0)
    for d in d_it:
        dsum += d
    return dsum


def minimal_test_1(length, count):
    rng = np.random.RandomState(12345678)
    with h5py.File('/home/ben/covid/benchmarking.hdf5', 'w') as hf:
        for c in range(count):
            vals = generate_a_vals(length, 0, 100, rng)
            with utils.Timer("writing source vals {}".format(c)):
                hf.create_dataset("vals_{}".format(c), chunks=(1<<20,), data=vals)

    with h5py.File('/home/ben/covid/benchmarking.hdf5', 'r+') as hf:
        for c in range(count):
            vname = "vals_{}".format(c)
            with utils.Timer("reading {}".format(vname)):
                vals = hf[vname][:]
            vals *= 2
            v2name = "dest_vals_{}".format(c)
            with utils.Timer("writing {}".format(v2name)):
                hf.create_dataset(v2name, chunks=(1<<20,), data=vals)


def iterator_test_1(length):
    a_ids, a_vals, b_ids = generate_dataset_1(length)
    s = Session()
    with h5py.File('/home/ben/covid/benchmarking.hdf5', 'w') as hf:
        wa_vals = s.create_numeric(hf, 'a_vals', 'int32')
        wa_vals.data.write(a_vals)

        wa_vals2 = s.get(hf['a_vals'])
        print(fast_sum(iter(ops.data_iterator(wa_vals2))))

def raw_np_test_1(length, count):
    rng = np.random.RandomState(12345678)
    for c in range(count):
        vals = generate_a_vals(length, 0, 100, rng)
        with utils.Timer("writing source vals {}".format(c)):
            np.save('/home/ben/covid/test_save/vals_{}'.format(c), vals)

    for c in range(count):
        vname = '/home/ben/covid/test_save/vals_{}.npy'.format(c)
        with utils.Timer("reading {}".format(vname)):
            vals = np.load(vname)
        vals *= 2
        v2name = '/home/ben/covid/test_save/dest_vals_{}'.format(c)
        with utils.Timer("writing {}".format(v2name)):
            np.save(vname, vals)


def read_id_from_csv(file_name, field_count):
    import csv
    with open(file_name) as f:

        rdr = csv.reader(f)
        fields = next(iter(rdr))
        if field_count == 1:
            ids = list()
            with utils.Timer("reading id from dataset"):
                for r in rdr:
                    ids.append(r[0])
        else:
            values = list()
            for _ in range(field_count):
                values.append(list())
            with utils.Timer("reading {} fields from dataset".format(field_count)):
                for r in rdr:
                    for i in range(field_count):
                        values[i].append(r[i])
                    del r

def read_fields_from_hdf5(file_name, field_count):
    fields = ('id', 'created_at', 'updated_at', 'version', 'country_code', 'reported_by_another', 'same_household_as_reporter', 'contact_additional_studies', 'year_of_birth', 'height_cm', 'weight_kg', 'gender', 'race_other', 'ethnicity', 'profile_attributes_updated_at', 'has_diabetes')
    print(len(fields))
    s = Session()
    with h5py.File(file_name, 'r') as hf:
        with utils.Timer("reading {} fields from dataset".format(field_count)):
            for f in range(field_count):
                field = s.get(hf['patients'][fields[f]])
                if isinstance(field, flds.IndexedStringField):
                    indices = field.indices[:]
                    values = field.values[:]
                else:
                    data = field.data[:]

# pd_test_1(1 << 24, 64)
# hs_test_1(1 << 30, 4)
# raw_np_test_1(1 << 29, 4)
# minimal_test_1(1 << 29, 16)
# iterator_test_1(1 << 24)

# read_id_from_csv('/home/ben/covid/patients_export_geocodes_20200830040058.csv', 1)
read_fields_from_hdf5('/home/ben/covid/ds_20200830_full.hdf5', 16)
