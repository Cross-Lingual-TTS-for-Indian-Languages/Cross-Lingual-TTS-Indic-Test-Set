import random
import os


random.seed(42)


# Load language metadata
 
data_folder =" " #Add dataset path of langugae ex: Telugu
english= ""  #Add dataset path of english
out_dir = f"./{lang}_english" #Change to Your Output Path
os.makedirs(out_dir, exist_ok=True)

GEN_TARGET_SECONDS =3600 #Change According the Requirement

def load_metadata(data_dir):

    text_file = os.path.join(data_dir, "text")
    utt2dur_file = os.path.join(data_dir, "utt2dur")
    wavscp_file = os.path.join(data_dir, "wav.scp")

    utt2text = {}
    with open(text_file, encoding="utf-8") as f:
        for line in f:
            u, t = line.strip().split(maxsplit=1)
            utt2text[u] = t

    utt2dur = {}
    with open(utt2dur_file) as f:
        for line in f:
            u, d = line.strip().split()
            utt2dur[u] = float(d)

    utt2wav = {}
    with open(wavscp_file) as f:
        for line in f:
            u, w = line.strip().split(maxsplit=1)
            utt2wav[u] = w

    return utt2text, utt2dur, utt2wav


def select_gen_utts(utt2dur):

    candidates = [u for u, d in utt2dur.items() if 4 <= d <= 10]
    random.shuffle(candidates)

    gen_utts = []
    total = 0

    for u in candidates:

        d = utt2dur[u]

        if total + d > GEN_TARGET_SECONDS:
            continue

        gen_utts.append(u)
        total += d

    print("GEN hours:", total / 3600)

    return gen_utts


 


eng_text, eng_dur, eng_wav = load_metadata(english)
eng_gen = select_gen_utts(eng_dur)
eng_ref = [u for u in eng_gen if 4 <= eng_dur[u] <= 7]

for lang in languages:
    random.seed(42)
    indic_lang = f"{data_folder}/{lang}/test"
   
    indic_text, indic_dur, indic_wav = load_metadata(indic_lang)
  

    

    out_lst = os.path.join(out_dir, "test_set.lst")
    out_wavscp = os.path.join(out_dir, "test_set_wav.scp")
     
    # Select GEN sets
    indic_gen = select_gen_utts(indic_dur)
   


    # REF candidates (subset of GEN)
    indic_ref = [u for u in indic_gen if 4 <= indic_dur[u] <= 7]
   
    if not eng_ref:
        raise ValueError("No English REF candidates (4-7s)")
    if not indic_ref:
        raise ValueError(f"No REF candidates for {lang}")

    pairs = []
    needed_utts = set()


     
    # Case 1: ENG REF → indic GEN
     

    for gen in indic_gen:

        ref = random.choice(eng_ref)

        pairs.append(
            f"{ref}\t{eng_dur[ref]:.3f}\t{eng_text[ref]}"
            f"\t{gen}\t{indic_dur[gen]:.3f}\t{indic_text[gen]}"
        )

        needed_utts.add(ref)
        needed_utts.add(gen)


     
    # Case 2: indic REF → ENG GEN
     

    for gen in eng_gen:

        ref = random.choice(indic_ref)

        pairs.append(
            f"{ref}\t{indic_dur[ref]:.3f}\t{indic_text[ref]}"
            f"\t{gen}\t{eng_dur[gen]:.3f}\t{eng_text[gen]}"
        )

        needed_utts.add(ref)
        needed_utts.add(gen)


     
    # Write test_set.lst
     

    with open(out_lst, "w", encoding="utf-8") as f:
        for p in pairs:
            f.write(p + "\n")


     
    # Write wav.scp
     

    with open(out_wavscp, "w") as f:

        for utt in needed_utts:

            if utt in indic_wav:
                f.write(f"{utt} {indic_wav[utt]}\n")

            elif utt in eng_wav:
                f.write(f"{utt} {eng_wav[utt]}\n")


    print("Total pairs:", len(pairs))
    print("Saved to:", out_dir)
