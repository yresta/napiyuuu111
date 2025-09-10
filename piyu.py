import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Token Bot dari BotFather ---
TOKEN = "7973264888:AAFvY8G_-skFdEDO1X5gERfb99HtuLRc_wE"
BOT_USERNAME = "piyuishere_bot"  # tanpa '@'

# QnA database (lebih banyak + random jawaban lucu)
answers = {
    # INFO UMUM
    "treasure": [
        "TREASURE itu boy group YG Entertainment, debut 7 Agustus 2020 💎",
        "TREASURE tuh anak-anak YG yang gemes + talented, debutnya 2020 🎶 uwuwuw~",
        "Boy group dengan 10 member aktif, vibes mereka kayak grup WA keluarga ✨",
        "Kalo dunia ada Avengers, K-pop punya TREASURE 😎🔥",
        "TREASURE = bias kamu + bias wrecker semua orang 🤭",
        "Pokoknya kalo udah jadi Teume, dompet ga pernah aman lagi 💸🤣"
    ],
    "member treasure": [
        "Sekarang ada 10 member aktif: Hyunsuk, Jihoon, Yoshi, Junkyu, Jaehyuk, Asahi, Doyoung, Haruto, Jeongwoo, Junghwan ✨",
        "Ada 10 member aktif, rame banget kayak anak kos lagi masak bareng 🍳",
        "10 orang + 10 bias + 10 alasan Teume susah move on 💙",
        "Sekarang 10 member, tapi energinya 1000 ⚡"
    ],
    "member keluar": [
        "Bang Yedam & Mashiho keluar resmi November 2022 😢 tapi mereka tetep di hati Teume 💙",
        "Mashiho & Yedam pamit 2022, tapi kenangan mereka manis uwu 🥺",
        "Dulu 12, sekarang 10… tapi feel-nya tetep family 💎",
        "Mereka ga di grup, tapi tetep jadi bagian sejarah TREASURE ✨"
    ],
    "fandom": [
        "Fandomnya Teume alias Treasure Maker 💙 uwuwuw~",
        "Namanya Teumeee 💎 keluarga global Treasure!",
        "Teume tuh fandom paling sabar, kuat, dan suka nabung buat lightstick 💡🤣"
    ],
    "debut": [
        "TREASURE debut 7 Agustus 2020 dengan lagu 'BOY' 🎶",
        "Debutnya tahun 2020, judul lagunya 'BOY'. Masih bayi waktu itu 🍼✨",
        "2020 = pandemi, tapi juga tahun lahirnya TREASURE 💎",
        "Debutnya bikin Teume pada teriak 'UWU siapa itu yang cakep-cakep?!' 😍"
    ],
    "lagu populer": [
        "Lagu populer: BOY, I Love You, MMM, JIKJIN, Hello, Bona Bona 🎶",
        "Hit besar mereka tuh JIKJIN 🚗💨, Hello 👋, sama Bona Bonaaa 🎤",
        "Playlist Teume wajib ada JIKJIN, kalo nggak bot Piyu ngamuk 🤖🔥",
        "Bona Bona = lagu wajib di konser buat jungkir balik 🕺"
    ],

    # MEMBER DETAIL (extra kocak)
    "hyunsuk": [
        "Hyunsuk leader karismatik + rapper 🔥",
        "Hyunsuk si brain + swag leader 😎",
        "Keliatan swag, tapi kadang kayak papa muda ngejagain anak-anak 🤭",
        "Hyunsuk itu kayak dosen killer tapi sebenernya sayang muridnya 😆"
    ],
    "jihoon": [
        "Jihoon leader & vokalis, juga MC di acara musik 📺",
        "Visual + leader + MC, paket lengkap uwuw 😍",
        "Kalo Jihoon marah = anak-anak auto diem kek murid ketauan nyontek 🤣",
        "Dia bisa jadi leader, MC, model, kayak multi-level marketing 😆"
    ],
    "asahi": [
        "Asahi jenius musik Jepang, suka bikin lagu 🎶",
        "Asahi si artsy, diem tapi dalam 💙",
        "Asahi = iceberg luar kalem ❄️ dalamnya lava panas 🎇",
        "Dia kayak alien kreatif, musiknya suka bikin Teume teleport 🚀"
    ],
    "jeongwoo": [
        "Jeongwoo vokalis utama dengan suara powerful 🔥",
        "High note killer kita 🎶",
        "Suara Jeongwoo = instant goosebumps 😍",
        "Masih bocil tapi nyanyinya udah level senior 🤯"
    ],
    "junkyu": [
        "Junkyu honey vocal & visual 🐻",
        "Suara Junkyu kayak madu 🍯 bikin candu!",
        "Junkyu = teddy bear besar bisa nyanyi 🎶",
        "Kalo Junkyu senyum, semua Teume auto leleh 🫠"
    ],
    "jaehyuk": [
        "Jaehyuk itu sunshine mood maker ☀️",
        "Ceria + chaos = Jaehyuk 😆",
        "Jaehyuk tuh kayak temen yang ngajak 'ayo healing' tiap weekend 🏞️",
        "Moodbooster grup, bikin vibes selalu positif ✨"
    ],
    "haruto": [
        "Haruto rapper ganteng asal Jepang 🐲",
        "Wajahnya tegas, hatinya uwu 😆",
        "Haruto = anak SMA tinggi banget yang suka ngerap di kantin 🎤",
        "Rapper swag tapi kalo senyum jadi anak bayi 🍼"
    ],
    "junghwan": [
        "Junghwan si maknae, bayi raksasa 🐣",
        "Maknae gemes lahir 2005 🍼✨",
        "Junghwan kadang keliatan cool, tapi hatinya masih suka main bola plastik ⚽🤣",
        "Maknae tapi badannya kayak bodyguard Teume 😎"
    ],

    # LEADER UPDATE
    "leader": [
        "Sekarang leader-nya Junkyu & Asahi mulai Januari 2025 💎",
        "Era baru TREASURE! Junkyu + Asahi jadi leader 🫡",
        "Double leader baru, vibes-nya kayak OSIS ganti ketua 😆",
        "Hyunsuk & Jihoon udah lulus jadi leader, sekarang tongkat estafet ke Junkyu-Asahi ✨"
    ],
    "kenapa ganti leader": [
        "Sekarang sistemnya rotasi tiap 2-3 tahun biar fresh 💫",
        "Biar semua member kebagian pengalaman jadi leader 🚀",
        "YG biar kayak sekolah, ganti ketua kelas tiap semester 🤣",
        "Supaya Teume ga bosen liat leader yang itu-itu aja 😜"
    ],

    # COMEBACK & TOUR
    "comeback 2025": [
        "Ada single 'LAST NIGHT' Des 2024, mini-album Feb 2025, full album pertengahan tahun! 😎",
        "Rencana comeback: mini album Februari, full album Juli/Agustus 2025~",
        "Siapin tabungan, 2025 dompet Teume auto kering 💸",
        "Comebacknya bertubi-tubi, Piyu aja ngos-ngosan keep up 😵‍💫"
    ],
    "tour": [
        "Fan meeting Maret 2025, world tour mulai Oktober! 🌍",
        "Tur dunia dimulai Oktober 2025, gak cuma Asia, full global!",
        "Tour = siap-siap rebutan tiket kaya rebutan sembako 🤯",
        "Worldwide tour! Teume siap jadi atlet marathon ke konser 🏃‍♀️💨"
    ],
}


# Random fallback kalau pertanyaan ga dikenal
fallback_replies = [
    "Ehehe maap aku piyu ga ngerti 😅 coba tanya yang lain dong~",
    "Uwuwu aku bingung 🐧, ayo tanya soal TREASURE lagi 💎",
    "Loh aku blank 😵 coba ulang pertanyaannya hihi",
    "Aku piyu malah kepikiran ayam goreng 🍗😂",
    "Coba tanya tentang member atau lagu TREASURE deh ✨"
]

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    greet = random.choice([
        "Haloooo aku piyuuu 🐧✨ siap nemenin Teume tanya-tanya TREASURE 💎",
        "Haiii aku bot piyu, wushhh~ 💨 siap jawab tentang TREASURE 🫶",
        "Uwuwuw halo Teumee 💎 aku piyu siap jadi teman curhat tentang TREASURE 😆"
    ])
    await update.message.reply_text(greet)

# QnA handler
async def qna(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    reply = None
    for key, vals in answers.items():
        if key in text:
            reply = random.choice(vals)
            break

    if reply:
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text(random.choice(fallback_replies))

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, qna))

    print("Piyu udah onlen uwuwu 🐧🚀")
    app.run_polling()

if __name__ == "__main__":
    main()