const sohbetAlani = document.getElementById("sohbet-alani");

const mesajInput = document.getElementById("mesaj");

const sorButonu = document.getElementById("sor-butonu");

const isimInput = document.getElementById("isim");

const telefonInput = document.getElementById("telefon");

const ilgiInput = document.getElementById("ilgi");

const kaydetButonu = document.getElementById("kaydet-butonu");

const sonuc = document.getElementById("sonuc");


// AI ile yapılan konuşmayı burada tutuyoruz.
const sohbetGecmisi = [];


// Kullanıcı mesajını ekrana ekler.
function kullaniciMesajiEkle(mesaj) {

    sohbetAlani.innerHTML += `
        <div class="ml-auto max-w-[85%]">
            <div class="rounded-2xl rounded-br-md bg-[#64aaaa] px-4 py-3 text-sm leading-6 text-white shadow-sm">
                ${mesaj}
            </div>
        </div>
    `;
}


// AI mesajını ekrana ekler.
function aiMesajiEkle(mesaj) {

    sohbetAlani.innerHTML += `
        <div class="max-w-[85%]">
            <div class="mb-1 text-xs font-medium text-[#4d9293]">
                İZDEN
            </div>

            <div class="rounded-2xl rounded-bl-md bg-white/80 px-4 py-3 text-sm leading-6 text-gray-700 shadow-sm">
                ${mesaj}
            </div>
        </div>
    `;
}


// AI cevap beklenirken gösterilir.
function yukleniyorGoster() {

    sohbetAlani.innerHTML += `
        <div
            id="ai-yukleniyor"
            class="max-w-[85%]"
        >

            <div class="mb-1 text-xs font-medium text-[#4d9293]">
                İZDEN
            </div>

            <div class="inline-flex items-center gap-2 rounded-2xl rounded-bl-md bg-white/80 px-4 py-3 text-sm text-gray-500 shadow-sm">

                <span>
                    Düşünüyor
                </span>

                <span class="flex gap-1">

                    <span class="h-1.5 w-1.5 animate-bounce rounded-full bg-gray-400"></span>

                    <span
                        class="h-1.5 w-1.5 animate-bounce rounded-full bg-gray-400"
                        style="animation-delay: 0.15s"
                    ></span>

                    <span
                        class="h-1.5 w-1.5 animate-bounce rounded-full bg-gray-400"
                        style="animation-delay: 0.3s"
                    ></span>

                </span>

            </div>

        </div>
    `;

    sohbetAlani.scrollTop = sohbetAlani.scrollHeight;
}


// Yükleniyor mesajını kaldırır.
function yukleniyorKaldir() {

    const yukleniyor =
        document.getElementById("ai-yukleniyor");

    if (yukleniyor) {
        yukleniyor.remove();
    }
}


// Sohbete mesaj gönderir.
async function mesajGonder(mesaj) {

    if (!mesaj) {
        return;
    }


    kullaniciMesajiEkle(mesaj);

    mesajInput.value = "";

    sorButonu.disabled = true;

    yukleniyorGoster();


    try {

        const response = await fetch("/api/sohbet", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                mesaj: mesaj,
                gecmis: sohbetGecmisi
            })

        });


        const data = await response.json();


        yukleniyorKaldir();


        if (!data.basari) {

            aiMesajiEkle(
                data.mesaj || "Bir hata oluştu."
            );

            return;
        }


        aiMesajiEkle(data.cevap);


        // Konuşma geçmişine kullanıcı mesajını ekle.
        sohbetGecmisi.push({
            role: "user",
            content: mesaj
        });


        // Konuşma geçmişine AI cevabını ekle.
        sohbetGecmisi.push({
            role: "assistant",
            content: data.cevap
        });


    } catch (error) {

        yukleniyorKaldir();

        aiMesajiEkle(
            "Şu anda bağlantı kuramıyorum. Lütfen biraz sonra tekrar dene."
        );

    } finally {

        sorButonu.disabled = false;

        mesajInput.focus();

        sohbetAlani.scrollTop =
            sohbetAlani.scrollHeight;
    }
}


// Sor butonu.
sorButonu.addEventListener("click", () => {

    const mesaj = mesajInput.value.trim();

    mesajGonder(mesaj);
});


// Enter ile mesaj gönderme.
mesajInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {

        event.preventDefault();

        const mesaj =
            mesajInput.value.trim();

        mesajGonder(mesaj);
    }
});


// "İz Bırak" butonu.
function izBirak() {

    const mesaj =
        "İZDEN'e kendi yaratıcı çalışmamı bırakmak istiyorum. Nasıl iz bırakabilirim?";

    mesajGonder(mesaj);

    isimInput.focus();
}


// "Bir İşi Devam Ettir" butonu.
function isiDevamEttir() {

    const mesaj =
        "İZDEN'de başka birinin bıraktığı yaratıcı işi devam ettirmek istiyorum. Nasıl katılabilirim?";

    mesajGonder(mesaj);
}


// Katılım formu.
kaydetButonu.addEventListener("click", async () => {

    const isim = isimInput.value.trim();

    const telefon = telefonInput.value.trim();

    const ilgi = ilgiInput.value.trim();


    // Zorunlu alan kontrolü.
    if (!isim || !telefon) {

        sonuc.textContent =
            "Lütfen ad ve telefon bilgilerinizi doldurun.";

        sonuc.className =
            "min-h-6 text-sm text-red-600";

        return;
    }


    // Kaydet butonunu geçici olarak kapat.
    kaydetButonu.disabled = true;


    try {

        const response = await fetch("/api/leads", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                isim: isim,

                telefon: telefon,

                mesaj: ilgi
            })

        });


        const data = await response.json();


        if (data.basari) {

            sonuc.textContent =
                "Bilgilerin başarıyla kaydedildi. Teşekkürler.";

            sonuc.className =
                "min-h-6 text-sm text-[#4d9293]";


            isimInput.value = "";

            telefonInput.value = "";

            ilgiInput.value = "";


        } else {

            sonuc.textContent =
                data.mesaj;

            sonuc.className =
                "min-h-6 text-sm text-red-600";
        }


    } catch (error) {

        sonuc.textContent =
            "Kayıt sırasında bir bağlantı problemi oluştu.";

        sonuc.className =
            "min-h-6 text-sm text-red-600";


    } finally {

        kaydetButonu.disabled = false;
    }

});