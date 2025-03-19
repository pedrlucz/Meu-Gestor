


// Alternar para a tela de registro
registerBtn.addEventListener('click', () => {
    container.classList.add('active');  // adiciona a classe "active" para mostrar o formulário de registro
});

// Alternar para a tela de login
loginBtn.addEventListener('click', () => {
    container.classList.remove('active');  // remove a classe "active" para mostrar o formulário de login
});

