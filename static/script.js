document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('installmentForm');
    const tenorYearsInput = document.getElementById('tenor_years');
    const periodsPerYearInput = document.getElementById('periods_per_year');
    const inputPmtsContainer = document.getElementById('input_pmts_container');

    function updateInputPmts() {
        inputPmtsContainer.innerHTML = '';
        const tenorYears = parseInt(tenorYearsInput.value) || 0;
        const periodsPerYear = parseInt(periodsPerYearInput.value) || 0;
        const numPayments = tenorYears * periodsPerYear + 1;

        for (let i = 0; i < numPayments; i++) {
            const label = document.createElement('label');
            label.textContent = `Payment ${i}:`;
            const input = document.createElement('input');
            input.type = 'number';
            input.name = `input_pmts[${i}]`;
            input.min = 0;
            input.max = 1;
            input.step = 0.01;
            inputPmtsContainer.appendChild(label);
            inputPmtsContainer.appendChild(input);
        }
    }

    tenorYearsInput.addEventListener('input', updateInputPmts);
    periodsPerYearInput.addEventListener('input', updateInputPmts);

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = isNaN(value) ? value : parseFloat(value);
        });

        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        displayResult(result);
    });
});

function displayResult(result) {
    const resultContainer = document.getElementById('resultContainer');
    resultContainer.innerHTML = JSON.stringify(result, null, 2);
}
