#!/usr/bin/env python
from functools import partial
import pandas as pd
import os
from tifffile import imread

df = pd.read_csv('IDR_transfer_files.20191027_235752.csv', dtype=str)
fillna = ''
df['cycle'].fillna(fillna, inplace=True)

basedir = '/uod/idr/filesets/idr0071-feldman-crisprko/20191104-gcloud/'

with open('idr0071-feldman-crisprko-files-unrenamed.txt') as f:
    local_filelist = set(f.read().split())


def rowfunc(r, exp):
    project = 'idr0071-feldman-crisprko/experiment{}'.format(exp)
    process = 'process' if (r['path'] == '{}/process'.format(exp)) else 'raw'
    cycleifset = (r['cycle'] + ' ') if r['cycle'] else ''
    # Prefix datasets with {exp} due to https://github.com/ome/omero-blitz/issues/91
    # They will have to be renamed later
    dataset = '{exp} {cycleifset}{tag} {well} {process}'.format(
        **r, exp=exp, cycleifset=cycleifset, process=process)

    filepath = r.file.replace('gs://idr_transfer/', basedir)

    return pd.Series([
        'Project:name:{}/Dataset:name:{}'.format(project, dataset),
        filepath,
        os.path.splitext(os.path.basename(r.file))[0].strip(),
    ])


for exp in 'ABCDEF':
    print('Experiment', exp)
    experiment = df.loc[(df['experiment'] == exp) & (df['ext'] == 'tif')]
    import_list = experiment.apply(partial(rowfunc, exp=exp), axis=1)
    for f in import_list.loc[:,1]:
        assert f in local_filelist, 'Not found: ' + f
    import_list.to_csv('idr0071-experiment{}-filelist-tif.tsv'.format(exp), sep='\t', header=False, index=False)
