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
        "{session}/fmap/sub-{subject}_{session}_run-{item:02d}_part-{part}_epi"
    )

    # localisers
    localiser = create_key(
        "{session}/func/sub-{subject}_{session}_task-{localiser_category}_run-{item:02d}_part-{part}_bold"
    )

    # tasks
    tasks = create_key(
        "{session}/func/sub-{subject}_{session}_task-{task}_run-{item:02d}_part-{part}_bold"
    )
    # avatar = create_key('{session}/func/sub-{subject}_task-avatar_run-{item:01d}_bold')
    # avatar = create_key('sub-{subject}/func/sub-{subject}_task-avatar_bold')

    info = {
        t1w: [],
        # dwi: [],
        # rest: [],
        fmap: [],
        localiser: [],
        tasks: [],
        # avatar: []
    }

    for s in seqinfo:
        # exceptions specific to this study
        if ((s.date == "20190607LG") or (s.date == "20190709LG")) and (
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
            info[fmap].append({"item": s.series_id, "part": part})

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
            if "ret" in s.protocol_name:
                info[localiser].append(
                    {
                        "item": s.series_id,
                        "localiser_category": "retinotopy",
                        "part": part,
                    }
                )
            if "AuditoryLoc" in s.protocol_name:
                info[localiser].append(
                    {
                        "item": s.series_id,
                        "localiser_category": "auditory",
                        "part": part,
                    }
                )

        # tasks
        if "iso" in s.protocol_name:
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
            if "wheretheressmoke" in s.protocol_name:
                info[tasks].append(
                    {"item": s.series_id, "task": "wheretheressmoke", "part": part}
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
