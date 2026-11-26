"""Names the cartoon can say out loud: common Indian first names, surnames and family words, each recorded once per
voice, so that people who type their names into the app's Hosts setting hear them in the same natural voice.

Each entry is "Devanagari English [other English spellings]". Typed names are matched with key(), which irons out
common spelling differences (Pooja/Puja, Laxmi/Lakshmi, Shobhit/Sobhit, Karthik/Kartik), or by the Devanagari itself.
A name that is not here is shown on screen as typed, and the voice says "यजमान जी" for it.

python build.py <event> --names records any missing names for the event's voices into builder/namebank/.
"""
import json
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BANK = Path(__file__).resolve().parent.parent / "namebank"

SPECIAL = {"_and": "और", "_yajman": "यजमान जी"}   # joining word and the stand-in for names it can't say

NAMES_TEXT = """
आरव Aarav
आदित्य Aditya
अभय Abhay
अभिनव Abhinav
अभिषेक Abhishek
अभिजीत Abhijeet Abhijit
आदर्श Adarsh
अजय Ajay
अजीत Ajit Ajeet
अक्षय Akshay
आकाश Akash Aakash
अखिल Akhil
आलोक Alok
अमन Aman
अमर Amar
अमित Amit
अमोल Amol
आनंद Anand
अनिल Anil
अनिकेत Aniket
अंकित Ankit
अंकुर Ankur
अनमोल Anmol
अनुज Anuj
अनुपम Anupam
अनुराग Anurag
अर्जुन Arjun
अरुण Arun
अरविंद Arvind Aravind
आशीष Ashish
अशोक Ashok
आशुतोष Ashutosh
अश्विन Ashwin
अतुल Atul
अविनाश Avinash
अयान Ayaan Ayan
आयुष Ayush
बालाजी Balaji
बलराम Balram
भरत Bharat
भास्कर Bhaskar
भावेश Bhavesh
भाविन Bhavin
भूपेंद्र Bhupendra
बिपिन Bipin
बिस्वजीत Biswajit
ब्रजेश Brajesh
चंदन Chandan
चंद्रशेखर Chandrashekhar
चेतन Chetan
चिंतन Chintan
चिराग Chirag
दक्ष Daksh
दर्शन Darshan
देबाशीष Debashish Debasish
दीपक Deepak
दीपांशु Deepanshu
देव Dev
देवांश Devansh
देवेंद्र Devendra
धर्मेंद्र Dharmendra
धर्मेश Dharmesh
धीरज Dheeraj
ध्रुव Dhruv
दिलीप Dilip
दिनेश Dinesh
दिव्यांश Divyansh
गगन Gagan
गणेश Ganesh
गौरव Gaurav
गौतम Gautam
गिरीश Girish
गोकुल Gokul
गोपाल Gopal
गोविंद Govind
हार्दिक Hardik
हरि Hari
हरीश Harish
हर्ष Harsh
हर्षित Harshit
हेमंत Hemant
हिमांशु Himanshu
हितेश Hitesh
इशान Ishaan Ishan
जगदीश Jagdish
जतिन Jatin
जय Jay Jai
जयंत Jayant
जिग्नेश Jignesh
जितेंद्र Jitendra
जितेश Jitesh
कैलाश Kailash
कमल Kamal
कपिल Kapil
करण Karan
कार्तिक Kartik Karthik
कौशल Kaushal
केशव Keshav
केतन Ketan
किशन Kishan
किशोर Kishore Kishor
कृष्ण Krishna
कृष्णन Krishnan
कुणाल Kunal
कुलदीप Kuldeep
कुमार Kumar
लक्ष्य Lakshya
लक्ष्मण Lakshman
ललित Lalit
लव Luv Lav
लोकेश Lokesh
माधव Madhav
महेंद्र Mahendra
महेश Mahesh
मणि Mani
मनीष Manish
मनोज Manoj
मनु Manu
मयंक Mayank
मितेश Mitesh
मोहन Mohan
मोहित Mohit
मुकेश Mukesh
मुकुल Mukul
मुरली Murali Murli
नकुल Nakul
नमन Naman
नारायण Narayan
नरेंद्र Narendra
नरेश Naresh
नवीन Naveen Navin
नीरज Neeraj Niraj
निखिल Nikhil
निलेश Nilesh
निरव Nirav
निशांत Nishant
नितिन Nitin
नितेश Nitesh
ओम Om
ओंकार Omkar
ओमप्रकाश Omprakash
पंकज Pankaj
परेश Paresh
पार्थ Parth
पवन Pawan
पीयूष Piyush
प्रभात Prabhat
प्रभु Prabhu
प्रदीप Pradeep
प्रकाश Prakash
प्रमोद Pramod
प्रणव Pranav
प्रसाद Prasad
प्रशांत Prashant
प्रथमेश Prathamesh
प्रतीक Prateek Pratik
प्रवीण Praveen Pravin
प्रेम Prem
पुनीत Puneet
पुष्पेंद्र Pushpendra
राघव Raghav
रघु Raghu
राहुल Rahul
राज Raj
राजन Rajan
रजत Rajat
राजेंद्र Rajendra
राजेश Rajesh
राजीव Rajeev Rajiv
राजू Raju
राकेश Rakesh
राम Ram
रमेश Ramesh
रणवीर Ranveer Ranvir
रवि Ravi
रविंद्र Ravindra
ऋषभ Rishabh
ऋषि Rishi
रितेश Ritesh
ऋतिक Hrithik Ritik
रोहन Rohan
रोहित Rohit
रूपेश Rupesh
सचिन Sachin
सागर Sagar
साहिल Sahil
समर Samar
समीर Sameer Samir
संदीप Sandeep Sandip
संजय Sanjay
संजीव Sanjeev Sanjiv
संकेत Sanket
संतोष Santosh
सार्थक Sarthak
सतीश Satish
सत्यम Satyam
सौरभ Saurabh Sourabh
सौरव Sourav Saurav
सायन Sayan
शंकर Shankar
शांतनु Shantanu
शरद Sharad
शशांक Shashank
शिव Shiv
शिवम Shivam
शोभित Shobhit
श्रीनिवास Srinivas Shrinivas
श्रेयस Shreyas
शुभम Shubham
श्याम Shyam
सिद्धार्थ Siddharth
सोहन Sohan
सुभाष Subhash
सुब्रत Subrata
सुधाकर Sudhakar
सुदीप Sudeep Sudip
सुधीर Sudhir
सुमित Sumit
सुनील Sunil
सूरज Suraj
सुरेंद्र Surendra
सुरेश Suresh
सुशील Sushil
सुयश Suyash
स्वप्निल Swapnil
तनमय Tanmay
तापस Tapas
तरुण Tarun
तेजस Tejas
तुषार Tushar
उदय Uday
उज्ज्वल Ujjwal
उमेश Umesh
उत्कर्ष Utkarsh
वैभव Vaibhav
वरुण Varun
वेद Ved
वेंकटेश Venkatesh
विभोर Vibhor
विग्नेश Vignesh
विजय Vijay
विकास Vikas
विक्रम Vikram
विनय Vinay
विनीत Vineet
विनोद Vinod
विपिन Vipin
विराज Viraj
विशाल Vishal
विवेक Vivek
योगेश Yogesh
यश Yash
युवराज Yuvraj
आरती Aarti Arti
आराध्या Aaradhya Aradhya
अदिति Aditi
आकांक्षा Akanksha
अलका Alka
अमृता Amrita
अनामिका Anamika
अनन्या Ananya
अंजलि Anjali
अंजू Anju
अंकिता Ankita
अनीता Anita
अनु Anu
अनुपमा Anupama
अनुराधा Anuradha
अनुषा Anusha
अनुष्का Anushka
अपर्णा Aparna
अर्चना Archana
आशा Asha
अश्विनी Ashwini
बबीता Babita
भारती Bharti Bharati
भावना Bhavna Bhavana
भुवना Bhuvana
बिंदु Bindu
चंचल Chanchal
चंदा Chanda
चारु Charu
चेतना Chetna
दक्षा Daksha
दीपा Deepa
दीपिका Deepika
दीप्ति Deepti
देविका Devika
ध्वनि Dhwani
डिंपल Dimple
दिव्या Divya
दुर्गा Durga
गरिमा Garima
गौरी Gauri
गायत्री Gayatri
गीता Geeta Gita
गीतांजलि Geetanjali
हरिणी Harini
हेमा Hema
हेमलता Hemlata
हेतल Hetal
हिना Hina Heena
हिरल Hiral
इंदु Indu
इंद्राणी Indrani
ईशा Isha Esha
इशिता Ishita
जाह्नवी Jahnavi Janvi
जया Jaya
ज्योति Jyoti
काजल Kajal
कल्पना Kalpana
कमला Kamla Kamala
कंचन Kanchan
करिश्मा Karishma
कविता Kavita
काव्या Kavya
कीर्ति Kirti Keerthi
खुशबू Khushboo Khushbu
खुशी Khushi
किंजल Kinjal
किरण Kiran
कोमल Komal
कृतिका Kritika
कुसुम Kusum
लक्ष्मी Lakshmi
लता Lata
लावण्या Lavanya
लीना Leena
माधवी Madhavi
मधु Madhu
माधुरी Madhuri
मालती Malti
मंजू Manju
मानसी Mansi
मीना Meena
मीनाक्षी Meenakshi
मीरा Meera Mira
मेघा Megha
मिताली Mitali
मोना Mona
मोनिका Monika
मौमिता Moumita
मृणाल Mrunal
नम्रता Namrata
नंदिनी Nandini
नीलम Neelam
नीता Neeta Nita
नीतू Neetu
नेहा Neha
निधि Nidhi
निकिता Nikita
निर्मला Nirmala
निशा Nisha
नित्या Nithya Nitya
पद्मा Padma
पल्लवी Pallavi
पारुल Parul
पार्वती Parvati
पायल Payal
पौलमी Poulomi
पूजा Pooja Puja
पूनम Poonam
प्रगति Pragati
प्रज्ञा Pragya
प्राजक्ता Prajakta
प्रतिभा Pratibha
प्रीति Preeti Priti
प्रिया Priya
प्रियंका Priyanka
पुष्पा Pushpa
राधा Radha
राधिका Radhika
रजनी Rajni Rajani
रम्या Ramya
रानी Rani
रश्मि Rashmi
रत्ना Ratna
रीना Reena
रेखा Rekha
रेणु Renu
रेशमा Reshma
रेवती Revathi Revati
ऋचा Richa
रिया Riya
ऋतु Ritu
रूपा Roopa Rupa
रुचि Ruchi
साधना Sadhana
सलोनी Saloni
संध्या Sandhya
संगीता Sangeeta Sangita
सपना Sapna
सरला Sarla
सरस्वती Saraswati
सरिता Sarita
सौम्या Saumya Sowmya
सविता Savita
सायली Sayali
सीमा Seema
शबनम Shabnam
शैलजा Shailja
शालिनी Shalini
शर्मिष्ठा Sharmistha
शीला Sheela Sheila
शिखा Shikha
शिल्पा Shilpa
शिवानी Shivani
शोभा Shobha
श्रद्धा Shraddha
श्रुति Shruti
शुभांगी Shubhangi
श्वेता Shweta
सिमरन Simran
स्मिता Smita
स्नेहा Sneha
सोनल Sonal
सोनम Sonam
सोनिया Sonia
श्रीदेवी Sridevi
सुचित्रा Suchitra
सुधा Sudha
सुमन Suman
सुनीता Sunita
सुप्रिया Supriya
सुषमा Sushma
स्वाति Swati
तनुजा Tanuja
तनुश्री Tanushree
तन्वी Tanvi
तारा Tara
तेजस्विनी Tejaswini
तृप्ति Tripti
उमा Uma
उर्वशी Urvashi
उषा Usha
वैशाली Vaishali
वंदना Vandana
वाणी Vani
वर्षा Varsha
वसुधा Vasudha
वीना Veena
विद्या Vidya
विनीता Vineeta
यामिनी Yamini
अमनदीप Amandeep
अमरजीत Amarjeet
बलजीत Baljeet
दलजीत Daljeet
गगनदीप Gagandeep
गुरलीन Gurleen
गुरमीत Gurmeet
गुरप्रीत Gurpreet
हरभजन Harbhajan
हरजीत Harjeet
हरलीन Harleen
हरमन Harman
हरप्रीत Harpreet
इंदरजीत Inderjeet
जसलीन Jasleen
जसप्रीत Jaspreet
जसविंदर Jasvinder
कुलविंदर Kulvinder
मनदीप Mandeep
मनजीत Manjeet
मनप्रीत Manpreet
नवजोत Navjot
नवनीत Navneet
परमजीत Paramjeet
राजवीर Rajveer
रणजीत Ranjeet Ranjit
सुखविंदर Sukhvinder
आलिया Aaliya Alia
आमिर Aamir Amir
अहमद Ahmed Ahmad
अली Ali
अमजद Amjad
अनवर Anwar
आरिफ़ Arif
असलम Aslam
आसिफ़ Asif
आयशा Ayesha Aisha
फ़ैज़ Faiz
फ़रहा Farah
फ़रहान Farhan
फ़ातिमा Fatima
हमीद Hamid
हसन Hasan Hassan
इमरान Imran
इरफ़ान Irfan
जावेद Javed
करीम Kareem Karim
ख़ालिद Khalid
मरियम Mariam Maryam
मोहम्मद Mohammed Mohammad Muhammad Mohd
नदीम Nadeem
नसीम Naseem
नाज़िया Nazia
नूर Noor
परवेज़ Parvez
रहीम Rahim
रिज़वान Rizwan
रुबीना Rubina
रुख़सार Rukhsar
सबा Saba
सलमान Salman
समीना Sameena
सना Sana
शबाना Shabana
शाहरुख़ Shahrukh
शाहीन Shaheen
शाहिद Shahid
सोहेल Sohail
तारिक़ Tariq
वसीम Waseem Wasim
यास्मीन Yasmin Yasmeen
यूसुफ़ Yusuf
ज़ैद Zaid
ज़ीनत Zeenat
ज़ोया Zoya
एंथनी Anthony
डेविड David
फ़्रांसिस Francis
जॉर्ज George
जेम्स James
जॉन John
जोसेफ़ Joseph
मारिया Maria
मैरी Mary
माइकल Michael
पॉल Paul
पीटर Peter
रोज़ी Rosy Rosie
सारा Sarah Sara
थॉमस Thomas
बबली Babli
बेबी Baby
बबलू Bablu
बिट्टू Bittu
बंटी Bunty
छोटू Chhotu
चिंटू Chintu
डॉली Dolly
गोलू Golu
गुड्डी Guddi
गुड्डू Guddu
हनी Honey
लाडो Lado
मिंटू Mintu
मोनू Monu
मुन्ना Munna
मुन्नी Munni
पप्पू Pappu
पिंकी Pinky Pinki
पिंटू Pintu
रिंकू Rinku
सोनू Sonu
सन्नी Sunny
टिंकू Tinku
अग्रवाल Agarwal Aggarwal Agrawal
आहूजा Ahuja
अंसारी Ansari
अरोड़ा Arora
बनर्जी Banerjee
बंसल Bansal
बत्रा Batra
भट्ट Bhatt Bhat
बोस Bose
चटर्जी Chatterjee
चौधरी Chaudhary Choudhary
चौहान Chauhan
चोपड़ा Chopra
दास Das
देशपांडे Deshpande
देसाई Desai
ढिल्लों Dhillon
डिसूज़ा Dsouza Dsousa
दुबे Dubey Dube
फ़र्नांडिस Fernandes
घोष Ghosh
गिल Gill
गोयल Goyal Goel
गुप्ता Gupta
अय्यर Iyer
जैन Jain
जोशी Joshi
कपूर Kapoor Kapur
ख़ान Khan
खन्ना Khanna
कुलकर्णी Kulkarni
मल्होत्रा Malhotra
मेहता Mehta
मेनन Menon
मिश्रा Mishra
मित्तल Mittal
मुखर्जी Mukherjee
नागर Nagar
नायर Nair
पांडे Pandey Pande
पटेल Patel
पाटिल Patil
पिल्लई Pillai
क़ुरैशी Qureshi
राठौर Rathore
राव Rao
रेड्डी Reddy
रॉय Roy
सक्सेना Saxena
सेन Sen
सेठ Seth
सेठी Sethi
शाह Shah
शेख़ Shaikh Sheikh
शर्मा Sharma
शील Sheel
शुक्ला Shukla
सिद्दीक़ी Siddiqui
सिंह Singh
सिंघल Singhal
श्रीवास्तव Srivastava Shrivastava
ठाकुर Thakur
तिवारी Tiwari
त्रिपाठी Tripathi
वर्मा Verma
यादव Yadav
जी Ji
फ़ैमिली Family
परिवार Parivar
मम्मी Mummy Mommy
मॉम Mom
पापा Papa
माँ Maa Ma
दादी Dadi
दादा Dada
नानी Nani
नाना Nana
चाचा Chacha
चाची Chachi
मामा Mama
मामी Mami
बुआ Bua
फूफा Phupha Fufa
मौसी Mausi Masi
मौसा Mausa
ताऊ Tau
ताई Tai
भैया Bhaiya Bhaiyya
भाभी Bhabhi
दीदी Didi
जीजू Jiju
जीजा Jija
भाई Bhai
बहन Behen Behan
अंकल Uncle
आंटी Aunty Auntie
साहब Sahab Saheb
मैडम Madam
सर Sir
पंडित Pandit
गुरुजी Guruji
बाबा Baba
"""


