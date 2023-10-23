window.onload = function () {
    document.getElementById("download").addEventListener("click", () => {
        const invoice = document.getElementById("invoice"); // Perbaikan: Gunakan "document" sebelum "getElementById"
        
        console.log(window); // Perbaikan: Tidak ada yang dicetak di sini

        var options = { // Perbaikan: Ganti "option" menjadi "options"
            filename: 'results.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 }, // Perbaikan: "scall" harus menjadi "scale"
            jsPDF: { unit: 'in', format: 'letter' }
        };
        html2pdf().from(invoice).set(options).save(); // Perbaikan: Menggunakan "outputPdf()" untuk menghasilkan PDF
    });
}
