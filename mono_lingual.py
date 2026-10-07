import random
from collections import defaultdict
import os

 
GEN_TARGET_SECONDS = 7200  # 2 hours
data_dir ="./input_folder"/  #Add dataset path of langugae ex: Telugu
out_dir = "./output_folder" #Add dataset path of english
os.makedirs(out_dir, exist_ok=True)
for lang in languages:

    random.seed(42)

   
    
    text_file = os.path.join(data_dir, "text")
    utt2dur_file = os.path.join(data_dir, "utt2dur")
    utt2spk_file = os.path.join(data_dir, "utt2spk")
    wavscp_file = os.path.join(data_dir, "wav.scp")

   

    out_lst = os.path.join(out_dir, f"test_set.lst")
    out_wavscp = os.path.join(out_dir, f"test_set_wav.scp")

   
    # Load metadata
  

    utt2text = {}
    with open(text_file, encoding="utf-8") as f:
        for line in f:
            u,t = line.strip().split(maxsplit=1)
            utt2text[u] = t

    utt2dur = {}
    with open(utt2dur_file) as f:
        for line in f:
            u,d = line.strip().split()
            utt2dur[u] = float(d)

    utt2spk = {}
    with open(utt2spk_file) as f:
        for line in f:
            u,s = line.strip().split()
            utt2spk[u] = s

    utt2wav = {}
    with open(wavscp_file) as f:
        for line in f:
            u,w = line.strip().split(maxsplit=1)
            utt2wav[u] = w

 
    # Step 1: select GEN up to 2 hrs
 

    gen_candidates = [u for u,d in utt2dur.items() if 4 <= d <= 10]
    random.shuffle(gen_candidates)

    gen_utts = []
    total_dur = 0

    for u in gen_candidates:

        d = utt2dur[u]

        if total_dur + d > GEN_TARGET_SECONDS:
            break

        gen_utts.append(u)
        total_dur += d

    print(f"{lang} GEN hours:", total_dur/3600)

 
    # Step 2: group GEN by speaker
  
    spk2gen = defaultdict(list)

    for u in gen_utts:
        spk2gen[utt2spk[u]].append(u)

    pairs = []
    needed_utts = set()

 
    # Step 3: pairing
     -

    for gen in gen_utts:

        spk = utt2spk[gen]

        # ref candidates (4–7 sec from GEN only)
        ref_candidates = [
            u for u in spk2gen[spk]
            if 4 <= utt2dur[u] <= 7 and u != gen
        ]

        # if none available → self pair
        if not ref_candidates:
            ref = gen
        else:
            ref = random.choice(ref_candidates)

        pairs.append(
            f"{ref}\t{utt2dur[ref]:.3f}\t{utt2text[ref]}"
            f"\t{gen}\t{utt2dur[gen]:.3f}\t{utt2text[gen]}"
        )

        needed_utts.add(ref)
        needed_utts.add(gen)

 
    # write lst
 

    with open(out_lst,"w",encoding="utf-8") as f:
        for p in pairs:
            f.write(p+"\n")

 
    # write wav.scp
 

    with open(out_wavscp,"w") as f:
        for utt in needed_utts:
            if utt in utt2wav:
                f.write(f"{utt} {utt2wav[utt]}\n")

    print(f"{lang}: {len(pairs)} pairs generated")
