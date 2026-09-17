/* =========================================================
   EIGENLAB — INTERACTION & VISUALIZATION
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       K SLIDER
    ====================================================== */

    const kRange = document.getElementById("kRange");
    const kValue = document.getElementById("kValue");

    function updateKValue() {
        if (!kRange || !kValue) return;

        kValue.textContent = kRange.value;

        const min = Number(kRange.min || 1);
        const max = Number(kRange.max || 64);
        const value = Number(kRange.value);

        const percentage =
            ((value - min) / (max - min)) * 100;

        kRange.style.setProperty(
            "--slider-progress",
            `${percentage}%`
        );
    }

    if (kRange) {
        kRange.addEventListener("input", updateKValue);
        updateKValue();
    }


    /* =====================================================
       IMAGE FILE NAME
    ====================================================== */

    const imageInput = document.getElementById("imageInput");
    const fileName = document.getElementById("fileName");

    if (imageInput && fileName) {

        imageInput.addEventListener("change", () => {

            if (imageInput.files && imageInput.files.length > 0) {

                const file = imageInput.files[0];

                fileName.textContent = file.name;

                fileName.style.color = "#69b7ff";

            } else {

                fileName.textContent =
                    "PNG, JPG, JPEG or other image";

                fileName.style.color = "";

            }

        });

    }


    /* =====================================================
       DRAG & DROP UPLOAD
    ====================================================== */

    const dropZone = document.querySelector(".drop-zone");

    if (dropZone && imageInput) {

        ["dragenter", "dragover"].forEach(eventName => {

            dropZone.addEventListener(eventName, event => {

                event.preventDefault();

                dropZone.classList.add("drag-active");

            });

        });


        ["dragleave", "drop"].forEach(eventName => {

            dropZone.addEventListener(eventName, event => {

                event.preventDefault();

                dropZone.classList.remove("drag-active");

            });

        });


        dropZone.addEventListener("drop", event => {

            const files = event.dataTransfer.files;

            if (!files || files.length === 0) {
                return;
            }

            const file = files[0];

            if (!file.type.startsWith("image/")) {
                return;
            }

            imageInput.files = files;

            if (fileName) {
                fileName.textContent = file.name;
                fileName.style.color = "#69b7ff";
            }

        });

    }


    /* =====================================================
       EIGENVALUE CHART
    ====================================================== */

    const canvas = document.getElementById("eigenChart");

    if (!canvas) {
        return;
    }

    const rawValues = canvas.dataset.values || "";

    if (!rawValues.trim()) {
        return;
    }

    const values = rawValues
        .split(",")
        .map(value => Number(value.trim()))
        .filter(value => Number.isFinite(value));


    if (!values.length) {
        return;
    }


    /* =====================================================
       CANVAS SETUP
    ====================================================== */

    const ctx = canvas.getContext("2d");

    if (!ctx) {
        return;
    }


    function resizeCanvas() {

        const rect = canvas.getBoundingClientRect();

        const dpr = window.devicePixelRatio || 1;

        canvas.width = Math.max(
            1,
            Math.floor(rect.width * dpr)
        );

        canvas.height = Math.max(
            1,
            Math.floor(230 * dpr)
        );

        ctx.setTransform(
            dpr,
            0,
            0,
            dpr,
            0,
            0
        );

        drawEigenvalueChart();

    }


    /* =====================================================
       DRAW CHART
    ====================================================== */

    function drawEigenvalueChart() {

        const width = canvas.clientWidth;
        const height = 230;

        if (!width) {
            return;
        }

        ctx.clearRect(0, 0, width, height);


        /* -----------------------------------------------
           Chart dimensions
        ------------------------------------------------ */

        const padding = {
            top: 20,
            right: 18,
            bottom: 35,
            left: 45
        };

        const chartWidth =
            width -
            padding.left -
            padding.right;

        const chartHeight =
            height -
            padding.top -
            padding.bottom;


        /* -----------------------------------------------
           Background
        ------------------------------------------------ */

        ctx.fillStyle = "#0c1420";

        ctx.fillRect(
            0,
            0,
            width,
            height
        );


        /* -----------------------------------------------
           Grid
        ------------------------------------------------ */

        const maxValue =
            Math.max(...values, 1);

        const gridLines = 4;

        ctx.lineWidth = 1;
        ctx.strokeStyle =
            "rgba(148, 163, 184, 0.10)";

        ctx.fillStyle =
            "#718096";

        ctx.font =
            '9px "Cascadia Code", Consolas, monospace';

        for (let i = 0; i <= gridLines; i++) {

            const ratio = i / gridLines;

            const y =
                padding.top +
                chartHeight -
                ratio * chartHeight;

            ctx.beginPath();

            ctx.moveTo(
                padding.left,
                y
            );

            ctx.lineTo(
                width - padding.right,
                y
            );

            ctx.stroke();


            const label =
                (maxValue * ratio).toPrecision(3);

            ctx.textAlign = "right";

            ctx.fillText(
                label,
                padding.left - 8,
                y + 3
            );

        }


        /* -----------------------------------------------
           Bars
        ------------------------------------------------ */

        const count = values.length;

        const gap =
            count > 50 ? 1 : 3;

        const barWidth =
            Math.max(
                1,
                (chartWidth -
                    gap * (count - 1)) /
                count
            );


        values.forEach((value, index) => {

            const normalized =
                Math.max(
                    0,
                    Math.min(
                        1,
                        value / maxValue
                    )
                );

            const barHeight =
                normalized * chartHeight;

            const x =
                padding.left +
                index * (barWidth + gap);

            const y =
                padding.top +
                chartHeight -
                barHeight;


            /* Dominant components */
            if (index < 5) {

                ctx.fillStyle =
                    "#69b7ff";

            } else if (index < 10) {

                ctx.fillStyle =
                    "#4da3ff";

            } else {

                ctx.fillStyle =
                    "rgba(77, 163, 255, 0.32)";

            }


            ctx.fillRect(
                x,
                y,
                barWidth,
                barHeight
            );

        });


        /* -----------------------------------------------
           X axis
        ------------------------------------------------ */

        ctx.strokeStyle =
            "rgba(148, 163, 184, 0.20)";

        ctx.beginPath();

        ctx.moveTo(
            padding.left,
            padding.top + chartHeight
        );

        ctx.lineTo(
            width - padding.right,
            padding.top + chartHeight
        );

        ctx.stroke();


        /* -----------------------------------------------
           X labels
        ------------------------------------------------ */

        ctx.fillStyle = "#718096";

        ctx.font =
            '8px "Cascadia Code", Consolas, monospace';

        ctx.textAlign = "center";

        const labels = [1, 5, 10, 20, 32, 64];

        labels.forEach(label => {

            if (label > count) {
                return;
            }

            const index = label - 1;

            const x =
                padding.left +
                index * (barWidth + gap) +
                barWidth / 2;

            ctx.fillText(
                `λ${label}`,
                x,
                height - 13
            );

        });


        /* -----------------------------------------------
           Chart title labels
        ------------------------------------------------ */

        ctx.fillStyle =
            "#8290a3";

        ctx.font =
            '8px "Cascadia Code", Consolas, monospace';

        ctx.textAlign = "left";

        ctx.fillText(
            "EIGENVALUE MAGNITUDE",
            padding.left,
            11
        );

        ctx.textAlign = "right";

        ctx.fillText(
            `${count} COMPONENTS`,
            width - padding.right,
            11
        );

    }


    /* =====================================================
       INITIAL DRAW
    ====================================================== */

    resizeCanvas();


    /* =====================================================
       RESPONSIVE REDRAW
    ====================================================== */

    let resizeTimer;

    window.addEventListener("resize", () => {

        clearTimeout(resizeTimer);

        resizeTimer = setTimeout(() => {
            resizeCanvas();
        }, 100);

    });


    /* =====================================================
       ANALYSIS FORM LOADING STATE
    ====================================================== */

    const analysisForm =
        document.getElementById("analysisForm");

    const runButton =
        document.querySelector(".run-button");

    if (analysisForm && runButton) {

        analysisForm.addEventListener("submit", () => {

            runButton.classList.add("loading");

            const buttonText =
                runButton.querySelector("span");

            if (buttonText) {
                buttonText.textContent =
                    "Analyzing…";
            }

        });

    }

});