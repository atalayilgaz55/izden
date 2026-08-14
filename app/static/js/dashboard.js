const alan = document.getElementById("leadler");

const toplamKayit =
    document.getElementById("toplam-kayit");


async function leadleriGetir() {

    try {

        const response = await fetch("/api/leads");

        const data = await response.json();


        if (!data.basari) {

            alan.innerHTML = `
                <div class="message">
                    Kayıtlar alınamadı.
                </div>
            `;

            return;
        }


        toplamKayit.textContent =
            data.leadler.length;


        if (data.leadler.length === 0) {

            alan.innerHTML = `
                <div class="message">
                    Henüz kayıt bulunmuyor.
                </div>
            `;

            return;
        }


        alan.innerHTML = "";


        data.leadler.forEach(lead => {

            const kayit =
                document.createElement("div");

            kayit.className = "record";


            kayit.innerHTML = `

                <div class="record-name">
                    ${lead.isim}
                </div>

                <div class="record-phone">
                    ${lead.telefon}
                </div>

                <div class="record-message">
                    ${lead.mesaj || "-"}
                </div>

                <div class="record-date">
                    ${lead.tarih}
                </div>

            `;


            alan.appendChild(kayit);

        });


    } catch (error) {

        alan.innerHTML = `
            <div class="message">
                Sunucuya bağlanırken bir problem oluştu.
            </div>
        `;

    }
}


leadleriGetir();