function enableSound() {
      const audio = document.getElementById('music');
      audio.muted = false;     // Səsi aç
      audio.play();            // Yenidən səsləndir
    }
        function showComingSoonAnimation() {
    // Animasiya divini yaradaq
    const animationDiv = document.createElement('div');
    animationDiv.style.position = 'fixed';
    animationDiv.style.top = '50%';
    animationDiv.style.left = '50%';
    animationDiv.style.transform = 'translate(-50%, -50%)';
    animationDiv.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
    animationDiv.style.padding = '30px 50px';
    animationDiv.style.borderRadius = '20px';
    animationDiv.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)';
    animationDiv.style.zIndex = '10000';
    animationDiv.style.textAlign = 'center';
    animationDiv.style.fontSize = '1.2rem';
    animationDiv.style.color = '#333';
    animationDiv.style.fontWeight = '600';
    animationDiv.style.display = 'flex';
    animationDiv.style.flexDirection = 'column';
    animationDiv.style.alignItems = 'center';
    animationDiv.style.justifyContent = 'center';
    animationDiv.style.gap = '20px';
    animationDiv.style.width = '300px';
    animationDiv.style.height = '200px';
    animationDiv.style.animation = 'fadeInUp 0.5s ease-out';
    
    // İkon və mesaj əlavə edək
    animationDiv.innerHTML = `
        <div style="font-size: 3rem;">🚧</div>
        <div>Bu səhifə hazırlıq mərhələsindədir</div>
        <div style="font-size: 0.9rem; color: #666;">Tezliklə xidmətinizdə olacaq</div>
    `;
    
    // Əsas səhifəyə əlavə edək
    document.body.appendChild(animationDiv);
    
    // 3 saniyədən sonra animasiya ilə silək
    setTimeout(() => {
        animationDiv.style.animation = 'fadeOut 0.5s ease-out';
        setTimeout(() => {
            document.body.removeChild(animationDiv);
        }, 500);
    }, 3000);
}
        // Limitsiz API konfiqurasiyası
        const OPEN_AI_API_KEY = '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';
        const API_ENDPOINT = 'https://openrouter.ai/api/v1/chat/completions';
        
        // Sistem promptu - AI-nın davranışını təyin edir
        const SYSTEM_PROMPT = `
        Siz UniChat, Azərbaycanda təhsil platforması üçün AI köməkçisisiniz. İstifadəçilərə universitet qəbulu, imtahan balı, akademik qruplar və karyera seçimləri ilə bağlı suallara cavab verin. 
        Azərbaycan dilində qısa, dəqiq və faydalı cavablar verin. Əsas diqqəti universitet seçimi, imtahan balı (buraxılış və blok balı), akademik qruplar (1-5) və ümumi təhsil məsələlərinə yönəldin. 
        Sual təhsil mövzusundan kənardırsa, istifadəçini təhsil mövzularına yönləndirin. Uzun cavablardan çəkinin.
        `;

        // Naviqasiya funksiyaları
        function showHomePage() {
            // Bütün qrup səhifələrini gizlə
            for (let i = 1; i <= 5; i++) {
                document.getElementById(`group-${i}`).classList.remove('active');
            }
            // Ana səhifəni göstər
            document.getElementById('home-page').style.display = 'block';
        }

        function selectGroup(groupNumber) {
            // Ana səhifəni gizlə
            document.getElementById('home-page').style.display = 'none';
            
            // Bütün qrup səhifələrini gizlə
            for (let i = 1; i <= 5; i++) {
                document.getElementById(`group-${i}`).classList.remove('active');
            }
            
            // Seçilmiş qrup səhifəsini göstər
            document.getElementById(`group-${groupNumber}`).classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Bal hesablama funksiyası
        function calculateScore(event, groupNumber) {
            event.preventDefault();
            
            const graduationInput = document.getElementById(`graduation-${groupNumber}`);
            const blockInput = document.getElementById(`block-${groupNumber}`);
            const graduationError = document.getElementById(`graduation-error-${groupNumber}`);
            const blockError = document.getElementById(`block-error-${groupNumber}`);
            const totalDiv = document.getElementById(`total-${groupNumber}`);
            const totalValue = document.getElementById(`total-value-${groupNumber}`);
            
            let isValid = true;
            
            // Xəta mesajlarını sıfırla
            graduationError.style.display = 'none';
            blockError.style.display = 'none';
            graduationInput.classList.remove('error');
            blockInput.classList.remove('error');
            
            // Buraxılış balını yoxla
            const graduationScore = parseInt(graduationInput.value);
            if (!graduationScore && graduationScore !== 0) {
                graduationError.textContent = 'Buraxılış balını daxil edin';
                graduationError.style.display = 'block';
                graduationInput.classList.add('error');
                isValid = false;
            } else if (graduationScore < 0 || graduationScore > 300) {
                graduationError.textContent = 'Buraxılış balı 0-300 arasında olmalıdır';
                graduationError.style.display = 'block';
                graduationInput.classList.add('error');
                isValid = false;
            }
            
            // Blok balını yoxla
            const blockScore = parseInt(blockInput.value);
            if (!blockScore && blockScore !== 0) {
                blockError.textContent = 'Blok balını daxil edin';
                blockError.style.display = 'block';
                blockInput.classList.add('error');
                isValid = false;
            } else if (blockScore < 0 || blockScore > 400) {
                blockError.textContent = 'Blok balı 0-400 arasında olmalıdır';
                blockError.style.display = 'block';
                blockInput.classList.add('error');
                isValid = false;
            }
            
            // Əgər düzgündürsə, hesabla və göstər
            if (isValid) {
                const total = graduationScore + blockScore;
                totalValue.textContent = total;
                totalDiv.style.display = 'block';
                
                // Uğur animasiyası əlavə et
                totalDiv.style.animation = 'none';
                setTimeout(() => {
                    totalDiv.style.animation = 'fadeInUp 0.5s ease-out';
                }, 10);
                
                // Əgər AI chat aktivdirsə, mesaj göndər
                if (document.getElementById('supportChat').classList.contains('active')) {
                    addMessage(`${groupNumber}-ci qrup üçün ümumi balım ${total} oldu.`, 'user');
                    setTimeout(() => {
                        showTyping();
                        getAIResponse(`${groupNumber}-ci qrup üçün ümumi balım ${total} oldu.`)
                            .then(response => {
                                hideTyping();
                                addMessage(response, 'bot');
                            })
                            .catch(error => {
                                hideTyping();
                                addMessage('Bağışlayın, bir xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.', 'bot');
                            });
                    }, 500);
                }
            }
        }

        // Chat funksiyaları
        function toggleChat() {
            document.getElementById('supportChat').classList.toggle('active');
        }

        
        function showAnswer(id) {
            const chatBody = document.getElementById("supportChat");
            const answers = {
                1: "Bu sistemin mahiyyəti ondan ibarətdir ki, abituriyentin cari ildə topladığı bala əsaslanaraq, əvvəlki ilin qəbul statistikası ilə müqayisəli təhlil aparılır və nəticədə potensial qəbul oluna biləcək ali təhsil müəssisələri avtomatlaşdırılmış şəkildə təqdim edilir. Qeyd etmək lazımdır ki, universitetlərə qəbul prosesi Dövlət İmtahan Mərkəzi (DİM) tərəfindən, yalnız cari ildə abituriyentin topladığı bala əsasən həyata keçirilir. Bu səbəbdən sistemin verdiyi nəticələrdə müəyyən uyğunsuzluq və ya yanlışlıq ehtimalı mövcuddur.",
                2: "İlk öncə qrup seçilir, bundan sonra altqrupunuzu seçərək balınızı daxil edirsiniz.",
                3: "Reklam üçün əlaqə: uniazedu@gmail.com"
            };

            const messageDiv = document.createElement("div");
            messageDiv.classList.add("chat-message");
            messageDiv.innerHTML = `<div class="message-bot">${answers[id]}</div>`;
            chatBody.appendChild(messageDiv);
            chatBody.scrollTop = chatBody.scrollHeight;
        }

        // Xoş gəldin ekranını başlat
        setTimeout(() => {
            document.getElementById('welcome-screen').style.opacity = '0';
            setTimeout(() => {
                document.getElementById('welcome-screen').style.display = 'none';
            }, 800);
        }, 100);

        // Real-time validasiya üçün input event listener-ları əlavə et
        document.addEventListener('DOMContentLoaded', function() {
            for (let i = 1; i <= 5; i++) {
                const graduationInput = document.getElementById(`graduation-${i}`);
                const blockInput = document.getElementById(`block-${i}`);
                
                if (graduationInput) {
                    graduationInput.addEventListener('input', function() {
                        const value = parseInt(this.value);
                        if (value > 300) {
                            this.value = 300;
                        } else if (value < 0) {
                            this.value = 0;
                        }
                    });
                }
                
                if (blockInput) {
                    blockInput.addEventListener('input', function() {
                        const value = parseInt(this.value);
                        if (value > 400) {
                            this.value = 400;
                        } else if (value < 0) {
                            this.value = 0;
                        }
                    });
                }
            }
            
            // Xəbər bülleteni üçün
            document.querySelector('.newsletter-btn').addEventListener('click', function() {
                const email = document.querySelector('.newsletter-input').value;
                if (email) {
                    alert('Təşəkkürlər! Uğurla abunə oldunuz: ' + email);
                    document.querySelector('.newsletter-input').value = '';
                } else {
                    alert('Zəhmət olmasa e-mail ünvanınızı daxil edin.');
                }
            });

            // Xəbər bülleteni üçün Enter dəstəyi
            document.querySelector('.newsletter-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    document.querySelector('.newsletter-btn').click();
                }
            });
        });
function balYoxla(input) {
    const bal = parseInt(input.value);
    const blockId = input.id.split('-')[1]; // gets the block number (1, 2, 3, or 4)
    const mesaj = document.getElementById(`mesaj-${blockId}`);

    if (bal >= 1 && bal <= 49) {
        mesaj.innerHTML = "⚠ Siz ixtisaslaşmaya girə bilməzsiniz!";
        mesaj.className = "xeberdarliq qirmizi";
    } else if (bal >= 50 && bal <= 99) {
        mesaj.innerHTML = "ℹ Siz yalnız 150 ballıq ixtisaslar yazə bilərsiniz!";
        mesaj.className = "xeberdarliq sari";
    } else if (bal >= 100) {
        mesaj.innerHTML = "";
        mesaj.className = "xeberdarliq yasil";
    } else {
        mesaj.innerHTML = "";
        mesaj.className = "";
    }
}
