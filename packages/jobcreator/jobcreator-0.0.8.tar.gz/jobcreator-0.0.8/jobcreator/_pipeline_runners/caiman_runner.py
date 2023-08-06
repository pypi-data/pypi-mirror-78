#!/usr/bin/env python
import argparse
import logging
import glob
import os
import pickle
import sys
from time import sleep

import numpy as np

from ..utils.misc import get_settings

f = (
    "%(relativeCreated)12d [%(filename)s:%(funcName)20s():%(lineno)s]"
    "[%(process)d] %(message)s"
)
logging.basicConfig(
    format=f, filename="caiman.log", filemode="w", level=logging.DEBUG,
)

DEFAULT_MCORR_SETTINGS = {
    "fr": 10,  # movie frame rate
    "decay_time": 0.4,  # length of a typical transient in second
    "pw_rigid": False,  # flag for performing piecewise-rigid motion correction
    "max_shifts": (5, 5),  # maximum allowed rigid shift
    "gSig_filt": (3, 3),  # size of high pass spatial filtering, used in 1p data
    "strides": (48, 48),
    "overlaps": (24, 24),
    "max_deviation_rigid": (
        3
    ),  # maximum deviation allowed for patch with respect to rigid shifts
    "border_nan": "copy",  # replicate values along the boundaries
}

DEFAULT_CNMF_PARAMETERS = {
    "method_init": "corr_pnr",  # use this for 1 photon
    "K": None,  # upper bound on number of components per patch, in general None
    "gSig": (3, 3),  # gaussian width of a 2D gaussian kernel
    "gSiz": (13, 13),  # average diameter of a neuron, in general 4*gSig+1
    "merge_thr": 0.7,  # merging threshold, max correlation allowed
    "p": 1,  # order of the autoregressive system
    "tsub": 2,  # downsampling factor in time for initialization
    "ssub": 1,  # downsampling factor in space for initialization,
    "rf": 40,  # half-size of the patches in pixels
    "stride": 20,  # amount of overlap between the patches in pixels
    "only_init": True,  # set it to True to run CNMF-E
    "nb": 0,  # number of background components (rank) if positive
    "nb_patch": 0,  # number of background components (rank) per patch if gnb>0
    "method_deconvolution": "oasis",  # could use 'cvxpy' alternatively
    "low_rank_background": None,
    "update_background_components": True,
    # sometimes setting to False improve the results
    "min_corr": 0.8,  # min peak value from correlation image
    "min_pnr": 10,  # min peak to noise ration from PNR image
    "normalize_init": False,  # just leave as is
    "center_psf": True,  # leave as is for 1 photon
    "ssub_B": 2,  # additional downsampling factor in space for background
    "ring_size_factor": 1.4,  # radius of ring is gSiz*ring_size_factor,
    "del_duplicates": True,
    "border_pix": 0,
}

DEFAULT_QC_PARAMETERS = {
    "min_SNR": 2.5,  # adaptive way to set threshold on the transient size
    "rval_thr": 0.85,
    "use_cnn": False,
}


def parse_args():
    parser = argparse.ArgumentParser(description="Suite2p parameters")
    parser.add_argument("--file", default=[], type=str, help="options")
    parser.add_argument("--ncpus", default=1, type=int, help="options")
    parser.add_argument("--mc_settings", default="", type=str, help="options")
    parser.add_argument("--cnmf_settings", default="", type=str, help="options")
    parser.add_argument("--qc_settings", default="", type=str, help="options")
    args = parser.parse_args()

    file_path = args.file
    n_cpus = args.ncpus
    mc_settings = args.mc_settings
    cnmf_settings = args.cnmf_settings
    qc_settings = args.qc_settings

    return file_path, n_cpus, mc_settings, cnmf_settings, qc_settings


