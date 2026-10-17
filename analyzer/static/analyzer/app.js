/* ==========================================================================
   EIGENLAB — INTERACTION, STAGED LOADING & SPECTRAL VISUALIZATION
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    /* ── 1. K-Slider & Quick Presets ── */
    const kRange = document.getElementById("kRange");
    const kValue = document.getElementById("kValue");
    const kEchoList = document.querySelectorAll(".run-k-echo");
    const presetButtons = document.querySelectorAll(".preset-btn");

    function updateKValue(val) {
        if (!kRange) return;
        const currentVal = val !== undefined ? Number(val) : Number(kRange.value);
        kRange.value = currentVal;

        if (kValue) kValue.textContent = currentVal;
        kEchoList.forEach(echo => { echo.textContent = currentVal; });

        const min = Number(kRange.min || 1);
        const max = Number(kRange.max || 64);
        const percentage = max > min ? ((currentVal - min) / (max - min)) * 100 : 0;
        kRange.style.backgroundSize = `${percentage}% 100%`;

        // Update active state on preset buttons
        presetButtons.forEach(btn => {
            const btnK = Number(btn.dataset.k);
            btn.classList.toggle("active", btnK === currentVal);
        });
    }

    if (kRange) {
        kRange.addEventListener("input", () => updateKValue());
        updateKValue();
    }

    presetButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const presetVal = Number(btn.dataset.k);
            if (presetVal) updateKValue(presetVal);
        });
    });

    /* ── 2. Image Selection & Drag-and-Drop ── */
    const dropZone = document.getElementById("dropZone");
    const imageInput = document.getElementById("imageInput");
    const fileName = document.getElementById("fileName");
    const fileSubtext = document.getElementById("fileSubtext");
    const previewStrip = document.getElementById("previewStrip");
    const previewThumb = document.getElementById("previewThumb");

    function handleFile(file) {
        if (!file || !file.type.startsWith("image/")) return;

        if (fileName) fileName.textContent = file.name;
        if (fileSubtext) {
            const sizeKb = (file.size / 1024).toFixed(1);
            fileSubtext.textContent = `Selected: ${file.name} (${sizeKb} KB) · Ready for decomposition`;
        }

        if (dropZone) dropZone.classList.add("has-file");

        // Read thumbnail for immediate feedback
        const reader = new FileReader();
        reader.onload = e => {
            if (previewThumb && previewStrip) {
                previewThumb.src = e.target.result;
                previewStrip.style.display = "flex";
            }
        };
        reader.readAsDataURL(file);
    }

    if (dropZone && imageInput) {
        dropZone.addEventListener("click", e => {
            // Prevent recursive click if clicking input directly
            if (e.target !== imageInput) {
                imageInput.click();
            }
        });

        imageInput.addEventListener("change", () => {
            if (imageInput.files && imageInput.files[0]) {
                handleFile(imageInput.files[0]);
            }
        });

        ["dragenter", "dragover"].forEach(eventName => {
            dropZone.addEventListener(eventName, e => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.add("drag-over");
            });
        });

        ["dragleave", "drop"].forEach(eventName => {
            dropZone.addEventListener(eventName, e => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.remove("drag-over");
            });
        });

        dropZone.addEventListener("drop", e => {
            const files = e.dataTransfer?.files;
            if (files && files.length > 0 && files[0].type.startsWith("image/")) {
                imageInput.files = files;
                handleFile(files[0]);
            }
        });
    }

    /* ── 3. Staged Loading Overlay & Form Submission ── */
    const analysisForm = document.getElementById("analysisForm");
    const runBtn = document.getElementById("runBtn");
    const loadingOverlay = document.getElementById("eigenLoadingOverlay");
    const loaderStatusText = document.getElementById("loaderStatusText");
    const loaderStagesList = document.getElementById("loaderStagesList");

    if (analysisForm && runBtn) {
        let isSubmitting = false;

        const stagesSequence = [
            "Reading uploaded image data...",
            "Converting pixels to normalized grayscale matrix A ∈ [0, 1]...",
            "Constructing symmetric covariance matrix AᵀA...",
            "Computing eigenvalues and orthonormal eigenvectors...",
            "Extracting top-k principal subspace V_k...",
            "Projecting matrix onto eigenspace: P = A · V_k...",
            "Reconstructing approximation: A_k = P · V_kᵀ...",
            "Evaluating Frobenius norm and relative reconstruction error..."
        ];

        analysisForm.addEventListener("submit", e => {
            if (isSubmitting) {
                e.preventDefault();
                return;
            }

            if (!analysisForm.checkValidity()) return;

            // Check if either a file is selected or an existing image_name is present
            const hasNewFile = imageInput && imageInput.files && imageInput.files.length > 0;
            const existingImage = document.getElementById("imageNameInput")?.value;

            if (!hasNewFile && !existingImage) {
                alert("Please select or drop an image file to analyze.");
                e.preventDefault();
                return;
            }

            isSubmitting = true;
            runBtn.classList.add("loading");
            runBtn.disabled = true;

            if (loadingOverlay) {
                loadingOverlay.classList.add("active");
            }

            // Animate status stages illustrative progress
            let currentStage = 0;
            const stageItems = loaderStagesList ? loaderStagesList.querySelectorAll(".stage-item") : [];

            const stageTimer = setInterval(() => {
                currentStage++;
                if (currentStage < stagesSequence.length) {
                    if (loaderStatusText) {
                        loaderStatusText.textContent = stagesSequence[currentStage];
                    }
                    if (stageItems.length > 0) {
                        const stepIndex = Math.min(Math.floor(currentStage * (stageItems.length / stagesSequence.length)), stageItems.length - 1);
                        stageItems.forEach((item, idx) => {
                            item.classList.toggle("active", idx === stepIndex);
                            item.classList.toggle("complete", idx < stepIndex);
                        });
                    }
                } else {
                    clearInterval(stageTimer);
                }
            }, 420);
        });

        // Trigger loading screen on demo sample clicks as well
        document.querySelectorAll(".demo-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                if (loadingOverlay) {
                    loadingOverlay.classList.add("active");
                    if (loaderStatusText) {
                        loaderStatusText.textContent = "Loading demo sample & computing covariance eigen-decomposition...";
                    }
                }
            });
        });

        // Restore controls on back/forward cache navigation
        window.addEventListener("pageshow", () => {
            isSubmitting = false;
            if (runBtn) {
                runBtn.classList.remove("loading");
                runBtn.disabled = false;
            }
            if (loadingOverlay) {
                loadingOverlay.classList.remove("active");
            }
        });
    }

    /* ── 3B. Sarvam AI — Complete Conversational Chatbot & Translation Manager ── */
    (function initSarvamChatSystem() {
        // Global Chat State
        let currentLang = 'English';
        let conversationHistory = [];
        let isWaiting = false;

        // Context Extractor from Matrix Data
        function getAnalysisContext() {
            const sc = document.getElementById('sarvamAiContainer');
            return sc ? {
                matrix_rows: Number(sc.dataset.rows || 64),
                matrix_cols: Number(sc.dataset.cols || 64),
                rank: Number(sc.dataset.rank || 0),
                selected_k: Number(sc.dataset.k || 16),
                frobenius_error: Number(sc.dataset.frob || 0),
                relative_error_percent: Number(sc.dataset.rel || 0)
            } : {};
        }

        function getTimeStr() {
            const now = new Date();
            return now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
        }

        function escHtml(str) {
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        }

        function formatBotContent(raw) {
            let escaped = escHtml(raw);
            // Replace markdown code backticks `code`
            escaped = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');
            // Replace bold **text**
            escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
            // Replace newlines
            return escaped.replace(/\n/g, '<br>');
        }

        /* ── A. Language Switching & Toolbar ── */
        const langPills = document.querySelectorAll('.lang-pill');
        const activeLangDisplay = document.getElementById('activeLangName');
        const chatActiveLangLabel = document.getElementById('chatActiveLangLabel');
        const drawerActiveLang = document.getElementById('chatActiveLang');

        function setLanguage(lang) {
            currentLang = lang || 'English';

            // Update pills in main card
            langPills.forEach(pill => {
                pill.classList.toggle('active', pill.dataset.lang === currentLang);
            });

            // Update in-page button & badge
            if (activeLangDisplay) activeLangDisplay.textContent = currentLang;
            if (chatActiveLangLabel) chatActiveLangLabel.textContent = currentLang;
            if (drawerActiveLang) drawerActiveLang.textContent = currentLang;

            // Update drawer dropdown active option
            document.querySelectorAll('.chat-lang-option').forEach(opt => {
                opt.classList.toggle('active', opt.dataset.lang === currentLang);
            });

            // Append system notification in stream
            appendSystemNotice('Language switched to ' + currentLang);
        }

        langPills.forEach(pill => {
            pill.addEventListener('click', () => {
                const lang = pill.dataset.lang;
                if (lang) setLanguage(lang);
            });
        });

        /* ── B. Translation Action ── */
        const translateBtn = document.getElementById('sarvamTranslateBtn');
        const interpretationTextEl = document.getElementById('sarvamInterpretationText');
        const synthesisBadge = document.getElementById('synthesisLangBadge');
        const energyTextEl = document.getElementById('sarvamEnergyText');

        if (translateBtn && interpretationTextEl) {
            translateBtn.addEventListener('click', () => {
                const text = interpretationTextEl.textContent.trim();
                if (!text || translateBtn.classList.contains('loading')) return;

                translateBtn.classList.add('loading');
                translateBtn.disabled = true;

                fetch('/api/sarvam/translate/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        text: text,
                        language: currentLang
                    })
                })
                .then(r => r.json())
                .then(data => {
                    translateBtn.classList.remove('loading');
                    translateBtn.disabled = false;
                    if (data.success && data.translated_text) {
                        interpretationTextEl.textContent = data.translated_text;
                        if (synthesisBadge) {
                            synthesisBadge.textContent = currentLang.substring(0, 3).toUpperCase();
                        }
                    } else {
                        alert('Translation notice: ' + (data.error || 'Translation failed'));
                    }
                })
                .catch(err => {
                    translateBtn.classList.remove('loading');
                    translateBtn.disabled = false;
                    alert('Translation request error: ' + err.message);
                });
            });
        }

        /* ── C. In-Page Embedded Chatbot Console ── */
        const embeddedConsole  = document.getElementById('sarvamChatConsole');
        const embeddedStream   = document.getElementById('sarvamChatStream');
        const embeddedForm     = document.getElementById('sarvamChatForm');
        const embeddedInput    = document.getElementById('sarvamChatInput');
        const embeddedSubmit   = document.getElementById('sarvamChatSubmit');
        const embeddedClearBtn = document.getElementById('sarvamClearChatBtn');
        const embeddedChips    = document.querySelectorAll('#sarvamQuickChips .chat-quick-chip');

        /* ── D. Floating Drawer Chatbot ── */
        const bubbleBtn      = document.getElementById('chatBubbleBtn');
        const drawer         = document.getElementById('chatDrawer');
        const drawerMessages = document.getElementById('chatMessages');
        const drawerInput    = document.getElementById('chatInput');
        const drawerSendBtn  = document.getElementById('chatSendBtn');
        const drawerClearBtn = document.getElementById('chatClearBtn');
        const drawerUnread   = document.getElementById('chatUnreadBadge');
        const drawerLangSel  = document.getElementById('chatLangSelector');
        const drawerLangDrop = document.getElementById('chatLangDropdown');
        const drawerChips    = document.querySelectorAll('#chatQuickPrompts .quick-chip');

        let isDrawerOpen = false;

        function openDrawer() {
            if (!drawer || !bubbleBtn) return;
            isDrawerOpen = true;
            drawer.classList.add('open');
            bubbleBtn.classList.add('open');
            bubbleBtn.setAttribute('aria-expanded', 'true');
            if (drawerUnread) drawerUnread.style.display = 'none';
            if (drawerMessages) drawerMessages.scrollTop = drawerMessages.scrollHeight;
            setTimeout(() => drawerInput && drawerInput.focus(), 250);
        }

        function closeDrawer() {
            if (!drawer || !bubbleBtn) return;
            isDrawerOpen = false;
            drawer.classList.remove('open');
            bubbleBtn.classList.remove('open');
            bubbleBtn.setAttribute('aria-expanded', 'false');
            if (drawerLangDrop) drawerLangDrop.classList.remove('show');
        }

        if (bubbleBtn) {
            bubbleBtn.addEventListener('click', () => isDrawerOpen ? closeDrawer() : openDrawer());
        }

        document.addEventListener('click', e => {
            if (isDrawerOpen && drawer && bubbleBtn && !drawer.contains(e.target) && !bubbleBtn.contains(e.target)) {
                closeDrawer();
            }
        });

        document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && isDrawerOpen) closeDrawer();
        });

        if (drawerLangSel && drawerLangDrop) {
            drawerLangSel.addEventListener('click', e => {
                e.stopPropagation();
                const open = drawerLangDrop.classList.toggle('show');
                drawerLangSel.setAttribute('aria-expanded', String(open));
            });

            drawerLangDrop.querySelectorAll('.chat-lang-option').forEach(opt => {
                opt.addEventListener('click', e => {
                    e.stopPropagation();
                    setLanguage(opt.dataset.lang || 'English');
                    drawerLangDrop.classList.remove('show');
                    drawerLangSel.setAttribute('aria-expanded', 'false');
                });
            });

            document.addEventListener('click', e => {
                if (!drawerLangSel.contains(e.target)) {
                    drawerLangDrop.classList.remove('show');
                    drawerLangSel.setAttribute('aria-expanded', 'false');
                }
            });
        }

        /* ── Unified Message Append & UI Synchronizers ── */
        function appendSystemNotice(text) {
            // Embedded stream
            if (embeddedStream) {
                const sysEl = document.createElement('div');
                sysEl.className = 'chat-system-entry';
                sysEl.textContent = text;
                embeddedStream.appendChild(sysEl);
                embeddedStream.scrollTop = embeddedStream.scrollHeight;
            }
            // Drawer stream
            if (drawerMessages) {
                const sysEl = document.createElement('div');
                sysEl.className = 'chat-system-msg';
                sysEl.textContent = text;
                drawerMessages.appendChild(sysEl);
                drawerMessages.scrollTop = drawerMessages.scrollHeight;
            }
        }

        function appendUserMessage(text) {
            const time = getTimeStr();

            // Embedded stream
            if (embeddedStream) {
                const el = document.createElement('div');
                el.className = 'chat-bubble-entry user-entry';
                el.innerHTML = `
                    <div class="chat-entry-avatar">U</div>
                    <div class="chat-entry-content">
                        <div class="chat-bubble-card user-bubble">${escHtml(text)}</div>
                        <div class="chat-entry-meta">${time}</div>
                    </div>
                `;
                embeddedStream.appendChild(el);
                embeddedStream.scrollTop = embeddedStream.scrollHeight;
            }

            // Drawer stream
            if (drawerMessages) {
                const el = document.createElement('div');
                el.className = 'chat-msg user-msg';
                el.innerHTML = `
                    <div class="chat-msg-avatar user-avatar-icon" aria-hidden="true">U</div>
                    <div>
                        <div class="chat-msg-bubble">${escHtml(text)}</div>
                        <div class="chat-msg-time">${time}</div>
                    </div>
                `;
                drawerMessages.appendChild(el);
                drawerMessages.scrollTop = drawerMessages.scrollHeight;
            }
        }

        function appendBotMessage(formattedHtml) {
            const time = getTimeStr();

            // Embedded stream
            if (embeddedStream) {
                const el = document.createElement('div');
                el.className = 'chat-bubble-entry bot-entry';
                el.innerHTML = `
                    <div class="chat-entry-avatar">λ</div>
                    <div class="chat-entry-content">
                        <div class="chat-bubble-card bot-bubble">${formattedHtml}</div>
                        <div class="chat-entry-meta">Sarvam AI (${currentLang}) · ${time}</div>
                    </div>
                `;
                embeddedStream.appendChild(el);
                embeddedStream.scrollTop = embeddedStream.scrollHeight;
            }

            // Drawer stream
            if (drawerMessages) {
                const el = document.createElement('div');
                el.className = 'chat-msg bot-msg';
                el.innerHTML = `
                    <div class="chat-msg-avatar bot-avatar" aria-hidden="true">λ</div>
                    <div>
                        <div class="chat-msg-bubble">${formattedHtml}</div>
                        <div class="chat-msg-time">Sarvam AI · ${time}</div>
                    </div>
                `;
                drawerMessages.appendChild(el);
                drawerMessages.scrollTop = drawerMessages.scrollHeight;
            }
        }

        function showTypingIndicators() {
            const indicators = [];

            if (embeddedStream) {
                const el = document.createElement('div');
                el.className = 'chat-typing-entry';
                el.innerHTML = `
                    <div class="chat-entry-avatar" style="background:linear-gradient(135deg,#c9a96e,#a8854a);color:#07090c;font-weight:700;font-size:12px;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;">λ</div>
                    <div class="typing-bubble">
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                    </div>
                `;
                embeddedStream.appendChild(el);
                embeddedStream.scrollTop = embeddedStream.scrollHeight;
                indicators.push(el);
            }

            if (drawerMessages) {
                const el = document.createElement('div');
                el.className = 'chat-typing-indicator';
                el.innerHTML = `
                    <div class="chat-msg-avatar bot-avatar" aria-hidden="true">λ</div>
                    <div class="typing-dots" aria-label="Sarvam AI is typing">
                        <span></span><span></span><span></span>
                    </div>
                `;
                drawerMessages.appendChild(el);
                drawerMessages.scrollTop = drawerMessages.scrollHeight;
                indicators.push(el);
            }

            return indicators;
        }

        function removeTypingIndicators(indicators) {
            indicators.forEach(el => {
                if (el && el.parentNode) el.parentNode.removeChild(el);
            });
        }

        function setChatWaiting(val) {
            isWaiting = val;

            if (embeddedSubmit) {
                embeddedSubmit.disabled = val;
                embeddedSubmit.classList.toggle('loading', val);
            }
            if (embeddedInput) embeddedInput.disabled = val;

            if (drawerSendBtn) {
                drawerSendBtn.disabled = val;
                const si = drawerSendBtn.querySelector('.send-icon');
                const sp = drawerSendBtn.querySelector('.spin-icon');
                if (si) si.style.display = val ? 'none' : '';
                if (sp) sp.style.display = val ? '' : 'none';
            }
            if (drawerInput) drawerInput.disabled = val;
        }

        /* ── Unified Send Function ── */
        function sendQuestion(text) {
            const query = (text || '').trim();
            if (!query || isWaiting) return;

            appendUserMessage(query);
            conversationHistory.push({ role: 'user', content: query });

            // Clear inputs
            if (embeddedInput) embeddedInput.value = '';
            if (drawerInput) {
                drawerInput.value = '';
                drawerInput.style.height = 'auto';
            }

            const typingEls = showTypingIndicators();
            setChatWaiting(true);

            fetch('/api/sarvam/chat/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: query,
                    language: currentLang,
                    history: conversationHistory.slice(-8),
                    context: getAnalysisContext()
                })
            })
            .then(r => r.json())
            .then(data => {
                removeTypingIndicators(typingEls);
                setChatWaiting(false);

                if (data.success && data.answer) {
                    const formatted = formatBotContent(data.answer);
                    appendBotMessage(formatted);
                    conversationHistory.push({ role: 'assistant', content: data.answer });
                } else {
                    const errText = data.error || 'Sarvam AI could not generate a response. Please try again.';
                    appendBotMessage('⚠️ <em>' + escHtml(errText) + '</em>');
                }
            })
            .catch(err => {
                removeTypingIndicators(typingEls);
                setChatWaiting(false);
                appendBotMessage('⚠️ <em>Connection notice: ' + escHtml(err.message) + '</em>');
            });
        }

        /* ── Event Bindings: Embedded Console ── */
        if (embeddedForm) {
            embeddedForm.addEventListener('submit', e => {
                e.preventDefault();
                if (embeddedInput) sendQuestion(embeddedInput.value);
            });
        }

        embeddedChips.forEach(chip => {
            chip.addEventListener('click', () => {
                const q = chip.dataset.q;
                if (q) sendQuestion(q);
            });
        });

        if (embeddedClearBtn) {
            embeddedClearBtn.addEventListener('click', () => {
                conversationHistory = [];
                if (embeddedStream) {
                    embeddedStream.innerHTML = `
                        <div class="chat-bubble-entry bot-entry">
                            <div class="chat-entry-avatar">λ</div>
                            <div class="chat-entry-content">
                                <div class="chat-bubble-card bot-bubble">
                                    <p style="margin:0;">Conversation refreshed. Ask me any question regarding your decomposed matrix, eigenvalues, SVD, or viva examination in <strong>${currentLang}</strong>!</p>
                                </div>
                                <div class="chat-entry-meta">Sarvam AI · Reset</div>
                            </div>
                        </div>
                    `;
                }
            });
        }

        /* ── Event Bindings: Drawer Chatbot ── */
        if (drawerSendBtn && drawerInput) {
            drawerSendBtn.addEventListener('click', () => sendQuestion(drawerInput.value));
            drawerInput.addEventListener('keydown', e => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendQuestion(drawerInput.value);
                }
            });
            drawerInput.addEventListener('input', () => {
                drawerInput.style.height = 'auto';
                const nextH = Math.min(drawerInput.scrollHeight, 96);
                drawerInput.style.height = nextH + 'px';
                drawerInput.style.overflowY = drawerInput.scrollHeight > 96 ? 'auto' : 'hidden';
            });
        }

        drawerChips.forEach(chip => {
            chip.addEventListener('click', () => {
                const q = chip.dataset.q;
                if (q) sendQuestion(q);
            });
        });

        if (drawerClearBtn) {
            drawerClearBtn.addEventListener('click', () => {
                conversationHistory = [];
                if (drawerMessages) {
                    drawerMessages.innerHTML = `
                        <div class="chat-system-msg">Conversation cleared</div>
                        <div class="chat-msg bot-msg">
                            <div class="chat-msg-avatar bot-avatar" aria-hidden="true">λ</div>
                            <div>
                                <div class="chat-msg-bubble">
                                    Namaste! 🙏 I'm <strong>Sarvam AI</strong>. Ask me anything about eigenvalues, SVD, PCA, or select a regional language using the 🌐 button!
                                </div>
                                <div class="chat-msg-time">Sarvam AI · Reset</div>
                            </div>
                        </div>
                    `;
                }
            });
        }
    })();


    /* ── 4. High-DPI Eigenvalue Spectrum & Scree Plot Chart ── */
    const canvas = document.getElementById("eigenChart");
    if (!canvas) return;

    const rawValues = canvas.dataset.values || "";
    const eigenvalues = rawValues
        .split(",")
        .map(v => Number(v.trim()))
        .filter(Number.isFinite);

    if (eigenvalues.length === 0) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Get selected k
    const selectedK = Number(document.getElementById("kValue")?.textContent) || 8;

    function renderEigenSpectrumChart() {
        const rect = canvas.getBoundingClientRect();
        const parentW = canvas.parentElement ? canvas.parentElement.clientWidth - 40 : 0;
        const width = Math.max(300, Math.floor(rect.width || parentW || 640));
        const height = 240;

        const dpr = window.devicePixelRatio || 1;
        canvas.width = Math.floor(width * dpr);
        canvas.height = Math.floor(height * dpr);

        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.clearRect(0, 0, width, height);

        // Fill background
        ctx.fillStyle = "#111520";
        ctx.fillRect(0, 0, width, height);

        const padding = { top: 24, right: 28, bottom: 38, left: 54 };
        const chartW = width - padding.left - padding.right;
        const chartH = height - padding.top - padding.bottom;

        const maxVal = Math.max(...eigenvalues, 1);
        const count = eigenvalues.length;

        // Grid lines (4 horizontal steps)
        ctx.strokeStyle = "rgba(255, 255, 255, 0.07)";
        ctx.lineWidth = 1;
        ctx.fillStyle = "#6b6258";
        ctx.font = '10px "JetBrains Mono", monospace';
        ctx.textAlign = "right";

        for (let i = 0; i <= 4; i++) {
            const ratio = i / 4;
            const y = padding.top + chartH - (ratio * chartH);

            ctx.beginPath();
            ctx.moveTo(padding.left, y);
            ctx.lineTo(width - padding.right, y);
            ctx.stroke();

            const valLabel = (maxVal * ratio).toFixed(1);
            ctx.fillText(valLabel, padding.left - 8, y + 3.5);
        }

        // Draw eigenvalue bars
        const gap = count > 40 ? 1.5 : 3;
        const barW = Math.max(1.5, (chartW - gap * (count - 1)) / count);

        eigenvalues.forEach((val, idx) => {
            const barH = Math.max(2, (val / maxVal) * chartH);
            const x = padding.left + idx * (barW + gap);
            const y = padding.top + chartH - barH;

            // Highlight selected k components in gold, rest in muted
            if (idx < selectedK) {
                ctx.fillStyle = "#c9a96e";
            } else {
                ctx.fillStyle = "rgba(255, 255, 255, 0.12)";
            }

            ctx.fillRect(x, y, barW, barH);
        });

        // Cumulative energy line overlay (scree plot retention)
        const totalEnergy = eigenvalues.reduce((a, b) => a + b, 0);
        if (totalEnergy > 0) {
            let runningSum = 0;
            ctx.beginPath();
            ctx.strokeStyle = "rgba(244, 237, 227, 0.5)";
            ctx.lineWidth = 1.5;

            eigenvalues.forEach((val, idx) => {
                runningSum += val;
                const cumPercent = runningSum / totalEnergy;
                const x = padding.left + idx * (barW + gap) + barW / 2;
                const y = padding.top + chartH - (cumPercent * chartH);

                if (idx === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });
            ctx.stroke();
        }

        // Baseline axis
        ctx.strokeStyle = "rgba(255, 255, 255, 0.25)";
        ctx.beginPath();
        ctx.moveTo(padding.left, padding.top + chartH);
        ctx.lineTo(width - padding.right, padding.top + chartH);
        ctx.stroke();

        // X-axis component tick marks
        ctx.fillStyle = "#9a9080";
        ctx.font = '9px "JetBrains Mono", monospace';
        ctx.textAlign = "center";

        const ticks = [1, 8, 16, 32, 48, 64];
        ticks.forEach(t => {
            if (t <= count) {
                const idx = t - 1;
                const x = padding.left + idx * (barW + gap) + barW / 2;
                ctx.fillText(`λ${t}`, x, height - 12);
            }
        });

        // Top labels
        ctx.textAlign = "left";
        ctx.fillStyle = "#c9a96e";
        ctx.fillText("EIGENVALUE MAGNITUDE (λ)", padding.left, 14);

        ctx.textAlign = "right";
        ctx.fillStyle = "#9a9080";
        ctx.fillText(`COMPONENTS TOTAL: ${count}`, width - padding.right, 14);
    }

    renderEigenSpectrumChart();
    setTimeout(renderEigenSpectrumChart, 100);
    setTimeout(renderEigenSpectrumChart, 400);
    window.addEventListener("load", renderEigenSpectrumChart);

    if (window.ResizeObserver) {
        const resizeObs = new ResizeObserver(() => renderEigenSpectrumChart());
        resizeObs.observe(canvas.parentElement);
    } else {
        window.addEventListener("resize", renderEigenSpectrumChart);
    }
});