const kRange = document.querySelector('#kRange');
const kValue = document.querySelector('#kValue');

if (kRange && kValue) {
    kRange.addEventListener('input', () => {
        kValue.textContent = kRange.value;
    });
}

const chart = document.querySelector('#eigenChart');

if (chart) {
    const values = chart.dataset.values
        .split(',')
        .map((value) => Number(value))
        .filter((value) => Number.isFinite(value));
    const ctx = chart.getContext('2d');
    const width = chart.width = chart.clientWidth * window.devicePixelRatio;
    const height = chart.height = 180 * window.devicePixelRatio;
    const padding = 24 * window.devicePixelRatio;
    const maxValue = Math.max(...values, 1);
    const barGap = 3 * window.devicePixelRatio;
    const barWidth = (width - padding * 2 - barGap * (values.length - 1)) / values.length;

    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    ctx.clearRect(0, 0, width, height);
    ctx.strokeStyle = '#8792a2';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding / window.devicePixelRatio, 8);
    ctx.lineTo(padding / window.devicePixelRatio, 156);
    ctx.lineTo(width / window.devicePixelRatio - 12, 156);
    ctx.stroke();

    values.forEach((value, index) => {
        const normalized = value / maxValue;
        const x = padding / window.devicePixelRatio + index * ((barWidth + barGap) / window.devicePixelRatio);
        const barHeight = Math.max(2, normalized * 135);
        const y = 156 - barHeight;
        ctx.fillStyle = index === 0 ? '#1f4e79' : '#547a9f';
        ctx.fillRect(x, y, barWidth / window.devicePixelRatio, barHeight);
    });
}