def entries():
    out = []
    for line in NAMES_TEXT.strip().splitlines():
        parts = line.split()
        out.append({"hi": parts[0], "en": parts[1], "alt": parts[2:]})
    return out


def key(latin):
    """Spelling-insensitive key for a typed Latin name. Kept identical to nameKey() in the app."""
    s = re.sub(r"[^a-z]", "", latin.lower())
    for a, b in (("x", "ks"), ("ph", "f"), ("sh", "s"), ("w", "v"), ("q", "k"), ("z", "j")):
        s = s.replace(a, b)
    s = re.sub(r"([kgcjtdpb])h", r"\1", s)
    for a, b in (("ee", "i"), ("oo", "u"), ("aa", "a"), ("ii", "i"), ("uu", "u")):
        s = s.replace(a, b)
    s = re.sub(r"([^aeiou])\1+", r"\1", s)
    return s


def table():
    """Lookup data for the app: [[Devanagari, English, [keys...]], ...]."""
    rows, seen = [], {}
    for e in entries():
        keys = []
        for spelling in [e["en"]] + e["alt"]:
            k = key(spelling)
            if k and k not in keys:
                keys.append(k)
            if k in seen and seen[k] != e["hi"]:
                raise SystemExit(f"name key clash: {spelling} ({e['hi']}) and {seen[k]}")
            seen[k] = e["hi"]
        rows.append([e["hi"], e["en"], keys])
    return rows


