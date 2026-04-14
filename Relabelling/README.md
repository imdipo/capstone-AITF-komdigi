Aku bakal secara random ambil 2000 atau 3000 data, terus labelin pake gpt, paling gpt-4o-mini5. tujuannya buat jadiin ground truth yang kemudian aku bakal ngefinetuning IndoBERT atau distilBERT atau apapun itu. 

tujuannya biar bisa ngelabelin secara efisien aja sih, yakali 100.000 lebih data pake api nya openAI. brutal.

label yang dipake:

```python
["Agama", "Politik", "Kesehatan", "Sosial Budaya", "Ekonomi & Bisnis",
  "Sains & Teknologi", "Bencana & Keamanan", "Kriminalitas", "Hiburan & Olahraga", "Lainnya"]
```

## But Why?
tujuannya sih, kalau semua sudah punya label, kita bakal ambil beberapa label saja (misal politik dan sosial budaya). abis itu yang udah tersortir ini kita minta si gpt lagi buat bikinin sebuah claim yang kontradiksi

kalau udah ada claimnya, kan baru bisa kita bikin reasoning untuk bantahan terhadap claim "jahat" itu dengan bantuan fakta berita aslinya.

at the end of the day rencananya dataset SFT nya pake alpaca style, jadi kek strukturnya kayak gini sih kira kira

```python
{
  "instruction": "Analisis apakah narasi berikut merupakan disinformasi berdasarkan konteks berita yang tersedia.",
  "input_claim": "claim:[Hasil Parafrase Disinformasi tadi], sumber_berita:[teks_berita]",
  "response": "label: [label]. faktanya [reasoning_berita]"
}
```
