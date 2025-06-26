from django.shortcuts import render,redirect
import os
from django.conf import settings
import json

qrup_3_altqrup = ["Beynəlxalq münasibətlər", "Regionşünaslıq", "Beynəlxalq münasibətlər (tədris ingilis dilində)",
                  "Beynəlxalq münasibətlər (tədris türk dilində)", "Regionşünaslıq (Amerika üzrə, tədris ingilis dilində)",
                  "Regionşünaslıq (Amerika üzrə)", "Regionşünaslıq (Almaniya üzrə)", "Regionşünaslıq(Koreya üzrə)", "Regionşünaslıq(Türkiyə üzrə)",
                  "Regionşünaslıq (Böyük Britaniya üzrə,tədris ingilis dilində)", "Regionşünaslıq (Yaponiya üzrə)", "Regionşünaslıq (Türkiyə üzrə)",
                  "Regionşünaslıq (Fransa üzrə)", "Regionşünaslıq (Norveç üzrə)", "Regionşünaslıq (Qafqaz üzrə)", "Regionşünaslıq (Çin üzrə)",
                  "Regionşünaslıq(İsrailüzrə)", "Regionşünaslıq (Cənubi Amerika üzrə)", "Regionşünaslıq (ərəb ölkələri üzrə)",
                  "Regionşünaslıq(Pakistan üzrə)", "Regionşünaslıq (Mərkəzi və Şərqi Avropa üzrə)", "Regionşünaslıq (Böyük Britaniya üzrə)",
                  "Regionşünaslıq(İran üzrə)", "Regionşünaslıq (Rusiya üzrə)", "Regionşünaslıq (Balkan ölkələri üzrə)",
                  "Regionşünaslıq (Azərbaycan üzrə)", "Regionşünaslıq (İsrail və Yaxın Şərq üzrə)", "Regionşünaslıq (Xəzəryanı ölkələr üzrə)",
                  "Regionşünaslıq(Amerikaşünaslıq, Avropaşünaslıq, Asiyaşünaslıq, Şərqşünaslıq, tədris ingilis dilində)",
                  "Regionşünaslıq (Polşa üzrə)", "Regionşünaslıq (Çexiya üzrə)", "Regionşünaslıq (Ukrayna üzrə)", "Regionşünaslıq (Rusiya üzrə)",
                  "Regionşünaslıq (Belarus üzrə)", "Regionşünaslıq (Pakistan üzrə)", "Regionşünaslıq (ABŞ və Kanada, Avropa ölkələri, Yaxın və Orta Şərq üzrə)",
                  "Regionşünaslıq (Afrika üzrə)", "Regionşünaslıq (İndoneziya üzrə)", "Regionşünaslıq (Bolqarıstan üzrə)", "Regionşünaslıq (Yunanıstan üzrə)",
                  "Regionşünaslıq (regionlar üzrə)", "Regionşünaslıq (Avropa ölkələri üzrə)", "Regionşünaslıq (Avropa üzrə)"]


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def teklif(request):
    return render(request, "teklif.html")

def game(request):
    return render(request, 'game.html')


def uniler(request):
    return render(request, "uniler.html")

import os
from django.conf import settings
from django.shortcuts import render

def show_scores(request, group):
    if request.method == "POST":
        burax = request.POST.get("burax")
        blok = request.POST.get("blok")
        altqrup = request.POST.get("altqrup", "")

        try:
            burax = float(burax)
            blok = float(blok)
            total = round(burax + blok, 2)
            return redirect(f"/ballar-filter/{group}/?total={total}&altqrup={altqrup}")
        except (TypeError, ValueError):
            pass

    return render(request, "ballar.html", {
        "total": None,
        "result": [],
        "universities": [],
        "ixtisaslar": [],
        "group": group
    })


