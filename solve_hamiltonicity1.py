#!/usr/bin/env python3
"""CryptoHack Hamiltonicity 1 solver.

- `--mode local` : run an internal verifier simulation and prove we can forge all rounds.
- `--mode remote`: connect to challenge server and send forged proofs.

The exploit is a Fiat-Shamir grinding attack:
for each round, repeatedly sample commitments A until
    SHA256(params || fs_state || A)[-1] & 1
matches a branch we know how to answer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import socket
from dataclasses import dataclass
from typing import Callable

# Challenge parameters from official source.
P = 0x19DAD539E2D348CC3AB07D51F2BB6491D1552AA8CF1DB928920FD3D86946AED8805D2E279FA8632DD5FBAB8AAF7DF1069906B057CC785B7F191EF1B9B5DA38CFF2E7C64DA17BB56A058707D9FD69E546A95E502E556A314C587C7AE36C3D1122E6954F5D81DD9239E02F61B045360187B4CAEED271CEC1919A0D8A39E855040CF
Q = 0xCED6A9CF169A4661D583EA8F95DB248E8AA9554678EDC944907E9EC34A3576C402E9713CFD43196EAFDD5C557BEF8834C83582BE63C2DBF8C8F78DCDAED1C67F973E326D0BDDAB502C383ECFEB4F2A354AF28172AB518A62C3E3D71B61E8891734AA7AEC0EEC91CF017B0D8229B00C3DA65776938E760C8CD06C51CF42A82067
H1 = 250335104192448110684442096964171969189371208477846978499544515755228857598805930673171509152681305793789903169450438090936970626429806187630240086681623358732517929314870247393468568111513100989768455673769015138136779312483203922847547169463972757664497001482465636402329003817055202840451714256443734563502
H2 = 50837518481371967588098771977165879422445597094015682347125264774697010574110399136037637691883034517374621248070926110725252171239208140392324019115211573768989274797050961703999139947885402838647962534519882622024973824201026885393782961783980351898031905383197219266093119145616328556294476943229578292306

N = 5
ROUNDS = 128

# Public graph in challenge (non-Hamiltonian)
G_BAD = [
    [0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0],
]

# Helper graph with known Hamiltonian cycle (for e=1 answers)
G_GOOD = [
    [0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0],
]
CYCLE_GOOD = [(0, 4), (4, 2), (2, 3), (3, 1), (1, 0)]


@dataclass
class RoundProof:
    A: list[list[int]]
    z: list


def pedersen_commit(msg: int) -> tuple[int, int]:
    r = random.randint(0, Q)
    return (pow(H1, msg, P) * pow(H2, r, P)) % P, r


def pedersen_open(c: int, msg: int, r: int) -> bool:
    return (c * pow(H1, -msg, P) * pow(H2, -r, P)) % P == 1


def permute_matrix(m: list[list], perm: list[int]) -> list[list]:
    return [[m[perm[i]][perm[j]] for j in range(N)] for i in range(N)]


def commit_graph(g: list[list[int]]) -> tuple[list[list[int]], list[list[tuple[int, int]]]]:
    A = [[0] * N for _ in range(N)]
    opening = [[(0, 0)] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            c, r = pedersen_commit(g[i][j])
            A[i][j] = c
            opening[i][j] = (g[i][j], r)
    return A, opening


def hash_committed_graph(A: list[list[int]], state: bytes) -> bytes:
    h = hashlib.sha256(str((P, Q, H1, H2)).encode())
    h.update(state)
    h.update("".join(str(x) for row in A for x in row).encode())
    return h.digest()


def random_permutation() -> list[int]:
    p = list(range(N))
    random.shuffle(p)
    return p


def make_branch_0() -> RoundProof:
    # Honest statement: A is a permutation of G_BAD, with full openings.
    A, opening = commit_graph(G_BAD)
    perm = random_permutation()
    A_perm = permute_matrix(A, perm)
    op_perm = permute_matrix(opening, perm)
    # JSON-safe structure (lists instead of tuples)
    z = [perm, [[[m, r] for (m, r) in row] for row in op_perm]]
    return RoundProof(A=A_perm, z=z)


def make_branch_1() -> RoundProof:
    # Cheat statement: A commits to a different graph that *does* have a Hamiltonian cycle.
    A, opening = commit_graph(G_GOOD)
    perm = random_permutation()
    A_perm = permute_matrix(A, perm)

    inv = {old: new for new, old in enumerate(perm)}
    cycle = [[inv[u], inv[v]] for (u, v) in CYCLE_GOOD]
    r_vals = [opening[u][v][1] for (u, v) in CYCLE_GOOD]
    z = [cycle, r_vals]
    return RoundProof(A=A_perm, z=z)


def forge_round(fs_state: bytes, pick_target: Callable[[], int]) -> tuple[RoundProof, bytes, int, int]:
    """Return (proof, new_state, challenge_bit, attempts)."""
    target = pick_target()
    attempts = 0
    while True:
        attempts += 1
        proof = make_branch_0() if target == 0 else make_branch_1()
        new_state = hash_committed_graph(proof.A, fs_state)
        bit = new_state[-1] & 1
        if bit == target:
            return proof, new_state, bit, attempts


# ---------------------- Local verifier (for testing) ----------------------
def is_hamiltonian_cycle(cycle: list[list[int]], n: int) -> bool:
    if len(cycle) != n:
        return False
    if not all(len(edge) == 2 for edge in cycle):
        return False
    in_deg = [0] * n
    out_deg = [0] * n
    for u, v in cycle:
        if not (0 <= u < n and 0 <= v < n):
            return False
        out_deg[u] += 1
        in_deg[v] += 1
    return all(x == 1 for x in in_deg) and all(x == 1 for x in out_deg)


def verify_branch_0(A: list[list[int]], z: list) -> bool:
    perm, opening = z
    if sorted(perm) != list(range(N)):
        return False
    if len(opening) != N or any(len(row) != N for row in opening):
        return False

    # Depermute openings and compare to public G_BAD
    for i in range(N):
        for j in range(N):
            m, r = opening[i][j]
            if m != G_BAD[perm[i]][perm[j]]:
                return False
            if not pedersen_open(A[i][j], m, r):
                return False
    return True


def verify_branch_1(A: list[list[int]], z: list) -> bool:
    cycle, r_vals = z
    if not is_hamiltonian_cycle(cycle, N):
        return False
    if len(r_vals) != N:
        return False
    for (u, v), r in zip(cycle, r_vals):
        if not pedersen_open(A[u][v], 1, r):
            return False
    return True


def run_local(rounds: int) -> None:
    fs_state = b""
    total_attempts = 0
    for i in range(rounds):
        target = random.getrandbits(1)
        proof, fs_state, bit, attempts = forge_round(fs_state, lambda t=target: t)
        total_attempts += attempts

        ok = verify_branch_0(proof.A, proof.z) if bit == 0 else verify_branch_1(proof.A, proof.z)
        if not ok:
            raise RuntimeError(f"local verify failed at round {i}, bit={bit}")
        print(f"[local] round={i:03d} bit={bit} attempts={attempts}")
    print(f"[local] success rounds={rounds}, total_attempts={total_attempts}, avg={total_attempts/rounds:.2f}")


# -------------------------- Remote interaction ----------------------------
def recv_until_prompt(f) -> str:
    out = []
    while True:
        line = f.readline()
        if not line:
            break
        s = line.decode(errors="ignore")
        out.append(s)
        if "> " in s:
            break
    return "".join(out)


def run_remote(host: str, port: int, rounds: int) -> None:
    with socket.create_connection((host, port), timeout=10) as s:
        f = s.makefile("rwb", buffering=0)
        banner = recv_until_prompt(f)
        print(banner, end="")

        fs_state = b""
        total_attempts = 0

        for i in range(rounds):
            target = random.getrandbits(1)
            proof, fs_state, bit, attempts = forge_round(fs_state, lambda t=target: t)
            total_attempts += attempts

            payload = json.dumps({"A": proof.A, "z": proof.z}).encode() + b"\n"
            f.write(payload)
            line = f.readline().decode(errors="ignore")
            print(line, end="")
            if "Incorrect" in line:
                raise RuntimeError(f"server rejected round {i}")

        # read remaining output (usually flag)
        rest = f.read().decode(errors="ignore")
        print(rest)
        print(f"[remote] rounds={rounds}, total_attempts={total_attempts}, avg={total_attempts/rounds:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["local", "remote"], default="local")
    parser.add_argument("--host", default="archive.cryptohack.org")
    parser.add_argument("--port", type=int, default=3721)
    parser.add_argument("--rounds", type=int, default=ROUNDS)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.mode == "local":
        run_local(args.rounds)
    else:
        run_remote(args.host, args.port, args.rounds)


if __name__ == "__main__":
    main()
