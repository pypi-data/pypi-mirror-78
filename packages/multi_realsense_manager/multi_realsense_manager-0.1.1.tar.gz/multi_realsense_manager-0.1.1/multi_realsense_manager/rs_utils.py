#!/usr/bin/env python3

import numpy as np


def splice_imgs(imgs):
    npc = np.concatenate
    if len(imgs) == 1:
        return imgs[0]
    if len(imgs) == 2:
        return npc([imgs[0], imgs[1]], 0)
    if len(imgs) >= 3:
        idx = 0
        while idx < len(imgs):
            if not idx:
                big = npc([imgs[0], imgs[1]], 1)
            else:
                if len(imgs) - idx == 1:
                    big = npc([big[::2, ::2], imgs[idx]], 0)
                else:
                    big = npc([big, npc([imgs[idx], imgs[idx + 1]], 1)], 0)[::2, ::2]
            idx += 2
        return big


def merge_depth_image_for_vis(data):
    color = data["color"]
    depth = data["depth"]
    from skimage.exposure import equalize_hist

    vis = (
        color / 255 * (1 - equalize_hist(np.where(depth == 0, 80930, depth)))[..., None]
    )
    return (vis * 255).astype(np.uint8)


if __name__ == "__main__":
    pass