def filter_scores(request, group):
    results = []
    universities_set = set()
    ixtisaslar_set = set()

    total_score = request.GET.get("total")
    altqrup = request.GET.get("altqrup", "")
    try:
        total_score = float(total_score)
    except (TypeError, ValueError):
        total_score = None

    file_path = os.path.join(settings.BASE_DIR, "unichat/datas", f"universitetler_{group}qrup.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Altqrup məlumatı
    altqrup_data = []
    altqrup_path = os.path.join(settings.BASE_DIR, "unichat/datas", "altqrup_1.json")
    if os.path.exists(altqrup_path):
        with open(altqrup_path, "r", encoding="utf-8") as altdata:
            altqrup_data = json.load(altdata)

    for uni_name, majors in data.items():
        for major in majors:
            ixtisas = major["ixtisas"].strip()

            if altqrup == "TC" and ("Beynəlxalq münasibətlər" not in ixtisas and "Regionşünaslıq" not in ixtisas):
                continue
            elif altqrup == "DT" and ixtisas in []:  # qrup_3_altqrup varsa əlavə et
                continue
            elif altqrup == "RI" and ixtisas not in altqrup_data:
                continue
            elif altqrup == "RK" and ixtisas in altqrup_data:
                continue

            odenissiz = major.get("odenissiz_bali")
            odenisli = major.get("odenisli_bali")
            match = False

            if total_score is None:
                match = True
            elif (odenissiz is None and odenisli is None):
                match = True
            elif (odenissiz is not None and total_score >= odenissiz) or (
                odenisli is not None and total_score >= odenisli):
                match = True

            if match:
                universitet = uni_name.strip()
                eyani_qiyabi = "Əyani" if major["eyani_qiyabi"] == "Ə" else "Qiyabi"

                universities_set.add(universitet)
                ixtisaslar_set.add(ixtisas)

                results.append({
                    "universitet": universitet,
                    "ixtisas": ixtisas,
                    "eyani_qiyabi": eyani_qiyabi,
                    "odenissiz": odenissiz,
                    "odenisli": odenisli,
                })

    # Filter parametrləri
    universitet_filter = request.GET.get("universitet", "").lower()
    ixtisas_filter = request.GET.get("ixtisas", "").lower()
    eyani_qiyabi_filter = request.GET.get("eyani_qiyabi", "")

    if universitet_filter or ixtisas_filter or eyani_qiyabi_filter:
        results = [
            r for r in results
            if universitet_filter in r["universitet"].lower()
            and ixtisas_filter in r["ixtisas"].lower()
            and (eyani_qiyabi_filter == "" or r["eyani_qiyabi"] == eyani_qiyabi_filter)
        ]

    filtered_sorted_list = sorted(
        results,
        key=lambda x: (
            x["odenissiz"] is None,
            x["odenissiz"] if x["odenissiz"] is not None else float("inf"),
        ),
    )

    context = {
        "total": total_score,
        "result": filtered_sorted_list[::-1],
        "universities": sorted(universities_set),
        "ixtisaslar": sorted(ixtisaslar_set),
        "group": group
    }
    return render(request, "ballar.html", context)


def show_scores_5th_group(request):
    import json
    import os
    from django.conf import settings
    from django.shortcuts import render

    results = []
    group_num = 5

    if request.method == "POST":
        burax = request.POST.get("burax")

        if not burax:
            return render(
                request, "ballar.html", {"error": "Buraxılış balı daxil edilməyib."}
            )

        try:
            total_score = float(burax)
        except ValueError:
            return render(
                request,
                "ballar.html",
                {"error": "Buraxılış balı düzgün formatda deyil."},
            )

        file_path = os.path.join(
            settings.BASE_DIR, "unichat/datas", f"universitetler_{group_num}qrup.json"
        )

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for uni_name, majors in data.items():
            for major in majors:
                odenissiz = major.get("odenissiz_bali")
                odenisli = major.get("odenisli_bali")

                # None olsa da göstərmək üçün "match" şərtini dəyişirik:
                if odenissiz is None and odenisli is None:
                    match = True  # Heç bir bal yoxdursa, göstər
                elif (odenissiz is not None and total_score >= odenissiz) or (
                    odenisli is not None and total_score >= odenisli
                ):
                    match = True
                else:
                    match = False

                if match:
                    results.append(
                        {
                            "universitet": uni_name,
                            "ixtisas": major["ixtisas"],
                            "eyani_qiyabi": (
                                "Əyani" if major["eyani_qiyabi"] == "Ə" else "Qiyabi"
                            ),
                            "odenissiz": odenissiz,
                            "odenisli": odenisli,
                        }
                    )

        # Odenisli sahəsi olanları sortlayırıq
        filtered_sorted_list = sorted(
            results,
            key=lambda x: (
                x["odenissiz"] is None,
                x["odenissiz"] if x["odenissiz"] is not None else float("inf"),
            ),
        )

        context = {
            "total": total_score,
            "result": filtered_sorted_list[
                ::-1
            ],  # Ən yuxarıya böyük bal olanlar gəlsin
        }

        return render(request, "ballar.html", context=context)

    return render(request, "ballar.html")
