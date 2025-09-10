const larguraTela = window.innerWidth;
const alturaTela = window.innerHeight;
const ratio = window.devicePixelRatio;

let tela = document.querySelector(".screen-size");

tela.innerHTML += `
    <p style="margin-top=400px;">Largura: ${larguraTela}</p>
    <p>Altura: ${alturaTela}</p>
    <p>Device Pixel Ratio: ${ratio}</p>
`;
