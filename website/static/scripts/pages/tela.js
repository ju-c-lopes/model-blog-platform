const larguraTela = window.innerWidth;
const alturaTela = window.innerHeight;
const ratio = window.devicePixelRatio;

let tela = document.querySelector(".screen-size");

tela.innerHTML += `
    <p style="color: #6c6c6c;">Largura: ${larguraTela}</p>
    <p style="color: #6c6c6c;">Altura: ${alturaTela}</p>
    <p style="color: #6c6c6c;">Device Pixel Ratio: ${ratio}</p>
`;
