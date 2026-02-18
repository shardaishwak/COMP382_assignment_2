function convert() {
    const input = document.getElementById('input').value;
    const output = document.getElementById('output');
    //output.value = input;
    const output_value = window.convertCGFToCNF(input);
    output.value = output_value;

    // subtle flash to signal update
    output.style.borderColor = 'var(--accent)';
    setTimeout(() => output.style.borderColor = '', 600);
}

// also allow Ctrl+Enter
document.getElementById('input').addEventListener('keydown', e => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        convert();
    } else if (e.key === 'Enter' && document.getElementById('input').value.trim() === '') {
        output.value = 'Please enter a grammar to convert.';
    }
});