def run(
    file_path,
    n_cpus,
    mc_settings: dict = {},
    cnmf_settings: dict = {},
    qc_settings: dict = {},
):
    mkl = os.environ.get("MKL_NUM_THREADS")
    blas = os.environ.get("OPENBLAS_NUM_THREADS")
    vec = os.environ.get("VECLIB_MAXIMUM_THREADS")
    print(f"MKL: {mkl}")
    print(f"blas: {blas}")
    print(f"vec: {vec}")

    # we import the pipeline upon running so they aren't required for all installs
    import caiman as cm
    from caiman.motion_correction import MotionCorrect
    from caiman.source_extraction.cnmf import params as params
    from caiman.source_extraction import cnmf

    # load and update the pipeline settings
    mc_parameters = DEFAULT_MCORR_SETTINGS
    for k, v in mc_settings.items():
        mc_parameters[k] = v
    cnmf_parameters = DEFAULT_CNMF_PARAMETERS
    for k, v in cnmf_settings.items():
        cnmf_parameters[k] = v
    qc_parameters = DEFAULT_QC_PARAMETERS
    for k, v in qc_settings.items():
        qc_parameters[k] = v

    # get the filenames
    file_pattern = os.path.join(file_path, "*.tif*")
    fnames = glob.glob(file_pattern)
    print(fnames)
    mc_parameters["fnames"] = fnames

    opts = params.CNMFParams(params_dict=mc_parameters)

    print("starting server")
    # start the server

    n_proc = np.max([(n_cpus - 1), 1])
    c, dview, n_processes = cm.cluster.setup_cluster(
        backend="local", n_processes=n_proc, single_thread=False
    )
    print(n_processes)
    sleep(30)

    print("motion corr")
    sys.stdout.flush()
    pw_rigid = mc_parameters["pw_rigid"]
    mc = MotionCorrect(fnames, dview=dview, **opts.get_group("motion"))
    mc.motion_correct(save_movie=True)
    fname_mc = mc.fname_tot_els if pw_rigid else mc.fname_tot_rig
    if pw_rigid:
        bord_px = np.ceil(
            np.maximum(
                np.max(np.abs(mc.x_shifts_els)), np.max(np.abs(mc.y_shifts_els))
            ).astype(np.int)
        )

    print("writing mmap")
    sys.stdout.flush()
    bord_px = 0
    fname_new = cm.save_memmap(
        fname_mc, base_name="memmap_", order="C", border_to_0=bord_px
    )

    print("stopping server")
    sys.stdout.flush()
    cm.stop_server(dview=dview)

    # load mmap
    print("loading mmap")

    # load memory mappable file
    Yr, dims, T = cm.load_memmap(fname_new)
    images = Yr.T.reshape((T,) + dims, order="F")

    # Don't seed with predetermined binary masks
    Ain = None

    # starting server
    print("starting server")
    sys.stdout.flush()
    c, dview, n_processes = cm.cluster.setup_cluster(
        backend="local", n_processes=n_proc, single_thread=False
    )
    print(n_processes)
    sleep(30)

    opts.change_params(
        params_dict=cnmf_parameters
    )  # number of pixels to not consider in the borders)

    # starting server
    print("cnmf")
    sys.stdout.flush()
    cnm = cnmf.CNMF(n_processes=n_processes, dview=dview, Ain=Ain, params=opts)
    cnm.fit(images)

    print("evaluate components")
    sys.stdout.flush()
    cnm.params.set("quality", qc_parameters)
    cnm.estimates.evaluate_components(images, cnm.params, dview=dview)

    print("saving results")
    cnm.save(cnm.mmap_file[:-4] + "hdf5")

    # save the parameters in the same dir as the results
    final_params = cnm.params.to_dict()
    path_base = os.path.dirname(cnm.mmap_file)
    params_file = os.path.join(path_base, "all_caiman_parameters.pkl")
    with open(params_file, "wb") as fp:
        pickle.dump(final_params, fp)

    print("stopping server")
    cm.stop_server(dview=dview)


def main():
    (
        file_path,
        n_cpus,
        mc_settings_path,
        cnmf_settings_path,
        qc_settings_path,
    ) = parse_args()

    mc_settings = get_settings(mc_settings_path)
    cnmf_settings = get_settings(cnmf_settings_path)
    qc_settings = get_settings(qc_settings_path)

    # run the pipeline
    run(
        file_path=file_path,
        n_cpus=n_cpus,
        mc_settings=mc_settings,
        cnmf_settings=cnmf_settings,
        qc_settings=qc_settings,
    )
