#!/usr/bin/env python
import pandas as pd
from ome_model import experimental as ome
import os
import sys
import tifffile


def create_companion(tif, name, outstem):
    outpath = f'{outstem}companion.ome'
    tiflink = f'{outstem}tif'

    if not os.path.islink(tiflink):
        os.symlink(tif, tiflink)

    if not os.path.isfile(outpath):
        im = tifffile.imread(tif, is_ome=False)
        t, z, c = 1, 1, 1
        if len(im.shape) == 2:
            y, x = im.shape
        elif len(im.shape) == 3:
            c, y, x = im.shape
        elif len(im.shape) == 4:
            z, c, y, x = im.shape
        else:
            t, z, c, y, x = im.shape
        dt = str(im.dtype)

        companion = ome.Image(os.path.basename(name), x, y, z, c, t, order='XYCZT', type=dt)
        # TODO: Delete and regenerate all companion files after symlinking image to local path
        companion.add_tiff(os.path.basename(tif), planeCount=(t * z * c))        
        # companion.add_tiff(tif, planeCount=(t * z * c))
        for nc in range(c):
            companion.add_channel(samplesPerPixel=1)
        with open(outpath, 'wb') as o:
            ome.create_companion(images=[companion], out=o)


def rowfunc(r):
    prefix = '/uod/idr/filesets/idr0071-feldman-crisprko/20191104-gcloud/'
    companion_prefix = '/uod/idr/metadata/idr0071-feldman-crisprko/companions/'
    assert r['tif'].startswith(prefix) and r['tif'].endswith('.tif')
    companion_stem = r['tif'][len(prefix):-3]
    basepath = os.path.dirname(companion_stem)
    os.makedirs(basepath, exist_ok=True)
    create_companion(r['tif'], r['name'], companion_stem)
    return pd.Series([
        r['target'],
        f'{companion_prefix}{companion_stem}companion.ome',
        r['name'],
    ])


for filein in sys.argv[1:]:
    fileout = filein.replace('-tif', '-companion')
    print(f'{filein} ⇒ {fileout}')
    df = pd.read_csv(filein, dtype=str, names=('target', 'tif', 'name'), delimiter='\t')
    import_list = df.apply(rowfunc, axis=1)
    import_list.to_csv(fileout, sep='\t', header=False, index=False)
