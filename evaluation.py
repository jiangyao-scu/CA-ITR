import time
import torch
import numpy as np


def evalrank(img_embs, cap_embs, dataset, device, curve=None):
    # one image to five captions, since have repetitive images
    # for F30K, imgs 1000, captions 5000.
    # for COCO, imgs 5000, captions 25000. (5-fold is five times of 1000 imgs)
    if dataset == 'COD':
        img_embs = img_embs
    else:
        img_embs = img_embs[::5]

    print('Images: %d, Captions: %d' % (img_embs.shape[0], cap_embs.shape[0]))

    # sims = shard_attn_scores(img_embs, cap_embs)
    sims = img_embs @ cap_embs.T
    # sims = pairwise_inner(img_embs, cap_embs, curve)


    # npts = the number of images
    npts = img_embs.shape[0]

    r, rt = i2t(npts, sims, return_ranks=True, dataset=dataset)
    ri, rti = t2i(npts, sims, return_ranks=True, dataset=dataset)

    # # r[0] -> R@1, r[1] -> R@5, r[2] -> R@10
    # ar = (r[0] + r[1] + r[2]) / 3
    # ari = (ri[0] + ri[1] + ri[2]) / 3

    # rsum = r[0] + r[1] + r[2] + ri[0] + ri[1] + ri[2]
    # print("rsum: %.1f" % rsum)
    # print("Average i2t Recall: %.1f" % ar)
    print("Image to text (R@1, R@5, R@10): %.1f %.1f %.1f" % r[:3])
    # print("Average t2i Recall: %.1f" % ari)
    print("Text to image (R@1, R@5, R@10): %.1f %.1f %.1f" % ri[:3])

    if dataset!='COD':
        print("multiple fold evaluation")
        group_size = 1000
        num_groups = len(img_embs) // group_size + (1 if len(img_embs) % group_size else 0)

        results = []
        for i in range(num_groups):
            start_img = i * group_size
            end_img = (i + 1) * group_size if i < num_groups - 1 else len(img_embs)
            img_emb = img_embs[start_img:end_img]
            start_cap = i * group_size * 5
            end_cap = (i + 1) * group_size * 5 if i < num_groups - 1 else len(cap_embs)
            cap_emb = cap_embs[start_cap:end_cap]

            sims = img_emb @ cap_emb.T
            npts = img_emb.shape[0]

            mr, mrt = i2t(npts, sims, return_ranks=True, dataset=dataset)
            mri, mrti = t2i(npts, sims, return_ranks=True, dataset=dataset)

            print('------------------------------')
            print("Image to text (R@1, R@5, R@10): %.1f %.1f %.1f" % mr[:3])
            print("Text to image (R@1, R@5, R@10): %.1f %.1f %.1f" % mri[:3])

            results += [list(mr) + list(mri)]

        print("-----------------------------------")
        print("Mean metrics: ")
        mean_metrics = tuple(np.array(results).mean(axis=0).flatten())
        print("Image to text (R@1, R@5, R@10): %.1f %.1f %.1f" % mean_metrics[:3])
        print("Text to image (R@1, R@5, R@10): %.1f %.1f %.1f" % mean_metrics[5:8])


    return r, ri, rt, rti

def i2t(npts, sims, return_ranks=False, dataset='COD'):

    ranks = np.zeros(npts)
    top1 = np.zeros(npts)
    sims = sims.softmax(dim=-1)
    sims = sims.cpu().numpy()
    for index in range(npts):
        
        inds = np.argsort(sims[index])[::-1]

        if dataset != 'COD':
            rank = 1e20
            for i in range(5 * index, 5 * index + 5, 1):
                tmp = np.where(inds == i)[0][0]
                if tmp < rank:
                    rank = tmp
            ranks[index] = rank
            top1[index] = inds[0]
        else:
            rank = np.where(inds == index)[0][0]
            ranks[index] = rank
            top1[index] = inds[0]

    # Compute metrics
    r1 = 100.0 * len(np.where(ranks < 1)[0]) / len(ranks)
    r5 = 100.0 * len(np.where(ranks < 5)[0]) / len(ranks)
    r10 = 100.0 * len(np.where(ranks < 10)[0]) / len(ranks)
    medr = np.floor(np.median(ranks)) + 1
    meanr = ranks.mean() + 1

    if return_ranks:
        return (r1, r5, r10, medr, meanr), (ranks, top1)
    else:
        return (r1, r5, r10, medr, meanr)


def t2i(npts, sims, return_ranks=False, dataset='COD'):

    if dataset != 'COD':
        ranks = np.zeros(5 * npts)
        top1 = np.zeros(5 * npts)
    else:
        ranks = np.zeros(npts)
        top1 = np.zeros(npts)

    # --> (5N(caption), N(image))
    sims = sims.T

    sims = sims.softmax(dim=-1)
    sims = sims.cpu().numpy()

    for index in range(npts):
        if dataset != 'COD':
            for i in range(5):
                inds = np.argsort(sims[5 * index + i])[::-1]
                ranks[5 * index + i] = np.where(inds == index)[0][0]
                top1[5 * index + i] = inds[0]
        else:
            inds = np.argsort(sims[index])[::-1]
            ranks[index] = np.where(inds == index)[0][0]
            top1[index] = inds[0]

    # Compute metrics
    r1 = 100.0 * len(np.where(ranks < 1)[0]) / len(ranks)
    r5 = 100.0 * len(np.where(ranks < 5)[0]) / len(ranks)
    r10 = 100.0 * len(np.where(ranks < 10)[0]) / len(ranks)
    medr = np.floor(np.median(ranks)) + 1
    meanr = ranks.mean() + 1
    if return_ranks:
        return (r1, r5, r10, medr, meanr), (ranks, top1)
    else:
        return (r1, r5, r10, medr, meanr)



if __name__ == '__main__':

    pass
