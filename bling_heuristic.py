"""
bling_heuristic.py: Custom heuristic for heudiconv for the bling data. 
"""

__author__ = "Anuja Negi"

import os


def create_key(template, outtype=("nii.gz",), annotation_classes=None):
    if template is None or not template:
        raise ValueError("Template must be a valid format string")
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    t1w = create_key(
        "{session}/anat/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_T1w"
    )
    # dwi = create_key('{session}/dwi/sub-{subject}_run-{item:01d}_dwi')
    # rest = create_key('{session}/func/sub-{subject}_task-rest_rec-{rec}_run-{item:01d}_bold')

    # field maps
    fmap = create_key(
        "{session}/fmap/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_part-{part}"
    )
    fmap_with_dir = create_key(
        "{session}/fmap/sub-{subject}_{session}_acq-{acq}_dir-{dir}_run-{item:02d}_dir-{dir}_{suffix}"
    )

    # localisers
    localiser = create_key(
        "{session}/func/sub-{subject}_{session}_task-{localiser_category}_run-{item:02d}_part-{part}_bold"
    )

    # tasks
    tasks = create_key(
        "{session}/func/sub-{subject}_{session}_task-{task}_run-{item:02d}_part-{part}_bold"
    )

    # physio
    physio = create_key(
        "{session}/beh/sub-{subject}_{session}_run-{item:02d}_part-{part}_recording-{recording}_physio"
    )

    info = {t1w: [], fmap: [], fmap_with_dir: [], localiser: [], tasks: [], physio: []}

    for s in seqinfo:
        # exceptions specific to this study
        if ((s.date == "20190607") or (s.date == "20190709")) and (
            ("run01_5" in s.dcm_dir_name) or ("run01_6" in s.dcm_dir_name)
        ):
            # go to next iteration
            continue

        # t1w
        if "MEMPRAGE" in s.protocol_name:
            if "RMS" in s.series_description:
                info[t1w].append({"item": s.series_id, "acq": "MEMPRAGErms"})
            else:
                info[t1w].append({"item": s.series_id, "acq": "MEMPRAGE"})

        # field maps
        if "gre_field_mapping" in s.protocol_name:
            part = "mag" if "M" in s.image_type else "phase"
            if part == "mag":
                suffix = "magnitude"
            else:
                suffix = "phasediff"
            info[fmap].append(
                {"item": s.series_id, "acq": "gre", "part": part, "suffix": suffix}
            )
        if ("iso" in s.protocol_name) and ("se" in s.protocol_name):
            dir = s.protocol_name[-2:]
            info[fmap_with_dir].append(
                {"item": s.series_id, "acq": "se", "dir": dir, "suffix": "fieldmap"}
            )

        # localisers
        if "ep2d_neuro" in s.protocol_name:
            part = "mag" if "M" in s.image_type else "phase"
            if "CategoryLoc" in s.protocol_name:
                info[localiser].append(
                    {
                        "item": s.series_id,
                        "localiser_category": "category",
                        "part": part,
                    }
                )
            if "MTnew" in s.protocol_name:
                info[localiser].append(
                    {"item": s.series_id, "localiser_category": "mtnew", "part": part}
                )
            if "TOM" in s.protocol_name:
                info[localiser].append(
                    {"item": s.series_id, "localiser_category": "tom", "part": part}
                )
            if "MultipleDemand" in s.protocol_name:
                info[localiser].append(
                    {
                        "item": s.series_id,
                        "localiser_category": "multipledemand",
                        "part": part,
                    }
                )
            if "MotorMixed" in s.protocol_name:
                info[localiser].append(
                    {
                        "item": s.series_id,
                        "localiser_category": "motormixed",
                        "part": part,
                    }
                )
            if "avsnr" in s.protocol_name:
                info[localiser].append(
                    {"item": s.series_id, "localiser_category": "avsnr", "part": part}
                )
            if "AuditoryLoc" in s.protocol_name:
                info[localiser].append(
                    {
                        "item": s.series_id,
                        "localiser_category": "auditory",
                        "part": part,
                    }
                )
        # physio and other continuos data
        if ("ep2d_neuro" in s.protocol_name) or ("iso" in s.protocol_name):
            part = "mag" if "M" in s.image_type else "phase"
            if ("etcalib" in s.protocol_name) or ("eyetrack" in s.protocol_name):
                info[physio].append(
                    {"item": s.series_id, "part": part, "recording": "eyetracking"}
                )
            if "ret" in s.protocol_name:
                info[physio].append(
                    {"item": s.series_id, "part": part, "recording": "retinotopy"}
                )

        # tasks
        if ("iso" in s.protocol_name) or ("Audio" in s.protocol_name):
            part = "mag" if "M" in s.image_type else "phase"
            if "alternateithicatom" in s.protocol_name:
                info[tasks].append(
                    {"item": s.series_id, "task": "alternateithicatom", "part": part}
                )
            if "wheretheressmoke" in s.protocol_name:
                info[tasks].append(
                    {"item": s.series_id, "task": "wheretheressmoke", "part": part}
                )
            if "avatar" in s.protocol_name:
                info[tasks].append(
                    {"item": s.series_id, "task": "avatar", "part": part}
                )
            if "legacy" in s.protocol_name:
                info[tasks].append(
                    {"item": s.series_id, "task": "legacy", "part": part}
                )
            if "odetostepfather" in s.protocol_name:
                info[tasks].append(
                    {"item": s.series_id, "task": "odetostepfather", "part": part}
                )
            if "souls" in s.protocol_name:
                info[tasks].append({"item": s.series_id, "task": "souls", "part": part})
            if "howtodraw" in s.protocol_name:
                info[tasks].append(
                    {"item": s.series_id, "task": "howtodraw", "part": part}
                )
            if "life" in s.protocol_name:
                info[tasks].append({"item": s.series_id, "task": "life", "part": part})
            if "myfirstdaywiththeyankees" in s.protocol_name:
                info[tasks].append(
                    {
                        "item": s.series_id,
                        "task": "myfirstdaywiththeyankees",
                        "part": part,
                    }
                )
            if "naked" in s.protocol_name:
                info[tasks].append({"item": s.series_id, "task": "naked", "part": part})
            if "undertheinfluence" in s.protocol_name:
                info[tasks].append(
                    {"item": s.series_id, "task": "undertheinfluence", "part": part}
                )
            if "fromboyhoodtofatherhood" in s.protocol_name:
                info[tasks].append(
                    {
                        "item": s.series_id,
                        "task": "fromboyhoodtofatherhood",
                        "part": part,
                    }
                )

    return info