# ---------------------------------------------------------------- recording

def _clip_mp3(samples, rate, dest):
    import numpy as np
    import wave
    x = np.asarray(samples, dtype=np.float32)
    peak = float(np.max(np.abs(x))) or 1.0
    x = x / peak * 0.89
    x = np.concatenate([np.zeros(int(rate * 0.03), np.float32), x, np.zeros(int(rate * 0.06), np.float32)])
    wav = dest.with_suffix(".wav")
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ac", "1", "-codec:a", "libmp3lame", "-b:a", "64k", str(dest)], check=True)
    wav.unlink()


def build(voices):
    """Record every bank word missing for these voices and pack each voice into <voice>.mp3 + <voice>.json.

    The pack is the clips' MP3 files one after another; the index gives each word's byte range, onset and mouth cues.
    """
    import voice as V
    import lips as L
    BANK.mkdir(exist_ok=True)
    words = {e["hi"]: e["hi"] for e in entries()}
    words.update({k: v for k, v in SPECIAL.items()})
    tool = L.rhubarb()
    for vname in voices:
        idx_path, pack_path = BANK / f"{vname}.json", BANK / f"{vname}.mp3"
        old = json.loads(idx_path.read_text(encoding="utf-8")) if idx_path.exists() else {}
        old_pack = pack_path.read_bytes() if pack_path.exists() else b""
        todo = [w for w in words if w not in old]
        clips = {}
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            if todo:
                tts = V.engine(vname)
                for n, w in enumerate(todo):
                    audio = V.say(tts, words[w] + "।")
                    f = tmp / f"{n}.mp3"
                    _clip_mp3(audio.samples, audio.sample_rate, f)
                    clips[w] = f
                with ThreadPoolExecutor(6) as pool:
                    cues = dict(zip(todo, pool.map(lambda w: L.cues(clips[w], tool), todo)))
            index, pack = {}, bytearray()
            for w in sorted(words):
                if w in clips:
                    data, cue = clips[w].read_bytes(), cues[w]
                else:
                    o, n, cue = old[w]
                    data = old_pack[o:o + n]
                index[w] = [len(pack), len(data), cue]
                pack += data
        pack_path.write_bytes(bytes(pack))
        idx_path.write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":"), sort_keys=True), encoding="utf-8")
        print(f"name bank {vname}: {len(index)} words, {len(todo)} newly recorded, {len(pack) // 1024} KB")
