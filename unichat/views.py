from django.shortcuts import render
import os
from django.conf import settings

qrup_3_altqrup = ["Beynəlxalq münasibətlər", "Regionşünaslıq"]


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
        total_score = int(burax) + int(blok)
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
            total_score = int(burax)
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
