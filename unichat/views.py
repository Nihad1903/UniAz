from django.shortcuts import render
import os
from django.conf import settings

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


def uniler(request):
    return render(request, "uniler.html")

def show_scores(request, group):
    results = []
    group_num = group
    altqrup = request.POST.get("altqrup")

    if request.method == "POST":
        burax = request.POST.get("burax")
        blok = request.POST.get("blok")
        
        if 49 < float(blok) < 100:
            import json
            with open("unichat/datas/ballar_150.json", "r", encoding="utf-8") as data:
                ballar_150 = json.load(data)
                for qrup in ballar_150:
                    if qrup == f"group{group}":
                        data = qrup
                        
                data = ballar_150[f"qrup{group}"]
                context = {
                    "ixtisaslar": data
                }
            return render(request, "ballar_150.html", context=context)
        
        total_score = float(burax) + float(blok)
        total_score = round(total_score, 2)
        import json

        with open("unichat/datas/altqrup_1.json", "r", encoding="utf-8") as data:
            altqrup_data = json.load(data)

        file_path = os.path.join(
            settings.BASE_DIR, "unichat/datas", f"universitetler_{group_num}qrup.json"
        )
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for uni_name, majors in data.items():
            for major in majors:
                if altqrup == "TC" and (
                    "Beynəlxalq münasibətlər" not in major["ixtisas"]
                    and "Regionşünaslıq" not in major["ixtisas"]
                ):
                    continue
                elif altqrup == "DT" and major["ixtisas"] in qrup_3_altqrup:
                    continue
                if altqrup == "RI" and major["ixtisas"] not in altqrup_data:
                    continue
                elif altqrup == "RK" and major["ixtisas"] in altqrup_data:
                    continue
                match = False

                odenissiz = major.get("odenissiz_bali")
                odenisli = major.get("odenisli_bali")

                if odenissiz is None and odenisli is None:
                    match = True  
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
        filtered_sorted_list = sorted(
            results,
            key=lambda x: (
                x["odenissiz"] is None,
                x["odenissiz"] if x["odenissiz"] is not None else float("inf"),
            ),
        )
        context = {
            "total": total_score,
            "result": filtered_sorted_list[::-1],  # azalan sıra
        }
        return render(request, "ballar.html", context=context)


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
