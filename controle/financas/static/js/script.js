const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

// Alternar para a tela de registro
registerBtn.addEventListener('click', () => {
    container.classList.add('active');  // Adiciona a classe "active" para mostrar o formulário de registro
});

// Alternar para a tela de login
loginBtn.addEventListener('click', () => {
    container.classList.remove('active');  // Remove a classe "active" para mostrar o formulário de login
});
