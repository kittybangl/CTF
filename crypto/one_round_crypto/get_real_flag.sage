#!/usr/bin/env sage
import os
from pwn import remote
from sage.all import GF, Integer, Matrix, ZZ, vector, matrix


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def main():
    dim = 16
    num_rand_pts = 2**15 + 2**10

    host = os.environ.get("HOST", "archive.cryptohack.org")
    port = int(os.environ.get("PORT", 62821))

    F = GF(2)

    P = [os.urandom(dim) for _ in range(128)]
    C = [os.urandom(dim) for _ in range(128)]
    random_pts_bytes = [os.urandom(dim) for _ in range(num_rand_pts)]

    query = ""
    for el in P:
        for m in C:
            query += xor(el, m).hex()
    for pt in random_pts_bytes:
        query += pt.hex()

    io = remote(host, port)
    io.recvuntil(b"> ")
    io.sendline(query.encode())
    res = io.recvline().strip().decode()

    pt_chunks = []
    ct_chunks = []
    random_pts = []
    random_cts = []

    for a in range(len(P)):
        tmp_pt, tmp_ct = [], []
        for b in range(len(C)):
            phex = query[a * dim * 2 * len(C) + b * dim * 2:][: dim * 2]
            chex = res[a * dim * 2 * len(C) + b * dim * 2:][: dim * 2]
            tmp_pt.append(vector(F, Integer(phex, 16).digits(base=2, padto=8 * dim)))
            tmp_ct.append(vector(F, Integer(chex, 16).digits(base=2, padto=8 * dim)))
        pt_chunks.append(tmp_pt)
        ct_chunks.append(tmp_ct)

    base_off = len(P) * dim * 2 * len(C)
    for i in range(num_rand_pts):
        phex = query[base_off + i * dim * 2:][: dim * 2]
        chex = res[base_off + i * dim * 2:][: dim * 2]
        random_pts.append(vector(F, Integer(phex, 16).digits(base=2, padto=8 * dim)))
        random_cts.append(vector(F, Integer(chex, 16).digits(base=2, padto=8 * dim)))

    zero_8 = vector(F, [0] * 8)
    inv_mixing_2 = []
    for i in range(len(P)):
        if len(inv_mixing_2) == dim:
            break
        for j in range(i + 1, len(P)):
            try_ct = ct_chunks[i][0] + ct_chunks[j][0]
            if any(m2 * try_ct == zero_8 for m2 in inv_mixing_2):
                continue

            M = Matrix(F, [ct_chunks[i][k] + ct_chunks[j][k] for k in range(len(C))])
            if M.rank() == 8 * (dim - 1):
                inv_mixing_2.append(matrix(M.right_kernel().basis()))
                if len(inv_mixing_2) == dim:
                    break

    mixing_1 = []
    for m2 in inv_mixing_2:
        base_sub = matrix(m2.right_kernel().basis())
        base_pt = None
        cur_ker_pts = []
        for pt, ct in zip(random_pts, random_cts):
            if base_sub.stack(ct).rank() == 8 * (dim - 1):
                if base_pt is None:
                    base_pt = pt
                else:
                    cur_ker_pts.append(pt + base_pt)

        M = matrix(F, cur_ker_pts)
        mixing_1.append(matrix(M.right_kernel().basis()))

    pairs = 5000
    tmp1 = []
    tmp2 = []
    for pt, ct in zip(random_pts[:pairs + 100], random_cts[:pairs + 100]):
        tmp1.append([m1 * pt for m1 in mixing_1])
        tmp2.append([m2 * ct for m2 in inv_mixing_2])

    recovered_sboxes = None
    for _ in range(20):
        S = [{} for _ in range(dim)]
        ok = True
        for i in range(pairs):
            for pos in range(dim):
                S[pos][tuple(tmp1[i][pos])] = tmp2[i][pos]
        for j in range(pairs, pairs + 100):
            for pos in range(dim):
                if tuple(tmp1[j][pos]) not in S[pos] or S[pos][tuple(tmp1[j][pos])] != tmp2[j][pos]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            recovered_sboxes = S
            break

    if recovered_sboxes is None:
        raise RuntimeError("failed to recover equivalent S-boxes")

    inv_sboxes = [{} for _ in range(dim)]
    for i in range(dim):
        for k, v in recovered_sboxes[i].items():
            inv_sboxes[i][tuple(v)] = vector(F, k)

    io.recvline()  # =====

    inv_mixing_1 = mixing_1[0]
    for i in range(1, dim):
        inv_mixing_1 = inv_mixing_1.stack(mixing_1[i])
    inv_mixing_1 = inv_mixing_1.inverse()

    for _ in range(100):
        target = io.recvline(False)
        target = vector(F, Integer(target, 16).digits(base=2, padto=8 * dim))
        target = [m2 * target for m2 in inv_mixing_2]
        target = [inv_sboxes[i][tuple(x)] for i, x in enumerate(target)]
        target = vector(F, sum([list(x) for x in target], []))
        target = inv_mixing_1 * target

        guess = hex(int(ZZ(list(target), base=2)))[2:-2].zfill(2 * dim - 2)
        io.recvuntil(b"> ")
        io.sendline(guess.encode())

    print(io.recvline().decode().strip())


if __name__ == "__main__":
    main()
